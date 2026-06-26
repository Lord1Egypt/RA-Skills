---
name: imap-smtp-email
description: Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, and other standard email providers.
metadata:
  openclaw:
    emoji: "📧"
    requires:
      env:
        - IMAP_HOST
        - IMAP_USER
        - IMAP_PASS
        - SMTP_HOST
        - SMTP_USER
        - SMTP_PASS
      bins:
        - node
        - npm
    primaryEnv: SMTP_PASS
---

# IMAP/SMTP Email Tool

Read, search, and manage email via IMAP protocol. Send email via SMTP. Supports Gmail, Outlook, 163.com, and any standard IMAP/SMTP server.

## Configuration

Create `.env` in the skill folder or set environment variables:

```bash
# IMAP Configuration (receiving email)
IMAP_HOST=imap.gmail.com          # Server hostname
IMAP_PORT=993                     # Server port
IMAP_USER=your@email.com
IMAP_PASS=your_password
IMAP_TLS=true                     # Use TLS/SSL connection
IMAP_REJECT_UNAUTHORIZED=true     # Set to false for self-signed certs
IMAP_MAILBOX=INBOX                # Default mailbox

# SMTP Configuration (sending email)
SMTP_HOST=smtp.gmail.com          # SMTP server hostname
SMTP_PORT=587                     # SMTP port (587 for STARTTLS, 465 for SSL)
SMTP_SECURE=false                 # true for SSL (465), false for STARTTLS (587)
SMTP_USER=your@gmail.com          # Your email address
SMTP_PASS=your_password           # Your password or app password
SMTP_FROM=your@gmail.com          # Default sender email (optional)
SMTP_REJECT_UNAUTHORIZED=true     # Set to false for self-signed certs
```

## Common Email Servers

| Provider | IMAP Host | IMAP Port | SMTP Host | SMTP Port |
|----------|-----------|-----------|-----------|-----------|
| 163.com | imap.163.com | 993 | smtp.163.com | 465 |
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 |
| QQ Mail | imap.qq.com | 993 | smtp.qq.com | 587 |

**Important for Gmail:**
- Gmail does **not** accept your regular account password
- You must generate an **App Password**: https://myaccount.google.com/apppasswords
- Use the generated 16-character App Password as `IMAP_PASS` / `SMTP_PASS`
- Requires Google Account with 2-Step Verification enabled

**Important for 163.com:**
- Use **authorization code** (授权码), not account password
- Enable IMAP/SMTP in web settings first

## IMAP Commands (Receiving Email)

### check
Check for new/unread emails.

```bash
node scripts/imap.js check [--limit 10] [--mailbox INBOX] [--recent 2h]
```

Options:
- `--limit <n>`: Max results (default: 10)
- `--mailbox <name>`: Mailbox to check (default: INBOX)
- `--recent <time>`: Only show emails from last X time (e.g., 30m, 2h, 7d)

### fetch
Fetch full email content by UID.

```bash
node scripts/imap.js fetch <uid> [--mailbox INBOX]
```

### download
Download all attachments from an email, or a specific attachment.

```bash
node scripts/imap.js download <uid> [--mailbox INBOX] [--dir <path>] [--file <filename>]
```

Options:
- `--mailbox <name>`: Mailbox (default: INBOX)
- `--dir <path>`: Output directory (default: current directory)
- `--file <filename>`: Download only the specified attachment (default: download all)

### search
Search emails with filters.

```bash
node scripts/imap.js search [options]

Options:
  --unseen           Only unread messages
  --seen             Only read messages
  --from <email>     From address contains
  --subject <text>   Subject contains
  --recent <time>    From last X time (e.g., 30m, 2h, 7d)
  --since <date>     After date (YYYY-MM-DD)
  --before <date>    Before date (YYYY-MM-DD)
  --limit <n>        Max results (default: 20)
  --mailbox <name>   Mailbox to search (default: INBOX)
```

### mark-read / mark-unread
Mark message(s) as read or unread.

```bash
node scripts/imap.js mark-read <uid> [uid2 uid3...]
node scripts/imap.js mark-unread <uid> [uid2 uid3...]
```

### list-mailboxes
List all available mailboxes/folders.

```bash
node scripts/imap.js list-mailboxes
```

## SMTP Commands (Sending Email)

### send
Send email via SMTP.

```bash
node scripts/smtp.js send --to <email> --subject <text> [options]
```

**Required:**
- `--to <email>`: Recipient (comma-separated for multiple)
- `--subject <text>`: Email subject, or `--subject-file <file>`

**Optional:**
- `--body <text>`: Plain text body
- `--html`: Send body as HTML
- `--body-file <file>`: Read body from file
- `--html-file <file>`: Read HTML from file
- `--cc <email>`: CC recipients
- `--bcc <email>`: BCC recipients
- `--attach <file>`: Attachments (comma-separated)
- `--from <email>`: Override default sender

**Examples:**
```bash
# Simple text email
node scripts/smtp.js send --to recipient@example.com --subject "Hello" --body "World"

# HTML email
node scripts/smtp.js send --to recipient@example.com --subject "Newsletter" --html --body "<h1>Welcome</h1>"

# Email with attachment
node scripts/smtp.js send --to recipient@example.com --subject "Report" --body "Please find attached" --attach report.pdf

# Multiple recipients
node scripts/smtp.js send --to "a@example.com,b@example.com" --cc "c@example.com" --subject "Update" --body "Team update"
```

## Development Email Workflow

### Important Principles

**Template is for structure reference only - always customize content for each recipient.**

**Wrong (avoid):**
- ❌ Sending template email directly without customization
- ❌ Using hardcoded customer names, locations, or company info from templates
- ❌ Sending location-specific content to wrong regions

**Correct approach:**
- ✅ Use template structure only (greeting → company intro → attachments → call-to-action → signature)
- ✅ Customize content based on customer info (company name, country, industry)
- ✅ Generate dynamic HTML content for each recipient

### Pre-send Checklist

```markdown
1. [ ] **Collect customer information**
   - Company name
   - Country/region
   - Industry/business type
   - Contact person name (if available)
   - Email address

2. [ ] **Generate personalized email content**
   - Customize greeting with customer location/industry
   - Adjust tone and focus for different markets
   - Generate HTML file or prepare `--body` content

3. [ ] **Prepare attachments**
   - Product catalog PDF
   - Custom quotation (if applicable)
   - Verify all file paths are correct

4. [ ] **Send complete email in one message**
   - Include all attachments
   - Personalized content
   - Professional signature
```

### Complete Send Command Example

```bash
cd $WORKSPACE/skills/imap-smtp-email

node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Product Catalog from Your Company" \
  --html \
  --body-file "/path/to/customized-email.html" \
  --attach "/path/to/catalogue.pdf,/path/to/quotation.pdf"
```

## OKKI CRM Integration (Optional)

This skill supports automatic sync with OKKI CRM for tracking email communications.

### Configuration

Set environment variables in `.env`:

```bash
# OKKI CRM Integration
OKKI_CLI_PATH=/path/to/okki.py
VECTOR_SEARCH_PATH=/path/to/search-customers.py
PYTHON_VENV_PATH=python3
```

### Features

- Automatic customer matching via domain or vector search
- Email trail creation in OKKI (trail_type=102)
- Quotation trail creation (trail_type=101)
- Deduplication via `/tmp/okki-sync-processed.json`
- Unmatched email logging to `/tmp/okki-unmatched-emails.log`

### Manual Sync Command

```bash
node okki-sync.js quotation '{"dataFile":"/path/to/data.json","quotationNo":"QT-xxx"}'
```

## Discord Review Integration (Optional)

Configure Discord channel for email review workflow.

### Configuration

Edit `config/discord-config.json`:

```json
{
  "channel_id": "<your-discord-channel-id>",
  "guild_id": "",
  "review_channel": "email-review",
  "timeout_minutes": 30
}
```

Set environment variable:
```bash
DISCORD_BOT_TOKEN=your-discord-bot-token
```

## Dependencies

```bash
npm install
```

## Security Notes

- Store credentials in `.env` (add to `.gitignore`)
- **Gmail**: regular password is rejected — generate an App Password at https://myaccount.google.com/apppasswords
- For 163.com: use authorization code (授权码), not account password

## Troubleshooting

**Connection timeout:**
- Verify server is running and accessible
- Check host/port configuration

**Authentication failed:**
- Verify username (usually full email address)
- Check password is correct
- For 163.com: use authorization code, not account password
- For Gmail: regular password won't work — generate an App Password

**TLS/SSL errors:**
- Match `IMAP_TLS`/`SMTP_SECURE` setting to server requirements
- For self-signed certs: set `IMAP_REJECT_UNAUTHORIZED=false` or `SMTP_REJECT_UNAUTHORIZED=false`

## Related Files

- Main scripts: `scripts/imap.js`, `scripts/smtp.js`
- OKKI sync: `okki-sync.js`
- Discord review: `discord-review.js`
- Configuration: `config/discord-config.json`, `profiles/user-map.json`
