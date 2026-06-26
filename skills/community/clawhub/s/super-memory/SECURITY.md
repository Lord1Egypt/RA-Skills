# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| v12.1.x | ✅ |
| v12.0.x | ✅ |
| v10.x | ⚠️ Security fixes only |
| < v10 | ❌ |

## Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
- GitHub Security Advisories: [Report a vulnerability](https://github.com/agent-memory/agent-memory/security/advisories/new)
- Email: security@example.com

You should receive a response within 48 hours. If the vulnerability is confirmed:
- A patch will be released within 7 days for critical issues
- A patch will be released in the next version for non-critical issues

## Security Features

Agent Memory v12 includes:
- SQL injection prevention (identifier whitelisting)
- API Key timing attack protection (hmac.compare_digest)
- PII detection (zero-width chars / HTML entities / NFKC normalization)
- Brute force protection (persistent counters)
- Circuit Breaker (SQLite fault isolation)
- Backup encryption (Fernet key enforcement)
- GDPR auto-purge + ConsentManager
- CryptoStore auto-encryption for sensitive data

## Known Limitations

- Model daemon Unix socket has no authentication (local-only, acceptable for dev)
- CLI shell injection risk with special characters in user input (use SDK instead)
- Dependencies are not pinned by SHA256 hash
