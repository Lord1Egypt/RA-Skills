---
name: shieldclaw
description: "Security suite for OpenClaw. Provides security scanning, real-time protection, audit logging, and sensitive data encryption. Use this skill when users need security-related operations, threat detection, or data protection."
metadata:
  emoji: "🛡️"
  requires: {}
---

# ShieldClaw Security Suite

## Overview

ShieldClaw is a security skill suite for OpenClaw, providing four core capabilities:

- **Scan** - Security scanning
- **Guard** - Real-time protection
- **Audit** - Audit logging
- **Vault** - Sensitive data encryption

## Usage Scenarios

### 1. Security Scan (Scan)

Perform security checks before installing or using a Skill.

**Users might say:**
- "Scan this Skill for security issues"
- "Check if ~/projects/my-skill is safe"
- "Are there any risks in Skills in this directory"
- "Scan all Skills in the current directory"

**Capabilities:**
- Detect dangerous function calls
- Discover hardcoded keys/passwords
- Evaluate permission risks
- Identify suspicious network requests
- Provide risk score (0-100)

### 2. Real-time Guard (Guard)

Monitor and intercept suspicious file/network/process operations.

**Users might say:**
- "Enable file protection"
- "Protect ~/.ssh directory from access"
- "Block access to sensitive files"
- "View protection interception records"
- "Add /data/secrets to protection list"

**Capabilities:**
- File system monitoring
- Network request interception
- Process execution control
- Real-time alerts

### 3. Data Vault (Vault)

Encrypt and securely store sensitive data, with auto-detection and masking.

**Users might say:**
- "Encrypt this API Key"
- "Store this password for me"
- "Securely store this private key"
- "Mask sensitive data in this text"
- "View my saved sensitive data"

**Capabilities:**
- AES-256-GCM encryption
- Auto-detect sensitive information (phone, ID, email, etc.)
- Smart masking display
- System keychain for key storage

### 4. Security Audit (Audit)

Record operation logs and generate security reports.

**Users might say:**
- "Generate security report"
- "View recent security events"
- "Export audit logs"
- "View intercepted suspicious operations"
- "What security risks this month"

**Capabilities:**
- Complete operation audit trail
- Visualized reports
- PDF/Excel export
- Compliance checking

## Configuration

ShieldClaw supports the following configuration options:

| Option | Description | Default |
|--------|-------------|---------|
| scan.enabled | Enable scanning | true |
| scan.autoScanOnInstall | Auto-scan on install | true |
| guard.enabled | Enable protection | true |
| guard.strictMode | Strict mode (more sensitive) | false |
| guard.sensitivePaths | Protected paths list | ["~/.ssh", "~/.aws"] |
| audit.enabled | Enable audit | true |
| audit.retentionDays | Log retention days | 180 |
| vault.enabled | Enable encryption | true |

## Security Recommendations

1. **Scan before install**: Scan all third-party Skills before installation
2. **Encrypt sensitive data**: Use Vault for passwords, API Keys, private keys
3. **Protect critical directories**: Enable Guard for SSH keys, AWS credentials
4. **Regular audits**: Review security reports and audit logs regularly

## Notes

- Encryption keys are auto-managed in system keychain
- Audit logs stored in local SQLite database
- Some advanced features may require manual configuration
- Supports Windows, macOS, Linux platforms
