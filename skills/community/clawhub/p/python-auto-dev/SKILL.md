---
name: python-auto-dev
description: Automated Python code generation, testing, debugging, and optimization with integrated conda environment management. Uses default conda path "C:\anaconda3\condabin\conda.bat" and environment "py311". Project files are stored at H:\code\Daily. Use when Codex needs to: (1) Generate Python code from specifications, (2) Create and run automated tests, (3) Debug code with interactive tools, (4) Optimize performance and code quality, (5) Manage conda environments for Python projects. This skill bundles executable scripts that handle the entire Python development workflow end-to-end.
---

# Python Auto-Dev Skill

Complete automation for Python development: generate code from specs, add tests, debug, and optimize—all with the configured conda environment.

## Quick Start

When a user provides a coding task:

1. Generate Python code based on their requirements
2. Write unit tests using pytest or unittest
3. Run tests and capture output
4. Debug failures automatically
5. Optimize with profiling and linting
6. Deliver final code with test report

All operations use the `py311` conda environment at `C:\anaconda3\condabin\conda.bat` and store files under `H:\code\Daily`.

## Workflow

### Phase 1: Code Generation

Use `scripts/generate_code.py` to create Python code from a specification. The script accepts:
- `spec`: Natural language description of what the code should do
- `output_path`: Where to save the generated file (default: `H:\code\Daily\generated_<timestamp>.py`)

The generated code should include:
- Type hints
- Docstrings
- Basic error handling
- Modular design

### Phase 2: Test Creation

After code is generated, use `scripts/create_tests.py` to produce comprehensive unit tests:
- Tests edge cases
- Tests error conditions
- Uses pytest fixtures where appropriate
- Outputs to `H:\code\Daily\tests\`

### Phase 3: Test Execution & Debugging

Run tests with `scripts/run_tests.py`:
- Activates the conda environment
- Executes pytest with verbose output
- Captures results in a report file

If tests fail, invoke `scripts/debug_code.py`:
- Analyzes traceback
- Suggests fixes
- Can patch the code automatically (with confirmation)

### Phase 4: Optimization

Once tests pass, use `scripts/optimize_code.py`:
- Runs profiling (cProfile)
- Checks code quality (pylint/flake8)
- Suggests optimizations
- Can apply safe optimizations automatically

## Scripts Reference

All scripts are designed to be called directly by Codex. They handle conda activation internally.

- `scripts/generate_code.py` - Generate Python from spec
- `scripts/create_tests.py` - Create pytest/unittest suite
- `scripts/run_tests.py` - Execute tests and report
- `scripts/debug_code.py` - Analyze failures and suggest/patch
- `scripts/optimize_code.py` - Profile and improve code quality

See `references/script-usage.md` for detailed parameter descriptions and examples.

## Integration Notes

- Default conda path is hard-coded for this setup; modify scripts if path changes.
- All project files are isolated to `H:\code\Daily` to keep workspace clean.
- Scripts assume Windows environment (conda .bat activation).
- Output reports are saved as JSON and plain text for further processing.

## When to Use This Skill

Use this skill when the task involves creating new Python code with a complete development pipeline. It's ideal for:
- Rapid prototyping
- Educational examples
- Automated script generation
- Refactoring tasks with test coverage
- Optimization of existing code

Do not use for non-Python languages or when conda environment is unavailable.
