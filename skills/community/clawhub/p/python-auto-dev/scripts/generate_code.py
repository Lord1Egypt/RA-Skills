#!/usr/bin/env python
"""
Generate Python code from a natural language specification.

Usage:
    python generate_code.py --spec "Add two numbers" --output "path/to/file.py"
    python generate_code.py --spec "Read CSV and compute stats" --output H:\code\Daily\generated_20260310.py
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Default configuration (matches skill requirements)
DEFAULT_CONDA_PATH = r"C:\anaconda3\condabin\conda.bat"
DEFAULT_ENV = "py311"
DEFAULT_PROJECT_DIR = r"H:\code\Daily"

def generate_code(spec: str) -> str:
    """
    Generate Python code from specification.
    This is a template function - in production, this would use an AI model.
    For now, we'll generate a basic template structure.
    """
    # Parse the specification to determine what to generate
    spec_lower = spec.lower()

    # Generate appropriate code template
    if "add" in spec_lower and ("function" in spec_lower or "def" in spec_lower):
        code = f'''def add_numbers(a, b):
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b

if __name__ == "__main__":
    result = add_numbers(5, 3)
    print(f"Result: {{result}}")
'''
    elif "read" in spec_lower and "csv" in spec_lower:
        code = f'''import pandas as pd
from pathlib import Path

def read_csv_and_stats(filepath):
    """
    Read a CSV file and compute basic statistics.

    Args:
        filepath: Path to the CSV file

    Returns:
        Dictionary with statistics
    """
    df = pd.read_csv(filepath)
    stats = {{
        "rows": len(df),
        "columns": len(df.columns),
        "mean": df.mean(numeric_only=True).to_dict(),
        "std": df.std(numeric_only=True).to_dict(),
    }}
    return stats

if __name__ == "__main__":
    csv_path = input("Enter CSV path: ").strip()
    if Path(csv_path).exists():
        result = read_csv_and_stats(csv_path)
        print("Statistics:", result)
    else:
        print("File not found:", csv_path)
'''
    else:
        # Generic template
        code = f'''"""
Auto-generated Python script
Specification: {spec}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

def main():
    """
    Main function implementing: {spec}
    """
    # TODO: Implement based on specification
    print("This is a template. Implement: {{spec}}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
    return code

def main():
    parser = argparse.ArgumentParser(description="Generate Python code from specification")
    parser.add_argument("--spec", required=True, help="Natural language specification of the code to generate")
    parser.add_argument("--output", help="Output file path (default: auto-generated in project dir)")

    args = parser.parse_args()

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Auto-generate filename in project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.py"
        output_path = Path(DEFAULT_PROJECT_DIR) / filename

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate the code
    print(f"Generating code for: {args.spec}")
    code = generate_code(args.spec)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f"Code written to: {output_path}")
    print(f"File size: {len(code)} bytes")

    # Return path for pipeline
    return str(output_path)

if __name__ == "__main__":
    output_file = main()
    # Print output file path for downstream consumption
    print(f"OUTPUT_PATH:{output_file}")
