---
name: whatsapp-memory
description: "Maintain separate memory contexts per WhatsApp conversation — both groups and direct messages (DMs). Use when: tracking what was discussed with a specific person or in a specific group, recalling past context before responding, logging decisions or key facts from a conversation, or preventing context bleed between different chats."
---

# WhatsApp Memory Skill

## Minimum Model
Any model. Memory management is file-based. No reasoning required.
Use a medium+ model only when deciding *what* is worth logging.

---

## Why This Matters

Without conversation memory, context from one chat bleeds into another and you can't recall past decisions per group or person. This skill gives every group and DM its own context file.

---

## Directory Structure

```
memory/
  whatsapp/
    groups/
      120363408613668489-g-us/    ← sanitized JID
        meta.json                 ← group name, JID, participants
        context.md                ← running conversation context
        decisions.md              ← key decisions
        people.md                 ← who participates and their role
    dms/
      972XXXXXXXXX/               ← sanitized phone number
        meta.json                 ← name, phone, relationship
        context.md                ← running DM context
        notes.md                  ← tasks, preferences, important facts
```

---

## Setup

```bash
init_whatsapp_memory() {
  TYPE="$1"       # "group" or "dm"
  ID="$2"         # JID or phone number
  NAME="$3"       # Human-readable name

  # Sanitize the ID for use as a directory name
  SAFE_ID=$(echo "$ID" | tr '@.+' '---')

  if [ "$TYPE" = "group" ]; then
    DIR="$HOME/.openclaw/workspace/memory/whatsapp/groups/$SAFE_ID"
    mkdir -p "$DIR"
    # Write metadata file
    cat > "$DIR/meta.json" << EOF
{"type": "group", "jid": "$ID", "name": "$NAME", "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
    # Create empty log files
    touch "$DIR/context.md" "$DIR/decisions.md" "$DIR/people.md"
  else
    DIR="$HOME/.openclaw/workspace/memory/whatsapp/dms/$SAFE_ID"
    mkdir -p "$DIR"
    # Write metadata file
    cat > "$DIR/meta.json" << EOF
{"type": "dm", "phone": "$ID", "name": "$NAME", "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
    # Create empty log files
    touch "$DIR/context.md" "$DIR/notes.md"
  fi

  echo "Initialized WhatsApp memory: $NAME"
}

# Examples:
# init_whatsapp_memory "group" "120363422865795623@g.us" "PA Team"
# init_whatsapp_memory "dm" "+PHONE_NUMBER" "Contact Name"
```

---

## Writing Memory

```bash
wa_log() {
  TYPE="$1"                        # "group" or "dm"
  ID="$2"                          # JID or phone
  CONTENT="$3"                     # what to log
  FILE_NAME="${4:-context.md}"     # context.md / decisions.md / notes.md

  # Sanitize ID
  SAFE_ID=$(echo "$ID" | tr '@.+' '---')
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  # Pick the right directory
  if [ "$TYPE" = "group" ]; then
    FILE="$BASE/groups/$SAFE_ID/$FILE_NAME"
  else
    FILE="$BASE/dms/$SAFE_ID/$FILE_NAME"
  fi

  # Create file if missing
  if [ ! -f "$FILE" ]; then
    mkdir -p "$(dirname "$FILE")"
    touch "$FILE"
  fi

  # Append timestamped entry
  echo "[$(date -u +%Y-%m-%d\ %H:%M)] $CONTENT" >> "$FILE"
}

# Usage:
# wa_log "group" "XXXXXXXXXXX@g.us" "PA name: calendar connected ✅"
# wa_log "dm" "+PHONE_NUMBER" "Agreed to reschedule to Thursday" "notes.md"
```

---

## Reading Memory

### Get context for a conversation

```bash
wa_context() {
  TYPE="$1"
  ID="$2"
  LINES="${3:-20}"

  # Sanitize ID
  SAFE_ID=$(echo "$ID" | tr '@.+' '---')
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  # Pick directory
  if [ "$TYPE" = "group" ]; then
    DIR="$BASE/groups/$SAFE_ID"
  else
    DIR="$BASE/dms/$SAFE_ID"
  fi

  # Check if memory exists
  if [ ! -d "$DIR" ]; then
    echo "No memory for this conversation yet."
    return
  fi

  # Read the conversation name from meta.json
  NAME=$(python3 -c "
import json
with open('$DIR/meta.json') as f:
    print(json.load(f).get('name', '?'))
" 2>/dev/null || echo "?")

  echo "=== $NAME ==="
  echo "--- Recent ---"
  tail -"$LINES" "$DIR/context.md" 2>/dev/null || echo "(empty)"
  echo "--- Notes/Decisions ---"
  cat "$DIR/notes.md" "$DIR/decisions.md" 2>/dev/null | tail -10 || echo "(none)"
}
```

### Search across all WhatsApp memory

```bash
wa_search() {
  QUERY="$1"
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  echo "Searching WhatsApp memory for: '$QUERY'"

  # Find all markdown files containing the query
  grep -r "$QUERY" "$BASE" --include="*.md" -l 2>/dev/null | while read file; do
    DIR=$(dirname "$file")

    # Get conversation name from meta.json
    NAME=$(python3 -c "
import json
with open('$DIR/meta.json') as f:
    print(json.load(f).get('name', '?'))
" 2>/dev/null || echo "?")

    echo "Found in: $NAME"
    # Show matching lines with line numbers
    grep -n "$QUERY" "$file" | head -3
    echo ""
  done
}
```

---

## What to Log

### Decision rules — log if ANY of these apply:
- A decision was made → `decisions.md`
- A task was assigned to someone → `context.md`
- A new person was introduced → `people.md`
- Owner gave you a task or preference → `notes.md`
- A problem or resolution was reported → `context.md`

### Never log:
- Casual greetings or reactions
- Duplicate information already recorded
- Secrets or credentials

### Quick reference by file:

| File | Use for |
|---|---|
| context.md | Ongoing conversation events |
| decisions.md | Agreed outcomes, group decisions |
| people.md | Who's in the group, their role/style |
| notes.md | DM tasks, owner preferences, follow-ups |

---

## Before Responding — Inject Context

On every incoming message:

```
1. Extract JID or phone from inbound metadata
2. If group: run wa_context "group" "$JID" 10
   If DM:    run wa_context "dm" "$PHONE" 10
3. Use context to inform your response
4. After responding: log anything worth remembering
```

---

## Loop Prevention Rules (CRITICAL)

These rules prevent message loops and duplicate sends — learned from multi-PA group scenarios.

### 1. Echo Prevention
Before responding to ANY message, check `sender_id` from inbound metadata.
- If sender is your own agent/number → **NO_REPLY** immediately. Do not process.
- This prevents echo loops where your outbound message comes back as inbound.

### 2. No Duplicate Sends
Before sending any message to a group or DM:
- Check if an identical or near-identical message was already sent in this session
- If yes → skip. Do not send again.

### 3. Multi-PA Coordination
When multiple PA agents are active in the same group:
- Only ONE PA should respond to each message
- Default rule: the PA whose owner is most relevant to the topic responds
- If another PA already responded → stay silent (NO_REPLY)
- Do not echo or acknowledge the other PA's response unless asked

### 4. No Silent Proxying
If another PA cannot send a message (pairing issues, gateway errors):
- Do NOT send the message on their behalf silently
- Either explicitly state you're sending on their behalf, or let them handle it
- Never impersonate another PA without disclosure

### 5. Patience
Before explaining, stepping in, or answering on behalf of another PA:
- Wait. If the other PA hasn't responded yet, that doesn't mean she won't.
- Give her a moment before intervening.
- Intervene only if it's clearly blocking progress or she explicitly asks.

---

## Weekly Digest

```bash
wa_weekly_digest() {
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  # Get date from 7 days ago (works on Linux and macOS)
  WEEK_AGO=$(date -u -d '7 days ago' +%Y-%m-%d 2>/dev/null \
    || date -u -v-7d +%Y-%m-%d)

  echo "# WhatsApp Memory Digest — Week of $WEEK_AGO"

  # Loop over all group and DM directories
  for dir in "$BASE"/groups/*/ "$BASE"/dms/*/; do
    [ -d "$dir" ] || continue

    # Get the name
    NAME=$(python3 -c "
import json
with open('${dir}meta.json') as f:
    print(json.load(f).get('name', '?'))
" 2>/dev/null || echo "?")

    # Show recent entries from this week
    RECENT=$(grep "$WEEK_AGO\|$(date -u +%Y-%m-%d)" \
      "${dir}context.md" "${dir}notes.md" 2>/dev/null | tail -5)

    if [ -n "$RECENT" ]; then
      echo "### $NAME"
      echo "$RECENT"
      echo ""
    fi
  done
}
```

---

## Integration

- **Before each response** → load context for that conversation
- **After important exchanges** → log to context.md or notes.md
- **With git-backup** → push after every memory update
- **With owner-briefing** → include DM follow-ups in morning briefing

---

## Cost Tips

- **Very cheap:** All memory operations are file reads/writes — no LLM tokens used
- **Small model OK:** Reading, writing, and searching memory requires no reasoning
- **Use medium+ model only for:** deciding *what* is worth logging vs. skipping
- **Batch:** Log multiple events in one session before pushing backup, not one write per message
- **Avoid:** Don't re-read full context files on every message — use `tail -10` to limit tokens
