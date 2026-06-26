# secrets-audit — Status

**Status:** Ready
**Price:** $59
**Created:** 2026-03-27

## What It Does
Scans project directories for exposed secrets, API keys, tokens, and credentials. 40+ regex patterns covering AWS, GCP, Azure, OpenAI, Stripe, GitHub, databases, and more. Reports with severity ranking and remediation steps.

## Components
- `SKILL.md` — Main skill instructions with workflow
- `scripts/scan_secrets.py` — Core scanner (40+ patterns, entropy analysis, CI exit codes)
- `references/secret-patterns.md` — Extended pattern reference with remediation guide
- `references/prevention-guide.md` — Pre-commit hooks and .gitignore setup

## Testing
- [x] Scanner tested with sample project containing planted secrets
- [x] Detected AWS keys, DB URLs, Stripe keys, env passwords correctly
- [x] Text output format works with severity grouping
- [x] JSON output format works for CI integration
- [x] Exit codes: 0 (clean), 1 (medium), 2 (high) — working
- [x] False positive reduction via entropy filtering
- [x] Script executable

## Next Steps
- Package to .skill file
- Publish to ClawHub
