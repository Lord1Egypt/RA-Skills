# WheelSpotter

> 🎯 Your wheel-spotting scout. Finds reusable solutions before you build from scratch.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## What It Does

**WheelSpotter** spots reusable "wheels" before you write code. The core principle: **solutions must be directly integrable—not flashy but unusable toys.**

## Key Features

- 🎯 **Complexity-aware filtering** - Different search strategies for L1 (simple), L2 (medium), L3 (complex) requirements
- 🔍 **Intent-based platform selection** - Automatically activates relevant platforms (GitHub, PyPI, npm, Maven, Crates.io)
- 💰 **Cost control** - Token/time budgets with early termination when search cost exceeds self-build cost
- ✅ **Closed-loop delivery** - Returns actionable commands (`pip install X`) or clear "self-build" recommendation

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/wheelspotter.git
cd wheelspotter

# Install dependencies
pip install -r requirements.txt

# Basic usage
python scripts/search.py -q "python pdf parser" -c L2 -i library

# Multiple platforms
python scripts/search.py -q "react charting" -c L3 -p github,npm

# With GitHub token (recommended for higher rate limits)
python scripts/search.py -q "rust web framework" --token $GITHUB_TOKEN
```

## Usage Examples

### Find a Python library (L2 complexity)
```bash
python scripts/search.py -q "python excel read write" -c L2 -i library -p github,pypi
```

Output:
```json
{
  "status": "found",
  "recommendations": [
    {
      "name": "openpyxl/openpyxl",
      "source": "github",
      "url": "https://github.com/openpyxl/openpyxl",
      "stars": 3200,
      "action": "pip install openpyxl"
    }
  ]
}
```

### Find a Rust crate (L3 complexity)
```bash
python scripts/search.py -q "rust async runtime" -c L3 -p github,crates
```

### Simple function (L1 - recommends self-build)
```bash
python scripts/search.py -q "email validation" -c L1
```
Returns: "No suitable wheels found. Recommend self-build." (because email validation is ~10 lines of regex)

## CLI Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--query` | `-q` | Search keywords (required) | - |
| `--complexity` | `-c` | L1/L2/L3 | L2 |
| `--intent` | `-i` | library/service/tool/reference | library |
| `--platforms` | `-p` | Comma-separated list | github |
| `--limit` | `-l` | Max results per platform | 20 |
| `--token` | `-t` | GitHub token (optional) | - |
| `--output` | `-o` | Output file | stdout |

## Platform Support

| Platform | Best For | Note |
|----------|----------|------|
| GitHub | All intents | Primary source, star-based ranking |
| PyPI | Python libraries | Exact package name search |
| npm | JavaScript packages | Popularity-based ranking |
| Maven | Java libraries | Central repository search |
| Crates.io | Rust crates | Download-based ranking |

## How It Works

```
User Query
    ↓
[1] Complexity Grading (L1/L2/L3)
    ↓
[2] Intent Classification (library/service/tool/reference)
    ↓
[3] Multi-Platform Search (parallel API calls)
    ↓
[4] Hard Filtering (stars, update time, archived status)
    ↓
[5] Top 5 Recommendations with actionable commands
```

### Cost Control Matrix

| Complexity | Token Budget | Time Budget | Star Threshold |
|------------|--------------|-------------|----------------|
| L1 Simple | 300 | 8s | ≥10 |
| L2 Medium | 600 | 12s | ≥50 |
| L3 Complex | 800 | 15s | ≥100 |

## Project Structure

```
wheelspotter/
├── SKILL.md              # Skill definition (for AI agents)
├── README.md             # This file
├── scripts/
│   └── search.py         # Standalone search script (wheelspot CLI)
├── requirements.txt      # Python dependencies
└── LICENSE              # MIT License
```

## Use as a Skill

This project is designed to work as a WorkBuddy skill. The `SKILL.md` file contains:
- Trigger conditions (when to activate)
- Workflow steps (complexity grading, intent classification, filtering)
- Integration instructions

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Named "WheelSpotter" because it spots reusable wheels before you build from scratch.
