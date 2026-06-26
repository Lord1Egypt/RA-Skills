---
name: save-to-email
description: Send emails through the Resend API. Use when the user wants to send an email, deliver a report by email, forward generated content to an inbox, or trigger an email notification. Trigger on phrases like "send email", "发邮件", "邮件通知", "email this", or "把结果发到邮箱".
metadata:
  openclaw:
    requires:
      env:
        - RESEND_API_KEY
        - RESEND_FROM
      bins:
        - curl
        - python3
    primaryEnv: RESEND_API_KEY
---

# Save To Email

Send HTML emails with Resend.

## When To Use

Use this skill when the user wants Claude to:

- send a formatted email
- email a generated report or summary
- deliver HTML content to one or more recipients
- trigger a lightweight notification email

## Setup

This skill requires a local `.env` file in the skill root with:

```bash
RESEND_API_KEY=your_resend_api_key
RESEND_FROM="Your Name <sender@yourdomain.com>"
```

If `.env` is missing, load the variables from the shell environment before using the script.

## Command

```bash
./scripts/send-email.sh "recipient@example.com" "Subject" "<p>HTML content</p>"
```

## Input Rules

- Argument 1: recipient email address
- Argument 2: subject
- Argument 3: HTML body

Use valid HTML. For plain text, wrap content in `<pre>` or convert line breaks to `<br>`.

## Examples

```bash
./scripts/send-email.sh \
  "recipient@example.com" \
  "Daily Report" \
  "<h2>Summary</h2><p>All jobs finished successfully.</p>"
```

```bash
html="<h1>Project Update</h1><ul><li>Task A done</li><li>Task B in progress</li></ul>"
./scripts/send-email.sh "recipient@example.com" "Project Status" "$html"
```

## Notes

- The script reads `.env` automatically when present.
- Do not hardcode API keys or private sender addresses in this repository.
- Check [README.md](README.md) for public setup guidance.
