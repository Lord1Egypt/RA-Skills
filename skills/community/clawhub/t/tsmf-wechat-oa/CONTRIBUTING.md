# Contributing to WeChat Official Account Auto-Writing System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS)

### Suggesting Features

1. Open an issue with the label `enhancement`
2. Describe the feature and its use case
3. Explain why it would benefit the project

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests if available
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/wechat-allauto-gzh.git
cd wechat-allauto-gzh

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

## Adding New Themes

To add a new theme, edit `scripts/markdown_to_wechat_html.py`:

```python
THEME_PRESETS['your_theme'] = {
    'name': 'Your Theme Name',
    'description': 'Theme description',
    'body': {
        'font_size': '16px',
        'line_height': '1.75',
        'color': '#333333',
        # ... more styles
    },
    'h1': { ... },
    'h2': { ... },
    # ... other elements
}
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Security

- Never commit sensitive information (API keys, credentials)
- Use environment variables for secrets
- Report security vulnerabilities privately

## Questions?

Feel free to open an issue for any questions or discussions.

Thank you for contributing!