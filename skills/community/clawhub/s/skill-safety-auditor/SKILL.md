---
name: skill-safety-auditor
description: Perform comprehensive security audits on skills to identify vulnerabilities, unsafe patterns, and compliance issues. Use when auditing skills for security, checking for hardcoded secrets, injection risks, or before releasing skills.
---

# Skill Safety Auditor

## Overview

The `skill-safety-auditor` skill performs comprehensive security audits on skills to identify vulnerabilities, unsafe code patterns, permission issues, and compliance violations. It helps ensure skills meet security standards before release or deployment.

## When to Use

- During skill development for early issue detection
- Before releasing a new skill to production
- As part of the release approval process
- When the user asks to "audit" or "security check" a skill
- During periodic security reviews
- When reviewing third-party skills

## Core Concepts

### Audit Types

| Type | Description | Speed |
|------|-------------|-------|
| `quick-scan` | Fast surface-level check | ~1s |
| `audit` | Comprehensive analysis | ~5-10s |
| `report` | Full audit with JSON output | ~10s |

### Vulnerability Categories

| Category | Checks For | Severity |
|----------|------------|----------|
| `secrets` | Hardcoded API keys, passwords, tokens | Critical |
| `injection` | Command injection, path traversal | High |
| `permissions` | Unsafe file permissions | Medium |
| `dependencies` | Known vulnerable dependencies | High |
| `network` | Insecure HTTP connections | Low |

### Severity Levels

- **Critical**: Immediate security risk, must fix before release
- **High**: Significant risk, strongly recommended to fix
- **Medium**: Moderate risk, should address
- **Low**: Minor issue, consider fixing
- **Info**: Informational, optional to address

## Input

Accepts:
- Path to skill directory
- Audit type specification
- Output format preference
- Vulnerability type filters

## Output

Produces:
- Console output with findings
- JSON audit reports
- Summary statistics
- Pass/fail status

## Workflow

### Quick Security Check

1. Run quick-scan on target skill
2. Review any immediate issues
3. Address critical/high findings

### Comprehensive Audit

1. Run full audit with verbose output
2. Review all findings by severity
3. Generate JSON report for records
4. Address findings in priority order
5. Re-run audit to verify fixes

### Pre-Release Audit

1. Audit skill with all checks enabled
2. Generate formal report
3. Review with team
4. Fix all critical/high issues
5. Document accepted low-risk items

## Commands

### Quick Scan
```bash
./scripts/quick-scan.sh /path/to/skill
```

### Full Audit
```bash
./scripts/audit-skill.sh /path/to/skill --verbose
```

### Generate Report
```bash
./scripts/audit-skill.sh /path/to/skill --output report.json
```

### Filter by Type
```bash
./scripts/audit-skill.sh /path/to/skill --types secrets,injection
```

### List Past Audits
```bash
./scripts/list-audits.sh [--skill <name>] [--since 2024-01-01]
```

## Output Format

### Console Output
```
🔍 Starting security audit: my-skill
================================
✅ SKILL.md exists
Scanning for secrets...
Scanning for injection vulnerabilities...
[high] injection: eval() detected
  File: src/utils.js:15
  Recommendation: Avoid eval(), use safer alternatives

================================
Validation complete:
  Errors: 0
  Warnings: 1
❌ Validation FAILED
```

### JSON Report
```json
{
  "audit_id": "AUDIT-20240313-001",
  "skill": "my-skill",
  "timestamp": "2024-03-13T10:30:00Z",
  "summary": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 1
  },
  "findings": [
    {
      "id": "SEC-001",
      "severity": "high",
      "type": "injection",
      "file": "src/utils.js",
      "line": 15,
      "description": "eval() detected - potential code injection",
      "recommendation": "Avoid eval(), use safer alternatives"
    }
  ],
  "passed": false,
  "recommendations": [
    "Remove eval() from src/utils.js:15",
    "Add input validation to all user inputs"
  ]
}
```

## Audit Checks

### Secrets Detection
- API keys and tokens
- Database passwords
- Private keys
- Access credentials
- Environment variable patterns

### Code Safety
- eval() usage
- Function constructor
- setTimeout/setInterval with strings
- Child process execution
- Dynamic code execution

### File Permissions
- World-writable files
- Executable permissions on data files
- Sensitive file accessibility

### Dependencies
- Known CVE vulnerabilities
- Deprecated packages
- Potentially dangerous packages

### Network Security
- HTTP vs HTTPS URLs
- Insecure API endpoints
- Missing certificate validation

## Quality Rules

- Always run before releasing skills
- Fix all critical/high findings
- Document accepted risks
- Re-audit after fixes
- Keep audit history

## Good Trigger Examples

- "Audit this skill for security issues"
- "Security check before release"
- "Scan for hardcoded secrets"
- "Check for injection vulnerabilities"
- "Run security audit on skill X"

## Limitations

- Static analysis only; cannot detect runtime vulnerabilities
- May produce false positives for legitimate patterns
- Cannot verify external service security
- Does not test actual runtime behavior
- Limited to known vulnerability patterns

## Resources

### scripts/
- `audit-skill.sh` - Full security audit
- `quick-scan.sh` - Fast security check
- `list-audits.sh` - View audit history
- `test.sh` - Test skill functionality

### references/
- Security best practices
- Common vulnerability patterns
- OWASP guidelines reference
