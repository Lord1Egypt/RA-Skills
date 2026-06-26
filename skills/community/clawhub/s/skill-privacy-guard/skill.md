---
name: skill-privacy-guard
description: STOPS all sensitive information from entering skill files. Automatically blocks usernames, paths, personal data when creating or updating skills. CRITICAL - highest priority.
user-invocable: false
disable-model-invocation: false
priority: 1
---

# Skill Privacy Guard

PREVENTS sensitive information from entering skill files. Acts as a security gate that blocks personal data, ensuring all skills remain generic and shareable.

---

## Trigger Conditions

**AUTO-TRIGGER after:**
- Creating a new skill file
- Editing/updating any skill.md file
- User explicitly requests sanitization with keywords: "sanitize", "remove sensitive info", "clean skill"

**CRITICAL:** This skill has TOP PRIORITY. Always run after skill modifications.

---

## What to Remove

### 1. Absolute Paths & File Systems
Replace OS-specific absolute paths with generic notation:

| Pattern | Replace With |
|---------|-------------|
| `C:\Users\{username}\` | `~/` |
| `/home/{username}/` | `~/` |
| `/Users/{username}/` | `~/` |
| `C:\Users\{username}\.claude\` | `~/.claude/` |
| `D:\Projects\myproject\` | `~/projects/example/` |
| `/var/www/mysite/` | `/var/www/example/` |

### 2. Usernames & Identifiers
Replace actual usernames with generic placeholders:

| Context | Replace With |
|---------|-------------|
| File paths | `alice`, `bob`, `user` |
| Profile names | `{username}` placeholder |
| Session examples | Generic names |
| Employee IDs | `EMP-12345` |
| User IDs | `user-id-123` |

### 3. Network & Infrastructure
**CRITICAL - Block all network identifiers:**

- **IP Addresses** → `192.0.2.1` (TEST-NET-1), `10.0.0.1` (generic private)
- **MAC Addresses** → `00:00:00:00:00:00` or `{MAC}`
- **Hostnames** → `server1.example.com`, `host.local`
- **Ports with context** → `8080` (generic), avoid specific service ports
- **Internal domains** → `.example.com`, `.local`
- **VPN endpoints** → `vpn.example.com`
- **Load balancer IPs** → `lb.example.com`

### 4. Credentials & Secrets
**NEVER INCLUDE - Remove immediately:**

- API keys (AWS, Google, etc.)
- Access tokens (Bearer, OAuth)
- Passwords, passphrases
- Private keys (SSH, SSL/TLS)
- Certificates
- Session tokens, cookies
- Database passwords
- Encryption keys
- JWT tokens
- Service account credentials
- SSH fingerprints

### 5. Database & Connection Strings
**Sanitize all connection information:**

- Connection strings → Use placeholder format
- Database names → `example_db`, `myapp_prod`
- Table names → `users`, `products` (generic)
- Schema names → `public`, `main`
- Redis/Cache endpoints → `redis.example.com:6379`

**Example:**
```
Before: mongodb://admin:pass123@10.1.2.3:27017/mycompany
After:  mongodb://{user}:{pass}@{host}:{port}/{database}
```

### 6. Personal Information (PII)
**Remove or genericize:**

- Real email addresses → `user@example.com`
- Phone numbers → `+1-555-0100` (reserved)
- Real names → `Alice Smith`, `Bob Jones`
- Physical addresses → `123 Main St, Anytown, ST 12345`
- Company names → `Acme Corp`, `Example Inc`
- Credit card numbers → `4111-1111-1111-1111` (test card)
- Social security numbers → `XXX-XX-XXXX`
- Passport numbers → `XXXXXXXXX`
- Driver's license → `DL-XXXXXXX`
- National IDs → Placeholder format

### 7. Cloud & Service Identifiers
**Sanitize cloud-specific information:**

- AWS Account IDs → `123456789012` (example)
- AWS Access Keys → `AKIAIOSFODNN7EXAMPLE`
- GCP Project IDs → `my-project-12345`
- Azure Subscription IDs → `{subscription-id}`
- Docker image names with private registry → `registry.example.com/image`
- S3 bucket names → `my-bucket-example`
- CloudFront distributions → `{distribution-id}`

### 8. Version Control & Code
**Sanitize VCS information:**

- Git remote URLs with credentials → Remove credentials
- Git commit hashes (personal repos) → `abc1234` (generic)
- Branch names with usernames → `feature/example-feature`
- Personal repository names → `user/example-repo`

**Example:**
```
Before: https://user:token@github.com/mycompany/private-repo.git
After:  https://github.com/example-org/example-repo.git
```

### 9. Dates & Timestamps with Context
Replace specific dates in examples:

- Recent dates → `2026-01-15` (generic date)
- Timestamps → `2026-01-01T00:00:00Z`
- Or use placeholders: `{YYYY-MM-DD}`, `{timestamp}`

### 10. URLs & Endpoints
**Sanitize web resources:**

- Internal URLs → `https://internal.example.com`
- API endpoints with auth → Remove tokens/keys
- Webhook URLs with secrets → `https://hooks.example.com/{id}`
- Admin panels → `https://admin.example.com`

### 11. License & Product Keys
**NEVER include:**

- Software license keys
- Product activation codes
- Serial numbers
- Registration codes

### 12. File Hashes & Checksums
**Remove if contextual:**

- MD5/SHA hashes of personal files → Generic hash or `{hash}`
- Keep only if demonstrating algorithm

### 13. Custom Internal Systems
**Genericize:**

- Internal tool names → `internal-tool`, `corp-system`
- Proprietary system identifiers
- Custom protocol schemes
- Internal service names

---

## Sanitization Process

### Step 1: Detect Modified Skill

After a skill file is created or modified, automatically:
1. Identify the skill file path
2. Read the complete content
3. Scan for sensitive patterns

### Step 2: Scan for Sensitive Information

**Regular expressions to check:**

```regex
# ===== FILE PATHS =====
# Windows paths with username
C:\\Users\\[^\\]+\\

# Unix paths with username  
/home/[^/]+/
/Users/[^/]+/

# Absolute paths
[A-Z]:\\[^`\n]+
/var/www/(?!example)[^/\s]+

# ===== NETWORK =====
# IP addresses (IPv4) - excluding reserved ranges
\b(?!(?:10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.|192\.168\.|192\.0\.2\.|127\.))\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b

# IPv6 addresses
\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b

# MAC addresses
\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b

# Private hostnames (not example.com/localhost)
\b(?!example\.com|localhost)[a-z0-9-]+\.(local|internal|corp|lan)\b

# ===== CREDENTIALS & SECRETS =====
# AWS Access Key IDs
\b(?:AKIA|ASIA)[0-9A-Z]{16}\b

# AWS Secret Keys
\b[A-Za-z0-9/+=]{40}\b

# Generic API keys
\b[aA][pP][iI][-_]?[kK][eE][yY]\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}

# Bearer tokens
[Bb]earer\s+[A-Za-z0-9\-._~+/]+=*

# Basic auth in URLs
https?://[^:]+:[^@]+@

# JWT tokens
eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*

# Private keys
-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----

# ===== PERSONAL INFORMATION =====
# Real email addresses (not example.com)
\b[A-Za-z0-9._%+-]+@(?!example\.com|test\.com|demo\.com)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b

# Phone numbers (various formats)
\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}

# SSN format
\b\d{3}-\d{2}-\d{4}\b

# Credit card numbers
\b(?:\d{4}[-\s]?){3}\d{4}\b

# ===== USERNAMES & IDS =====
# Specific usernames in file patterns
\b([a-z]{5,}_(python|java|go|cpp))\b

# Employee IDs
\b(?:EMP|EMPLOYEE)[-_]?\d{4,}\b

# User IDs in paths
/users?/\d{5,}/

# ===== DATABASE =====
# Connection strings with credentials
(?:mongodb|mysql|postgresql|redis)://[^:]+:[^@]+@[^/\s]+

# Database hosts with specific names
\b(?:db|database|sql|mongo|redis)[-.](?!example)[a-z0-9-]+\.[a-z]{2,}\b

# ===== CLOUD & SERVICES =====
# AWS Account IDs (12 digits, not example)
\b(?!123456789012)\d{12}\b

# Docker private registries
\b(?!registry\.example\.com)[a-z0-9.-]+\.(?:azurecr\.io|gcr\.io|dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com)

# S3 bucket names (specific ones)
s3://(?!example-bucket)[a-z0-9.-]{3,63}/

# ===== VERSION CONTROL =====
# Git URLs with credentials
git@(?!github\.com/example)[a-z0-9.-]+:[^/\s]+/[^\s]+\.git
https?://[^:]+:[^@]+@(?:github|gitlab|bitbucket)\.com

# Personal Git commit hashes in context
\bcommit\s+[0-9a-f]{7,40}\b

# ===== DATES WITH CONTEXT =====
# Recent specific dates (2024-2026 range)
202[4-6]-(?:0[4-9]|1[0-2])-(?:[0-2][0-9]|3[01])

# Timestamps with recent dates
202[4-6]-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}

# ===== OTHER =====
# File hashes (MD5, SHA1, SHA256) in personal context
\b[a-f0-9]{32}\b
\b[a-f0-9]{40}\b
\b[a-f0-9]{64}\b

# License keys (typical patterns)
\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b

# Internal tool/service names
\b(?:corp|internal|prod|staging)[-_][a-z0-9-]+\b
```

### Step 3: Apply Replacements

Create a sanitized version with:

**Path replacements:**
```
C:\Users\*\.claude\             →  ~/.claude/
/home/*/.claude/                →  ~/.claude/
/Users/*/.claude/               →  ~/.claude/
```

**Username replacements in examples:**
```
john_python.md                  →  alice_python.md
mary_java.md                    →  bob_java.md
userspecificname                →  {username}
```

**Date replacements in examples:**
```
Recent specific dates            →  Generic dates (2026-01-15)
```

### Step 4: Validate & Update

1. Verify all sensitive patterns are removed
2. Ensure skill functionality is preserved
3. Write sanitized content back to skill file
4. Report what was sanitized

---

## Security Checklist

Before finalizing any skill, verify:

**✓ Credentials & Secrets**
- [ ] No API keys, tokens, passwords
- [ ] No private keys or certificates
- [ ] No session tokens or cookies
- [ ] No authentication credentials

**✓ Network Information**
- [ ] No real IP addresses (use TEST-NET or generic)
- [ ] No MAC addresses
- [ ] No internal hostnames
- [ ] No specific port configurations with context

**✓ Personal Information**
- [ ] No real email addresses (use example.com)
- [ ] No phone numbers (use +1-555-0100)
- [ ] No real names (use Alice, Bob)
- [ ] No physical addresses
- [ ] No government IDs (SSN, passport, etc.)

**✓ Infrastructure**
- [ ] No real database connection strings
- [ ] No specific cloud account IDs
- [ ] No private registry URLs
- [ ] No internal service names

**✓ Identifiers**
- [ ] No real usernames (use placeholders)
- [ ] No employee IDs
- [ ] No specific project names
- [ ] No proprietary system names

**✓ File Paths**
- [ ] All paths use `~/` notation
- [ ] No absolute paths with usernames
- [ ] No drive letters (C:\, D:\)

---

## Output Format

After sanitization, output:

```
🔒 Skill Sanitized: {skill_name}

Security scan completed:
  ✓ {N} absolute path(s) → replaced with ~/
  ✓ {N} username(s) → replaced with generic names
  ✓ {N} IP address(es) → replaced with TEST-NET
  ✓ {N} email(s) → replaced with example.com
  ✓ {N} credential(s) → REMOVED
  ✓ {N} date(s) → replaced with generic dates
  ✓ {N} hostname(s) → replaced with example.com
  ✓ {N} connection string(s) → replaced with placeholder
  ✓ {N} other sensitive item(s) → removed/replaced

🛡️  Skill is now secure, generic, and shareable.
```

If no sensitive info found:
```
✓ Skill already secure: {skill_name}
  No sensitive information detected.
```

If CRITICAL issues found (credentials, keys):
```
🚨 CRITICAL: Blocked sensitive data in {skill_name}

REMOVED:
  ⚠️  {N} API key(s)
  ⚠️  {N} password(s)
  ⚠️  {N} private key(s)
  ⚠️  {N} token(s)

These items were completely removed (not replaced).
Manual review recommended.
```

---

## Important Rules

### Priority Rules

1. **SECURITY FIRST** - When in doubt, remove or genericize
2. **Zero tolerance for credentials** - Never allow API keys, passwords, tokens
3. **Err on the side of caution** - Better to over-sanitize than leak data
4. **Block, don't log** - Never log sensitive data during sanitization process

### Functional Rules

5. **Never break functionality** - Only replace examples/paths, not actual logic
6. **Preserve placeholders** - Keep existing `{username}`, `{domain}` intact
7. **Use generic examples** - alice, bob, user for examples
8. **Cross-platform paths** - Always use `~/` notation
9. **No false positives** - Don't replace technical terms unless clearly identifiable

### Replacement Standards

10. **Consistent replacements** - Same input → same output across all skills
11. **Use standard test data** - TEST-NET IPs, +1-555-0100 phones, example.com domains
12. **Document replacements** - Track what was changed in output
13. **Verify after replacement** - Ensure skill still makes sense

### Red Flags - ALWAYS investigate

- Anything that looks like a key or token
- Long alphanumeric strings (40+ chars)
- Strings with "key", "secret", "token", "password" nearby
- Connection strings with @ symbol
- URLs with authentication
- Base64-encoded strings in sensitive contexts
- Hex strings (MD5, SHA hashes)
- JSON with "password", "token", "secret" fields

---

## Edge Cases & Special Handling

### DON'T Sanitize (False Positives to Avoid)

- **Code variable names** - `username`, `password` as variable names in code examples
- **Placeholder syntax** - `{username}`, `{domain}`, `{api-key}` already in placeholder format
- **Technical terms** - `python`, `java`, `nodejs` as technology names
- **Generic examples** - `alice`, `bob`, `user` already used as generic names
- **Reserved ranges** - `192.0.2.x`, `10.0.0.x` already in use as examples
- **Example domains** - `example.com`, `test.com`, `localhost`
- **Test phone numbers** - `+1-555-0100` series (already reserved)
- **Documentation IDs** - `user-id-123`, `session-abc` in placeholder format
- **Algorithm examples** - Hash outputs when demonstrating algorithms
- **Public APIs** - Public API endpoints that are meant to be public

### DO Sanitize (True Positives)

- **Actual credentials** - Even if commented out or in example sections
- **Real paths** - Even in comments or documentation
- **Personal identifiers** - Names, emails, IDs specific to individuals
- **Internal systems** - Private hostnames, internal IPs, proprietary names
- **Recent timestamps** - Dates/times that correlate to real events
- **Organization data** - Real company names, project names, team names
- **Cloud resources** - Actual account IDs, bucket names, instance IDs
- **Version control** - Real repository URLs, commit hashes from private repos

### Special Cases

**Localhost & Local Development:**
- Keep: `localhost`, `127.0.0.1`, `0.0.0.0`
- Sanitize: Specific local network IPs like `192.168.1.100`

**Ports:**
- Keep: Standard ports (80, 443, 3000, 8080) without context
- Sanitize: Unusual ports that might identify specific services

**Documentation URLs:**
- Keep: Official documentation links (docs.python.org, github.com/project/repo)
- Sanitize: Links to internal wikis, private repos, company intranets

**Code Examples:**
- Keep: Demonstrative code that shows structure
- Sanitize: Real code snippets from actual projects

**Error Messages:**
- Keep: Generic error formats
- Sanitize: Error messages with real paths, usernames, or system info

**Log Samples:**
- Keep: Sanitized log format examples
- Sanitize: Real log entries with timestamps, IPs, or usernames

---

## Manual Invocation

User can explicitly trigger with:
- "sanitize this skill"
- "remove sensitive info from {skill_name}"
- "clean up the skill"

Then follow the same process above.
