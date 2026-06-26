---
name: secrets-audit
description: Scan projects and codebases for exposed secrets, API keys, tokens, passwords, and sensitive credentials. Detects hardcoded secrets in source code, config files, environment files, and git history. Use when asked to audit a project for secrets, check for exposed credentials, scan for API keys, find hardcoded passwords, review security of a codebase, check for leaked tokens, audit .env files, or verify no secrets are committed. Triggers on "secrets audit", "scan for secrets", "find exposed keys", "check for credentials", "security scan", "leaked secrets", "hardcoded passwords", "API key exposure", "credential check".
---

# Secrets Audit

Scan any project directory for exposed secrets, hardcoded credentials, and sensitive data leaks. Produces a severity-ranked report with remediation steps.

## Quick Start

```bash
# Full project scan
python3 scripts/scan_secrets.py /path/to/project

# Scan with git history check
python3 scripts/scan_secrets.py /path/to/project --git-history

# Scan specific file types only
python3 scripts/scan_secrets.py /path/to/project --extensions .py,.js,.ts,.env,.yml,.json

# JSON output for CI integration
python3 scripts/scan_secrets.py /path/to/project --format json
```

## What Gets Detected

### High Severity
- API keys (AWS, GCP, Azure, OpenAI, Stripe, etc.)
- Database connection strings with credentials
- Private keys (RSA, SSH, PGP)
- OAuth tokens and refresh tokens
- JWT secrets and signing keys
- Password fields with literal values

### Medium Severity
- `.env` files with populated secrets
- Config files with credentials (database.yml, settings.py, etc.)
- Hardcoded URLs with embedded auth (user:pass@host)
- Webhook URLs with tokens
- Generic high-entropy strings in assignment context

### Low Severity
- TODO/FIXME comments mentioning secrets
- Placeholder credentials (admin/admin, test/test)
- Example API keys in documentation
- Commented-out credentials

### Ignored (False Positive Reduction)
- Lock files (package-lock.json, yarn.lock, etc.)
- Binary files
- Minified JS/CSS
- Test fixtures clearly marked as fake
- node_modules, .git, vendor directories

## Scan Output

The scanner produces a structured report:

```
=== Secrets Audit Report ===
Project: /path/to/project
Scanned: 247 files | Skipped: 1,203 files
Time: 2.3s

--- HIGH SEVERITY (3 findings) ---

[H1] AWS Access Key ID
  File: src/config/aws.js:14
  Match: AKIA...EXAMPLE
  Context: const accessKey = "AKIA..."
  Fix: Move to environment variable AWS_ACCESS_KEY_ID

[H2] Database Password
  File: config/database.yml:8
  Match: password: "pr0duction_p@ss"
  Fix: Use DATABASE_URL env var or secrets manager

--- MEDIUM SEVERITY (5 findings) ---
...

--- SUMMARY ---
High: 3 | Medium: 5 | Low: 2 | Total: 10
Recommendation: Rotate all HIGH severity credentials immediately
```

## Workflow

### 1. Scan

Run `scripts/scan_secrets.py` against the target directory. The script:
- Recursively walks the directory tree
- Skips binary files, lock files, and dependency directories
- Applies 40+ regex patterns from `references/secret-patterns.md`
- Calculates entropy for potential secrets
- Deduplicates findings

### 2. Review

Present findings grouped by severity. For each finding:
- Show the file, line number, and surrounding context
- Explain what type of secret was found
- Assess whether it's a real secret or false positive

### 3. Remediate

For each confirmed finding, provide specific remediation:
- Which environment variable to use
- How to add to `.gitignore`
- Whether the secret needs rotation (if committed to git)
- Example code showing the fix

### 4. Verify

After remediation:
- Re-run the scan to confirm fixes
- Check git history if secrets were ever committed
- Recommend adding pre-commit hooks to prevent future leaks

## Git History Scanning

When `--git-history` flag is used, the script also checks:
- Deleted files that contained secrets
- Previous versions of files that had secrets removed
- Commits with "secret", "password", "key" in messages

Important: if a secret was ever committed to git, it must be rotated even if later removed — it exists in git history.

## CI Integration

The script returns exit codes for CI pipelines:
- `0` — No findings
- `1` — Low/medium findings only
- `2` — High severity findings (should block deployment)

JSON output (`--format json`) can be parsed by CI tools for automated reporting.

## Pre-commit Hook Setup

After an audit, recommend setting up a pre-commit hook. See `references/prevention-guide.md` for hook installation and configuration.
