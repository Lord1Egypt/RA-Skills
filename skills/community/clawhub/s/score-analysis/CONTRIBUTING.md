# Contributing to Score Analysis Skill

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Python version, etc.)

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear title
   - Description of the feature
   - Use cases
   - Any implementation ideas

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation if needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/score-analysis.git
cd score-analysis

# Install dependencies
pip install python-docx matplotlib pandas numpy openpyxl
```

### Running Tests

```bash
# Run example
python scripts/generate_report.py
python scripts/generate_radar_charts.py
```

## Code Style

### Python

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Documentation

- Update README.md for new features
- Add comments for complex logic
- Keep documentation up to date

## Commit Messages

- Use clear, descriptive messages
- Start with a verb in imperative mood
- Keep first line under 72 characters
- Reference issues when applicable

Example:
```
Add support for multiple exam comparisons

- Add trend analysis for multiple exams
- Update report template
- Fix chart generation for large datasets

Closes #123
```

## Pull Request Process

1. Update README.md with details of changes
2. Update the version number if applicable
3. Ensure all tests pass
4. Request review from maintainers
5. Address review feedback
6. Merge after approval

## Questions?

Feel free to open an issue for any questions about contributing!
