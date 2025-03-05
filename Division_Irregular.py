import random
import csv


def encontrar_numeros_con_diferencia(objetivo, numero_divisiones, porcentaje_diferencia=0.1, max_intentos=1000):
    # Pre-cálculo de valores importantes
    m = objetivo / numero_divisiones
    m_low = m * (1 - porcentaje_diferencia)
    m_high = m * (1 + porcentaje_diferencia)

    for _ in range(max_intentos):
        numeros = []
        suma_actual = 0.0
        valido = True

        # Generar los primeros n-1 números con restricciones
        for i in range(numero_divisiones - 1):
            numeros_restantes = numero_divisiones - i
            suma_restante = objetivo - suma_actual

            # Calcular límites para el número actual
            min_actual = max(m_low, suma_restante - (numeros_restantes - 1) * m_high)
            max_actual = min(m_high, suma_restante - (numeros_restantes - 1) * m_low)

            if min_actual > max_actual:
                valido = False
                break

            # Generar número dentro del rango permitido
            numero = random.uniform(min_actual, max_actual)
            numeros.append(numero)
            suma_actual += numero

        if not valido:
            continue

        # Calcular y validar el último número
        ultimo_numero = objetivo - suma_actual
        if not (m_low <= ultimo_numero <= m_high):
            continue

        numeros.append(ultimo_numero)

        # Aproximar y ajustar decimales
        numeros_redondeados = [round(num, 2) for num in numeros]
        suma_redondeada = sum(numeros_redondeados)
        diferencia = round(objetivo - suma_redondeada, 2)

        if diferencia == 0:
            return numeros_redondeados

        # Ajustar último número manteniendo la precisión
        nuevo_ultimo = numeros_redondeados[-1] + diferencia
        if not (m_low <= nuevo_ultimo <= m_high):
            continue

        numeros_redondeados[-1] = round(nuevo_ultimo, 2)
        
        # Verificación final
        if sum(numeros_redondeados) == objetivo:
            return numeros_redondeados

    return None


# Interfaz de usuario y ejecución
valor_objetivo = int(input("Ingrese el valor objetivo: "))
numero_divisiones = int(input("Ingrese el numero de divisiones: "))

resultado = encontrar_numeros_con_diferencia(
    valor_objetivo, numero_divisiones, porcentaje_diferencia=0.1
)

if resultado is not None:
    print(f"Conjunto válido encontrado: {resultado}")
    print(f"Suma verificada: {sum(resultado):.2f}")

    # Exportar a CSV
    with open("resultados.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Posición", "Numero"])
        for i, numero in enumerate(resultado):
            writer.writerow([i + 1, numero])
        writer.writerow(["Total", sum(resultado)])
else:
    print("No se encontró un conjunto válido.")
