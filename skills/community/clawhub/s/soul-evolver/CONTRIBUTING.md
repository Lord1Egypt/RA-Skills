# Contributing to SoulForge

Thank you for your interest in contributing to SoulForge!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/relunctance/soul-evolver.git
cd soul-evolver

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
# or for development
pip install -e ".[dev]"

# Run tests
python3 tests/test_soulforge.py
```

## Project Structure

```
soul-evolver/
├── soulforge/           # Core Python package
│   ├── __init__.py
│   ├── config.py        # Configuration management
│   ├── memory_reader.py # Memory source reading
│   ├── analyzer.py      # MiniMax API integration
│   └── evolver.py       # File update logic
├── scripts/
│   └── soulforge.py     # CLI entry point
├── references/
│   └── ARCHITECTURE.md  # Technical architecture
└── tests/
    └── test_soulforge.py # Unit tests
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to public functions
- Keep functions small and focused

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high coverage of core modules

```bash
# Run tests
python3 tests/test_soulforge.py

# Run with pytest (if installed)
pytest tests/
```

## Commit Messages

Use conventional commit format:

```
type(scope): description

Types: feat, fix, docs, test, refactor, chore
Scope: config, reader, analyzer, evolver, cli
```

Examples:
- `feat(analyzer): add support for new memory source`
- `fix(evolver): prevent duplicate patterns`
- `docs: update README with new examples`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Add tests
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Reporting Issues

Please include:
- SoulForge version
- Python version
- Minimal reproduction case
- Expected vs actual behavior

## Questions?

Open an issue for discussion before submitting PR if it's a significant change.
