# Python CLI Template

When planning a Python CLI tool, ensure the following standards are met:

## Project Structure
- `pyproject.toml` for dependency management.
- `src/` layout for the package.
- `main.py` or `cli.py` as the entry point.

## Standard Libraries
- **`argparse`**: For CLI argument parsing (prefer over raw `sys.argv`).
- **`logging`**: Configure basic logging to stderr.
- **`pathlib`**: Use for all file path operations.

## Patterns
- Include a `--verbose` flag.
- Use `if __name__ == "__main__":` guard.
- Handle `KeyboardInterrupt` gracefully.
