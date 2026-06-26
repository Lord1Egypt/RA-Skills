# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x     | ✅ Active support  |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public issue**
2. Use [GitHub's private vulnerability reporting](https://github.com/joelovestech/shrink/security/advisories/new)
3. Or email: joe@joelovestech.com

We will acknowledge receipt within 48 hours and provide a fix timeline within 7 days.

## Security Considerations

- **API keys**: Shrink reads Anthropic API keys from environment variables or OpenClaw's `auth-profiles.json`. Keys are never logged, stored, or transmitted beyond the Anthropic API.
- **Session files**: Shrink modifies OpenClaw session JSONL files in place. A `.bak` backup is created by default before any writes.
- **No network calls** beyond the Anthropic vision API for image description.
- **Redaction:** The `--redact` flag strips sensitive data (PII, secrets, or all) during extraction. Redaction is performed by the vision model at extraction time — sensitive data is never written to the session file when redaction is enabled. This supports GDPR data minimization principles and HIPAA safe harbor requirements.
- **No telemetry** or data collection of any kind.
