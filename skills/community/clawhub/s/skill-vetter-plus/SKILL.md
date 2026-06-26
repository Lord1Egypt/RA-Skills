---
name: skill-vetter-plus
description: "Security scanner for AI agent skills. 9 built-in detection signatures. Identifies secrets, unsafe execution patterns, and prompt injection. Sub-50ms results."
homepage: https://certainlogic.ai/products/skill-vetter-plus
---

# Skill Vetter Plus

## What It Does

Scans AI agent skills for security issues:
- 9 built-in detection signatures (secrets, execution, prompt injection)
- Sub-50ms scan time
- Run before installing any unknown skill

## How to Use

```bash
# Scan any skill directory
python3 scripts/vetter.py /path/to/installed/skill

# JSON output for piping
python3 scripts/vetter.py /path/to/skill --json
```

## Signatures

| ID | Severity | What It Finds |
|---|---|---|
| hardcoded-api-key | high | `api_key`, `api-key` |
| hardcoded-secret | high | `secret_key`, `secret-token`, `auth_token` |
| hardcoded-password | high | `password` |
| unsafe-eval | critical | `eval(` |
| unsafe-exec | critical | `exec(` |
| unsafe-os-system | critical | `os.system(` |
| subprocess-shell-true | high | `shell=True` |
| raw-network | medium | `urllib.request`, `requests.post`/`get` |
| prompt-injection | critical | `ignore previous instructions`, `ignore the above` |

## What It Does NOT Do

- No AST analysis (text matching only)
- Cannot detect control-flow obfuscation
- Cannot analyze compiled binaries
- Not a replacement for manual code review

## Results

```
Scanned 12 files in 23ms
Found 1 issue(s):
  [CRITICAL] unsafe-eval at /skill/scripts/mail.py:45
    → eval() can execute arbitrary code (matched: 'eval(')
```

## Pro Upgrade

| Feature | Pro ($49) |
|---|---|
| Real-time scanning | ✅ |
| Weekly signature updates | ✅ |
| Team sharing | ✅ |
| Custom signatures | ✅ |
| Priority support | ✅ |

## Limitations

- Text-based pattern matching
- Cannot detect all malware — only patterns in the signature database

## Attribution

- Built by: CertainLogic
- Concept: Skill security pre-checking (industry standard practice)

## Links

- GitHub: https://github.com/CertainLogicAI/skill-vetter-plus
- ClawHub: https://clawhub.ai/certainlogicai/skill-vetter-plus
- Docs: https://certainlogic.ai/docs/skill-vetter-plus

---

*Built by CertainLogic*
