---
name: stm-assistant
version: 1.0.0
description: "Professional email outreach on behalf of your human. Branded signatures, Reply-To routing, CC tracking."
metadata: {"openclaw":{"emoji":"📧","requires":{"bins":["mcporter"]}}}
user-invocable: true
---

# STM Assistant — Send on Behalf

Send professional emails from a dedicated agent inbox on behalf of your human.

## Setup Requirements

1. **Agent inbox** — via AgentMail (`mcporter call agentmail.create_inbox displayName="Your Assistant"`) or any SMTP provider
2. **Hosted signature logo** — small image (60x60px), hosted URL (Gmail blocks inline base64)
3. **mcporter** with agentmail configured

## Sending Protocol

### Every outbound email MUST:

1. **CC your human** — no exceptions. They see every email you send.
2. **Set Reply-To** to your human's real email address — replies go to them, not the agent inbox.
3. **Use full legal name** on formal correspondence.
4. **Include the branded signature:**

```html
<div>
  <div style="font-weight: bold;">Human's Full Name</div>
  <div>human@email.com</div>
  <img src="https://your-hosted-logo.png" width="60" height="60" />
  <div style="color: #aaa; font-size: 10px;">Sent on behalf of [Name] by their personal assistant</div>
</div>
```

### Approval Rules

- **Routine emails** (scheduling, follow-ups, informational) — send directly, notify human after
- **High-stakes emails** (legal, financial, employment, first contact with important people) — draft and get explicit approval before sending
- When in doubt → ask first

### Sending via AgentMail

```bash
mcporter call agentmail.send_message \
  inboxId=your-agent@agentmail.to \
  to='[{"email":"recipient@example.com","name":"Recipient Name"}]' \
  subject="Subject Line" \
  html="<p>Email body with signature</p>" \
  cc='[{"email":"human@email.com"}]'
```

**Important:** Use `text` (plain text) or `html` (formatted) parameters. Never `body` or `htmlBody` — those don't exist and produce empty emails.

## Inbox Monitoring

Check for replies on a regular cycle (heartbeat or cron):

```bash
mcporter call agentmail.list_threads inboxId=your-agent@agentmail.to limit=5 labels='["unread"]'
```

After processing a reply:
```bash
mcporter call agentmail.update_message \
  inboxId=your-agent@agentmail.to \
  messageId=MSG_ID \
  removeLabels='["unread"]' \
  addLabels='["processed"]'
```

**Always mark processed emails.** Unread inbox = broken assistant.


