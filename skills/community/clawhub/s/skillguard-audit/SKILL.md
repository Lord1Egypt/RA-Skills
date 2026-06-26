---
name: skillguard
description: Audit OpenClaw skills for security risks before installation via SkillGuard API.
homepage: https://api.agentsouls.io
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["curl", "jq", "clawhub"] } } }
---

# SkillGuard

Audit any OpenClaw skill for security risks **before** you install it.

Calls the SkillGuard API (`https://api.agentsouls.io/api/audit`) and returns a verdict, risk score, and threat list.

## Usage

### Audit a skill from ClawHub by name

```bash
bash skills/skillguard/audit.sh --name <skill-slug>
```

This uses `clawhub inspect --file` to pull the skill's SKILL.md (and any scripts), then sends the code to the audit API.

### Audit a local file

```bash
bash skills/skillguard/audit.sh --code <path-to-file>
```

Reads the file and sends its contents for audit.

### Output

Returns JSON with:
- **verdict**: `SAFE` | `CAUTION` | `DANGEROUS`
- **riskScore**: 0–100
- **threats**: list of identified risks

Example:
```json
{
  "verdict": "CAUTION",
  "riskScore": 35,
  "threats": ["Executes arbitrary shell commands", "Accesses network without disclosure"]
}
```

## When to use

**Before installing any new skill**, run:

```bash
bash skills/skillguard/audit.sh --name <skill-name>
```

If verdict is `DANGEROUS`, do **not** install. If `CAUTION`, review the threats and decide with the user.

## Privacy Notice

⚠️ **Data transmission**: When you run an audit, the **full source code** of the skill is sent to the SkillGuard API (`https://api.agentsouls.io`) for analysis. No code is stored permanently — it is analyzed in-memory and discarded after the audit completes. The API returns only the verdict, risk score, and detected threats.

If you prefer not to send code to an external service, you can self-host the SkillGuard audit engine (contact us for details) or review skill code manually.
