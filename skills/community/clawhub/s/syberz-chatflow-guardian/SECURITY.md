# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of ChatFlow Guardian seriously. If you believe you have found a security vulnerability, please report it to us following these steps:

### 1. **DO NOT** disclose the vulnerability publicly
### 2. **DO NOT** create a public issue
### 3. Email security report to: security@openclaw.ai

### What to include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### Response Timeline:
- **24 hours**: Initial response and triage
- **72 hours**: Status update
- **7 days**: Fix implementation or workaround
- **14 days**: Public disclosure (if applicable)

## Security Best Practices

### Data Handling
- Conversation data is processed locally when possible
- No sensitive data is stored persistently without encryption
- Data retention: 30 days maximum
- GDPR compliant data handling

### Authentication & Authorization
- Platform-specific authentication mechanisms
- No hardcoded credentials
- Secure API key management
- Principle of least privilege

### Code Security
- Regular dependency updates
- Security-focused code reviews
- Static analysis tools
- Input validation and sanitization

### Network Security
- HTTPS for all external communications
- Rate limiting to prevent abuse
- IP filtering where applicable
- Secure WebSocket connections

## Security Features

### Built-in Protections
- Input validation and sanitization
- Output encoding to prevent XSS
- CSRF protection for web interfaces
- SQL injection prevention (where applicable)

### Privacy Controls
- User opt-out for data collection
- Data anonymization options
- Local processing mode
- Clear privacy policy

### Monitoring & Auditing
- Security event logging
- Anomaly detection
- Regular security audits
- Compliance monitoring

## Dependency Security

### Regular Updates
- Automated dependency scanning
- Regular security updates
- Vulnerability monitoring
- Patch management

### Trusted Sources
- Official package repositories
- Verified publishers
- Code signing where available
- Supply chain security

## Responsible Disclosure

We believe in responsible disclosure and will:
- Acknowledge receipt of vulnerability reports
- Work with researchers to understand scope
- Provide timely updates
- Credit researchers (if desired)
- Coordinate public disclosure

## Contact

### Security Team
- Email: 969027040@qq.com
- PGP Key: Available upon request
- Response Time: 24-48 hours

### General Support
- Email: 969027040@qq.com
- Discord: https://discord.gg/openclaw
- Documentation: https://docs.openclaw.ai

## Security Updates

Subscribe to security updates:
- GitHub security advisories
- OpenClaw security announcements
- Email newsletter (opt-in)

---

*Last Updated: 2026-03-27*