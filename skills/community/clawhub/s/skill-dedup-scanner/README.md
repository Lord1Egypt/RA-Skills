# Skill Dedup Scanner 🔍

Multi-language skill duplicate detector - Scans for duplicates and naming conflicts.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run scan
python3 scripts/main.py ~/.openclaw/workspace/skills/

# Specify language
python3 scripts/main.py ~/.openclaw/workspace/skills/ --lang zh
```

## Documentation

- English: [SKILL.md](SKILL.md)
- 中文：[SKILL.zh-CN.md](SKILL.zh-CN.md)
- GitHub: [https://github.com/shyjsarah/skills/tree/main/skill-dedup-scanner](https://github.com/shyjsarah/skills/tree/main/skill-dedup-scanner)

## Development

```bash
# Run with verbose output
python3 scripts/main.py ~/.openclaw/workspace/skills/ -v

# Output to file
python3 scripts/main.py ~/.openclaw/workspace/skills/ -o report.md

# JSON output
python3 scripts/main.py ~/.openclaw/workspace/skills/ --json
```
