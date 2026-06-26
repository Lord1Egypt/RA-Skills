---
name: resend-email
description: Send emails using Resend API. Use when the user needs to send emails without configuring SMTP servers. Supports text and HTML emails, multiple recipients, CC/BCC, and bulk sending. Ideal for notifications, alerts, newsletters, and automated email workflows.
---

# Resend Email Sender

Send emails via Resend API - no SMTP configuration needed.

## Quick Start

### 1. Configure

Set environment variables in `.env`:

```bash
RESEND_API_KEY=your_resend_api_key
RESEND_FROM=onboarding@resend.dev  # Optional, defaults to Resend test domain
```

Get API key at https://resend.com

### 2. Send Email

```bash
openclaw run resend-email \
  --to="recipient@example.com" \
  --subject="Hello" \
  --text="Plain text message"
```

## Usage

### Basic Text Email

```bash
openclaw run resend-email \
  --to="user@example.com" \
  --subject="Notification" \
  --text="Your task is complete."
```

### HTML Email

```bash
openclaw run resend-email \
  --to="user@example.com" \
  --subject="Welcome" \
  --html="<h1>Welcome!</h1><p>Thanks for joining.</p>"
```

### Multiple Recipients

```bash
openclaw run resend-email \
  --to="user1@example.com,user2@example.com,user3@example.com" \
  --subject="Team Update" \
  --text="Meeting at 3 PM."
```

### CC and BCC

```bash
openclaw run resend-email \
  --to="primary@example.com" \
  --cc="manager@example.com" \
  --bcc="archive@example.com" \
  --subject="Report" \
  --text="Please find the attached report."
```

### From Agent

When agent needs to send email:

```bash
# Use exec to call the skill
exec openclaw run resend-email \
  --to="recipient@example.com" \
  --subject="Automated Notification" \
  --text="This email was sent automatically by the agent."
```

## Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RESEND_API_KEY` | Yes | - | Your Resend API key |
| `RESEND_FROM` | No | `onboarding@resend.dev` | Default sender address |

## Sender Addresses

- **Test domain**: `onboarding@resend.dev` (default, no setup required)
- **Custom domain**: `noreply@yourdomain.com` (requires domain verification in Resend dashboard)

## Limitations

- Attachments not supported (Resend API requires base64 encoding)
- Rate limits apply based on Resend plan
- Email size limits per Resend documentation

## Troubleshooting

**"RESEND_API_KEY not configured"**
- Set `RESEND_API_KEY` in `.env` file or environment

**"Failed to send email: Unauthorized"**
- Check API key is correct and active
- Verify API key has email sending permission

**"Failed to send email: Bad Request"**
- Check recipient email format is valid
- Verify `from` address is verified (for custom domains)

## Resources

- `scripts/send_email.py` - Main email sending script
