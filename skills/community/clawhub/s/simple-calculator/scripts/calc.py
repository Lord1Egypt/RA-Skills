#!/usr/bin/env python3
"""Simple calculator - evaluates basic math expressions."""
import sys
import re

def calc(expr: str) -> str:
    expr = expr.strip()
    if not re.match(r'^[\d\s\+\-\*\/\%\.\(\)]+$', expr):
        return "Error: invalid expression"
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        if isinstance(result, float) and result == int(result):
            result = int(result)
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: calc.py \"expression\"")
        sys.exit(1)
    print(calc(sys.argv[1]))
