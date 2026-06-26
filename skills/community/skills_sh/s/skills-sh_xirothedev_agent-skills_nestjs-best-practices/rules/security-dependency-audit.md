---
title: Regular Dependency Security Audits
impact: CRITICAL
section: 1
impactDescription: Prevents exploitation of known vulnerabilities in packages
tags: security, dependencies, npm-audit, snyk
---

## Regular Dependency Security Audits

Outdated dependencies contain known vulnerabilities that attackers exploit. Automated scanning with npm audit, bun audit, and Snyk catches issues before production. **Never deploy without clean dependency audit.**

**Incorrect (vulnerable deps):**

```json
// package.json - outdated packages 🚨
{
  "dependencies": {
    "lodash": "^4.17.20",  // CVE-2021-23337
    "express": "^4.17.1"    // Multiple CVEs
  }
}
```

**Correct (automated security):**

```json
// package.json
{
  "scripts": {
    "audit:fix": "npm audit fix",
    "audit:check": "npm audit --audit-level high",
    "audit:bun": "bun pm audit",
    "security:scan": "snyk test"
  }
}
```

```bash
# Pre-commit / CI checks
bun run audit:check
npm audit --audit-level high
bun pm audit           # Bun's audit check
snyk test --severity-threshold=high
```

**Workflow:**
- `npm audit` or `bun pm audit` weekly in CI/CD
- `npm audit fix` auto-updates patches
- Snyk/Dependabot for vulnerability alerts
- Pin major versions, auto-patch minors