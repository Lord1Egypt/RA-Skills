#!/usr/bin/env python
"""
Analyze test failures and suggest fixes or apply patches.

Usage:
    python debug_code.py --report "path/to/report.json" --code "path/to/code.py" --output "path/to/fixed_code.py"
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# Default configuration
DEFAULT_CONDA_PATH = r"C:\anaconda3\condabin\conda.bat"
DEFAULT_ENV = "py311"
PROJECT_DIR = r"H:\code\Daily"

def extract_traceback_lines(stdout: str, stderr: str = "") -> list:
    """Extract traceback sections from test output (both Python tracebacks and pytest format)."""
    combined = stdout + "\n" + stderr

    # First, try full Python traceback pattern
    traceback_blocks = re.findall(r'(Traceback \(most recent call last\):.*?)(?=\n\n|\Z)', combined, re.DOTALL)

    if traceback_blocks:
        return traceback_blocks

    # If not found, try pytest format: look for "E   <ErrorType>: <message>" lines
    # and capture the surrounding context
    pytest_errors = []
    lines = combined.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('E   ') and ':' in line:
            # Extract error type and message
            error_line = line.strip()[4:]  # remove "E   "
            if ' ' in error_line:
                error_type, error_message = error_line.split(' ', 1)
            else:
                error_type = error_line
                error_message = ""
            # Get a few lines of context
            context_start = max(0, i - 4)
            context_lines = lines[context_start:i+1]
            context = '\n'.join(context_lines)
            pytest_errors.append(f"Pytest error:\n{context}\nError: {error_type}: {error_message}")
        i += 1

    return pytest_errors

def analyze_failure(traceback: str, code_content: str) -> dict:
    """
    Analyze a traceback and suggest a fix.

    Returns a dictionary with:
    - error_type: e.g., "NameError", "TypeError"
    - message: Error message
    - suggested_fix: Text description of what to change
    - line_number: Approximate line number where error occurred
    - context: Code snippet around error
    - raw_traceback: Original traceback text
    """
    lines = traceback.split('\n')

    # Determine if this is a pytest-style output or a standard traceback
    is_pytest = any('in test_' in line and '::' in line for line in lines[:5])

    file_path = "unknown"
    line_num = -1
    error_type = ""
    error_message = ""

    if is_pytest:
        # Pytest format: look for lines like "tests\test_factorial_impl.py:19: in test_factorial_basic"
        # and then "factorial_impl.py:20: in factorial"
        # and then "E   TypeError: ..."
        for line in lines:
            # Match file:line: in function
            match = re.search(r'(\S+):(\d+): in (\S+)', line)
            if match:
                file_path = match.group(1)
                line_num = int(match.group(2))
                # Continue to find the actual error type and message in the following lines
                continue
            # Look for error line: "E   TypeError: message"
            if line.strip().startswith('E   '):
                err_content = line.strip()[4:]
                if ' ' in err_content:
                    error_type, error_message = err_content.split(' ', 1)
                else:
                    error_type = err_content
                break
    else:
        # Standard traceback: parse "File \"...\", line X"
        error_line = ""
        for line in lines:
            if line.strip().startswith("File"):
                error_line = line
                break

        match = re.search(r'File "([^"]+)", line (\d+)', error_line)
        if match:
            file_path = match.group(1)
            line_num = int(match.group(2))
        else:
            file_path = "unknown"
            line_num = -1

        # Find the actual error (last non-empty line that's not a File/Traceback line)
        for line in reversed(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith("File") and not stripped.startswith("Traceback"):
                if ':' in stripped:
                    error_type, error_message = stripped.split(':', 1)
                    error_type = error_type.strip()
                    error_message = error_message.strip()
                break

    # Get context from code if we have line number and the code_content corresponds to the file
    context_snippet = ""
    if line_num > 0 and code_content and Path(file_path).name == Path(code_content).name:
        code_lines = code_content.split('\n')
        start = max(0, line_num - 3)
        end = min(len(code_lines), line_num + 2)
        context_lines = code_lines[start:end]
        context_snippet = '\n'.join(f"{i+1}: {line}" for i, line in enumerate(context_lines, start))

    # Generate suggested fix based on error type
    suggested_fix = generate_suggestion(error_type, error_message, code_content, line_num)

    return {
        "error_type": error_type,
        "error_message": error_message,
        "file": file_path,
        "line_number": line_num,
        "context": context_snippet,
        "suggested_fix": suggested_fix,
        "raw_traceback": traceback
    }

def generate_suggestion(error_type: str, message: str, code: str, line_num: int) -> str:
    """Generate a textual suggestion for fixing the error."""
    suggestions = {
        "NameError": "Check if the variable is defined before use. Ensure imports are correct.",
        "TypeError": "Verify the types of arguments passed. Use type casting if needed.",
        "IndentationError": "Fix indentation. Use 4 spaces per indentation level consistently.",
        "SyntaxError": "Check syntax on the indicated line. Missing parentheses, colons, or quotes often cause this.",
        "ImportError": "Verify the module name and ensure it's installed in the conda environment.",
        "ModuleNotFoundError": "Same as ImportError - check module installation via conda/pip.",
        "AttributeError": "Check that the object has the attribute/method you're calling.",
        "KeyError": "Ensure the key exists in the dictionary before accessing.",
        "IndexError": "Verify list/sequence indices are within bounds.",
        "ValueError": "Provide a valid value for the parameter (e.g., valid int, correct format).",
        "FileNotFoundError": "Check the file path. Use absolute paths or verify relative path is correct.",
        "PermissionError": "Ensure you have read/write permissions for the file.",
        "ZeroDivisionError": "Add a check to prevent division by zero.",
        "AssertionError": "The test assertion failed. Verify the expected vs actual values."
    }

    base = suggestions.get(error_type, "Review the error message and context. Check the indicated line and surrounding code.")

    # Add specific message if helpful
    if "name" in message.lower() and "is not defined" in message.lower():
        var_name = message.split("'")[1] if "'" in message else "variable"
        return f"Define the variable '{var_name}' before using it. Check for typos in variable name."
    elif "takes" in message.lower() and "positional argument" in message.lower():
        return f"Fix function call: wrong number of arguments. Check function signature."
    elif "missing" in message.lower() and "required" in message.lower():
        return f"Provide all required positional arguments in the function call."

    return base

def apply_patch(code: str, line_num: int, new_line: str) -> str:
    """Replace the line at line_num with new_line."""
    lines = code.split('\n')
    if 1 <= line_num <= len(lines):
        lines[line_num - 1] = new_line
        return '\n'.join(lines)
    return code

def main():
    parser = argparse.ArgumentParser(description="Debug code by analyzing test failures")
    parser.add_argument("--report", required=True, help="JSON report from run_tests.py")
    parser.add_argument("--code", required=True, help="Original code file that failed")
    parser.add_argument("--output", help="Output file for patched code (default: overwrites original if patch applied)")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't patch")

    args = parser.parse_args()

    # Load report
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: Report file not found: {report_path}")
        sys.exit(1)

    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)

    # Load code
    code_path = Path(args.code)
    if not code_path.exists():
        print(f"Error: Code file not found: {code_path}")
        sys.exit(1)

    with open(code_path, 'r', encoding='utf-8') as f:
        code_content = f.read()

    # Check if any failures
    if report.get("passed", 0) == 0 and report.get("failed", 0) == 0 and report.get("errors", 0) == 0:
        print("No failures detected. All tests passed!")
        sys.exit(0)

    # Analyze tracebacks
    stdout = report.get("stdout", "")
    stderr = report.get("stderr", "")
    tracebacks = extract_traceback_lines(stdout, stderr)

    if not tracebacks:
        print("No tracebacks found in output. Tests may have failed for other reasons.")
        print("Summary:", report.get("summary", ""))
        sys.exit(0)

    print(f"Found {len(tracebacks)} failure(s) to analyze:\n")

    analyses = []
    for i, tb in enumerate(tracebacks, 1):
        analysis = analyze_failure(tb, code_content)
        analyses.append(analysis)
        print(f"--- Failure {i} ---")
        print(f"Error: {analysis['error_type']}: {analysis['error_message']}")
        print(f"Location: {analysis['file']}:{analysis['line_number']}")
        print(f"Context:")
        print(analysis['context'])
        print(f"\nSuggestion: {analysis['suggested_fix']}\n")

    # Write debug report
    debug_report = {
        "timestamp": datetime.now().isoformat(),
        "code_file": str(code_path),
        "test_report": str(report_path),
        "analyses": analyses
    }

    debug_report_path = Path(PROJECT_DIR) / "reports" / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    debug_report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(debug_report_path, 'w', encoding='utf-8') as f:
        json.dump(debug_report, f, indent=2, ensure_ascii=False)

    print(f"Debug analysis saved to: {debug_report_path}")

    # If not analyze-only, could apply patches (but for safety, we'll just output suggestions)
    if args.output and analyses:
        # For this automated skill, we won't auto-patch unless specifically instructed
        # The calling agent should review suggestions and decide
        print(f"\nNOTE: Automatic patching is disabled for safety. Review the suggestions above")
        print(f"and manually modify the code or re-run with a patch script.")

    sys.exit(0)

if __name__ == "__main__":
    main()
