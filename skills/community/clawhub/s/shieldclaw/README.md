# ShieldClaw

A security skill suite for OpenClaw, providing comprehensive security protection.

## Features Overview

| Module | Function | Use Case |
|--------|----------|----------|
| **Scan** | Security Scanning | Detect risks before installing Skills |
| **Guard** | Real-time Protection | Intercept suspicious operations |
| **Audit** | Audit Logging | Security reports and traceability |
| **Vault** | Sensitive Data Encryption | Secure storage for passwords/keys |

## Installation

Install via ClawHub:

```bash
npx clawhub@latest install shieldclaw
```

Or search "ShieldClaw" directly in OpenClaw.

## Usage

After installation, use ShieldClaw through natural language in OpenClaw:

### Security Scan

- "Scan this Skill for security issues"
- "Check the security of ~/projects/my-skill"
- "Scan Skills in current directory"

### Real-time Guard

- "Enable file protection for ~/.ssh directory"
- "Block access to sensitive files"
- "View protection interception records"

### Sensitive Data Protection

- "Encrypt this API Key"
- "Store this password for me"
- "Mask sensitive data in this text"

### Security Audit

- "Generate recent security report"
- "View intercepted suspicious operations"
- "Export security logs"

## Configuration

ShieldClaw creates configuration files automatically on first use:

- **Windows**: %APPDATA%/shieldclaw/config.json
- **macOS**: ~/Library/Application Support/shieldclaw/config.json
- **Linux**: ~/.config/shieldclaw/config.json

### Default Configuration

```json
{
  "scan": {
    "enabled": true,
    "autoScanOnInstall": true
  },
  "guard": {
    "enabled": true,
    "strictMode": false,
    "sensitivePaths": ["~/.ssh", "~/.aws"]
  },
  "audit": {
    "enabled": true,
    "retentionDays": 180
  },
  "vault": {
    "enabled": true
  }
}
```

### Modify Configuration

Change settings through OpenClaw conversation:
- "Disable auto scan"
- "Add /data/secrets to protection list"
- "Set log retention to 90 days"

## Data Storage

ShieldClaw stores data locally:

- **Database**: shieldclaw.db - Audit logs and configuration
- **Logs**: logs/ - Runtime logs
- **Keys**: System keychain (auto-managed)

## Changelog

### v1.0.4
- Fixed Linux CLI environment compatibility
- Support for macOS/Windows/Linux platforms

### v1.0.1
- Completely free and open source
- Removed all paid restrictions

### v1.0.0
- Initial release
- Provide Scan/Guard/Audit/Vault features

## License

MIT
