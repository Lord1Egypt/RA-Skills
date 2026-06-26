# Script Usage Guide

Complete reference for all scripts in the python-auto-dev skill.

## Configuration Defaults

All scripts share these defaults:
- Conda path: `C:\anaconda3\condabin\conda.bat`
- Conda environment: `py311`
- Project directory: `H:\code\Daily`

## 1. generate_code.py

Generates Python code from a natural language specification.

```bash
python generate_code.py --spec "Add two numbers" --output "H:\code\Daily\my_script.py"
```

**Parameters:**
- `--spec` (required): Natural language description of code to generate
- `--output` (optional): Output file path. If omitted, auto-generates `generated_<timestamp>.py` in project dir.

**Output:**
- Writes Python code to the specified file
- Returns `OUTPUT_PATH:<filepath>` for pipeline consumption

**Capabilities:**
- Recognizes common patterns (e.g., "add numbers", "read CSV")
- Generates type hints and docstrings
- Modular structure with main guard

## 2. create_tests.py

Creates pytest/unittest suites for existing Python code.

```bash
python create_tests.py --code "H:\code\Daily\my_script.py" --output "H:\code\Daily\tests\test_my_script.py"
```

**Parameters:**
- `--code` (required): Path to the Python file to test
- `--output` (optional): Output test file path. Default: `tests/test_<source_name>.py`

**Output:**
- Generates pytest test classes for each function
- Includes placeholder assertions and TODOs
- Returns `OUTPUT_PATH:<filepath>`

**Capabilities:**
- Parses code with AST
- Extracts functions, classes, and methods
- Creates test skeleton automatically

## 3. run_tests.py

Executes pytest tests in the conda environment and generates a JSON report.

```bash
python run_tests.py --test-dir "H:\code\Daily\tests" --code-dir "H:\code\Daily" --report "H:\code\Daily\reports\report.json"
```

**Parameters:**
- `--test-dir` (required): Directory containing test files
- `--code-dir` (optional): Source code directory. Default: `H:\code\Daily`
- `--report` (optional): JSON report path. Default: `reports/test_report_<timestamp>.json`

**Output:**
- Runs pytest with verbose output
- Creates JSON report with pass/fail counts
- Returns `REPORT_PATH:<report_path>`
- Console shows test results

**Capabilities:**
- Activates conda environment before running
- Captures stdout and stderr
- Generates JUnit XML if needed (future extension)

## 4. debug_code.py

Analyzes test failures from a report and suggests fixes.

```bash
python debug_code.py --report "H:\code\Daily\reports\report.json" --code "H:\code\Daily\my_script.py"
```

**Parameters:**
- `--report` (required): JSON report from run_tests.py
- `--code` (required): Original code file that was tested
- `--output` (optional): Path for patched code (not auto-applied)
- `--analyze-only` (flag): Only show analysis, no output

**Output:**
- Prints analysis for each failure
- Saves detailed debug report to `reports/debug_<timestamp>.json`
- Includes error type, context, and suggested fix

**Capabilities:**
- Extracts traceback blocks
- Identifies error type (NameError, TypeError, etc.)
- Provides contextual code snippets
- Generates textual suggestions

**Note:** Does not auto-patch for safety. Use suggestions to manually fix.

## 5. optimize_code.py

Profiles code and checks quality metrics.

```bash
python optimize_code.py --code "H:\code\Daily\my_script.py" --run-profile
```

**Parameters:**
- `--code` (required): Python file to optimize
- `--profile` (optional): Output path for raw profile data (.prof)
- `--report` (optional): JSON report path
- `--run-profile` (flag): Actually run profiling (can be slow)

**Output:**
- JSON report with profiling stats and quality checks
- Console summary with top suggestions
- Returns `REPORT_PATH:<report_path>`

**Capabilities:**
- Runs cProfile to identify bottlenecks
- Runs pylint for code quality
- Runs flake8 for style issues
- Generates prioritized optimization suggestions

**Note:** Use the data to guide manual optimizations. This tool surfaces insights but does not auto-modify code.

## Typical Pipeline

A complete automated workflow:

```bash
# 1. Generate code
python generate_code.py --spec "Your task here" --output "H:\code\Daily\generated.py"

# 2. Create tests
python create_tests.py --code "H:\code\Daily\generated.py"

# 3. Run tests
python run_tests.py --test-dir "H:\code\Daily\tests" --report "H:\code\Daily\reports\test_report.json"

# 4. If failures: debug
python debug_code.py --report "H:\code\Daily\reports\test_report.json" --code "H:\code\Daily\generated.py"

# 5. When tests pass: optimize
python optimize_code.py --code "H:\code\Daily\generated.py" --run-profile
```

## Environment Setup

Before using these scripts, ensure:
1. Conda is installed at `C:\anaconda3\condabin\conda.bat`
2. The `py311` environment exists and has:
   - pytest
   - pylint
   - flake8
   - pandas (if needed)

Create environment if needed:

```bash
call "C:\anaconda3\condabin\conda.bat" create -n py311 python=3.11
call "C:\anaconda3\condabin\conda.bat" activate py311
pip install pytest pylint flake8 pandas
```

All scripts automatically activate the environment before running commands.
