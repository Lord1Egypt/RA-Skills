---
name: remind-me
description: "Create, list, and cancel reminders and cron jobs scoped to the channel they were requested from. Use when: user says 'remind me', 'set an alarm', 'schedule a cron', 'alert me when', 'every day at X do Y', 'cancel my reminder', 'list my reminders'. Auto-detects source channel, chat ID, and user timezone. Delivers back to originating chat. Asks for clarification if schedule or intent is ambiguous before creating anything."
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":["uv","openclaw"]}}}
---

# Skill: Remind Me

## When to use
- User says "remind me to...", "set a reminder", "set an alarm"
- User says "every Monday at 9 AM...", "every 30 minutes check..."
- User says "in 20 minutes tell me...", "at 3 PM send me..."
- User wants to schedule a recurring cron job via chat
- User says "cancel my reminder", "delete that cron", "stop the alert"
- User says "list my reminders", "what reminders do I have?"
- User wants to know what cron jobs are active in this chat

## When NOT to use
- User wants to check a stock price right now (not scheduled) → use `stock-price-checker-pro`
- User wants to run a one-time task immediately (no scheduling involved)

---

## ⚠️ CRITICAL: Always resolve these FOUR things before creating a reminder

Before calling the script, you MUST have all four resolved:

| Field | Question to answer | Example |
|---|---|---|
| **WHAT** | What should happen / be said? | "Check NVDA stock price" |
| **WHEN / HOW OFTEN** | One-time or recurring? At what time/interval? | "Every Monday at 9 AM" |
| **WHERE** | Which channel + chat ID to deliver to? | Auto-detected from session |
| **TIMEZONE** | What timezone should times be interpreted in? | Auto-detected from USER.md |

### Missing field rules

- **WHAT is missing** → Ask: "What would you like me to remind you about?"
- **WHEN is missing AND cannot be reasonably assumed** → Ask: "How often, or at what time?"
- **WHEN is missing BUT can be reasonably assumed as once** → Assume one-shot, but confirm: "Just once, right?"
- **WHERE is always auto-detected** → Never ask the user for this. Read it from session context (see below).
- **TIMEZONE is always auto-detected** → Never ask unless unresolvable (see Step 2 below).

### Do NOT create the job until all four are confirmed.

---

## Step 1 — Auto-detect channel, chat ID, and timezone from context

### Channel and chat ID
The source channel and chat ID are available in your session context. Extract them before doing anything else.

- **channel**: the platform the message arrived on (e.g. `telegram`, `discord`)
- **chatId / to**: the specific chat or user ID within that platform (e.g. `<chatId>`)

These two values are passed as `--channel` and `--to` to the script.
**Never ask the user for these. Never hardcode them. Always read from session context.**

### Timezone — 3-tier resolution (in priority order)

Resolve the user's timezone using this exact priority chain:

| Priority | Source | How to read it |
|---|---|---|
| 1 | **Message itself** | User says "at 9 AM London time" or "remind me at 3 PM EST" → extract from their words |
| 2 | **`USER.md`** | Read the `Timezone:` field from `/root/.openclaw/workspace/USER.md` |
| 3 | **Ask the user** | Only if tiers 1 and 2 both fail — ask once, then offer to save it |

**Rules:**
- If tier 1 applies → use it directly, no need to check USER.md
- If tier 2 applies → use it silently, do not mention it to the user
- If tier 3 triggers → ask: _"What timezone are you in? (e.g. London, New York, Lagos)"_ — then offer: _"Want me to remember your timezone for future reminders?"_ If they say yes, update `USER.md`
- The resolved timezone is passed as `tz:<IANA>` to the script
- If no timezone can be resolved at all, pass `tz:UTC` and mention it in the confirmation summary

---

## Step 2 — Parse the user's intent

From the user's natural language request, extract:

### Schedule type
Map what the user said to one of three prefixed schedule strings.

> ⚠️ When the user states a clock time (e.g. "9 AM", "3 PM", "noon"), always interpret it in their resolved timezone (from Step 1), not UTC. The `--tz` flag passed to the script ensures cron expressions fire at the correct local time.

| What user said | Schedule string to pass |
|---|---|
| "every 30 minutes" | `every:30m` |
| "every hour" | `every:1h` |
| "every day at 9 AM" | `cron:0 9 * * *` |
| "every Monday at 9 AM" | `cron:0 9 * * 1` |
| "weekdays at 8 AM" | `cron:0 8 * * 1-5` |
| "every Friday at 5 PM" | `cron:0 17 * * 5` |
| "in 20 minutes" | `at:20m` |
| "in 2 hours" | `at:2h` |
| "at 3 PM today" | `at:<computed duration from now>` |
| "once at 9:30 AM tomorrow" | `at:<computed duration from now>` |

### One-shot vs recurring
- `at:` → always one-shot (`--once` is auto-set by the script)
- `every:` or `cron:` → recurring by default
- If user says "just once" or "one time" with a `cron:` or `every:` → pass `--once`

### Job name
Generate a short, descriptive name from the user's request.
- "Remind me to check NVDA every Monday" → `"NVDA Check - Monday 9AM"`
- "Alert me in 20 minutes" → `"Alert - 20min"`
- "Grocery reminder at noon" → `"Groceries - Noon"`

### Message
The message is what the agent will say or do when the job fires.
Craft it clearly so the agent knows exactly what to do:
- "Remind me to do groceries" → `"Reminder: Time to do groceries! 🛒"`
- "Check NVDA every Monday at 9 AM" → `"Check the current NVDA stock price and send me a summary."`
- "Send me a motivational quote every morning" → `"Send me an inspiring motivational quote to start the day."`

---

## Step 3 — Clarification rules (ask before acting)

### Ask when:
1. **No schedule at all**: "Remind me to call John" → no time/frequency given
   > Ask: "Sure! When would you like me to remind you — just once at a specific time, or on a recurring schedule?"

2. **Ambiguous frequency**: "Remind me often" or "check regularly"
   > Ask: "How often? Every hour, every day, or something else?"

3. **Conflicting signals**: "Remind me every Monday but just once"
   > Ask: "Just to confirm — should this be a one-time reminder or repeat every Monday?"

### Do NOT ask when:
- Everything is clear: "Remind me every Monday at 9 AM to check NVDA" → create immediately
- One-shot is obvious from context: "Remind me in 20 minutes" → at:20m, once
- User confirms after your clarification question → proceed immediately

### Confirmation before creating (always):
Before calling the script, summarise what you're about to set up and get a quick confirmation:

> "Got it! Here's what I'll set up:
> ⏰ **Reminder:** Check NVDA stock price
> 🔁 **Schedule:** Every Monday at 9 AM
> 🌍 **Timezone:** Africa/Lagos (UTC+1)
> 📱 **Delivered to:** This chat
>
> Shall I go ahead?"

Always include the **Timezone** line in the confirmation summary. If falling back to UTC because none was found, say so clearly:
> 🌍 **Timezone:** UTC (no timezone found — times will be in UTC)

Only proceed after user confirms.

---

## Commands

### Create a reminder

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "<job name>" \
  "<what to say or do>" \
  "<every:duration | cron:expr | at:duration>" \
  "<channel>" \
  "<chatId>" \
  [once] \
  [tz:<IANA timezone>]
```

- `tz:` is optional but **always include it** when a timezone was resolved (tiers 1–2)
- Pass `tz:UTC` explicitly when falling back — makes the stored description accurate
- Examples: `tz:Africa/Lagos`, `tz:America/New_York`, `tz:Europe/London`, `tz:Asia/Kolkata`
- Common short names are accepted: `tz:EST`, `tz:IST`, `tz:CET`, `tz:Lagos`, `tz:London`

### List reminders for this chat

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py list \
  "<channel>" \
  "<chatId>"
```

### Cancel a reminder by name

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name "<job name>"
```

### Cancel a reminder by ID

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel id "<job id>"
```

---

## Examples

### Example 1 — Clear request, no clarification needed

**User:** "Remind me every Monday at 9 AM to check NVDA"

1. Detect: channel=telegram, to=<chatId>
2. Read USER.md → Timezone: Africa/Lagos → resolves to `Africa/Lagos`
3. Parse: WHAT="Check NVDA stock price", WHEN=cron:0 9 * * 1, one-shot=false
4. Confirm with user (include timezone line)
5. Run:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "NVDA Check - Monday 9AM" \
  "Check the current NVDA stock price and send me a summary." \
  "cron:0 9 * * 1" \
  "telegram" \
  "<chatId>" \
  "tz:Africa/Lagos"
```

---

### Example 2 — Missing frequency, ask first

**User:** "Remind me to go do groceries by 12 PM"

1. Detect: channel=telegram, to=<chatId>
2. Read USER.md → Timezone: Africa/Lagos → resolves to `Africa/Lagos`
3. Parse: WHAT="Do groceries", WHEN=12 PM but frequency unclear
4. Ask: "Just to confirm — is this a one-time reminder for today at noon, or should I remind you every day at 12 PM?"
5. User says: "Just today"
6. Compute duration from now to today's noon **in Africa/Lagos time** → e.g. `at:3h30m`
7. Confirm (include timezone line), then run:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "Groceries - Noon" \
  "Reminder: Time to go do groceries! 🛒" \
  "at:3h30m" \
  "telegram" \
  "<chatId>" \
  once \
  "tz:Africa/Lagos"
```

---

### Example 3 — List reminders

**User:** "What reminders do I have?"

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py list \
  "telegram" \
  "<chatId>"
```

Format the output as a readable list, not raw JSON. Example response:

> You have **2 active reminders** in this chat:
>
> 1. **NVDA Check - Monday 9AM** 🔁 Every Monday at 9 AM
>    _"Check the current NVDA stock price..."_
>    🌍 Timezone: Africa/Lagos (UTC+1)
>    Next run: Mon 10 Mar 2026, 09:00
>
> 2. **Groceries - Noon** (one-time)
>    _"Time to go do groceries!"_
>    🌍 Timezone: Africa/Lagos (UTC+1)
>    Runs in: 3h 30m

---

### Example 4 — Cancel a reminder

**User:** "Cancel my NVDA reminder"

1. List jobs for this channel/chat first (internally)
2. Find the matching job by name
3. Confirm: "Cancel **NVDA Check - Monday 9AM**? This will stop all future runs."
4. User confirms
5. Run:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py cancel name "NVDA Check - Monday 9AM"
```

---

### Example 5 — One-shot in-chat reminder

**User:** "In 30 seconds send me a love letter"

> `at:` schedules are duration-based (relative to now), so timezone does not affect when they fire.
> Still pass `tz:` so it is stored in the job description for consistency.

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "Love Letter - 30s" \
  "Write a beautiful, heartfelt love letter. Make it romantic and touching." \
  "at:30s" \
  "telegram" \
  "<chatId>" \
  "tz:Africa/Lagos"
```

---

### Example 6 — Timezone in message, no USER.md entry

**User:** "Remind me every day at 8 AM New York time to drink water"

1. Detect: channel=telegram, to=<chatId>
2. Tier 1 hit: "New York time" → resolves to `America/New_York` — no need to check USER.md
3. Parse: WHAT="Drink water", WHEN=cron:0 8 * * *, one-shot=false
4. Confirm with user
5. Run:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "Drink Water - 8AM NY" \
  "Reminder: Time to drink water! 💧" \
  "cron:0 8 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:America/New_York"
```

---

### Example 7 — No timezone anywhere, ask user

**User:** "Remind me every day at 7 AM to exercise"

1. Detect: channel=telegram, to=<chatId>
2. Tier 1: no timezone in message
3. Tier 2: USER.md Timezone field is empty
4. Tier 3: Ask — _"What timezone are you in? (e.g. London, Lagos, New York)"_
5. User says: "Lagos"
6. Resolve: `Africa/Lagos`
7. Offer: _"Want me to remember Lagos time for future reminders?"_
8. If yes → update USER.md: `Timezone: Africa/Lagos`
9. Confirm, then run:

```bash
uv run /root/.openclaw/workspace/skills/remind-me/src/main.py create \
  "Exercise - 7AM" \
  "Reminder: Time to exercise! 💪" \
  "cron:0 7 * * *" \
  "telegram" \
  "<chatId>" \
  "tz:Africa/Lagos"
```

---

## Channel scoping rules

- Jobs created from **Group A** are only visible when listing from **Group A**
- Jobs created from **Group B** are only visible when listing from **Group B**
- Jobs created from the **main/private chat** are visible only in that main chat
- The script handles this automatically via the `[remind-me:channel:chatId]` tag embedded in each job's description
- **Never show a user jobs that belong to a different chat**

---

## Output formatting

After running any command, always format the result in plain conversational language — never dump raw JSON to the user.

### On create success:
> ✅ Done! I've set up your reminder:
> ⏰ **NVDA Check** — Every Monday at 9 AM
> 📱 Delivered to this chat

### On list (empty):
> You have no active reminders in this chat.

### On cancel success:
> ✅ Reminder **"NVDA Check - Monday 9AM"** has been cancelled.

### On error:
> ❌ Something went wrong: `<error message>`
> Want me to try again?

---

## Notes

- `uv run` auto-installs dependencies from the inline script header — no pip or venv needed.
- The script calls `openclaw cron` CLI internally — the gateway must be running.
- Always use `--channel "last"` behaviour naturally: since `--to` is set to the originating chat ID, delivery is always back to the right place.
- Do NOT use sessions_spawn, web search, or any other tool to create cron jobs — always go through this script.
- Do NOT hardcode channel IDs. Always read from session context.
- The `at:` schedule prefix does not support standard cron expressions — use `cron:` for those.