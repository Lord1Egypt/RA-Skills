# STM Assistant

**Professional email outreach on behalf of your human.**

Send branded, professional emails from a dedicated agent inbox — with proper signatures, Reply-To routing, and CC tracking. Your human never touches the send button.

## The Problem

Your human needs to send professional emails (attorney outreach, vendor inquiries, scheduling requests) but keeps putting them off. You could draft them, but they still have to copy-paste into their email client.

## What This Does

STM Assistant gives your agent:

1. **A dedicated outbound inbox** — via [AgentMail](https://agentmail.to) or any SMTP provider
2. **Branded email signatures** — logo, name, "sent on behalf of" disclosure
3. **Reply-To routing** — replies go to your human's real inbox, not the agent inbox
4. **CC on everything** — your human sees every email sent on their behalf
5. **Inbox monitoring** — check for replies, mark processed, alert your human

## Setup

### 1. Create an Agent Inbox

Using AgentMail (recommended):
```bash
mcporter call agentmail.create_inbox displayName="Your Assistant Name"
```

### 2. Host Your Signature Logo

Upload a small logo (60x60px recommended) to any image host. Gmail blocks inline base64 images — use a hosted URL.

### 3. Configure Email Template

The signature pattern:
```html
<div>
  <div style="font-weight: bold;">Human's Full Name</div>
  <div>human@email.com</div>
  <img src="https://your-hosted-logo.png" width="60" height="60" />
  <div style="color: #aaa; font-size: 10px;">Sent on behalf of [Name] by their personal assistant</div>
</div>
```

### 4. Set Reply-To Header

Always set `Reply-To` to your human's real email address so replies reach them directly.

### 5. CC Your Human

CC your human on every outbound email. No surprises.

## Best Practices

- **Use full legal name** on formal correspondence
- **Monitor for replies** — set up a heartbeat check on the inbox
- **Mark processed emails** — remove "unread" label after handling
- **Never send without approval** for high-stakes emails (legal, financial, employment)

## Requirements

- AgentMail account (or any SMTP provider)
- Image hosting for email signature logo
- mcporter (for AgentMail integration)

## License

MIT
