# secrets-audit — Log

## 2026-03-27

### Done
- Initialized skill with scripts, references directories
- Wrote SKILL.md with quick start, detection categories, workflow, CI integration
- Built `scripts/scan_secrets.py` — 40+ patterns covering AWS/GCP/Azure/OpenAI/Stripe/GitHub/databases/webhooks/Telegram/etc.
- Includes Shannon entropy calculation for false positive reduction
- Git history scanning (deleted files, suspicious commit messages)
- CI-friendly exit codes (0/1/2) and JSON output format
- Created `references/secret-patterns.md` — extended pattern reference with remediation
- Created `references/prevention-guide.md` — pre-commit hooks, .gitignore, secrets managers
- Tested with sample project — all planted secrets detected correctly
- Created STATUS.md

### Decisions
- Priced at $59 — dev-focused, lower barrier to entry
- Pure Python stdlib — no external dependencies needed
- Entropy threshold at 2.5 bits — good balance of sensitivity vs false positives
- Skip directories/files aggressively to keep scan fast

### Blockers
- None — ready to package
