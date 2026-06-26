---
name: security-review
description: Review code changes for security vulnerabilities. Checks for OWASP Top 10, secrets exposure, injection flaws, auth issues, and insecure defaults. Use when reviewing PRs, commits, or code diffs.
triggers:
  - security review
  - check for vulnerabilities
  - secure code review
  - OWASP check
---

# Security Code Review

Review code changes for security vulnerabilities, following OWASP Top 10 and secure coding best practices.

## What to Check

### Injection (SQL, Command, LDAP, XSS)
- User input used in queries without parameterization
- Template literals in SQL strings
- `eval()`, `exec()`, `os.system()` with user input
- Unescaped output in HTML templates

### Authentication & Session
- Hardcoded credentials or API keys
- Weak password requirements
- Missing rate limiting on auth endpoints
- Session fixation or missing regeneration
- JWT without expiration or with weak signing

### Authorization
- Missing access control checks on endpoints
- IDOR (direct object reference without ownership check)
- Role checks that can be bypassed
- Privilege escalation paths

### Secrets & Data Exposure
- API keys, tokens, passwords in code or configs
- Sensitive data in logs
- PII without encryption
- .env files or secrets committed to git

### Configuration
- Debug mode enabled in production
- CORS set to wildcard (*)
- Missing security headers
- Default credentials unchanged
- Verbose error messages exposing internals

## Output Format

For each finding:
```
**FINDING:** [Title]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**File:** [path:line]
**Code:** [the problematic code]
**Issue:** [what's wrong]
**Fix:** [how to fix it, with code example]
**OWASP:** [category reference]
```

## Rules
- Focus on HIGH and CRITICAL findings first
- Provide working fix code, not just descriptions
- If no security issues found, say so clearly
- Note any areas that need manual review (business logic, auth flows)
