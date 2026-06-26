# Contributing to Vision Tool

Thank you for your interest in contributing to Vision Tool! This document provides guidelines for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Ollama version)

### Suggesting Features
1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Proposed implementation (if you have ideas)

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests if applicable
5. Ensure code passes existing tests
6. Update documentation if needed
7. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.8+
- Ollama with qwen3.5:4b model
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/vision-tool.git
cd vision-tool

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -e .
pip install ruff pytest pytest-cov
```

### Development Commands

Once your environment is set up, use these standard commands:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run code checks
ruff check .

# Format code
ruff format .

# Check formatting without applying changes
ruff format --check .

# Check import sorting
ruff check --select I .

# Run all checks (linting)
ruff check . && ruff format --check . && ruff check --select I .

# Install/update dependencies
pip install -e .
pip install ruff pytest pytest-cov

# Clean build files
rm -rf build/ dist/ *.egg-info/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache/ htmlcov/ .ruff_cache/
```

### Quick Reference

| Task | Command |
|------|---------|
| Set up environment | `python3 -m venv .venv && source .venv/bin/activate && pip install -e . && pip install ruff pytest pytest-cov` |
| Run tests | `pytest tests/ -v` |
| Code checks | `ruff check .` |
| Format code | `ruff format .` |
| Full linting | `ruff check . && ruff format --check . && ruff check --select I .` |

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Run `black .` before committing
- Use meaningful variable and function names

### Testing
- Write tests for new features
- Ensure existing tests pass: `pytest`
- Test with different image types and prompts

## Project Structure
```
vision-tool/
├── SKILL.md          # Skill documentation
├── README.md         # Project overview
├── CONTRIBUTING.md   # This file
├── LICENSE           # License file
├── pyproject.toml    # Python project config
├── main.py           # Main entry point
├── vision            # Bash wrapper script
├── scripts/          # Core implementation
│   └── vision_workflow_optimized.py
└── tests/            # Test files (to be added)
```

## Release Process
1. Update version in `pyproject.toml` and `SKILL.md`
2. Update CHANGELOG.md (to be added)
3. Run tests: `pytest`
4. Create a release tag: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`

## Questions?
Open an issue or join the OpenClaw community discussions.
