---
name: telegram-group-onboard
description: "Automatically onboard new Telegram groups so the bot responds immediately — with project setup. Use when: (1) a user says they're creating a new Telegram group with the bot, (2) the bot was added to a new group but doesn't respond, (3) someone reports the bot ignores messages in a group. Solves the groupPolicy=allowlist chicken-and-egg problem by watching gateway logs for dropped messages, extracting the chat_id, adding it to config with requireMention=false, creating a project for the group, and hot-reloading. One smooth flow."
---

# Telegram Group Onboard

## The Problem

OpenClaw defaults to `groupPolicy: "allowlist"` for Telegram. New groups are **silently blocked** until their chat_id is added to `channels.telegram.groups` in `openclaw.json`. The bot receives the messages but drops them before the agent sees them.

**Recommended fix:** Set `channels.telegram.groupPolicy: "open"` at the top level. This is safe when `dmPolicy: "pairing"` is active - strangers can't DM the bot without pairing first, and they can only interact in groups they're already a member of. With `groupPolicy: "open"`, new groups work immediately without manual allowlisting.

```json5
{
  "channels": {
    "telegram": {
      "dmPolicy": "pairing",        // strangers must pair first
      "groupPolicy": "open",        // groups work automatically
      // ...
    }
  }
}
```

If you prefer the allowlist approach (stricter), the flow below handles onboarding manually.

**Key discovery:** Dropped messages still appear in gateway logs with full metadata:
```json
{"chatId": -5131368894, "title": "My-New-Group", "reason": "not-allowed"}
```

## Onboarding Flow

### When the user says "I'm creating a new group with the bot":

**Step 1: Start watching logs**

```bash
# Local
tail -f "$(ls -t /tmp/openclaw/openclaw-*.log | head -1)" | grep --line-buffered "not-allowed"

# Remote
ssh <server> "tail -f \$(ls -t /tmp/openclaw/openclaw-*.log | head -1)" | grep --line-buffered "not-allowed"
```

Tell the user: "I'm watching — create the group, add the bot, and send any message."

**Step 2: Extract chat_id from log**

Log lines contain JSON with field `"1"` holding `{chatId, title, reason}`:
```bash
echo '<log_line>' | jq -r '."1".chatId, ."1".title'
```

**Step 3: Add to config**

```bash
scripts/add-telegram-group.sh <chat_id> false open
```

Arguments: `<chat_id> [requireMention=false] [groupPolicy=open]`

- `requireMention: false` — bot responds to ALL messages (no @mention needed)
- `groupPolicy: open` — any group member can trigger the bot

For remote servers:
```bash
scp scripts/add-telegram-group.sh <server>:/tmp/
ssh <server> "bash /tmp/add-telegram-group.sh <chat_id> false open"
```

**Step 4: Wait for hot-reload**

OpenClaw detects config changes automatically — no restart needed. Verify in logs:
```
config hot reload applied (channels.telegram.groups.*)
```

If no hot-reload within 10 seconds: `openclaw gateway restart` (or via SSH).

**Step 5: Create project for the group**

After the group is allowlisted, set up a project (per the `telegram-projects` skill):

1. Create `projects/<chat_id>/project.md`:
```markdown
# Project: <group_title>

- **Chat ID:** <chat_id>
- **Created:** <date>
- **Status:** active
- **Description:** <from group title or user input>
```

2. Create `projects/<chat_id>/knowledge.md`:
```markdown
# Project Knowledge

_No knowledge entries yet. Add permanent knowledge by saying "permanentes Knowledge: [content]" or use `/knowledge add [content]`._
```

3. Create `projects/<chat_id>/glossary.md` (empty)

4. Add entry to `PROJECTS.md` table

5. For remote servers, create these files via SSH or scp.

**Step 6: Confirm to user**

Send to the NEW group (not the main chat):
```
👋 Gruppe ist eingerichtet! Ich antworte hier auf alle Nachrichten.

📁 Projekt "[group_title]" wurde angelegt.

Diese Gruppe hat jetzt ein eigenes Projekt mit permanentem Wissen — wie ein ChatGPT-Projekt, nur in Telegram. Alles was ihr als Knowledge speichert, lade ich bei jeder Nachricht automatisch mit.

Type /helpme for all available commands. 🔥
```

Also tell the user in the main chat: "Gruppe [title] ist live — Projekt angelegt, bot antwortet ohne @mention. Probier's aus!"

## Config Structure

```json5
{
  "<chat_id>": {
    "requireMention": false,  // respond to everything
    "groupPolicy": "open"     // any member can trigger
  }
}
```

## Quick Reference

| Scenario | Command |
|----------|---------|
| Add group (full access) | `scripts/add-telegram-group.sh -5131368894 false open` |
| Add group (mention only) | `scripts/add-telegram-group.sh -5131368894 true open` |
| Check if group exists | `jq '.channels.telegram.groups["<ID>"]' ~/.openclaw/openclaw.json` |
| Watch for new groups | `tail -f <logfile> \| grep "not-allowed"` |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No log entries for new group | Privacy mode blocks messages | Make bot group admin or `/setprivacy` disable via @BotFather |
| Config updated but still no response | Hot-reload failed | `openclaw gateway restart` |
| Bot only responds to @mentions | `requireMention: true` | Re-run script with `false` |
