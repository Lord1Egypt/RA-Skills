---
name: deploy-guardian
description: "Pre-deployment verification checklist — tests, types, build, secrets scan, environment validation. Use before pushing to production or staging."
metadata: { "openclaw": { "emoji": "🚀", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "bins": ["git"], "anyBins": ["npm", "python", "python3", "cargo"] }, "os": ["darwin", "linux", "win32"] } }
---

# Deploy Guardian — Pre-Deployment Verification

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Before deploying to production or staging
- User says "deploy check", "ready to deploy?", "pre-deploy", "deploy guardian"
- Before creating a release tag
- Before merging a major PR

## WHEN NOT TO TRIGGER

- Local development iterations
- Draft PRs or WIP branches
- Exploratory prototyping with no deployment intent

---

## PREREQUISITES

This skill requires `git` on PATH. Gates 2-4 auto-detect and run only the toolchain present in the project:

| Toolchain | Required for | Detection |
|-----------|-------------|-----------|
| `npm`/`npx` | Node.js projects | `package.json` exists |
| `python`/`python3` | Python projects | `setup.py`, `pyproject.toml`, or `requirements.txt` exists |
| `cargo` | Rust projects | `Cargo.toml` exists |
| `docker` | Containerized builds | `Dockerfile` exists |

The agent MUST check which toolchain is available before running commands. Skip any gate sub-step whose toolchain is absent — do NOT fail the gate for missing optional toolchains.

---

## PROTOCOL — 6 GATES

Each gate must PASS before proceeding. One FAIL = deployment blocked.

### Gate 1 — GIT STATUS

```bash
git status
git log --oneline -5
git remote update --prune 2>/dev/null && git status -uno
```

Verify:
- [ ] Working tree is clean (no uncommitted changes)
- [ ] On the correct branch (main/release/deploy)
- [ ] Branch is up to date with remote (`git rev-parse HEAD` == `git rev-parse @{u}`)
- [ ] No merge conflicts pending

### Gate 2 — TESTS

Detect the project type and run ONLY the matching test runner:

```bash
# Auto-detect: run the FIRST matching runner only
if [ -f package.json ]; then
  npm test 2>&1
elif [ -f pyproject.toml ] || [ -f setup.py ] || [ -f requirements.txt ]; then
  python -m pytest -v 2>&1 || python3 -m pytest -v 2>&1
elif [ -f Cargo.toml ]; then
  cargo test 2>&1
else
  echo "SKIP: No recognized test runner found"
fi
```

Verify:
- [ ] All tests pass (zero failures)
- [ ] No skipped critical tests
- [ ] Exit code is 0

**Note**: This executes project test scripts, which run code from the repository. Only run in trusted repositories or sandboxed environments.

### Gate 3 — TYPE CHECK & LINT

Auto-detect and run ONLY the matching toolchain:

```bash
# TypeScript (if tsconfig.json exists)
[ -f tsconfig.json ] && npx tsc --noEmit 2>&1

# Python (if .py files exist)
[ -f pyproject.toml ] && python -m ruff check . 2>&1

# ESLint (if .eslintrc* exists)
ls .eslintrc* eslint.config.* 2>/dev/null && npx eslint . 2>&1
```

Verify:
- [ ] Zero type errors
- [ ] Zero lint errors (warnings acceptable)
- [ ] SKIP if no type checker / linter is configured (not a failure)

### Gate 4 — BUILD

Auto-detect and run ONLY the matching build system:

```bash
if [ -f package.json ] && grep -q '"build"' package.json; then
  npm run build 2>&1
elif [ -f Dockerfile ]; then
  docker build --dry-run . 2>&1
elif [ -f Cargo.toml ]; then
  cargo build --release 2>&1
else
  echo "SKIP: No build step detected"
fi
```

Verify:
- [ ] Build completes with exit code 0
- [ ] Output artifacts generated in expected location
- [ ] SKIP if no build system detected (not a failure)

**Note**: Build commands execute project scripts. Same sandboxing considerations as Gate 2 apply.

### Gate 5 — SECRETS SCAN

```bash
# Check for leaked secrets in recent commits (last 5)
git diff HEAD~5..HEAD -- . ':!*.lock' ':!*.sum' | grep -inE "(api[_-]?key|secret|token|password|private[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}" || echo "PASS: No secrets pattern detected"

# Check .env files not committed to git
git ls-files | grep -E "\.env$|\.env\.\w+" | head -10

# Check .gitignore has secret patterns
if [ -f .gitignore ]; then
  COVERAGE=$(grep -cE "\.env|secret|credential|\.pem|\.key" .gitignore)
  echo "Gitignore secret coverage: $COVERAGE patterns"
fi
```

Verify:
- [ ] No secrets pattern in recent commits
- [ ] Zero `.env` files tracked by git
- [ ] `.gitignore` covers at least 3 secret patterns
- [ ] No `.pem`, `.key`, `.p12` files tracked

**Limitations**: This grep-based scan catches common patterns but is not a substitute for dedicated secret scanners (gitleaks, trufflehog, detect-secrets). For production environments, consider running a dedicated scanner as an additional step.

**Warning**: Command output may display matched secret-like patterns in the terminal. Run this gate in a secure terminal session where output is not logged to shared systems.

### Gate 6 — ENVIRONMENT VALIDATION

Run concrete automated checks for the target environment:

```bash
# Check required env vars are documented
if [ -f .env.example ]; then
  echo "PASS: .env.example exists ($(wc -l < .env.example) vars documented)"
else
  echo "WARN: No .env.example — required variables not documented"
fi

# Check for pending database migrations (common frameworks)
[ -d migrations ] && ls -1t migrations/ | head -3
[ -d alembic/versions ] && ls -1t alembic/versions/ | head -3

# Check SSL cert validity (if curl available)
if command -v curl &>/dev/null && [ -n "$DEPLOY_URL" ]; then
  curl -sI --max-time 5 "$DEPLOY_URL" | head -5
fi

# Check Docker health (if applicable)
[ -f docker-compose.yml ] && docker compose config --quiet 2>&1 && echo "PASS: docker-compose config valid"
```

Verify:
- [ ] `.env.example` or equivalent documentation exists
- [ ] No unapplied migrations in queue
- [ ] Target URL responds (if `$DEPLOY_URL` is set)
- [ ] Docker config valid (if applicable)
- [ ] SKIP individual checks when not applicable (not a failure)

---

## SECURITY CONSIDERATIONS

1. **Code execution**: Gates 2-4 execute project scripts (`npm test`, `npm run build`, `cargo test`). These commands run arbitrary code from the repository. **Only run this skill on repositories you trust**, or execute within a sandboxed environment (Docker container, CI/CD pipeline, OpenClaw sandbox mode).

2. **Secret exposure**: Gate 5 scans diffs for secret patterns. Matched patterns are displayed in terminal output. Ensure your terminal session is not logged to shared monitoring systems.

3. **Network access**: Gate 6 optionally makes outbound HTTP requests (via `curl`) only if `$DEPLOY_URL` is explicitly set. No other network access is required.

4. **No persistence**: This skill does not modify any configuration files, install packages, store credentials, or make changes outside the terminal session. It is read-only except for the build artifacts produced by Gate 4.

5. **Sandboxing recommendation**: For maximum safety, run deploy-guardian inside a CI/CD pipeline or a sandboxed agent environment rather than directly on a developer workstation.

---

## OUTPUT FORMAT

```markdown
# Deploy Guardian Report
**Date**: [YYYY-MM-DD HH:MM]
**Branch**: [branch name]
**Commit**: [short SHA]
**Target**: [production/staging]
**Toolchain**: [detected: node/python/rust/docker]

## Gate Results

| # | Gate | Status | Details |
|---|------|--------|---------|
| 1 | Git Status | PASS/FAIL | [clean, correct branch, up to date] |
| 2 | Tests | PASS/FAIL/SKIP | [X passed, Y failed, or skipped reason] |
| 3 | Type Check & Lint | PASS/FAIL/SKIP | [errors count or skipped reason] |
| 4 | Build | PASS/FAIL/SKIP | [success or error summary] |
| 5 | Secrets Scan | PASS/FAIL | [patterns found or clean] |
| 6 | Environment | PASS/WARN/SKIP | [checks run and results] |

## Verdict: [CLEAR TO DEPLOY / BLOCKED / CLEAR WITH WARNINGS]

## Blockers (if any)
1. [What needs to be fixed — file:line reference]

## Warnings (if any)
1. [Non-blocking issues to be aware of]

## Recommended Deployment Command
[The actual deploy command to run]
```

---

## RULES

1. **All gates must pass** — no exceptions, no overrides
2. **Secrets gate is non-negotiable** — one leaked secret = full stop
3. **Auto-detect toolchain** — never run commands for absent toolchains
4. **SKIP is not FAIL** — absent toolchains produce SKIP, not FAIL
5. **Test failures block deployment** — even flaky tests must be investigated
6. **Document blockers** — always explain WHY with file:line references
7. **Never auto-deploy** — always wait for explicit user confirmation
8. **Trusted repos only** — warn user if running on an unfamiliar repository

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
