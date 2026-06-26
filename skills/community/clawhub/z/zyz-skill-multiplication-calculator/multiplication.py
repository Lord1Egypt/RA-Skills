def multiply(numbers):
    result = 1.0
    for num in numbers:
        result *= float(num)
    return result

def parse_input(input_str):
    # Parse input like "multiply 5 8" or "multiply 2.5 4 6"
    parts = input_str.strip().split()
    if not parts or parts[0] != "multiply":
        return "Invalid format. Use: multiply <num1> <num2> ..."
    try:
        numbers = list(map(float, parts[1:]))
        if len(numbers) < 2:
            return "Please provide at least two numbers to multiply."
        return multiply(numbers)
    except ValueError:
        return "Invalid number(s). Please enter valid numbers."

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python multiplication.py 'multiply <num1> <num2> ...'")
        sys.exit(1)
    input_str = sys.argv[1]
    print(parse_input(input_str))