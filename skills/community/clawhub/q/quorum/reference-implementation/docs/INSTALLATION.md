# Quorum Installation Guide

This guide covers how to install Quorum and its optional dependencies.

## Core Installation

### Requirements

- Python 3.10 or later
- pip (Python package installer)

### Install Quorum

**Option 1: Development Installation (Recommended)**

```bash
cd reference-implementation
pip install -e .
```

**Option 2: Direct Installation**

```bash
cd reference-implementation
pip install -r requirements.txt
python -m quorum --help
```

### API Keys

Quorum uses [LiteLLM](https://docs.litellm.ai/) as its universal LLM provider, supporting 100+ models including Anthropic Claude, OpenAI, Mistral, and Groq.

Set your API keys as environment variables:

```bash
# Anthropic (Claude)
export ANTHROPIC_API_KEY=your-key-here

# OpenAI
export OPENAI_API_KEY=your-key-here

# Other providers supported by LiteLLM
export MISTRAL_API_KEY=your-key-here
export GROQ_API_KEY=your-key-here
```

## Optional Dependencies

Quorum's pre-screen engine can integrate with external security and code quality tools for enhanced analysis. These tools are **optional** and Quorum will gracefully skip their analysis if not installed.

### DevSkim (Security Scanner)

[Microsoft DevSkim](https://github.com/Microsoft/DevSkim) is a security analysis tool that scans code for security vulnerabilities.

**Installation:**

```bash
# Install .NET (required for DevSkim)
# On macOS with Homebrew:
brew install dotnet

# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0

# Install DevSkim globally
dotnet tool install --global Microsoft.CST.DevSkim.CLI
```

**Verify Installation:**

```bash
devskim --version
```

**What DevSkim adds to Quorum:**
- Security vulnerability detection across multiple languages
- CWE (Common Weakness Enumeration) mapping
- SARIF (Static Analysis Results Interchange Format) output parsing
- Findings integrated as pre-screen evidence for LLM critics

### Ruff (Python Code Quality)

[Ruff](https://github.com/astral-sh/ruff) is a fast Python linter and formatter.

**Installation:**

```bash
# Install via pip
pip install ruff

# Or via pipx (isolated installation)
pipx install ruff

# Or via Homebrew (macOS)
brew install ruff
```

**Verify Installation:**

```bash
ruff --version
```

**What Ruff adds to Quorum:**
- Python code quality analysis
- PEP 8 style checking
- Security rule detection (via bandit-style rules)
- Import sorting and unused import detection
- Findings integrated as pre-screen evidence

## Testing Installation

Verify your Quorum installation with the included examples:

```bash
# Test core functionality
quorum run --target examples/sample-research.md --depth quick

# Test with external tools (if installed)
echo 'password = "secret123"' > test_security.py
quorum run --target test_security.py --depth quick
rm test_security.py
```

## Troubleshooting

### DevSkim Not Found

If you see "DevSkim not installed, skipping DevSkim checks" in the logs:

1. Ensure .NET is installed: `dotnet --version`
2. Ensure DevSkim is in PATH: `which devskim` (Unix) or `where devskim` (Windows)
3. Reinstall DevSkim: `dotnet tool uninstall --global Microsoft.CST.DevSkim.CLI && dotnet tool install --global Microsoft.CST.DevSkim.CLI`

### Ruff Not Found

If you see "Ruff not installed, skipping Ruff checks" in the logs:

1. Ensure Ruff is in PATH: `which ruff` (Unix) or `where ruff` (Windows)
2. Reinstall Ruff: `pip install --upgrade ruff`

### Permission Issues

If you encounter permission errors with global tool installation:

```bash
# Use user-local installation for DevSkim
dotnet tool install --global Microsoft.CST.DevSkim.CLI --tool-path ~/.dotnet/tools

# Add to PATH in your shell profile (.bashrc, .zshrc, etc.)
export PATH="$PATH:$HOME/.dotnet/tools"
```

### Performance

External tools add minimal overhead (~50-200ms per file):

- **DevSkim**: Comprehensive security scanning, recommended for all security-sensitive code
- **Ruff**: Fast Python linting, recommended for all Python projects

Both tools run in parallel with Quorum's built-in pre-screen checks for optimal performance.

---

## Next Steps

After installation, see the [main README](../README.md) for usage examples and the [Rubric Building Guide](../../docs/guides/RUBRIC_BUILDING_GUIDE.md) for information on evaluation criteria.