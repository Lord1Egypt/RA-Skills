---
name: session-storage-management
description: Analyze and clean up OpenClaw session storage files. Use when the user wants to manage session files, clean up old sessions, delete cron/heartbeat, or organize session storage. Triggers on phrases like "clean up sessions", "delete old sessions", "manage session storage", "remove cron sessions", "session cleanup".
---

# Session Storage Management

## Overview

This skill helps analyze and clean up OpenClaw session files stored in the agents sessions directory. It categorizes sessions by type (cron, chat, deleted, reset, heartbeat), presents them to the user for review, and handles safe deletion while protecting the current active session.

## Workflow

### Step 1: Analyze Session Files

Scan the sessions directory and categorize all session files:

1. **Active `.jsonl` files** - Current session files
   - Cron sessions (isolated cron job runs)
   - Heartbeat sessions
   - Chat sessions (direct conversations)
   - Supergroup/other test sessions

2. **`.deleted.<timestamp>` files** - Previously deleted sessions

3. **`.reset.<timestamp>` files** - Sessions from `/new` or `/reset` commands

### Step 2: Identify Current Session

Always identify and exclude the current session from deletion candidates:

```bash
# Get current session ID from session context
# It will be in the system prompt or can be extracted from the current session file
```

The current session should NEVER be deleted without explicit user confirmation in a separate step.

### Step 3: Present Categories to User

Show summary statistics:

```
📊 Session Analysis Summary:
├── Active .jsonl files: N total
│   ├── Cron sessions: N
│   ├── Heartbeat sessions: N
│   ├── Chat sessions: N
│   └── Other sessions: N
├── .deleted files: N
└── .reset files: N

✅ Current session (protected): <session-id>
```

Then ask the user:
> "Would you like me to:
> 1. Show the full detailed list of all sessions with descriptions
> 2. Delete specific categories (e.g., 'delete all cron and .deleted files')
> 3. Delete everything except the current session"

### Step 4: Handle Current Session Warning

If the current session appears in any deletion category (it shouldn't, but check anyway), display a prominent warning:

```
⚠️  WARNING: Your current session was found in the deletion list!
   Session: <session-id>
   
This is the session you're currently using. Deleting it will not affect
your current conversation, but the session file will be removed.

Do you want to delete your current session file as well? (yes/no)
```

### Step 5: Execute Deletion

After user confirmation:

1. Delete confirmed files
2. Report count and types of deleted files
3. Show remaining files
4. Estimate disk space freed

## Categorization Logic

Analyze session content to determine type:

```bash
# Example analysis
content=$(head -10 "$file" | jq -r '.message.content[]? | select(.type=="text") | .text' 2>/dev/null | head -5)

if echo "$content" | grep -qiE "cron.*[a-f0-9-]{36}"; then
    type="cron"
elif echo "$content" | grep -qiE "heartbeat|HEARTBEAT"; then
    type="heartbeat"
elif echo "$content" | grep -qiE "new session|Session Startup"; then
    type="chat"
else
    type="other"
fi
```

## Safety Rules

1. **Never delete without explicit confirmation** - Always show what will be deleted and wait for "yes"
2. **Protect current session** - Exclude it from bulk deletion, ask separately if user wants it deleted
3. **Preserve last chat session** - If multiple chat sessions exist, keep at least the most recent one unless user explicitly says otherwise
4. **Report everything** - Show full list of files being deleted with their sizes

## Example Session Analysis Output

```
╔══════════════════════════════════════════════════════════════╗
║ SESSION ANALYSIS                                             ║
╚══════════════════════════════════════════════════════════════╝

📁 Location: ~/.openclaw/agents/main/sessions/

Category Breakdown:
  🕐 Cron sessions: 13 (isolated job runs)
  💓 Heartbeat sessions: 1  
  💬 Chat sessions: 2
  🗑️  .deleted files: 14
  🔄 .reset files: 23

Total files: 56
Estimated size: 12 MB

✅ Protected: <current-session-id> (current conversation)
```
