# Skill Safety Auditor

Perform comprehensive security audits on skills to identify vulnerabilities and safety issues.

## Quick Start

```bash
# Quick security scan
./scripts/quick-scan.sh /path/to/skill

# Full security audit
./scripts/audit-skill.sh /path/to/skill --verbose

# Generate JSON report
./scripts/audit-skill.sh /path/to/skill --output report.json
```

## Features

- **Secrets Detection**: Find hardcoded API keys, passwords, tokens
- **Code Safety**: Detect injection vulnerabilities, unsafe patterns
- **Dependency Check**: Identify known CVE vulnerabilities
- **Permission Audit**: Verify safe file permissions
- **Network Security**: Check for insecure connections

## Vulnerability Types

| Type | Checks For |
|------|------------|
| secrets | Hardcoded credentials |
| injection | Command injection, path traversal |
| dependencies | Known CVEs |
| permissions | Unsafe file modes |
| network | Insecure HTTP URLs |

## Severity Levels

- **Critical**: Must fix before release
- **High**: Strongly recommended to fix
- **Medium**: Should address
- **Low**: Consider fixing
- **Info**: Optional

## Related Documentation

See [SKILL.md](./SKILL.md) for complete documentation.
