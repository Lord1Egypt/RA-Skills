# 🛡️ skill-trust-auditor

**Audit any ClawHub skill for security risks BEFORE you install it.**

## 🛠️ Installation

Install the owner-qualified release:
```bash
openclaw skills install @jonathanjing/skill-trust-auditor
```

## What it does

1. Requests OpenClaw's registry verification envelope for the exact owner-qualified release
2. Optionally fetches the target skill's `SKILL.md` and bounded referenced files for local review
3. Runs regex-based heuristic checks against known attack vectors
4. Calculates a **Trust Score (0-100)** with detailed findings
5. Optionally uses **LLM-as-judge** for ambiguous intent

## Trust Score

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100 | ✅ SAFE | Install freely |
| 70-89 | ⚠️ CAUTION | Review flagged items |
| 50-69 | 🟠 RISKY | Only if you understand the risks |
| 0-49 | 🔴 DO NOT INSTALL | High probability of malicious intent |

## Risk patterns detected

- **HIGH** (-30 pts): `process.env` access, `curl | bash`, reverse shells, base64 payloads, reading `~/.openclaw` secrets, data exfiltration via POST
- **MEDIUM** (-10 pts): External API calls, file writes outside workspace, reading MEMORY.md
- **LOW** (-3 pts): Standard web fetches, workspace-only reads

## Usage

Just tell your agent:

> "Audit steipete/some-skill before I install it"

First verify the exact release, then optionally run the deeper local audit:

```bash
openclaw skills verify @owner/skill --json
bash "{baseDir}/scripts/audit.sh" steipete/some-skill
bash "{baseDir}/scripts/audit.sh" steipete/some-skill --llm
bash "{baseDir}/scripts/audit.sh" steipete/some-skill --json-only
```

## Requirements

- Python 3.10+
- Anthropic API key (optional, for `--llm` mode)

## Philosophy

- **Zero trust by default** — every skill must prove it's safe
- **Explainable** — every deduction shows exact file, line, and match
- **White Box** — no black-box scoring; all rules are in `patterns.json`
- **ClawHavoc-aware** — patterns specifically target known Feb 2026 attack vectors
- **Heuristic, not proof** — a high score never authorizes installation or replaces exact-version review

## License

MIT
