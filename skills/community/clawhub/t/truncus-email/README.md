# truncus-email

OpenClaw skill for sending transactional emails through the Truncus API.

## 5-Second Demo

> **You:** "Send an alert email to ops@acme.com that the staging database is running low on disk space."
>
> **Agent:** Sent email to ops@acme.com with subject "Alert: Staging database disk space low" via Truncus. Message ID: `clxyz123`.

## What It Does

- Sends transactional emails (alerts, reports, receipts, notifications) via a single REST endpoint
- Enforces idempotency on every send to prevent duplicates
- Supports HTML and plain text bodies, attachments, CC/BCC, scheduled sending
- Validates requests locally before calling the API
- Simulates sends when no API key is configured (local dev mode)
- Handles rate limits and retries automatically

## Install

Clone into your OpenClaw skills directory:

```bash
git clone https://github.com/vanmoose/truncus-openclaw-skill.git ~/.openclaw/skills/truncus-email
```

Or add to a workspace:

```bash
git clone https://github.com/vanmoose/truncus-openclaw-skill.git skills/truncus-email
```

No dependencies. No build step. The skill is a single `SKILL.md` file.

## Get an API Key

1. Go to [https://truncus.co](https://truncus.co)
2. Create an account (3,000 emails/month free, no credit card required)
3. Generate an API key with the `send` scope (and `read_events` if you want delivery tracking)
4. Set it in your environment:

```bash
export TRUNCUS_API_KEY="tr_live_your_key_here"
```

## Local Dev Mode

If `TRUNCUS_API_KEY` is not set, the skill simulates email sends without calling the API. It prints the payload that would be sent and returns a mock success. Useful for testing workflows before going live.

## Example Use Cases

- **Monitoring alert**: "Email the on-call team that API latency exceeded 500ms"
- **Generated report**: "Build a weekly revenue summary table and email it to finance@company.com"
- **User notification**: "Send a welcome email to the new signup with their account details"
- **Incident response**: "Send a post-mortem summary to the engineering distribution list"
- **Scheduled digest**: "Send tomorrow's daily digest at 9am UTC to all team leads"

## API Response Format

### Successful send

```json
{
  "status": "sent",
  "message_id": "cuid-string",
  "provider_message_id": "ses-message-id"
}
```

### Rate limited

```
HTTP 429
Retry-After: 5
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
```

```json
{
  "error": "Rate limit exceeded (60/min). Retry in 5s.",
  "code": "RATE_LIMIT_MINUTE"
}
```

### Validation error

```json
{
  "error": "to: Invalid email; Either html, react, or template_id is required",
  "code": "INVALID_REQUEST"
}
```

### Monthly quota exceeded

```
HTTP 429
X-Monthly-Limit: 3000
X-Monthly-Sent: 3000
X-Monthly-Remaining: 0
```

```json
{
  "error": "Monthly send limit reached (3,000/3,000 on free plan). Upgrade your plan or wait until next month.",
  "code": "MONTHLY_LIMIT_EXCEEDED"
}
```

## Why Truncus

- **Deterministic delivery**: idempotency keys prevent duplicate sends, full event trace per email
- **EU data residency**: AWS SES eu-west-1, Supabase eu-central-1
- **Observable**: every email has a timeline (queued, sent, delivered, bounced, opened, clicked)
- **Predictable pricing**: Free 3K/mo, Pro $19/mo (25K), Scale $99/mo (250K)
- **Agent-native**: MCP server, OpenAPI spec, sandbox mode, CLI

## License

MIT
