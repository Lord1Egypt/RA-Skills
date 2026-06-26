---
name: skill-dedup-scanner
description: Scans installed skills for duplicates and naming conflicts. Detects similar skills that may cause model confusion. Use before publishing new skills or when troubleshooting trigger conflicts. Supports English and Chinese (auto-detect or --lang flag).
---

# Skill Dedup Scanner 🔍

Detects duplicate or similar skills that may cause model confusion.

## When to Use

- Before publishing a new skill
- When skills trigger incorrectly
- Auditing existing skill collection
- Resolving naming conflicts
- Checking for similar skill names/descriptions

## Usage

### Basic Scan

```bash
# Auto-detect language
python3 scripts/main.py ~/.openclaw/workspace/skills/

# Specify language
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang en
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang zh
```

### Advanced Options

```bash
# Custom threshold (0-1)
python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.8

# Output to file
python3 scripts/main.py ~/.openclaw/workspace/skills/ -o audit_report.md

# JSON output
python3 scripts/main.py ~/.openclaw/workspace/skills/ --json

# Verbose mode
python3 scripts/main.py ~/.openclaw/workspace/skills/ -v
```

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--lang` | `-l` | Language: en, zh, auto | auto |
| `--threshold` | `-t` | Similarity threshold (0-1) | 0.7 |
| `--output` | `-o` | Output file path | stdout |
| `--json` | `-j` | Output in JSON format | false |
| `--verbose` | `-v` | Verbose output | false |

## Output

Generates a detailed report with:
- Similarity scores (name + description)
- Conflict analysis
- Actionable recommendations
- List of safe/unique skills

## Similarity Thresholds

| Score | Level | Action |
|-------|-------|--------|
| > 0.85 | 🔴 High | Consider merging or renaming |
| 0.7-0.85 | 🟡 Medium | Clarify descriptions |
| < 0.7 | ✅ Safe | No action needed |

## Language Support

- **English** (`--lang en`)
- **Chinese** (`--lang zh`)
- **Auto-detect** (`--lang auto`) - Detects system locale

## Examples

### Example 1: Quick Scan

```bash
$ python3 scripts/main.py ~/.openclaw/workspace/skills/
🔍 Scan Directory: /home/user/.openclaw/workspace/skills
📦 Total Skills: 15

✅ No Duplicate Skills Found

All skills have distinct names and descriptions. No optimization needed.
```

### Example 2: Find Conflicts

```bash
$ python3 scripts/main.py ~/.openclaw/workspace/skills/ --threshold 0.6
🔍 Scan Directory: /home/user/.openclaw/workspace/skills
📦 Total Skills: 15

⚠️ Found 2 Groups of Similar Skills

### 1. 🔴 High Similarity Warning

**Skill A:** `tushare-finance`
**Skill B:** `stock-analyzer`

**Similarity Score:** 85%

**Analysis:**
- Name Similarity: 60%
- Description Similarity: 85%

**Recommendations:**
- Clarify the distinction in descriptions
- Rename to make purposes more distinct
```

## Project Structure

```
skill-dedup-scanner/
├── scripts/
│   ├── main.py                 # Main entry point
│   ├── skill_scanner.py        # Skill scanner
│   ├── similarity_checker.py   # Similarity calculator
│   ├── report_generator.py     # Report generator
│   └── locale_loader.py        # Multi-language support
├── locales/
│   ├── en.json                 # English translations
│   └── zh.json                 # Chinese translations
├── references/
│   └── best_practices.md       # Skill naming best practices
└── output/                     # Generated reports
```

## Requirements

- Python 3.7+
- PyYAML (`pip install pyyaml`)

## License

MIT
