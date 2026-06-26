# Skill Vetter Plus

## What It Is

The fastest security scanner for AI agent skills on ClawHub, with **9 built-in detection signatures**.

**Use case:** Install before trying any new skill. Run one command. Know if it's safe.

## How It Works

1. Point vetter at any skill directory
2. Scans every file line-by-line against 9 signature types
3. Reports findings in under 50ms

## Signatures (9 Built-In)

| ID | Category | Severity | Description |
|---|---|---|---|
| `hardcoded-api-key` | secrets | high | Possible hardcoded API key |
| `hardcoded-secret` | secrets | high | Possible hardcoded secret or token |
| `hardcoded-password` | secrets | high | Possible hardcoded password |
| `unsafe-eval` | execution | critical | `eval()` can execute arbitrary code |
| `unsafe-exec` | execution | critical | `exec()` can execute arbitrary code |
| `unsafe-os-system` | execution | critical | `os.system()` can execute shell commands |
| `subprocess-shell-true` | execution | high | `subprocess` with `shell=True` is injectable |
| `raw-network` | network | medium | Raw network call found |
| `prompt-injection` | prompt | critical | Potential prompt injection language |

## Installation

```bash
clawhub install skill-vetter-plus
```

## Usage

```bash
# Scan a skill
python3 scripts/vetter.py /path/to/skill

# Scan with JSON output
python3 scripts/vetter.py /path/to/skill --json

# Use custom signatures
python3 scripts/vetter.py /path/to/skill --signatures /path/to/signatures.json
```

## What It Detects

- Hardcoded API keys, tokens, passwords
- `eval()`, `exec()`, `os.system()`, `subprocess(shell=True)`
- Raw network requests
- Prompt injection language

## What It Does NOT Detect

- Malicious logic hidden in control flow
- Exploits in compiled binaries
- Vulnerabilities in skill dependencies
- Social engineering in descriptions

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Pass — no issues found |
| 1 | Fail — one or more issues found |

## Pro Tier

| Feature | Pro |
|---|---|
| Real-time scanning | ✅ |
| Signature updates | Weekly |
| Team sharing | ✅ |
| Custom rules | ✅ |
| Reports | Basic |
| Priority support | Email |

**Upgrade:** https://certainlogic.ai/shop/skill-vetter-plus-pro

## Why Vetter Plus?

- **Fast** — Returns results in under 50ms
- **Comprehensive** — 9 detection signatures covering secrets, execution, and prompts
- **Clear** — Tells you exactly what was found and where
- **Extensible** — Add your own signatures via JSON

## Limitations

- Text-based pattern matching (no AST analysis)
- Cannot detect all malware — only patterns in the signature database
- Recommend: Use as first-line screening, not final security audit

## From the Builder

CertainLogic builds tools for reliability. I test every scanner signature against real skills before release. If something slips through, I fix it and push an update. No obfuscation. No hiding.

## Links

- GitHub: https://github.com/CertainLogicAI/skill-vetter-plus
- ClawHub: https://clawhub.ai/certainlogicai/skill-vetter-plus
- Docs: https://certainlogic.ai/docs/skill-vetter-plus

---

*Built by CertainLogic | [certainlogic.ai](https://certainlogic.ai)*
