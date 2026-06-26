#!/usr/bin/env python3
"""
Calculator script for mathematical expressions.
Supports basic arithmetic, scientific functions, and unit conversions.
"""

import sys
import math
import json
import re
from decimal import Decimal, InvalidOperation

def evaluate_expression(expr):
    """
    Safely evaluate a mathematical expression.
    Supports: +, -, *, /, **, %, parentheses, and math functions.
    """
    # Clean the expression
    expr = expr.strip()
    
    # Define allowed names (math functions and constants)
    allowed_names = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'log2': math.log2,
        'ln': math.log,
        'exp': math.exp,
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil,
        'pow': pow,
        'max': max,
        'min': min,
        'pi': math.pi,
        'e': math.e,
        'degrees': math.degrees,
        'radians': math.radians,
        'factorial': math.factorial,
        'gcd': math.gcd,
    }
    
    # Replace common symbols
    expr = expr.replace('^', '**')
    expr = expr.replace('×', '*')
    expr = expr.replace('÷', '/')
    expr = expr.replace('π', 'pi')
    
    # Handle percentage (e.g., 50% -> 0.5)
    expr = re.sub(r'(\d+(?:\.\d+)?)%', r'(\1/100)', expr)
    
    try:
        # Compile and evaluate safely
        code = compile(expr, '<string>', 'eval')
        
        # Check for disallowed names
        for name in code.co_names:
            if name not in allowed_names:
                return {"error": f"Unknown function or variable: {name}"}
        
        result = eval(code, {"__builtins__": {}}, allowed_names)
        
        # Format result
        if isinstance(result, (int, float)):
            # Round very small numbers to 0
            if abs(result) < 1e-15:
                result = 0
            # Format nicely
            if isinstance(result, float):
                # Remove floating point artifacts
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
        
        return {"result": result}
    
    except ZeroDivisionError:
        return {"error": "Division by zero"}
    except OverflowError:
        return {"error": "Result too large"}
    except ValueError as e:
        return {"error": f"Invalid value: {str(e)}"}
    except SyntaxError:
        return {"error": "Invalid expression syntax"}
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}

def convert_units(value, from_unit, to_unit):
    """
    Convert between common units.
    Supported categories: length, mass, temperature, volume, area, time.
    """
    # Length conversions (to meters)
    length_units = {
        'm': 1, 'meter': 1, 'meters': 1,
        'km': 1000, 'kilometer': 1000, 'kilometers': 1000,
        'cm': 0.01, 'centimeter': 0.01, 'centimeters': 0.01,
        'mm': 0.001, 'millimeter': 0.001, 'millimeters': 0.001,
        'mi': 1609.34, 'mile': 1609.34, 'miles': 1609.34,
        'yd': 0.9144, 'yard': 0.9144, 'yards': 0.9144,
        'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
        'in': 0.0254, 'inch': 0.0254, 'inches': 0.0254,
        'nm': 1852, 'nautical': 1852, 'nauticalmile': 1852,
    }
    
    # Mass conversions (to grams)
    mass_units = {
        'g': 1, 'gram': 1, 'grams': 1,
        'kg': 1000, 'kilogram': 1000, 'kilograms': 1000,
        'mg': 0.001, 'milligram': 0.001, 'milligrams': 0.001,
        'lb': 453.592, 'pound': 453.592, 'pounds': 453.592,
        'oz': 28.3495, 'ounce': 28.3495, 'ounces': 28.3495,
        't': 1000000, 'ton': 1000000, 'tons': 1000000, 'tonne': 1000000,
    }
    
    # Volume conversions (to liters)
    volume_units = {
        'l': 1, 'liter': 1, 'liters': 1, 'litre': 1, 'litres': 1,
        'ml': 0.001, 'milliliter': 0.001, 'milliliters': 0.001,
        'gal': 3.78541, 'gallon': 3.78541, 'gallons': 3.78541,
        'qt': 0.946353, 'quart': 0.946353, 'quarts': 0.946353,
        'pt': 0.473176, 'pint': 0.473176, 'pints': 0.473176,
        'cup': 0.236588, 'cups': 0.236588,
        'fl oz': 0.0295735, 'floz': 0.0295735, 'fluidounce': 0.0295735,
        'tbsp': 0.0147868, 'tablespoon': 0.0147868, 'tablespoons': 0.0147868,
        'tsp': 0.00492892, 'teaspoon': 0.00492892, 'teaspoons': 0.00492892,
    }
    
    # Area conversions (to square meters)
    area_units = {
        'm2': 1, 'sqm': 1, 'squaremeter': 1, 'squaremeters': 1,
        'km2': 1000000, 'sqkm': 1000000,
        'cm2': 0.0001, 'sqcm': 0.0001,
        'ha': 10000, 'hectare': 10000, 'hectares': 10000,
        'acre': 4046.86, 'acres': 4046.86,
        'ft2': 0.092903, 'sqft': 0.092903,
        'in2': 0.00064516, 'sqin': 0.00064516,
    }
    
    # Time conversions (to seconds)
    time_units = {
        's': 1, 'sec': 1, 'second': 1, 'seconds': 1,
        'min': 60, 'minute': 60, 'minutes': 60,
        'h': 3600, 'hr': 3600, 'hour': 3600, 'hours': 3600,
        'd': 86400, 'day': 86400, 'days': 86400,
        'wk': 604800, 'week': 604800, 'weeks': 604800,
        'mo': 2592000, 'month': 2592000, 'months': 2592000,
        'y': 31536000, 'year': 31536000, 'years': 31536000,
    }
    
    # Normalize unit names
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()
    
    # Try to find matching unit category
    for units_dict, name in [(length_units, 'length'), (mass_units, 'mass'), 
                              (volume_units, 'volume'), (area_units, 'area'), 
                              (time_units, 'time')]:
        if from_unit in units_dict and to_unit in units_dict:
            # Convert to base unit then to target
            base_value = value * units_dict[from_unit]
            result = base_value / units_dict[to_unit]
            return {"result": result, "category": name}
    
    # Temperature conversion (special handling)
    if from_unit in ['c', 'celsius', '°c'] and to_unit in ['f', 'fahrenheit', '°f']:
        return {"result": (value * 9/5) + 32, "category": "temperature"}
    if from_unit in ['f', 'fahrenheit', '°f'] and to_unit in ['c', 'celsius', '°c']:
        return {"result": (value - 32) * 5/9, "category": "temperature"}
    if from_unit in ['c', 'celsius', '°c'] and to_unit in ['k', 'kelvin']:
        return {"result": value + 273.15, "category": "temperature"}
    if from_unit in ['k', 'kelvin'] and to_unit in ['c', 'celsius', '°c']:
        return {"result": value - 273.15, "category": "temperature"}
    if from_unit in ['f', 'fahrenheit', '°f'] and to_unit in ['k', 'kelvin']:
        return {"result": (value - 32) * 5/9 + 273.15, "category": "temperature"}
    if from_unit in ['k', 'kelvin'] and to_unit in ['f', 'fahrenheit', '°f']:
        return {"result": (value - 273.15) * 9/5 + 32, "category": "temperature"}
    
    return {"error": f"Unsupported unit conversion: {from_unit} to {to_unit}"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No expression provided"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "calc":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "No expression provided for calculation"}))
            sys.exit(1)
        expr = ' '.join(sys.argv[2:])
        result = evaluate_expression(expr)
        print(json.dumps(result))
    
    elif command == "convert":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: convert <value> <from_unit> <to_unit>"}))
            sys.exit(1)
        try:
            value = float(sys.argv[2])
            from_unit = sys.argv[3]
            to_unit = sys.argv[4]
            result = convert_units(value, from_unit, to_unit)
            print(json.dumps(result))
        except ValueError:
            print(json.dumps({"error": "Invalid numeric value"}))
            sys.exit(1)
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
