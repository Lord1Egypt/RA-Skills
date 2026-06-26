---
name: security-scanner
description: "7-phase security audit pipeline — reconnaissance, dependency scan, application tests, API security, hardening check, OWASP verification, report. Use before production deployments or post-incident."
metadata: { "openclaw": { "emoji": "🛡️", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "bins": ["git"], "anyBins": ["npm", "pip", "pip3", "cargo"] }, "os": ["darwin", "linux", "win32"] } }
---

# Security Scanner — 7-Phase Audit Pipeline

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Before any production deployment
- After a security incident
- Regular scheduled audit (monthly recommended)
- New dependency or library added
- User says "security audit", "check for vulnerabilities", "scan security"
- Code review for security-sensitive features (auth, payments, data handling)

## WHEN NOT TO TRIGGER

- Simple UI changes with no data handling
- Documentation-only changes

---

## PREREQUISITES

**Required**:
- `git` — Used in Phase 6 to scan git history for leaked secrets via `git log --all -p`. Detection: `which git` or `git --version`.

**Optional** (auto-detected for dependency scanning in Phase 2):
- `npm` — Node.js package manager. Runs `npm audit --json` for JavaScript/TypeScript projects. Detected via `which npm` and presence of `package.json`.
- `pip` / `pip3` — Python package manager. Runs `pip audit` for Python projects. Detected via `which pip` or `which pip3` and presence of `requirements.txt` or `pyproject.toml`.
- `cargo` — Rust package manager. Runs `cargo audit` for Rust projects. Detected via `which cargo` and presence of `Cargo.toml`.
- `curl` — Used optionally in Phase 5 for HTTP security header checks. Only invoked when the user provides a target URL. Detected via `which curl`.

If no package manager is detected, Phase 2 is skipped with a note in the report.

---

## PROTOCOL — 7 PHASES

### Phase 1 — RECONNAISSANCE

Map the attack surface:
1. List all entry points (routes, APIs, webhooks, forms)
2. Identify data flows (user input -> storage -> output)
3. Map authentication and authorization boundaries
4. Identify external service integrations
5. Check for exposed ports and services

```bash
# Node.js — find all route definitions
grep -rn "app\.\(get\|post\|put\|delete\|patch\)" --include="*.js" --include="*.ts" -l

# Python — find all route definitions
grep -rn "@app\.\(route\|get\|post\)" --include="*.py" -l
```

### Phase 2 — DEPENDENCY SCAN

Check for known vulnerabilities in dependencies:

```bash
# Node.js — requires npm
npm audit --json 2>/dev/null || echo "npm audit not available — install npm or skip Phase 2"

# Python — requires pip-audit (pip install pip-audit)
pip audit 2>/dev/null || echo "pip audit not available — install pip-audit or skip Phase 2"

# Rust — requires cargo-audit (cargo install cargo-audit)
cargo audit 2>/dev/null || echo "cargo-audit not available — install cargo-audit or skip Phase 2"
```

For each vulnerability found:
- Severity (Critical/High/Medium/Low)
- CVE identifier
- Affected package and version
- Available fix version
- Is it exploitable in this context?

> **NOTE**: `npm audit` and `pip audit` make network calls to vulnerability databases (registry.npmjs.org, pypi.org/pyup.io). These are read-only queries.

### Phase 3 — APPLICATION SECURITY TESTS

Check OWASP Top 10:

1. **Injection** (SQL, NoSQL, OS, LDAP)
   - Search for string concatenation in queries
   - Verify parameterized queries are used
   ```bash
   grep -rn "f['\"].*SELECT\|f['\"].*INSERT\|f['\"].*UPDATE" --include="*.py"
   grep -rn "query.*\+\|exec.*\+" --include="*.js" --include="*.ts"
   ```

2. **Broken Authentication**
   - Check session management: `grep -rn "session\|cookie\|jwt\|token" --include="*.py" --include="*.js" --include="*.ts" | grep -i "expir\|ttl\|maxage"`
   - Verify MFA implementation if applicable

3. **Sensitive Data Exposure**
   - Search for hardcoded secrets:
   ```bash
   grep -rniE "(password|secret|api_key|token|private_key)\s*[:=]\s*['\"][^'\"]{8,}" --include="*.py" --include="*.js" --include="*.ts" --include="*.env"
   ```
   - Check HTTPS enforcement, HSTS headers

4. **XSS** — Search for unsanitized user input in HTML output:
   ```bash
   grep -rn "innerHTML\|dangerouslySetInnerHTML\|v-html\|\|safe" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.html" --include="*.py"
   ```
5. **CSRF** — Verify anti-CSRF tokens on state-changing endpoints
6. **Insecure Deserialization** — Search for dangerous deserialization:
   ```bash
   grep -rn "eval(\|pickle\.loads\|yaml\.load(" --include="*.py" --include="*.js" --include="*.ts"
   ```

### Phase 4 — API SECURITY

For each API endpoint:
1. Authentication required? (JWT, API key, session)
2. Authorization enforced? (role checks, ownership validation)
3. Rate limiting configured?
4. Input validation present? (schema validation, type checking)
5. Response doesn't leak internal details? (stack traces, DB structure)
6. CORS properly configured?

### Phase 5 — HARDENING CHECK

Verify infrastructure hardening.

**HTTP Security Headers** (only when user provides a target URL):

```bash
# Replace $TARGET_URL with the URL provided by the user
curl -sI "$TARGET_URL" | grep -iE "(strict-transport|content-security|x-frame|x-content-type)"
```

> **IMPORTANT**: Only run this check when user provides a target URL. Never make network requests to URLs not explicitly provided by the user.

Checklist:
- [ ] `Strict-Transport-Security` header present
- [ ] `Content-Security-Policy` header present
- [ ] `X-Frame-Options` header present
- [ ] `X-Content-Type-Options: nosniff` header present
- [ ] No server version exposed in response headers
- [ ] Debug mode disabled in production config
- [ ] Error pages don't leak stack traces (inspect error handlers in code)
- [ ] File upload restrictions enforced (check upload handlers for size/type validation)

### Phase 6 — SECRETS VERIFICATION

```bash
# Check git history for leaked secrets (local operation, no network)
git log --all -p | grep -iE "(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]" | head -20

# Verify .gitignore covers sensitive files
cat .gitignore | grep -E "(\.env|secret|credential|\.pem|\.key)"
```

Verify:
- [ ] `.env` files listed in `.gitignore`
- [ ] No secrets found in git history
- [ ] Secrets stored in environment variables or vault
- [ ] No secrets printed in logs or error messages

### Phase 7 — REPORT

Generate a structured security report using the OUTPUT FORMAT below.

---

## LIMITATIONS

**Grep-based scanning (Phases 3 and 6)** uses pattern matching to detect common vulnerability signatures. This approach has inherent limitations:

**False positives**:
- Comments or documentation containing patterns like `password = "example"` will be flagged
- Test fixtures with dummy secrets (e.g., `api_key = "test_key_123"`) will trigger alerts
- String comparisons against constant values (e.g., `if method == "SELECT"`) may be flagged as injection

**False negatives**:
- Obfuscated secrets (base64-encoded, split across variables) will not be detected
- Indirect injection via variable references (e.g., `query = build_query(user_input)`) is not caught
- Secrets committed then deleted from history require `--all` flag and full history scan
- Framework-specific vulnerability patterns not covered by generic regexes

**Recommendation**: Complement grep-based scans with dedicated tools:
- **SAST**: Semgrep, CodeQL, or Bandit (Python)
- **Secrets**: gitleaks, trufflehog, or detect-secrets
- **DAST**: OWASP ZAP, Burp Suite, or Nuclei
- **SCA**: Snyk, Dependabot, or Trivy

---

## RULES

1. **Never skip phases** — even if project seems simple
2. **Evidence-based** — every finding must have file:line or command output
3. **Severity accuracy** — don't inflate or downplay risks
4. **Actionable remediation** — every finding must include HOW to fix
5. **No false security** — passing this scan doesn't mean 100% secure

---

## SECURITY CONSIDERATIONS

- **Commands executed**: `grep` (local pattern matching), `git log` (local history scan), `npm audit` / `pip audit` / `cargo audit` (dependency vulnerability check), `curl` (HTTP HEAD request — Phase 5 only).
- **Network access**: Phase 2 dependency scanners (`npm audit`, `pip audit`) make read-only queries to vulnerability databases. Phase 5 makes ONE outbound HTTP HEAD request via `curl` to check security headers — only when the user provides a target URL. All other phases are local-only.
- **Data read**: Source files, dependency manifests, git history — all within the local repository.
- **File modification**: None. This skill is read-only.
- **Persistence**: None.
- **Credentials**: None required by the skill itself. Scanned output may display secret-like patterns found in the repository — run in a secure terminal.
- **Sandboxing**: Not required (no code execution). Standard terminal security applies when displaying scan results.

---

## OUTPUT FORMAT

```markdown
# Security Audit Report
**Date**: [YYYY-MM-DD]
**Scope**: [project/module name]
**Auditor**: [agent name]

## Executive Summary
- Critical: [count] | High: [count] | Medium: [count] | Low: [count]
- Overall Risk: [Critical/High/Medium/Low]

## Findings

### [CRITICAL/HIGH] Finding Title
- **Category**: [OWASP category]
- **Location**: [file:line]
- **Description**: [what's wrong]
- **Impact**: [what could happen]
- **Remediation**: [how to fix]
- **Status**: [Open/Fixed]

## Dependency Vulnerabilities
| Package | Severity | CVE | Fix Version |
|---------|----------|-----|-------------|
| ...     | ...      | ... | ...         |

## Hardening Status
| Check | Status |
|-------|--------|
| HSTS  | [PASS/FAIL] |
| CSP   | [PASS/FAIL] |
| ...   | ...    |

## Recommendations (Priority Order)
1. [Most critical action]
2. [Second priority]
3. [Third priority]
```

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
