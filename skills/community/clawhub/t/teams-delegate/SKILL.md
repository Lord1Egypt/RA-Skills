---
name: teams-delegate
description: Delegate your Microsoft Teams inbox to your AI agent. Use when the user wants to: auto-reply to Teams messages, have the agent monitor and respond to their boss or colleagues, summarize unread Teams conversations, draft context-aware replies, filter what needs human attention vs what the agent can handle, or manage Teams communication hands-free. Triggers on requests like "reply to my boss on Teams", "check my Teams messages", "handle my Teams inbox", "auto-reply on Teams", or "what did I miss on Teams".
---

# Teams Delegate

Let the agent own your Teams inbox. Read messages, draft replies, send them — with awareness of who's messaging you and what actually needs your attention.

## Setup (one time)

1. Register an Azure app at https://portal.azure.com → Azure Active Directory → App Registrations → New
   - Platform: Mobile/Desktop (enables device code flow)
   - In Authentication → scroll to "Advanced settings" → set "Allow public client flows" to Yes (required for device code)
   - NOTE: Use the old Azure portal experience — click "switch to old experience" in the yellow banner if you see it
   - Add API permissions: Chat.Read, Chat.ReadWrite, ChannelMessage.Read.All, ChannelMessage.Send, Presence.Read.All, User.Read
   - Grant admin consent if on a corporate tenant

2. Save the client ID:
   ```
   python3 scripts/auth.py --client-id YOUR_CLIENT_ID
   ```

3. Authenticate:
   ```
   python3 scripts/auth.py
   ```
   Follow the device code prompt. Token saved to ~/.teams-delegate/token.json and auto-refreshes.

## Core Commands

```bash
python3 scripts/teams.py inbox          # List recent chats with previews
python3 scripts/teams.py read <chatId>  # Read full conversation
python3 scripts/teams.py reply <chatId> "message"  # Send reply
python3 scripts/teams.py summary        # Dump all pending chats for agent review
```

## Agent Workflow

### Checking the inbox
1. Run `summary` to get all recent conversations in one pass
2. Classify each message:
   - **Agent handles:** acknowledgements, scheduling confirmations, "got it" responses, simple status updates
   - **Needs human:** decisions, sensitive topics, anything the user explicitly wants to see, urgent/high importance from boss
3. For messages the agent handles: draft reply → run `reply`
4. For messages needing human: summarize and present to user

### Drafting replies
- Match the tone of the conversation (casual 1:1 vs formal channel)
- Keep it brief — Teams is chat, not email
- If replying on behalf of someone, don't pretend to be them; write as their assistant if context requires
- Check `importance` field — urgent messages from managers need immediate escalation to user

### Auto-reply mode
When user says "handle my Teams" or "auto-reply while I'm out":
1. Run `summary` every N minutes (use cron or heartbeat)
2. Apply classification rules above
3. Send approved replies automatically
4. Log everything — what was sent, to whom, when
5. Alert user for anything flagged as needing human attention

## Priority Rules (defaults — user can override)
- Messages marked `urgent` → always escalate to user
- Messages from designated VIPs (boss, key clients) → draft only, wait for approval
- Group chat messages → lower priority, reply only if directly @mentioned
- Channel messages → summarize only unless @mentioned

## Graph API Reference
See references/graph-api.md for full endpoint docs, auth scopes, and rate limit details.

---

## Author

Built by **Nate Teshome** — [@takeovernat](https://github.com/takeovernat)

Website: [stellarsitesai.com](https://stellarsitesai.com)
GitHub: [github.com/takeovernat](https://github.com/takeovernat)

Found a bug or want to contribute? Open an issue or PR on [GitHub](https://github.com/takeovernat/teams-delegate).
