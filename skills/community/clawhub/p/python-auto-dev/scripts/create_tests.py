#!/usr/bin/env python
"""
Create unit tests for a given Python code file.

Usage:
    python create_tests.py --code "path/to/code.py" --output "path/to/test_file.py"
"""

import argparse
import ast
import inspect
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project directory to path for imports
PROJECT_DIR = r"H:\code\Daily"
sys.path.insert(0, PROJECT_DIR)

def analyze_code(filepath: str) -> dict:
    """Parse Python file and extract functions and classes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return {"error": f"Syntax error in code: {e}"}

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node) or "",
                "lineno": node.lineno
            })
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append({
                        "name": item.name,
                        "args": [arg.arg for arg in item.args.args],
                        "docstring": ast.get_docstring(item) or "",
                        "lineno": item.lineno
                    })
            classes.append({
                "name": node.name,
                "methods": methods,
                "docstring": ast.get_docstring(node) or ""
            })

    return {
        "filename": Path(filepath).name,
        "functions": functions,
        "classes": classes,
        "raw_content": content
    }

def generate_test_code(analysis: dict) -> str:
    """Generate pytest test code based on analysis."""
    lines = []
    lines.append('"""')
    lines.append(f'Automated tests for {analysis["filename"]}')
    lines.append(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('"""')
    lines.append('')
    lines.append('import pytest')
    lines.append('import sys')
    lines.append('from pathlib import Path')
    lines.append('')

    # Add import for the module being tested
    module_name = Path(analysis["filename"]).stem
    lines.append(f'# Import the module under test')
    lines.append(f'sys.path.insert(0, r"{PROJECT_DIR}")')
    lines.append(f'import {module_name}')
    lines.append('')

    # Generate tests for functions
    for func in analysis["functions"]:
        func_name = func["name"]
        args = func["args"]
        docstring = func["docstring"]

        lines.append(f'class Test{func_name.capitalize()}:')
        lines.append(f'    """Tests for {func_name}"""')
        lines.append('')

        # Create a simple test that calls the function with example values
        if args:
            # Generate placeholder arguments
            arg_placeholders = []
            for arg in args:
                if arg == 'self':
                    continue
                arg_lower = arg.lower()
                # Provide reasonable test values based on arg name
                if 'path' in arg_lower or 'file' in arg_lower:
                    arg_placeholders.append('r"test.csv"')
                elif 'url' in arg_lower or 'link' in arg_lower:
                    arg_placeholders.append('"https://example.com"')
                elif 'num' in arg_lower or 'count' in arg_lower or 'index' in arg_lower or arg_lower in ('n', 'i', 'x', 'value', 'size', 'length'):
                    arg_placeholders.append('5')
                elif 'text' in arg_lower or 'string' in arg_lower or 'name' in arg_lower:
                    arg_placeholders.append('"test"')
                elif 'list' in arg_lower or 'array' in arg_lower or 'items' in arg_lower:
                    arg_placeholders.append('[1, 2, 3]')
                elif 'dict' in arg_lower or 'map' in arg_lower or 'data' in arg_lower:
                    arg_placeholders.append('{"key": "value"}')
                elif 'bool' in arg_lower or 'flag' in arg_lower:
                    arg_placeholders.append('True')
                else:
                    arg_placeholders.append('None')

            args_str = ", ".join(arg_placeholders)
            lines.append(f'    def test_{func_name}_basic(self):')
            lines.append(f'        """Basic test for {func_name}"""')
            lines.append(f'        result = {module_name}.{func_name}({args_str})')
            lines.append(f'        assert result is not None')
            lines.append('')
        else:
            lines.append(f'    def test_{func_name}_returns(self):')
            lines.append(f'        """Test {func_name} returns something"""')
            lines.append(f'        result = {module_name}.{func_name}()')
            lines.append(f'        # TODO: Add proper assertions based on expected behavior')
            lines.append(f'        assert result is not None')
            lines.append('')

        lines.append('')

    # Generate tests for class methods
    for cls in analysis["classes"]:
        cls_name = cls["name"]
        lines.append(f'class Test{cls_name}:')
        lines.append(f'    """Tests for {cls_name} class"""')
        lines.append('')

        for method in cls["methods"]:
            method_name = method["name"]
            if method_name.startswith("__"):
                continue  # Skip dunder methods for now

            args = method["args"]
            lines.append(f'    def test_{method_name}(self):')
            lines.append(f'        """Test {cls_name}.{method_name}"""')
            lines.append(f'        # TODO: Implement test')
            lines.append(f'        pytest.skip("Not implemented")')
            lines.append('')

        lines.append('')

    # Add a simple integration test that runs the main function if it exists
    if "main" in [f["name"] for f in analysis["functions"]]:
        lines.append('def test_main_execution():')
        lines.append('    """Test that main function can be called"""')
        lines.append('    try:')
        lines.append(f'        result = {module_name}.main()')
        lines.append('        assert result is not None')
        lines.append('    except Exception as e:')
        lines.append('        pytest.fail(f"main() raised {{e}}")')
        lines.append('')

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate unit tests for Python code")
    parser.add_argument("--code", required=True, help="Path to the Python code file to test")
    parser.add_argument("--output", help="Output test file path (default: tests/test_<filename>.py)")

    args = parser.parse_args()

    code_path = Path(args.code)
    if not code_path.exists():
        print(f"Error: Code file not found: {code_path}")
        sys.exit(1)

    # Analyze the code
    print(f"Analyzing code: {code_path}")
    analysis = analyze_code(str(code_path))

    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        sys.exit(1)

    print(f"Found: {len(analysis['functions'])} functions, {len(analysis['classes'])} classes")

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Place in tests/ subdirectory
        tests_dir = Path(PROJECT_DIR) / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        test_filename = f"test_{code_path.stem}.py"
        output_path = tests_dir / test_filename

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate test code
    test_code = generate_test_code(analysis)

    # Write test file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(test_code)

    print(f"Test file written to: {output_path}")
    print(f"Test file size: {len(test_code)} bytes")

    return str(output_path)

if __name__ == "__main__":
    output_file = main()
    print(f"OUTPUT_PATH:{output_file}")
