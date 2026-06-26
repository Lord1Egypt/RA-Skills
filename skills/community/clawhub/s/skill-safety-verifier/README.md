# Skill Safety Verifier

**[English](README.md) | [Chinese](README_zh.md)**

> Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources.

## Why This Matters

AI agents run with elevated permissions and can:
- Execute arbitrary commands
- Access file systems
- Make network requests
- Read environment variables

**Unvetted skills = security risk**

## Features

- Code Pattern Scanning - Detect dangerous code (exec/eval/subprocess)
- GitHub Advisory API - Check dependencies for known CVEs
- Permission Analysis - Analyze required permissions from config
- Risk Classification - Classify skills as Safe/Low/Medium/High
- Risk Radar Visualization - Progress bar with color-coded scores

---

## Prerequisites

### Python Version
- Python 3.8 or higher

### Required Dependencies
```bash
# Option 1: Install via pip
pip install -r requirements.txt

# Option 2: Install via setup.py
pip install -e .

# Option 3: Manual install
pip install requests>=2.28.0
```

### Optional (for development)
```bash
pip install pytest pytest-cov
```

---

## Quick Start

### Installation

#### Option 1: Clone and install
```bash
git clone https://github.com/ttttstc/skill-safety-verifier.git
cd skill-safety-verifier
pip install -e .
```

#### Option 2: Via ClawdHub
```bash
npx skills add ttttstc/skill-safety-verifier
```

#### Option 3: Direct download
```bash
# Just download and use
wget https://raw.githubusercontent.com/ttttstc/skill-safety-verifier/main/analyzer.py
wget https://raw.githubusercontent.com/ttttstc/skill-safety-verifier/main/risk_radar.py
```

### Usage

```bash
# Option 1: After pip install
skill-safety-check /path/to/skill

# Option 2: Direct Python
python analyzer.py /path/to/skill
python3 analyzer.py /path/to/skill

# Output JSON
python analyzer.py /path/to/skill --json

# Help
python analyzer.py --help
```

---

## Project Structure

```
skill-safety-verifier/
├── bin/                      # Entry point scripts
│   └── skill-safety-check   # CLI launcher
├── analyzer.py               # Main analyzer
├── risk_radar.py             # Risk radar renderer
├── requirements.txt           # Python dependencies
├── setup.py                  # Package configuration
├── SKILL.md                  # OpenClaw skill definition
├── README.md                 # English documentation
├── README_zh.md              # Chinese documentation
└── LICENSE                  # MIT license
```

---

## Workflow

```
User triggers installation
    |
    v
1. Clone skill repository
    |
    v
2. Parallel scanning:
   - Scan code patterns (exec/eval/subprocess)
   - Check GitHub Advisory API
   - Analyze permissions
    |
    v
3. Calculate risk scores
    |
    v
4. Render Risk Radar
    |
    v
User decision
```

---

## Risk Classification

| Level | Score | Color | Action |
|-------|-------|-------|--------|
| Safe | 0-10 | Green | Install & use freely |
| Low | 11-30 | Yellow | Install with caution |
| Medium | 31-60 | Orange | Review code first |
| High | 61-100 | Red | Do not install |

---

## Output Examples

### Safe Skill

```
skill-name - Risk Assessment

Risk Radar:
  Network      0/50  Green
  Vulnerabil. 0/25  Green
  Permissions 0/50  Green
  Total       0/100 Green

Recommendation: Safe to install
```

### Medium Risk Skill

```
skill-name - Risk Assessment

Risk Radar:
  Network      20/50 Yellow
  Vulnerabil.  5/25  Green
  Permissions 25/50 Orange
  Total        50/100 Orange

Warning: Network calls detected
Recommendation: Review code before install
```

---

## Configuration

### Cache Directory
Default: `~/.cache/skill-safety/`

### Cache TTL
- Advisory data: 24 hours
- Skill dependencies: 6 hours

### GitHub API
- No authentication required (60 requests/hour)
- With authentication: 5000 requests/hour

---

## Integration

### With ClawdHub

```bash
# Install with auto-verification
npx skills add <owner/repo> --verify
```

### In Your Own Pipeline

```python
from analyzer import analyze_skill

result = analyze_skill('/path/to/skill')
print(result['scores'])
# {'network': 0, 'vuln': 0, 'permission': 25, 'total': 25}
```

---

## Best Practices

1. Always verify - Never install unvetted skills
2. Read the code - Automated checks aren't enough
3. Least privilege - Only grant necessary permissions
4. Isolate - Run high-risk skills in containers
5. Monitor - Log all skill activity

---

## Troubleshooting

### "No module named 'requests'"
```bash
pip install requests
```

### "SSL certificate verify failed"
The analyzer uses SSL verification by default. If you encounter issues, you can disable SSL verification (not recommended for production).

### "API rate limit exceeded"
Wait an hour or use a GitHub token for higher rate limits.

---

## Related

- ClawdHub (https://clawhub.com) - Skill marketplace
- GitHub Advisory API (https://api.github.com/advisories)
- OpenClaw Docs (https://docs.openclaw.ai)

---

## License

MIT License - see LICENSE file for details.
