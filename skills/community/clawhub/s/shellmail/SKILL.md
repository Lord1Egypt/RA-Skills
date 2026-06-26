---
name: shellmail
version: 1.2.2
description: Email API for AI agents. Check inbox, read emails, extract OTP codes, search messages via ShellMail. Trigger on "check email", "inbox", "otp", "verification code", "shellmail", or any email-related requests.
homepage: https://shellmail.ai
source: https://github.com/aaronbatchelder/shellmail
env:
  SHELLMAIL_TOKEN:
    required: true
    sensitive: true
    description: Bearer token for ShellMail API authentication (grants access to inbox and OTPs)
  SHELLMAIL_API_URL:
    required: false
    default: https://shellmail.ai
    description: API base URL (only change for self-hosted instances)
metadata:
  openclaw:
    requires:
      env:
        - SHELLMAIL_TOKEN
      bins:
        - curl
        - python3
      primaryEnv: SHELLMAIL_TOKEN
---

# ShellMail

Email for AI agents via shellmail.ai. Create inboxes, receive mail, extract OTPs automatically.

## ⚠️ Security & Privacy Notice

**This skill requires a sensitive `SHELLMAIL_TOKEN` that grants full access to your inbox and OTPs.**

When you set up this skill for the first time, you'll be instructed to save the token into agent configuration using `gateway config.patch`. This means:
- The agent will retain persistent access to your ShellMail inbox
- The token remains active until you explicitly revoke it or remove it from config
- Only proceed if you fully trust shellmail.ai and understand these privacy implications

**Best practices:**
- Use ShellMail for agent-related activities only, not personal email
- Use disposable/separate recovery emails when possible
- Review the `gateway config.patch` command output before confirming
- Revoke access when you no longer need this skill

## First-Time Setup

If no token is configured:

1. Ask user for desired email name (e.g., "atlas") and a recovery email
   - Or use `auto` for the name to generate a random address (e.g., "swift-reef-4821")
2. Run: `{baseDir}/scripts/shellmail.sh create <name> <recovery_email>`
3. If the address is already taken:
   - If the user says it was their old address: try creating with the same recovery email — deleted addresses are held for 14 days and can be reclaimed
   - Otherwise: suggest a different name or use `auto`
   - Do NOT suggest recovery unless the user confirms it's their previous inbox
4. Save the returned token:

```
gateway config.patch {"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":"sm_..."}}}}}
```

   **⚠️ Important:** Before running this command, explain to the user:
   - This saves the token into agent configuration for persistent access
   - The agent will retain access to their inbox/OTPs until the token is removed or revoked
   - They should only proceed if they trust shellmail.ai and understand the privacy implications
   - Show them the exact command and ask for confirmation before executing

5. Tell user to save the token safely — it won't be shown again
6. Suggest user send a test email to their new address to verify it's working
7. Once they confirm, run `inbox` to show the test email arrived

## Token Recovery

Only use recovery if the user explicitly says they lost access to an existing inbox they own:

```bash
{baseDir}/scripts/shellmail.sh recover <address@shellmail.ai> <recovery_email>
```

This sends a new token to the recovery email on file. Do not suggest this for "address taken" errors.

## Commands

```bash
{baseDir}/scripts/shellmail.sh <command>
```

### Check Inbox
```bash
{baseDir}/scripts/shellmail.sh inbox
{baseDir}/scripts/shellmail.sh inbox --unread
```

### Read Email
```bash
{baseDir}/scripts/shellmail.sh read <email_id>
```

### Get OTP Code
```bash
# Get latest OTP
{baseDir}/scripts/shellmail.sh otp

# Wait up to 30 seconds for OTP
{baseDir}/scripts/shellmail.sh otp --wait 30

# Filter by sender
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

### Search Emails
```bash
{baseDir}/scripts/shellmail.sh search --query "verification"
{baseDir}/scripts/shellmail.sh search --otp
{baseDir}/scripts/shellmail.sh search --from stripe.com
```

### Other Commands
```bash
{baseDir}/scripts/shellmail.sh mark-read <id>
{baseDir}/scripts/shellmail.sh archive <id>
{baseDir}/scripts/shellmail.sh delete <id>
{baseDir}/scripts/shellmail.sh health
```

## Common Patterns

**User says "check my email":**
```bash
{baseDir}/scripts/shellmail.sh inbox --unread
```

**User says "get the verification code":**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30
```

**User says "wait for GitHub OTP":**
```bash
{baseDir}/scripts/shellmail.sh otp --wait 30 --from github.com
```

## Revoking Access

If the user wants to revoke the skill's access to their ShellMail inbox:

### Remove Token from Config
```bash
gateway config.patch '{"skills":{"entries":{"shellmail":{"env":{"SHELLMAIL_TOKEN":""}}}}}'
```

### Delete Account Entirely
```bash
{baseDir}/scripts/shellmail.sh delete-account
```

**Note:** Deleted addresses enter a 14-day hold window and can only be reclaimed by the original owner using the recovery email.

## API Reference

Base URL: `https://shellmail.ai`

All endpoints use `Authorization: Bearer $SHELLMAIL_TOKEN`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/mail` | GET | List emails (?unread=true&limit=50) |
| `/api/mail/:id` | GET | Read full email |
| `/api/mail/:id` | PATCH | Update {is_read, is_archived} |
| `/api/mail/:id` | DELETE | Delete email |
| `/api/mail/otp` | GET | Get OTP (?timeout=30000&from=domain) |
| `/api/mail/search` | GET | Search (?q=text&from=domain&has_otp=true) |
| `/api/addresses` | POST | Create {local, recovery_email} |
