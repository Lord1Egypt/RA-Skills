# Best Practices (SendGrid)

**Live-send safety:** these examples send real email through SendGrid and may incur charges. Obtain approval for the sender, all To/CC/BCC recipients, exact subject/body, template data and attachments before running them. Recipient data, content and attachments go to SendGrid and recipients. Minimize personal data; never include secrets, regulated data or sensitive files without authorization. Read only approved attachment/HTML files. Use a Mail Send-only API key from the environment and never print it. Use recipients you control for approved tests; example addresses are placeholders, not delivery approval.

## Required

- **Verified sender/domain**: Ensure `from` uses a verified sender identity.
- **Use both text + HTML**: Improves deliverability and accessibility.
- **Handle errors correctly**:
  - **400/401/403/422**: Fix request or credentials; do not retry.
  - **429**: Rate limit; retry with exponential backoff.
  - **5xx**: Retry with exponential backoff.

## Attachments

- Base64-encode content.
- Include `type` (MIME) when known.
- Keep payload sizes reasonable; avoid large attachments unless necessary.
- SendGrid limits: max 30 MB total payload; keep attachments under that cap.

## Rate Limits

- **429**: rate limited — retry with exponential backoff.
- **5xx**: server error — retry with exponential backoff.
- **400/401/403/422**: fix request or credentials; do **not** retry.

## Idempotency

SendGrid doesn’t support idempotency keys for Mail Send. If you need idempotency:
- Track your own message IDs and ensure you don’t send duplicates on retry.
- Persist send attempts and outcomes in your DB.

## Testing

- Avoid fake addresses at real providers (bounces hurt reputation).
- Prefer sending to addresses you control (e.g., `test@example.com`).
