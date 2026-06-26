# Security Considerations

## Overview

This QuickBooks API skill stores sensitive credentials locally in `config.json`. While this is acceptable for OAuth client applications, you should understand the security implications and take appropriate precautions.

## What is Stored

The `config.json` file contains:

- **Client ID**: Your QuickBooks app identifier (semi-public)
- **Client Secret**: Your QuickBooks app secret key (SENSITIVE)
- **Access Token**: Short-lived API access token (SENSITIVE)
- **Refresh Token**: Long-lived token for obtaining new access tokens (VERY SENSITIVE)
- **Realm ID**: QuickBooks company identifier (semi-public)

## Risk Assessment

### Medium Risk Scenarios
- **Local Machine Compromise**: If an attacker gains access to your machine, they can read `config.json` and access your QuickBooks data
- **Backup Exposure**: Unencrypted backups may contain credentials
- **Multi-user Systems**: Other users on the same machine may be able to read the file

### Low Risk Scenarios  
- **Network Eavesdropping**: All API communication is over HTTPS
- **Version Control Leak**: `.gitignore` prevents committing credentials (if used properly)

## Recommended Security Measures

### 1. File Permissions (Critical)

**Windows:**
```powershell
# Set to owner-only access
$acl = Get-Acl "config.json"
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($env:USERNAME, "FullControl", "Allow")
$acl.SetAccessRule($rule)
Set-Acl "config.json" $acl
```

**Linux/Mac:**
```bash
# Set to owner read/write only
chmod 600 config.json
```

### 2. Storage Location

Store the skill in a secure directory:
- ✅ User profile directory (`~/.openclaw/skills/`)
- ✅ Encrypted home directory
- ❌ Network shares
- ❌ Shared/public folders

### 3. Regular Credential Rotation

Rotate your QuickBooks app credentials regularly:

1. Log in to [Intuit Developer Portal](https://developer.intuit.com)
2. Go to your app's "Keys & credentials"
3. Generate new Client Secret
4. Update `config.json` with new secret
5. Re-authenticate with `qb_authenticate`

**Recommended rotation schedule**: Every 90 days for production, or immediately if compromise suspected

### 4. Token Management

- **Refresh tokens expire after 100 days of inactivity** - Use regularly or re-authenticate
- **Access tokens expire after 1 hour** - Automatically refreshed by the skill
- If you suspect token compromise, immediately:
  1. Revoke tokens in QuickBooks Developer Portal
  2. Delete `config.json`
  3. Regenerate app credentials
  4. Re-authenticate

### 5. Environment Separation

Keep sandbox and production credentials completely separate:

- Use different `config.json` files or separate skill directories
- Never use production credentials for testing
- Mark production config clearly: `config.production.json`

### 6. AutoStart Considerations

⚠️ **Do NOT enable autoStart until you've thoroughly tested the skill**

AutoStart means:
- The skill loads automatically when OpenClaw starts
- Credentials are loaded into memory without your explicit action
- Higher exposure window if your session is compromised

Only enable after:
- Verifying all tools work as expected
- Testing error handling
- Confirming no unexpected network calls
- Reviewing all code

### 7. Access Scoping

In your QuickBooks app settings, only enable the scopes you need:

- `com.intuit.quickbooks.accounting` - Full accounting access (required for this skill)
- Consider limited scopes if you only need read access

### 8. Monitoring & Auditing

Watch for suspicious activity:
- Unexpected API calls in QuickBooks audit log
- Unrecognized access from your app
- Token refresh failures (may indicate stolen tokens being revoked)

### 9. Machine Security

Protect your development machine:
- Use full disk encryption
- Enable screen lock with timeout
- Keep OS and security software updated
- Use firewall to limit network exposure
- Don't leave terminals with skill access open unattended

### 10. Incident Response

If you suspect credential compromise:

1. **Immediate Actions:**
   - Disconnect machine from network
   - Revoke tokens in QuickBooks Developer Portal
   - Change QuickBooks password
   - Delete `config.json`

2. **Investigation:**
   - Check QuickBooks audit logs for unauthorized access
   - Review recent API calls
   - Check file access logs for `config.json`

3. **Recovery:**
   - Generate new app credentials
   - Update skill with new credentials
   - Re-authenticate
   - Monitor for 30 days

## Alternative Security Approaches

For higher security requirements, consider:

### Option 1: System Keyring
Modify the skill to store tokens in the OS keyring:
- Windows Credential Manager
- macOS Keychain
- Linux Secret Service

### Option 2: Encrypted Storage
Encrypt `config.json` with a master password:
- Use libraries like `node-keytar` or `cryptr`
- Prompt for password on skill start
- Adds complexity but increases security

### Option 3: Environment Variables
Store Client ID/Secret in environment variables:
```bash
export QB_CLIENT_ID="your_id"
export QB_CLIENT_SECRET="your_secret"
```
Modify skill to read from environment instead of config file

### Option 4: External Secret Management
For enterprise use:
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- CyberArk

## Comparison to OAuth Best Practices

This skill follows OAuth2 best practices:
- ✅ Uses authorization code flow (not implicit)
- ✅ Stores tokens securely in local file (standard for desktop apps)
- ✅ Uses HTTPS for all API communication
- ✅ Implements automatic token refresh
- ✅ Does not expose credentials in code or logs
- ⚠️ Stores client secret locally (acceptable for non-public clients)

## Regulatory Compliance

If you're subject to compliance requirements:

### PCI DSS
- This skill does not handle credit card data directly
- QuickBooks API calls are PCI compliant (Intuit is PCI certified)

### SOC 2
- Document access controls for config.json
- Implement audit logging of skill usage
- Regular security reviews

### GDPR
- QuickBooks data may contain personal information
- Ensure proper data processing agreements
- Implement data retention policies

## FAQ

**Q: Is it safe to use this skill with production QuickBooks data?**  
A: Yes, if you follow the security measures above. The OAuth2 flow is industry-standard, and local credential storage is acceptable for desktop applications.

**Q: Can someone steal my credentials remotely?**  
A: Not unless they've already compromised your machine. All API traffic is over HTTPS. The main risk is local file access.

**Q: Should I commit config.json to Git?**  
A: **NO!** Never commit credentials to version control. It's already in `.gitignore`.

**Q: How do I know if my tokens were compromised?**  
A: Check QuickBooks audit logs for suspicious API activity or unexpected access times.

**Q: What's the worst that could happen?**  
A: An attacker with your tokens could read, create, modify, or delete QuickBooks data with the same permissions your account has. They cannot change your QuickBooks password or access other apps.

## Support

For Intuit security issues:
- [Intuit Security Center](https://security.intuit.com)
- [Report Security Vulnerability](https://trust.intuit.com/report-a-security-issue)

For skill-specific security concerns:
- Review this document
- Audit the source code in `run.js`
- Contact skill maintainer

---

**Last Updated**: February 21, 2026  
**Version**: 1.0.1
