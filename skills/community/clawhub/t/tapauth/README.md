# TapAuth Agent Skill

> Delegated access broker for AI agents. One API call to request OAuth access or a user-entered secret.

This is the official [Agent Skill](https://agentskills.io) for [TapAuth](https://tapauth.ai) — the trust layer between humans and AI agents.

## Install

Works with any agent that supports the [Agent Skills standard](https://agentskills.io):

```bash
npx skills add tapauth/skill
```

Compatible with: **Claude Code** · **Cursor** · **OpenClaw** · **OpenAI Codex** · **GitHub Copilot** · **VS Code** · and more.

## What It Does

Gives your AI agent the ability to get OAuth tokens or user-entered passwords/API keys from users. Instead of hardcoding credentials, TapAuth lets users approve access in their browser with clear request context and expiry controls.

```
Agent creates grant → User approves in browser → Agent gets scoped token or secret
```

No TapAuth API key needed. No signup needed. The user's approval is the gate.

## Supported Providers

| Provider | Reference | Scopes |
|----------|-----------|--------|
| GitHub | [references/github.md](references/github.md) | `repo`, `read:user`, `workflow`, etc. |
| Google (multi-service) | [references/google.md](references/google.md) | Drive, Calendar, Sheets, Docs, Contacts |
| Gmail | [references/gmail.md](references/gmail.md) | Read, send, manage emails |
| Linear | [references/linear.md](references/linear.md) | Issues, projects, teams |
| Vercel | [references/vercel.md](references/vercel.md) | Deployments, projects, env vars, domains |
| Notion | [references/notion.md](references/notion.md) | Pages, databases, search |
| Slack | [references/slack.md](references/slack.md) | Channels, messages, users, files |
| Asana | [references/asana.md](references/asana.md) | Tasks, projects, workspaces |
| Discord | [references/discord.md](references/discord.md) | Guilds, channels, messages, users |
| Sentry | [references/sentry.md](references/sentry.md) | Error tracking, projects, organizations |
| Apify | [references/apify.md](references/apify.md) | Actors, web scraping, datasets, automation |
| Manual Secret | Built in | User-entered passwords or fixed API keys |

## Quick Example

### CLI (recommended)

```bash
# 1. Create the grant and show the approval URL.
scripts/tapauth.sh github repo

# 2. Start the real request immediately; --token waits until approval completes.
curl -H "Authorization: Bearer $(scripts/tapauth.sh --token github repo)" \
  https://api.github.com/user/repos
```

### API (v1)

```bash
# 1. Create a grant
curl -X POST https://tapauth.ai/api/v1/grants \
  -H "Content-Type: application/json" \
  -d '{"provider": "github", "scopes": ["repo"]}'

# 2. User clicks the approval_url
# 3. Retrieve the token
curl https://tapauth.ai/api/v1/grants/{grant_id} \
  -H "Authorization: Bearer gs_..."
```

### Manual Secret

```bash
# Ask the user for a fixed API key. The approval page encrypts it in the browser.
scripts/tapauth.sh secret "Stripe Secret Key" "^sk_" "Use a Stripe secret key that starts with sk_"

# Retrieve it after approval
scripts/tapauth.sh --token secret "Stripe Secret Key" "^sk_" "Use a Stripe secret key that starts with sk_"
```

Use a short, unique, stable, human-readable description because it is part of the local lookup key. Put formatting instructions in `validation_hint`, not in the description. Validation regexes are checked in the browser as a UX guard. The optional validation hint is shown only when that check fails. Agents should validate the retrieved secret too. Expiry stops TapAuth from returning the secret; it does not rotate or revoke the underlying key.

## Links

- [tapauth.ai](https://tapauth.ai)
- [Documentation](https://tapauth.ai/docs)
- [Agent Skills Spec](https://agentskills.io)

## License

MIT
