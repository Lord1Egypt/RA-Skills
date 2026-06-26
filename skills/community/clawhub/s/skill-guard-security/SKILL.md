---
name: skillguard
description: |
  Security auditing for OpenClaw agent skills. Scans skills for dangerous patterns, 
  vulnerable dependencies, and suspicious behaviors before installation.
metadata:
  openclaw:
    emoji: "🛡️"
    category: security
    tags: [security, audit, safety, scanner]
    version: "0.3.0"
---

# SkillGuard

Security scanner for OpenClaw agent skills.

## What It Does

SkillGuard audits agent skills from ClawHub before you install them, detecting:
- Dangerous code patterns (command injection, eval usage)
- File system access risks
- Network call vulnerabilities  
- Suspicious shell commands
- Known vulnerable dependencies

## Usage

### CLI

```bash
# Audit by skill name
npx skillguard-audit --name <skill-slug>

# Audit local skill folder
npx skillguard-audit --path ./my-skill
```

### API Server

```bash
# Start the API server
npx skillguard-audit serve --port 3402

# Audit via API
curl -X POST http://localhost:3402/api/audit -d '{"name": "some-skill"}'
```

## Verdict

| Rating | Meaning |
|--------|---------|
| 🟢 SAFE | No significant security issues |
| 🟡 CAUTION | Potential risks, review recommended |
| 🔴 DANGEROUS | High-risk patterns, do not install |

## Integration

See [CLAWHUB_INTEGRATION.md](./CLAWHUB_INTEGRATION.md) for ClawHub integration patterns.

## Example Output

```json
{
  "skill": "some-skill",
  "verdict": "CAUTION",
  "score": 65,
  "risks": [
    {"type": "shell_command", "severity": "medium", "file": "index.js", "line": 42}
  ]
}
```
