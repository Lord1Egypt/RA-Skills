---
name: python-support
description: Python language support for OpenClaw agents. Provides environment setup, dependency management, linting, testing, and best practices for Python code execution. Use when running Python scripts, managing virtual environments, installing packages, debugging Python code, or ensuring code quality with linting and formatting.
---
# Python Support

## Quick Start

Use this skill for all Python-related operations in OpenClaw.

### Environment Check

Verify Python environment:
```bash
python3 --version
pip3 --list
which python3
```

### Running Scripts

Always use absolute paths and specify Python interpreter explicitly:
```bash
python3 /path/to/script.py
```

### Dependency Management

**Install packages safely:**
```bash
pip3 install --quiet package-name
```

For one-off scripts requiring dependencies, use inline installation with verification:
```python
import subprocess
import sys

def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", package])
```

### Best Practices

1. **Shebang**: Use `#!/usr/bin/env python3` for executable scripts
2. **Error handling**: Always include try/except blocks for external operations
3. **Encoding**: Specify `encoding="utf-8"` for all file operations
4. **Paths**: Use `pathlib.Path` for cross-platform path handling
5. **Output**: Prefer JSON or machine-readable formats for structured output

### References

- See [references/style-guide.md](references/style-guide.md) for Python style guidelines
- See [references/testing-patterns.md](references/testing-patterns.md) for testing patterns
- See [references/debugging-tips.md](references/debugging-tips.md) for debugging techniques
