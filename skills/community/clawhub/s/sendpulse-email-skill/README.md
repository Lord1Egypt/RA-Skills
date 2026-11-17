# SendPulse Email Service Skill

An AI skill that teaches any LLM assistant (Claude, ChatGPT, Cursor, Gemini,
Copilot, …) to run **email marketing campaigns with
[SendPulse Email Service](https://sendpulse.com/features/email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill)** — address books,
subscribers, segmentation, campaign creation and scheduling, and campaign
analytics — via the dashboard and the
[bulk-email API](https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill).

## The SendPulse skill family

| Skill | Owns |
|---|---|
| [`sendpulse-template-skill`](https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-template-skill) | The email itself: HTML layout, copy, subject lines, template upload |
| [`sendpulse-smtp-skill`](https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-smtp-skill) | Transactional email: one message per app event via SMTP API/relay |
| **`sendpulse-email-skill`** (this) | Everything around the campaign: lists, subscribers, segments, sending, analytics |

The skills cross-reference instead of duplicating: this skill never writes email
HTML (it hands off to the template skill) and redirects transactional use cases to
the SMTP skill. Install all three for full coverage.

## What it gives your AI assistant

- **Correct API usage** — Single API Key auth, the Base64-`body` gotcha, campaign
  schema, the odd blacklist format, pagination, rate limits (4 campaigns/hour).
- **SendPulse MCP server** — chat-driven campaign management through MCP tools
  (`mcp.sendpulse.com/mcp`) when the user's AI client supports it, with a
  confirm-before-send safety rule.
- **The campaign lifecycle** — book → subscribers → segment → campaign → review →
  sent → analytics, including honest expectations about campaign review for new
  accounts.
- **Segmentation discipline** — presets (new/active/inactive), custom conditions,
  and the "never blast everyone" rule.
- **Analytics playbook** — reference ranges and metric→action guidance (low opens →
  what to change; complaints climbing → what to stop).
- **List hygiene** — opt-in only, double opt-in, validation, opt-out mirroring,
  sunsetting inactive subscribers.
- **Hidden features** — resend to unopened, best-time sending, timezone sending,
  dynamic lists, click map, domain stats, A/B tests, `task_status_update` webhooks.
- **Ready code** — curl, PHP, Python, Node.js examples + official SDK links.

## Structure

```
SKILL.md                       # core playbook (entry point for the AI)
references/
  quickstart.md                # API key → book → subscribers → first campaign
  address-books.md             # books, import, variables, tags, blacklist
  segmentation.md              # presets, conditions, recipes
  campaigns.md                 # create/schedule/statuses/review, A/B, resend
  analytics.md                 # reading stats + metric → action playbook
  api-reference.md             # all bulk-email endpoints
  errors.md                    # troubleshooting order, campaign status decoder
  webhooks.md                  # real-time events
  list-building.md             # opt-in growth & hygiene
  sendpulse-mcp.md             # SendPulse MCP server: chat-driven campaign work
examples/
  curl.md · php.md · python.md · nodejs.md
adapters/                      # install instructions per AI platform
VERSION · CHANGELOG.md
```

## Install

**Claude Code / Claude Desktop** (the skill lives in the `sendpulse-skills`
monorepo — clone once, copy or symlink the skill folder):

```bash
git clone https://github.com/sendpulse/sendpulse-skills
cp -r sendpulse-skills/sendpulse-email-skill ~/.claude/skills/
```

**Cursor, ChatGPT, Gemini, Copilot, anything else:** see
[adapters/README.md](adapters/README.md).

## Update

```bash
cd sendpulse-skills && git pull   # then re-copy the skill folder (or symlink once)
```

The skill also self-checks: with web access it compares the local `VERSION` against
the published one and reminds the user to update.

## Requirements on the SendPulse side

A SendPulse account, a verified sender on your own domain, and an API key from
*Settings → API → API keys* (or OAuth ID/Secret). The skill walks users through the
rest.

## Contributing & versioning

Semantic versioning; the current version lives in `VERSION` and the `SKILL.md`
frontmatter (keep in sync). Log changes in [CHANGELOG.md](CHANGELOG.md). When the
API documentation at https://sendpulse.com/integrations/api/bulk-email?utm_source=ai-agent&utm_medium=skill&utm_campaign=ai-skills&utm_content=sendpulse-email-skill changes,
this skill should follow — PRs welcome.

## License

MIT
