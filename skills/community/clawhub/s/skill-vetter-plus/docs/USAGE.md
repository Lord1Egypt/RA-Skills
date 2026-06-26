# Usage Guide — skill-vetter-plus

## Installation

### From Source

```bash
git clone https://github.com/certainlogic/skill-vetter-plus.git
cd skill-vetter-plus
pip install -e .
```

### As OpenClaw Skill

Copy the folder into your skills directory and restart OpenClaw.

## Running Scans

### Basic Scan

```bash
python scripts/vetter.py /path/to/skill
```

### Verbose Output

```bash
python scripts/vetter.py -v /path/to/skill
```

### JSON for CI

```bash
python scripts/vetter.py -j /path/to/skill > report.json
```

### Batch Scanning

```bash
for d in ~/.openclaw/skills/*/; do
    python scripts/vetter.py "$d"
done
```

## Severity Explanations

| Severity | Meaning | Example |
|----------|---------|---------|
| Critical | Likely exploitable vulnerability | Active backdoor, known exploit pattern |
| High | Serious security risk | Hardcoded secret, prompt injection |
| Medium | Potential risk | Unsafe shell usage, unfiltered URL fetch |
| Low | Hygiene issue | World-writable script |
| Info | Suggestion | Missing SKILL.md |

## Interpreting Results

- **False positives happen.** A pattern match does not guarantee a real vulnerability.
- Review each HIGH+ finding manually before dismissing.
- Consider the skill's threat model: a local-only tool has different risk than a network-connected one.

## Custom Rules

You can extend the scanner by editing `RulesEngine` in `scripts/vetter.py` or by enabling `--deep` mode with semgrep (if installed) for additional rule coverage.
