# generic-mail-client

A generic email client skill. Supports any mailbox using IMAP/POP3 + SMTP with username and password authentication:
- Alibaba Cloud Enterprise Mail
- QQ Mail / 163 / Gmail / Outlook / Exchange (with IMAP/POP3/SMTP enabled)

## Capabilities

- Multi-account support — select mailbox via accountId
- Sending (SMTP):
  - Plain text / HTML / Markdown body
  - Multiple recipients (To/Cc/Bcc)
  - Attachments (base64 transfer)
- Receiving (IMAP/POP3):
  - List recent emails (by folder, date, unread status, keyword)
  - View email details (subject, body, attachment info)
  - Retrieve attachment content (optional)
  - Mark as read/unread, move emails (IMAP only)

## Security Notes

- All mailbox credentials (host/port/username/password) are stored only in the host configuration and are not visible to the LLM.
- Logs do not record full email bodies or attachment content — only API call results, email IDs, timestamps, and other metadata.
- It is strongly recommended to use a dedicated bot email account or app-specific password. Do not use your personal login password.
- Default rate limits and list size caps are enforced to prevent misuse as a spam tool.

## Configuration

See `config.example.yaml`. Copy it to `config.yaml` on the host side and inject it into the skill.
