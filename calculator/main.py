import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output

def main():
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"' )
        print('Example: python main.py "3 + 5"' )
        return

    expression = " ".join(sys.argv[1:])
    try:
        calculator = Calculator()
        result = calculator.evaluate(expression)
        result = float(result)
        to_print = format_json_output(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()