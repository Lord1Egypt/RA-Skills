---
name: clawguard
description: "Security scanner for ClawHub skills. Analyze before you install."
license: "MIT"
metadata:
  { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["uv"] } } }
---

# ClawGuard 🛡️

**Scan ClawHub skills for security risks before installing.**

ClawGuard performs static code analysis on ClawHub skills to detect:
- 🌐 Network exfiltration (HTTP POST to external URLs)
- 🔑 Credential access (API keys, tokens, passwords)
- ⚡ Shell command execution
- 💥 File destruction (rm -rf, unlink)
- 🎭 Code obfuscation (eval, base64 decode)
- 👻 Hidden files and directories

## Usage

### Scan by skill name
Download and scan a skill from ClawHub:
```bash
uv run {baseDir}/scripts/scan.py --skill <skill-name>
```

### Scan local directory
Scan a skill directory on your local filesystem:
```bash
uv run {baseDir}/scripts/scan.py --path /path/to/skill
```

### JSON output
Get results in JSON format:
```bash
uv run {baseDir}/scripts/scan.py --skill <skill-name> --json
```

## Examples

Scan the GitHub skill:
```bash
uv run {baseDir}/scripts/scan.py --skill github
```

Scan a local skill:
```bash
uv run {baseDir}/scripts/scan.py --path ~/.openclaw/skills/my-skill
```

## Risk Levels

- 🟢 **SAFE** (0-30): No significant risks detected
- 🟡 **CAUTION** (31-60): Review flagged items before installing
- 🔴 **DANGEROUS** (61-100): High-risk patterns detected — DO NOT INSTALL

## Exit Codes

- `0`: Safe
- `1`: Caution
- `2`: Dangerous

## Requirements

- Python 3.11+
- `uv` (Python package manager)
- `clawhub` CLI (optional, for downloading skills)

## How It Works

1. **Pattern Matching**: Regex-based detection of dangerous code patterns
2. **AST Analysis**: Python AST parsing for eval/exec detection
3. **URL Extraction**: Identifies all network endpoints
4. **Risk Scoring**: Weighted severity scoring (0-100)

## What It Detects

| Category | Weight | Examples |
|----------|--------|---------|
| Network exfiltration | 25 | POST to unknown URL with data |
| Credential access | 20 | Reading API keys, tokens |
| Shell execution | 15 | exec(), subprocess, system() |
| File destruction | 15 | rm -rf, unlink, rmdir |
| Obfuscation | 15 | eval(), atob(), Buffer.from |
| Hidden files | 10 | Dotfiles, hidden directories |

## Limitations

- **Static analysis only**: Cannot detect runtime behavior
- **Regex-based**: May have false positives/negatives
- **JS/TS**: Basic pattern matching (no full AST parsing)
- **Encrypted/minified code**: Cannot analyze obfuscated payloads

## Best Practices

1. **Always scan before installing** untrusted skills
2. **Review CAUTION-level findings** manually
3. **Check network endpoints** for unknown domains
4. **Never install DANGEROUS skills** without verification
5. **Report suspicious skills** to ClawHub moderators

## License

MIT
