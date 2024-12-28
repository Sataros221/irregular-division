import random
import csv


def encontrar_numeros_con_diferencia(objetivo,numero_divisiones, porcentaje_diferencia=0.1, intentos=10000000000):
    # Calcula la media y el rango de diferencia basado en el objetivo y el porcentaje de diferencia
    media = objetivo / numero_divisiones
    rango_diferencia = media * porcentaje_diferencia

    # Intenta encontrar un conjunto de números que sumen al objetivo
    for _ in range(intentos):
        numeros = []
        suma_actual = 0

        # Genera 24 números aleatorios dentro del rango especificado
        for _ in range(numero_divisiones):

            numero = random.uniform(media - rango_diferencia, media + rango_diferencia)

            # Si el número generado no excede el objetivo, se añade a la lista
            if suma_actual + numero <= objetivo:
                numeros.append(numero)
                suma_actual += numero
            else:

                # Si el número excede el objetivo, se genera un nuevo número dentro de un rango más pequeño
                numero = random.uniform(media - rango_diferencia, media)
                if suma_actual + numero <= objetivo:
                    numeros.append(numero)
                    suma_actual += numero
                else:
                    break
        # Si la suma de los números generados está cerca del objetivo, se devuelve la lista
        if abs(suma_actual - objetivo) <= 0.01:
            return [round(num, 2) for num in numeros]
    # Si no se encuentra un conjunto de números que sumen al objetivo, se devuelve None
    return None


valor_objetivo = int(input("Ingrese el valor objetivo: "))
numero_divisiones = int(input("Ingrese el numero de divisiones: "))
numeros_con_diferencia = encontrar_numeros_con_diferencia(
    valor_objetivo,numero_divisiones, porcentaje_diferencia=0.1
)

if numeros_con_diferencia is not None:
    print(f"Conjunto de números que suman {valor_objetivo}: {numeros_con_diferencia}")
    print(f"Suma del conjunto: {sum(numeros_con_diferencia)}")

    # Exportar a CSV
    with open("resultados.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Posicion", "Numero"])
        for i, numero in enumerate(numeros_con_diferencia):
            writer.writerow([i + 1, numero])
else:
    print("No se encontró un conjunto válido.")
