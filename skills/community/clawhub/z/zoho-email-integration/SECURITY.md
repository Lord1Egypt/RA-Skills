# Security Advisory - Zoho Email Integration

## Security Fixes in v2.2.1 (2026-02-12)

This release addresses **three critical security vulnerabilities** identified in ClawHub security audits.

### Fixed Vulnerabilities

#### 1. Command Injection in JavaScript Handler (CRITICAL)

**Issue:** The original `email-command.js` used shell command interpolation with user-supplied arguments, allowing potential command injection attacks.

**Attack Example:**
```javascript
/email search "; rm -rf ~; echo "
```

**Fix:** New `email-command-SECURE.js` uses `spawn()` with argument arrays instead of shell interpolation. No shell metacharacters are processed.

**Migration:**
```bash
# Replace vulnerable handler
cp examples/clawdbot-extension/email-command-SECURE.js \
   examples/clawdbot-extension/email-command.js
```

#### 2. Metadata Mismatch (HIGH)

**Issue:** Registry metadata claimed "Required env vars: none" and "Primary credential: none" when ZOHO_EMAIL + ZOHO_PASSWORD or OAuth tokens are actually required.

**Fix:** Updated `clawhub.json` metadata to accurately declare:
- Required environment variables: `ZOHO_EMAIL`
- Primary credential: `oauth2` (with app-password fallback)

#### 3. Insufficient Input Validation (MEDIUM)

**Issue:** No validation of email addresses or search queries.

**Fix:** Added input sanitization:
- Email address format validation
- Shell metacharacter filtering
- Length limits (1000 char max)
- Newline/carriage return removal

#### 4. Token File Permission Enforcement (LOW)

**Issue:** Permissions recommended but not verified on existing token files.

**Fix:** Added automatic permission check and enforcement:
- Checks token file permissions on handler initialization
- Automatically corrects insecure permissions to 0600
- Logs security warnings for visibility

#### 5. Path Traversal in Attachment Download (CRITICAL)

**Issue:** The `download_attachment()` function in `scripts/zoho-email.py` used untrusted attachment filenames directly for file writes, allowing arbitrary file write via malicious attachment names.

**Attack Example:**
An attacker could send an email with an attachment named:
- `../../../../etc/cron.d/backdoor` - Write to system cron
- `~/.ssh/authorized_keys` - Add SSH keys for persistence  
- `../../.bashrc` - Execute code on shell login

**Fix:** Implemented `_sanitize_filename()` function that:
- Strips all directory path components (Windows and Unix)
- Removes null bytes and dangerous characters
- Prevents hidden files (leading dots)
- Limits filename length to 200 characters
- Returns safe basename only

**Impact:** Prevents arbitrary file write, remote code execution, and privilege escalation through malicious email attachments.

**Code Change:**
```python
# Before (VULNERABLE)
if not output_path:
    output_path = filename  # filename from email header - UNSAFE!
with open(output_path, 'wb') as f:
    f.write(payload)

# After (SECURE)
if not output_path:
    safe_filename = self._sanitize_filename(raw_filename)
    safe_output_path = safe_filename
with open(safe_output_path, 'wb') as f:
    f.write(payload)
```

#### 6. Command Injection in Test Script (HIGH)

**Issue:** The `test-app-password.sh` script used `eval` to execute test commands with environment variables (`TEST_EMAIL`), allowing command injection if a malicious email address was provided.

**Attack Example:**
```bash
TEST_EMAIL="user@example.com' ; rm -rf / ; echo '" ./test-app-password.sh
```

**Fix:** 
1. Replaced `eval` with `bash -c` for safer command execution
2. Added regex validation of `TEST_RECIPIENT` email format before any command execution
3. Validation regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

**Impact:** Prevents arbitrary command execution during testing. Script now exits immediately if an invalid email address is detected.

---

## Security Best Practices

### 1. Credential Management

**OAuth2 (Recommended):**
```bash
# Run interactive setup
python3 scripts/oauth-setup.py

# Verify token file permissions
ls -la ~/.clawdbot/zoho-mail-tokens.json  # Should show -rw------- (600)
```

**App Password (Simple):**
```bash
# Use app-specific password, NOT your main Zoho password
export ZOHO_EMAIL="your-email@domain.com"
export ZOHO_PASSWORD="app-specific-password-here"
```

### 2. File Permissions

**Critical files must be secured:**
```bash
# Token file (OAuth2)
chmod 600 ~/.clawdbot/zoho-mail-tokens.json

# Credentials file (app password)
chmod 600 ~/.clawdbot/zoho-credentials.sh
```

**Verify:**
```bash
stat -c "%a %n" ~/.clawdbot/zoho-*
# Output should be: 600 filename
```

### 3. Command Handler Security

**If exposing /email commands to untrusted users:**

1. **Use the secure handler:**
   ```bash
   cp examples/clawdbot-extension/email-command-SECURE.js YOUR_SKILL_PATH/
   ```

2. **Add rate limiting** (not included - implement at bot level)

3. **Restrict command access** to authorized users only

4. **Monitor for abuse:**
   ```javascript
   // Add logging to handler
   console.log(`[AUDIT] User ${userId} executed: /email ${command}`);
   ```

### 4. Network Security

**OAuth setup opens localhost callback:**
- Port: 8080 (or next available)
- Listens only on 127.0.0.1 (not externally accessible)
- Automatically closes after authorization
- Safe on single-user systems

**If running on shared/multi-user server:**
- Use SSH tunnel for OAuth setup
- Or run setup on local machine, then copy token file

---

## Vulnerability Disclosure

Found a security issue? Please report responsibly:

1. **DO NOT** open a public GitHub issue
2. Email: brian@creativestudio.co.za
3. Include: description, impact, proof-of-concept (if applicable)
4. Allow reasonable time for fix before public disclosure

---

## Security Checklist

Before deploying this skill:

- [ ] Using OAuth2 or app-specific password (not main password)
- [ ] Token/credential files have 0600 permissions
- [ ] Using secure command handler (email-command-SECURE.js)
- [ ] Command access restricted to authorized users
- [ ] Audit logging enabled for sensitive operations
- [ ] No hardcoded credentials in code or version control
- [ ] Regular credential rotation policy established

---

## Changelog

**v2.2.1 (2026-02-12)**
- **[CRITICAL]** Fixed path traversal vulnerability in attachment download
- **[CRITICAL]** Fixed command injection in JavaScript handler
- **[HIGH]** Fixed command injection in test script (eval with untrusted input)
- **[MEDIUM]** Added input sanitization and validation for all user inputs
- **[LOW]** Added automatic token file permission enforcement
- Updated metadata to accurately declare credential requirements
- Added comprehensive security documentation (SECURITY.md)

**v2.2.0 (2026-02-12)**
- Initial security hardening (incomplete - use v2.2.1)

**v2.1.0**
- Original release with multiple critical security vulnerabilities

---

## References

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [OAuth2 Security Best Practices](https://datatracker.ietf.org/doc/html/rfc6819)
