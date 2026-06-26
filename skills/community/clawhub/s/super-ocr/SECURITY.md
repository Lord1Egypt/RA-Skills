# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability in Super OCR, please report it responsibly:

### Email
Send an email to [security@nima-ai.com](mailto:security@nima-ai.com) with:
- Subject: "Security Vulnerability in Super OCR"
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline
- Acknowledgment within 48 hours
- Initial assessment within 1 week
- Regular updates during investigation
- Public disclosure timeline coordinated with reporter

## Security Measures

### Code Review
- All pull requests undergo security review
- Dependency scanning for known vulnerabilities
- Automated security checks in CI/CD

### Dependencies
- Regular updates of third-party libraries
- Pinning of dependency versions
- Audit of security advisories

### Data Protection
- No sensitive data stored in repository
- No user data collection by design
- Secure handling of temporary files

## Best Practices

### For Users
- Keep Super OCR updated to latest version
- Review permissions before installation
- Monitor for unusual behavior
- Report suspicious activity

### For Contributors
- Follow secure coding practices
- Validate all inputs
- Sanitize outputs appropriately
- Use parameterized queries for file operations