---
name: security-audit
description: Run security audits on codebases using static analysis, dependency scanning, and manual code review patterns. Covers OWASP Top 10, secrets detection, dependency vulnerabilities, and infrastructure misconfigurations. Use when asked to scan code for vulnerabilities, perform a security review, audit a project, or check for security issues. Adapted from Trail of Bits methodology.
---

# Security Audit Skill

Perform security audits on codebases. Adapted from Trail of Bits security research methodology.

## When to Use
- Security review before deployment
- Code audit for vulnerabilities
- Dependency vulnerability check
- Infrastructure/config security review
- Portfolio project security hardening

## Audit Phases

### Phase 1: Reconnaissance
Understand the codebase before scanning:

```bash
# Language detection
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# Framework detection
ls package.json pyproject.toml Gemfile go.mod Cargo.toml requirements.txt 2>/dev/null

# Entry points
grep -r "app.listen\|createServer\|Flask(\|FastAPI(\|func main" --include="*.py" --include="*.js" --include="*.ts" --include="*.go" -l

# Environment and secrets files
find . -name ".env*" -o -name "*.pem" -o -name "*.key" -o -name "*secret*" -o -name "*credential*" | grep -v node_modules | grep -v .git
```

### Phase 2: Automated Scanning

**Secrets Detection:**
```bash
# Grep for common secret patterns
grep -rn "API_KEY\|SECRET\|PASSWORD\|TOKEN\|PRIVATE_KEY\|aws_access\|ssh-rsa" --include="*.py" --include="*.js" --include="*.ts" --include="*.env" --include="*.yaml" --include="*.yml" --include="*.json" . | grep -v node_modules | grep -v .git | grep -v "*.example"
```

**Dependency Vulnerabilities:**
```bash
# Node.js
npm audit --json 2>/dev/null | head -100

# Python
pip-audit 2>/dev/null || pip install pip-audit && pip-audit

# Check for outdated deps
npm outdated 2>/dev/null
pip list --outdated 2>/dev/null
```

**Common Vulnerability Patterns (grep-based):**
```bash
# SQL Injection (string concatenation in queries)
grep -rn "execute.*+\|execute.*%\|execute.*f'" --include="*.py" .
grep -rn "query.*+\|query.*\`" --include="*.js" --include="*.ts" .

# XSS (innerHTML, dangerouslySetInnerHTML)
grep -rn "innerHTML\|dangerouslySetInnerHTML\|v-html\|\$sce.trustAsHtml" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.vue" .

# Command Injection
grep -rn "exec(\|system(\|popen(\|subprocess.call\|child_process" --include="*.py" --include="*.js" --include="*.ts" .

# Path Traversal
grep -rn "\.\./" --include="*.py" --include="*.js" --include="*.ts" . | grep -v node_modules | grep -v test

# Hardcoded credentials
grep -rn "password.*=.*['\"].\+['\"]" --include="*.py" --include="*.js" --include="*.ts" --include="*.yaml" . | grep -v node_modules | grep -v test | grep -v example
```

### Phase 3: Infrastructure Review

```bash
# Dockerfile issues
grep -n "FROM.*latest\|--no-check-certificate\|curl.*\|.*http:" Dockerfile* 2>/dev/null

# CORS configuration
grep -rn "Access-Control-Allow-Origin.*\*\|cors({.*origin.*true\|CORS(.*allow_all" --include="*.py" --include="*.js" --include="*.ts" .

# TLS/SSL
grep -rn "verify.*False\|rejectUnauthorized.*false\|NODE_TLS_REJECT_UNAUTHORIZED" --include="*.py" --include="*.js" --include="*.ts" .

# Rate limiting (absence is a finding)
grep -rn "rateLimit\|rate.limit\|throttle\|slowDown" --include="*.py" --include="*.js" --include="*.ts" . || echo "WARNING: No rate limiting detected"
```

### Phase 4: Manual Review Focus Areas

Based on OWASP Top 10 (2021):
1. **A01 Broken Access Control** — Check auth middleware, route protection, IDOR patterns
2. **A02 Cryptographic Failures** — Weak hashing (MD5/SHA1 for passwords), missing encryption
3. **A03 Injection** — SQL, NoSQL, OS command, LDAP injection
4. **A04 Insecure Design** — Missing input validation, trust boundary violations
5. **A05 Security Misconfiguration** — Debug mode, default credentials, verbose errors
6. **A06 Vulnerable Components** — Outdated dependencies with known CVEs
7. **A07 Auth Failures** — Weak password policy, missing MFA, session fixation
8. **A08 Data Integrity Failures** — Unsigned updates, insecure deserialization
9. **A09 Logging Failures** — Missing audit logs, logging sensitive data
10. **A10 SSRF** — Unvalidated URL inputs, internal service access

## Report Format

```markdown
# Security Audit Report
**Project:** [name]
**Date:** [date]
**Scope:** [files/components audited]

## Executive Summary
[1-2 sentences: overall security posture]

## Critical Findings
### [CRITICAL-001] [Title]
- **Severity:** Critical/High/Medium/Low/Info
- **Category:** OWASP A0X
- **Location:** file:line
- **Description:** What's wrong
- **Impact:** What an attacker could do
- **Remediation:** How to fix it
- **Code:** [before/after snippets]

## Summary Table
| ID | Severity | Category | Title | Status |
|----|----------|----------|-------|--------|
| C-001 | Critical | A03 | SQL Injection in user search | Open |

## Recommendations
[Prioritized list of security improvements]
```

## Limitations
- Grep-based scanning has high false positive rate; manual verification required
- Cannot detect logic flaws or business logic vulnerabilities
- Does not replace professional penetration testing
- No runtime analysis (DAST); static only
