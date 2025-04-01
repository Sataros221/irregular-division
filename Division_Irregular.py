import random
import csv


def find_numbers_with_differential(objective, division_num, diferencial_percent=0.1, max_try=1000):
    # Pre-calculation of important values
    m = objective / division_num
    m_low = m * (1 - diferencial_percent)
    m_high = m * (1 + diferencial_percent)

    for _ in range(max_try):
        numbers = []
        suma_actual = 0.0
        valid = True

        # Generate the first n-1 numbers with restrictions
        for i in range(division_num - 1):
            rest_numbers = division_num - i
            rest_sum = objective - suma_actual

            # Calcular límites para el número actual
            min_actual = max(m_low, rest_sum - (rest_numbers - 1) * m_high)
            max_actual = min(m_high, rest_sum - (rest_numbers - 1) * m_low)

            if min_actual > max_actual:
                valid = False
                break

            # Generate number within the allowed range
            number = random.uniform(min_actual, max_actual)
            numbers.append(number)
            suma_actual += number

        if not valid:
            continue

        # Calculate and validate the last number
        ultimo_number = objective - suma_actual
        if not (m_low <= ultimo_number <= m_high):
            continue

        numbers.append(ultimo_number)

        # Approximate and adjust decimals
        numbers_redondeados = [round(num, 2) for num in numbers]
        suma_redondeada = sum(numbers_redondeados)
        diferencia = round(objective - suma_redondeada, 2)

        if diferencia == 0:
            return numbers_redondeados

        # Adjust last number while maintaining precision
        nuevo_ultimo = numbers_redondeados[-1] + diferencia
        if not (m_low <= nuevo_ultimo <= m_high):
            continue

        numbers_redondeados[-1] = round(nuevo_ultimo, 2)
        
        # Final verification
        if sum(numbers_redondeados) == objective:
            return numbers_redondeados

    return None


# UI
valor_objective = int(input("Enter the target value: "))
division_num = int(input("Enter the number of divisions: "))

result = find_numbers_with_differential(
    valor_objective, division_num, diferencial_percent=0.1
)

if result is not None:
    print(f"Valid set found: {result}")
    print(f"Verified sum: {sum(result):.2f}")

    # Export to CSV
    with open("results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Position", "Number"])
        for i, number in enumerate(result):
            writer.writerow([i + 1, number])
        writer.writerow(["Total", sum(result)])
else:
    print("No valid set found.")
