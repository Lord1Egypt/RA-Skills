---
name: smart-surprise
description: A proactive AI companion that initiates casual conversations with users at unpredictable times, making the AI feel like a real partner rather than a passive tool. Use when you want to bring surprise, warmth, and variety to user interactions — sending greetings, sharing tips, checking in on wellbeing, or sparking interesting conversations based on the user's personal preferences. Activate when: (1) a user installs this skill and triggers the initial cron, (2) you want to proactively reach out to a user instead of always waiting to be messaged first. This skill manages a self-perpetuating chain of one-shot cron jobs — each run delivers a personalized message, learns from user preferences, schedules the next random trigger, then deletes itself.
---

# Smart Surprise

## What This Skill Does

Smart Surprise transforms a passive AI assistant into a **proactive companion** that reaches out to users at unpredictable moments — with greetings, care, tips, news, or just a friendly chat. Over time it learns what the user likes and tailors content accordingly, making every interaction feel more personal.

Unlike fixed scheduled tasks that feel mechanical, Smart Surprise uses a **chain of self-deleting one-shot cron jobs** to create organic, surprise-driven interactions. The chain runs indefinitely and **learns continuously** from what the user responds to.

## How the Core Loop Works

```
[One-shot cron fires at scheduled time]
         ↓
[Main session agent runs]
         ↓
[Reads config + topics/preferences from topics.md]
         ↓
[Selects 2-3 topics based on user preferences]
         ↓
[Composes a personalized message]
         ↓
[Sends to user via openclaw message send]
         ↓
[Updates user preferences in topics.md]
         ↓
[Schedules next random trigger]
         ↓
[Deletes itself — chain continues permanently]
```

## Workflow

### Phase 1: Initial Setup (One Time Only)

When the user first installs and activates Smart Surprise, an initial one-shot cron job must be created. This is the **only manual step** — everything after is automatic and self-learning.

See [references/setup.md](references/setup.md) for the complete step-by-step setup guide.

### Phase 2: Runtime (Self-Perpetuating Chain)

Each triggered run executes the following steps:

**Step 1: Read configuration and preferences**
- Read `~/.openclaw/workspace/skills/smart-surprise/config.json` — static settings (timezone, location, intervals, etc.)
- Read `~/.openclaw/workspace/skills/smart-surprise/references/topics.md` — available topics + learned user preferences

**Step 2: Determine the next trigger time**
- Generate a random delay between `minIntervalMinutes` and `maxIntervalMinutes`
- If the next trigger would fall inside quiet hours → shift to `quietHoursEnd`
- Write the next scheduled time to `~/.openclaw/workspace/skills/smart-surprise/next_run.json`

**Step 3: Compose the message**
- Check current time and day in the user's configured timezone
- Randomly select **2-3 topics** from the active pool, weighted by user preference (topics the user likes are more likely to be selected)
- **Always include ≥1 interaction topic** (greeting, time-care, or check-in)
- Combine into a structured message: Opening → Body → Closing
- Generate content for each selected topic

**Step 4: Deliver the message**
```
openclaw message send --channel <channel> --target <channelTarget> --message "<composed_message>"
```

**Step 5: Learn from this interaction**
- After sending, silently update `topics.md` with any preference signals observed in this session
- Examples of preference signals:
  - User explicitly says "I don't like this topic" → record as `disliked`
  - User responds positively to a topic → record as `liked`
  - User asks for more of something → increase weight
  - User never responds to a topic → decrease weight
- The next run reads the updated preferences automatically

**Step 6: Schedule the next run**
- Use `openclaw cron add` with the random delay
- Set `deleteAfterRun: true` on the new job
- The job fires, executes, schedules the next, and deletes itself

**Step 7: Exit**
- The `deleteAfterRun: true` flag ensures self-deletion after completion
- No session cleanup needed — the main session handles this automatically

## Topics System

The topics system replaces the traditional "content categories" approach with a **learnable, extensible topic pool**.

### Topics

The skill ships with 11 initial topics:

- `greeting` — Warm, casual opening (interaction)
- `time-care` — Time-aware contextual care (interaction)
- `weather` — Weather-based practical suggestions (requires `location` in config)
- `calendar` — Google Calendar reminders (requires calendar integration)
- `health` — Health micro-tips
- `tips` — Useful tips and life hacks
- `history` — "On this day" historical facts
- `entertainment` — Movie/music recommendations
- `quote` — Quotes and poems
- `news` — Top news of the day
- `check-in` — Emotional connection / wellbeing question (interaction)

### Topic Extensibility

**This is not a closed list.** Users or the agent can add new topics at any time by editing `topics.md`. The agent can also create new topics during runtime if the user's interests suggest one.

### Preference Learning

Each topic in `topics.md` has a **preference state**: `normal`, `preferred`, or `dislike`. The agent updates these after each interaction based on user signals.

- `normal` — selected at normal frequency
- `preferred` — selected more often
- `dislike` — selected much less often (never fully excluded)

The agent listens for signals like "I love this" → `preferred`, "stop" → `dislike`, "talk more about Y" → `preferred`. `check-in` can never be `dislike`.

### Combination Rules

- Every message must contain at least 1 **interaction topic**
- Default: 2 topics per message (1 interaction + 1 informational)
- Maximum: 3 topics per message (never overwhelm)

### Message Structure

```
1. Opening:  greeting or time-care  (sets emotional tone)
2. Body:     1-2 informational topics  (tips/news/quote/etc.)
3. Closing:  check-in or time-care  (invites a response)
```

See [references/topics.md](references/topics.md) for the complete topic definitions, default weights, and preference learning rules.

## Configuration

All static configuration is in `~/.openclaw/workspace/skills/smart-surprise/config.json`. **No hardcoded values.**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `timezone` | `Asia/Shanghai` | User's IANA timezone |
| `location` | (required for weather) | City for weather lookups (e.g., `Beijing`, `New York`) |
| `quietHoursStart` | `22:00` | Quiet hours start (HH:MM) |
| `quietHoursEnd` | `08:00` | Quiet hours end (HH:MM) |
| `minIntervalMinutes` | `60` | Minimum random wait (minutes) |
| `maxIntervalMinutes` | `480` | Maximum random wait (minutes) |
| `channel` | (required) | OpenClaw channel name (`telegram`, `discord`, etc.) |
| `channelTarget` | (required) | Recipient ID on that channel (chat ID, user ID, etc.) |
| `characteristics` | `"warm, casual, playful"` | Natural language description of preferred communication style |

See [references/config.md](references/config.md) for the complete schema.

## Credentials & Sensitive Files

**Google Calendar Integration (optional):**
If you enable the `calendar` topic, the skill will attempt to read Google OAuth credentials. Two supported paths:
- `~/.openclaw/secrets/google-calendar.json` — OAuth token file
- `~/.openclaw/scripts/google-calendar.py` — helper script

⚠️ **These files contain sensitive tokens.** Only provide access if you trust the skill and understand what these files contain. If not configured, the `calendar` topic silently produces no output (no error is shown).

## File Structure

```
~/.openclaw/workspace/skills/smart-surprise/
├── config.json            # Static configuration (timezone, location, intervals)
├── next_run.json          # Runtime state — written by the agent, do NOT edit
└── references/
    ├── setup.md           # Installation guide
    ├── topics.md          # Topic definitions + user preference learning
    └── config.md          # Configuration field reference
```

## Skill Metadata

- **Type:** Proactive interaction / personal companion
- **Trigger mechanism:** Self-perpetuating cron chain (one-shot jobs, auto-delete)
- **Delivery:** User-configured channel (Telegram, Discord, WhatsApp, etc.)
- **Learning:** Continuous, preference-based topic weighting in topics.md
- **Installation:** One-time manual setup; chain runs forever and learns over time
- **Context:** Each run uses main session (sees conversation history)
