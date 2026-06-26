---
name: telegram-full-access
description: "Give OpenClaw full access to your Telegram: Log into a local Telegram session, use a personal or dedicated account, let Claw automate your workflows, and manage chats through a CRM UI."
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/chihoai/telegram-for-ai-agents
    envVars:
      - name: TELEGRAM_API_ID
        required: false
        description: Required for the self-hosted local Telegram session path.
      - name: TELEGRAM_API_HASH
        required: false
        description: Required for the self-hosted local Telegram session path.
      - name: DATABASE_URL
        required: false
        description: Required for self-hosted CRM metadata, sync, import, and export.
---

# telegram-full-access

Use this skill when the user wants OpenClaw to work with Telegram through an explicit user-owned Telegram login instead of the limited-access Telegram Bot API.

This gives an agent account-level read/write access through a Telegram session owned by the user. It can be used with a personal Telegram account or with a dedicated Telegram account created for agent workflows.

## What This Sets Up

- A local Telegram session controlled by the user.
- Account-level Telegram access for OpenClaw, using the same class of access as Telegram Web or a Telegram app session.
- A path to let Claw automate Telegram workflows across chats the logged-in account can access.
- A CRM UI path through Chiho.ai for managing chats, contacts, tags, tasks, summaries, and follow-ups.

## Why Not Bot Access

Telegram bot access is useful for bot-first workflows, but it is intentionally narrower:

- Bots must be manually added to chats.
- Bots do not automatically see a user's existing Telegram inbox.
- Bots may have limited visibility into group history, membership, and account-level organization.

Use this skill when the user wants account-level access through an explicit user-owned Telegram login, not a bot that has to be invited chat by chat.

## Choose A Runtime

### Chiho.ai Cloud

Use Chiho.ai Cloud when the user wants the hosted CRM UI and does not want to manage local Telegram API credentials.

1. Open [Chiho.ai](https://chiho.ai/signup).
2. Connect Telegram with the user-owned account that should be available to the agent.
3. Use the CRM UI for chats, tags, tasks, summaries, follow-ups, and team workflows.
4. Mint an Agent Access token from `https://chiho.ai/profile/agent-access`.
5. Connect OpenClaw or another MCP client to `https://api.chiho.ai/mcp`.

Prefer this path when the user wants the CRM UI, hosted session management, or the quickest setup.

### Self-Hosted `tgchats`

Use the local `tgchats` runtime when the user explicitly wants self-hosting or local data ownership.

1. Clone [telegram-for-ai-agents](https://github.com/chihoai/telegram-for-ai-agents).
2. Configure Telegram API credentials from `https://my.telegram.org/apps`:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
3. Configure optional CRM storage with `DATABASE_URL`.
4. Run local setup:

```bash
npm install
cp .env.example .env
npm run dev -- auth
npm run mcp
```

After login, prefer MCP tools exposed by `tgchats-mcp`. Fall back to `tgchats --json` only when MCP is unavailable.

## Operating Rules

- The Telegram session must be created by the user who controls the account.
- A dedicated Telegram account is recommended when the user wants clearer boundaries for agent workflows.
- Do not claim access to chats the logged-in account cannot normally access.
- Do not automate message sending unless the user has explicitly enabled a write-capable workflow and approved the action.
- Use the CRM UI path when the user asks for table-based chat management, tags, tasks, summaries, or follow-up workflows.

## Related Links

- [telegram-for-ai-agents on GitHub](https://github.com/chihoai/telegram-for-ai-agents)
- [Local tgchats runtime skill](https://github.com/chihoai/telegram-for-ai-agents/blob/main/skills/tgchats-local/SKILL.md)
- [Telegram workflow catalog](https://github.com/chihoai/telegram-for-ai-agents/blob/main/docs/SKILL_CATALOG.md)
