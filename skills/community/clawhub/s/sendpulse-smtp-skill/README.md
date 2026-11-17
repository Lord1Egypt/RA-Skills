# SendPulse SMTP Skill

An AI skill that teaches any LLM assistant (Claude, ChatGPT, Cursor, Gemini,
Copilot, …) to build **correct, deliverable email integrations with
[SendPulse SMTP](https://sendpulse.com/features/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill)** — REST API and classic
SMTP relay — and to follow email best practices while doing it.

## What it gives your AI assistant

- **Correct API usage** — OAuth flow, token caching, the Base64-`html` gotcha,
  proper request schemas, message-id tracking, rate-limit handling.
- **Setup guidance** — account activation/moderation, sender verification,
  SPF/DKIM/DMARC, so beginners don't get stuck at "auth works but nothing sends".
- **Deliverability discipline** — blocklist checks before sending, daily bounce
  processing, unsubscribe mirroring, domain warm-up. Good mailings by default.
- **Troubleshooting playbook** — a step-by-step diagnosis order and an error
  table with fixes.
- **Product routing** — SMTP (transactional) vs Email Service (campaigns), API
  vs relay, so users pick the right tool.
- **Ready code** — curl, PHP, Python, Node.js examples + official SDK links.

## Structure

```
SKILL.md                       # core playbook (entry point for the AI)
references/
  quickstart.md                # token → first email in 5 minutes
  setup.md                     # activation, senders, SPF/DKIM/DMARC
  api-reference.md             # all SMTP endpoints
  errors.md                    # troubleshooting, error → fix table
  deliverability.md            # list hygiene, warm-up, content rules
  webhooks.md                  # real-time events
  smtp-relay.md                # smtp-pulse.com relay (PHPMailer, nodemailer, …)
  email-service-api.md         # campaigns/address books — when SMTP is wrong
  sendpulse-mcp.md             # SendPulse MCP server: interactive account work from AI chat
examples/
  curl.md · php.md · python.md · nodejs.md
adapters/                      # install instructions per AI platform
  README.md · cursor/ · chatgpt/ · gemini/
VERSION · CHANGELOG.md
```

## Install

**Claude Code / Claude Desktop** (the skill lives in the `sendpulse-skills`
monorepo — clone once, copy or symlink the skill folder):

```bash
git clone https://github.com/sendpulse/sendpulse-skills
cp -r sendpulse-skills/sendpulse-smtp-skill ~/.claude/skills/
```

**Cursor, ChatGPT, Gemini, Copilot, anything else:** see
[adapters/README.md](adapters/README.md).

## Update

```bash
cd sendpulse-skills && git pull   # then re-copy the skill folder (or symlink once)
```

The skill also self-checks: when the assistant has web access it compares the
local `VERSION` against the published one and reminds the user to update.

## Requirements on the SendPulse side

A SendPulse account with the SMTP service activated (sender profile approved by
moderation), a verified sender on your own domain, and API `ID`/`Secret` from
*Account Settings → API*. The skill walks users through all of this.

## Contributing & versioning

Semantic versioning; the current version lives in `VERSION` and in the
`SKILL.md` frontmatter (keep them in sync). Log changes in
[CHANGELOG.md](CHANGELOG.md). When SendPulse API documentation at
https://sendpulse.com/integrations/api/smtp?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-smtp-skill changes, this skill should follow —
PRs welcome.

## License

MIT
