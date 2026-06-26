---
name: unformal-notifications
description: Get notified when someone completes an Unformal Pulse — via a scheduled Claude Code routine (hourly), a local desktop listener (real-time macOS notifications), or on-demand API polling. Use when the user wants to know about new responses, check their Unformal inbox, or set up recurring alerts for a Pulse they are running. Pairs with `unformal-api` for creating Pulses.
license: MIT
metadata:
  author: Spark Collective
  version: "1.1.0"
  website: https://unformal.ai
allowed-tools: Bash
---

# Unformal Notifications

Three ways to get notified about new responses on your Unformal Pulse. Pick one — or combine.

## When to use this skill

Trigger on any of these:
- "any new Unformal responses?"
- "check my Unformal"
- "who completed the [pulse name]?"
- "summarize today's responses"
- "set up a routine to check my Pulse"
- "notify me when responses come in"
- "did anyone finish the survey?"

## Prerequisites

- An Unformal API key — get one at [unformal.ai/studio/settings](https://unformal.ai/studio/settings) or via `POST /api/v1/signup`
- A Pulse ID — from `GET /api/v1/pulses` or the Studio URL

---

## Option A — Claude Code desktop routine (recommended)

**Best for**: always-on monitoring that shows up in your Claude Code desktop sidebar alongside your other routines. Runs locally, can use your local secrets files, and you pick the schedule visually in the desktop UI.

Ask Claude:

> **"Create a Claude Code desktop routine called `unformal-new-responses` that checks for new completed responses on my Unformal Pulse `<PULSE_ID>` using API key `<API_KEY>`. It should track the last-seen timestamp in `~/.unformal/last-seen`, only fetch new responses since that marker, and give me a concise digest (sentiment + summary + key quotes) or say 'No new responses' if there are none."**

### What Claude does

Creates a directory at `~/.claude/scheduled-tasks/<routine-name>/` containing a single `SKILL.md` file with:

```markdown
---
name: unformal-new-responses
description: Check for new completed responses on active Unformal Pulses
---

1. Load secrets: `source /path/to/load-secrets.sh` (optional — if keys are
   in a local env file, use it; otherwise embed API key inline)
2. Read marker: `SINCE=$(cat ~/.unformal/last-seen 2>/dev/null || echo 0)`
3. Fetch new responses:
   ```bash
   TMP=$(mktemp)
   curl -fsS "https://unformal.ai/api/v1/pulses/<PULSE_ID>/conversations?completedSince=$SINCE" \
     -H "Authorization: Bearer <API_KEY>" > "$TMP"
   ```
4. Parse & summarize with Python (read from the temp file to keep heredoc stdin clean):
   ```bash
   python3 << PYEOF
   import json
   with open("$TMP") as f:
       d = json.load(f)
   items = d.get("data", [])
   completed = [c for c in items if c.get("status") == "completed"]
   if not completed:
       print("NONE")
   else:
       print("FOUND " + str(len(completed)))
       for c in completed:
           echo = c.get("echo") or {}
           print("---")
           print("id: " + str(c.get("id", "")))
           print("sentiment: " + str(echo.get("sentimentScore", "?")) + "/10")
           print("summary: " + (echo.get("summary") or "(no summary)")[:300])
           for q in (echo.get("keyQuotes") or [])[:3]:
               print("quote: " + str(q)[:200])
   PYEOF
   ```
5. Update marker: `python3 -c "import time; print(int(time.time()*1000))" > ~/.unformal/last-seen`
6. Report briefly if NONE, or present a clean digest if FOUND.
```

### Setting the schedule

After creating the SKILL.md file, the routine appears in the Claude Code desktop sidebar under "Routines". **Set the cron schedule from the desktop UI** — click the routine and pick Daily / Weekdays / Custom / etc. The schedule is stored by the desktop app; the SKILL.md only defines the task.

### Key points

- Runs locally on your machine (unlike remote triggers) — has access to `~/` and local secrets
- Does NOT appear in [claude.ai/code/scheduled](https://claude.ai/code/scheduled) (that's the remote triggers UI — a separate system)
- Minimum cadence is whatever the desktop UI allows (typically 1 minute+)
- You can edit the SKILL.md anytime; changes take effect on next run

---

## Option B — Local desktop listener (real-time macOS notifications)

**Best for**: live in-session awareness while you're actively working. Runs on your machine, shows native OS notifications the second a response comes in.

### One-time install

```bash
mkdir -p ~/bin
curl -fsS https://unformal.ai/unformal-listen.sh > ~/bin/unformal-listen
chmod +x ~/bin/unformal-listen
export UNFORMAL_API_KEY=unf_xxx   # add to ~/.zshrc for persistence
```

### Run

```bash
unformal-listen                    # lists your Pulses
unformal-listen <pulse_id>         # starts listening
```

Leave it running in a spare terminal tab. Every completion:
- Pops a native macOS notification (Linux: `notify-send` fallback)
- Writes the event JSON to `~/.unformal/inbox/<timestamp>.json`
- Auto-reconnects on server-side timeouts

---

## Option C — On-demand check (no setup)

**Best for**: one-off lookups. The user asks "any new responses?" and you query the API right there.

```bash
# Responses completed in the last hour
SINCE=$(python3 -c "import time; print(int(time.time()*1000) - 3600000)")
curl -fsS "https://unformal.ai/api/v1/pulses/<PULSE_ID>/conversations?completedSince=$SINCE" \
  -H "Authorization: Bearer $UNFORMAL_API_KEY" | \
  jq '[.data[] | select(.status=="completed")] | sort_by(.completedAt) | reverse'
```

For "since last check" semantics with a local marker file:

```bash
mkdir -p ~/.unformal
LAST=$(cat ~/.unformal/last-seen 2>/dev/null || echo 0)
curl -fsS "https://unformal.ai/api/v1/pulses/<PULSE_ID>/conversations?completedSince=$LAST" \
  -H "Authorization: Bearer $UNFORMAL_API_KEY"
python3 -c "import time; print(int(time.time()*1000))" > ~/.unformal/last-seen
```

---

## Usage patterns (when the user asks you to check)

### If Option B (listener) is running

Summarize the newest events from the inbox:

```bash
ls -t ~/.unformal/inbox/*.json 2>/dev/null | head -5 | while read f; do
  cat "$f" | jq -r '{
    completedAt: .completedAt,
    summary: (.echo.summary // .summary // "no summary"),
    sentiment: .echo.sentimentScore,
    quotes: (.echo.keyQuotes // [] | .[0:2])
  }'
done
```

### If no listener is running

Fall back to the on-demand API call (Option C above).

### After acting on events, archive

```bash
mkdir -p ~/.unformal/processed
mv ~/.unformal/inbox/*.json ~/.unformal/processed/ 2>/dev/null || true
```

### What Claude can do with new responses

- Flag hot leads (high sentiment + specific keywords) and draft follow-ups
- Detect patterns across multiple completions and propose a Resonance-style summary
- Save interesting quotes to a notes file
- Trigger other skills (draft a Slack message, update a CRM, etc.)

---

## Inbox event shape

Each file in `~/.unformal/inbox/` (and each element of the API `.data[]` array) looks like:

```json
{
  "conversationId": "k17abc...",
  "pulseId": "k97xyz...",
  "echo": {
    "fields": {"budget_range": "$10k-20k", "timeline": "Q3"},
    "summary": "Strong fit. Mid-size agency ready to pilot.",
    "keyQuotes": ["We spend 3 hours weekly on status reports"],
    "sentimentScore": 7
  },
  "completedAt": "2026-04-17T10:32:01Z",
  "metadata": {"duration": 240, "messageCount": 12}
}
```

## Related

- `unformal-api` — create and manage Pulses (use first if no Pulse exists yet)
- Claude Code `schedule` skill — for Option A remote triggers
- [Listener source](https://unformal.ai/unformal-listen.sh)
- [SSE stream docs](https://unformal.ai/agents)
- [Manage scheduled routines](https://claude.ai/code/scheduled)
