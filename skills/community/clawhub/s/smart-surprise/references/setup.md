# Smart Surprise — Setup Procedure

This guide walks you through installing and activating Smart Surprise on your OpenClaw instance.

## Prerequisites

- Openclaw installed and configured with at least one messaging channel (Telegram, Discord, etc.)
- `openclaw` CLI accessible in your PATH

---

## Step 1: Create the Config File

Create `~/.openclaw/workspace/skills/smart-surprise/config.json`:

```json
{
  "timezone": "Asia/Shanghai",
  "location": "Beijing",
  "quietHoursStart": "22:00",
  "quietHoursEnd": "08:00",
  "minIntervalMinutes": 30,
  "maxIntervalMinutes": 120,
  "channel": "telegram",
  "channelTarget": "<USER_CHAT_ID>"
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `timezone` | IANA timezone identifier (e.g., `Asia/Shanghai`, `America/New_York`) |
| `location` | City for weather lookups (e.g., `Beijing`, `New York`) |
| `channel` | Your configured Openclaw channel name (`telegram`, `discord`, etc.) |
| `channelTarget` | Recipient ID on that channel (Telegram chat ID, Discord user ID, etc.) |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `quietHoursStart` | `"22:00"` | Quiet hours start (HH:MM, 24h) |
| `quietHoursEnd` | `"08:00"` | Quiet hours end (HH:MM, 24h) |
| `minIntervalMinutes` | `30` | Minimum random wait (minutes) |
| `maxIntervalMinutes` | `120` | Maximum random wait (minutes) |

---

## Step 2: Create the Initial Cron Trigger

Run this **once** to start the self-perpetuating chain. The initial trigger should be **~5 minutes after setup** so the agent has time to initialize. Generate the UTC timestamp dynamically:

```bash
# Generate UTC timestamp for 5 minutes from now
INIT_TIME=$(date -u -d "+5 minutes" +"%Y-%m-%dT%H:%MZ")

openclaw cron add \
  --name "Smart Surprise" \
  --session isolated \
  --delete-after-run \
  --at "$INIT_TIME" \
  --message "Read ~/.openclaw/workspace/skills/smart-surprise/SKILL.md and execute Phase 2: Runtime workflow. Deliver a greeting message to the user, then schedule the next random trigger and delete this job." \
  --timeout-seconds 900
```

> **Important:** Do NOT use a fixed timestamp like `2026-04-10T09:00Z`. Always use a dynamic timestamp (`now + 5 minutes`) so the first trigger fires shortly after the skill is installed, not at some arbitrary future date.

### Recommended Cron Job Parameters (JSON equivalent)

If you manage cron jobs via the JSON config file (e.g., editing `~/.openclaw/cron/jobs.json`), use these settings:

```json
{
  "name": "Smart Surprise",
  "enabled": true,
  "deleteAfterRun": true,
  "schedule": {
    "kind": "at",
    "at": "<INIT_TIME>"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Read ~/.openclaw/workspace/skills/smart-surprise/SKILL.md and execute Phase 2: Runtime workflow. Deliver a greeting message to the user, then schedule the next random trigger and delete this job.",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "none"
  }
}
```

> `<INIT_TIME>`: Use a UTC timestamp in ISO 8601 format (e.g., `2026-04-10T09:05:00.000Z`). Generate dynamically as `now + 5 minutes` so the first trigger fires shortly after installation, not at an arbitrary future date.

### Key parameters explained

| Parameter | Recommended Value | Why |
|-----------|-----------------|-----|
| `sessionTarget` | `isolated` | Runs in a fresh isolated session — avoids session-routing issues that cause hangs or token errors |
| `wakeMode` | `now` | Fires immediately at the scheduled time |
| `payload.timeoutSeconds` | `900` (15 min) | Gives the agent enough time to compose and send a message |
| `deleteAfterRun` | `true` | Job deletes itself after completion — enables the self-perpetuating chain |
| `delivery.mode` | `none` | Do NOT use `announce` — it sends all agent thinking/output to the user. Agent sends the final message via `openclaw message send` in SKILL.md Step 4. |

### ⚠️ Common Mistakes When Setting Up Cron Manually

> **Mistake 1 — Using `session:agent:main:telegram:direct:<chatId>` for `sessionTarget`**
>
> This session key relies on the Telegram plugin being active and correctly routed. It often fails with `Telegram bot token missing for account "default"` or causes the job to hang. Use `isolated` instead.
>
> **Mistake 2 — Using `--session main` in the CLI**
>
> This routes to the main embedded session, which gets blocked if the user is currently chatting. The job will hang in `running` state forever. Use `--session isolated` instead.
>
> **Mistake 3 — Using `mode: announce` in `delivery`**
>
> Setting `delivery.mode: "announce"` will send the agent's entire output (including all thinking and intermediate steps) to the user — which reveals the agent's internal reasoning process. Always use `mode: "none"` here. The agent sends the final message precisely via `openclaw message send` in SKILL.md Step 4.

### Finding Your Chat ID

- **Telegram:** Message `@userinfobot` — it replies with your numeric user ID
- **Other channels:** Check OpenClaw logs or session keys when you send a test message

---

## Step 3: Verify

```bash
openclaw cron list | grep -i surprise
```

You should see a `Smart Surprise` entry with status `running` or `idle`.

---

## How the Chain Works

1. The initial cron fires at the scheduled time
2. The agent reads config + topics.md, composes a message, sends it, updates preferences, schedules the next random trigger, then deletes itself
3. The next trigger fires at the random time (between `minIntervalMinutes` and `maxIntervalMinutes`)
4. Repeat forever

The agent continuously learns your preferences over time by updating topics.md after each interaction.

---

## Troubleshooting

### Job stuck in `running` state forever

**Cause:** Used `--session main` or `session:agent:main:telegram:direct:<chatId>` — the main session was busy when the job fired, or the Telegram session routing failed with a token error.

**Fix:**
```bash
# Find and remove the stuck job
openclaw cron list | grep -i surprise
openclaw cron rm <job-id>   # repeat for each job found

# Recreate with correct session target (isolated)
openclaw cron add \
  --name "Smart Surprise" \
  --session isolated \
  --delete-after-run \
  --at "<future-UTC-time>" \
  --message "Read ~/.openclaw/workspace/skills/smart-surprise/SKILL.md and execute Phase 2: Runtime workflow..." \
  --timeout-seconds 900
```

> **Note:** Always use `isolated` as the session target. The old `session:agent:main:telegram:direct:<chatId>` approach is prone to `Telegram bot token missing for account "default"` errors and session-routing hangs.

### Message appears to send but user doesn't receive it

**Check:** Is `delivery.channel` set to your configured channel name (e.g., `telegram`) and `delivery.to` set to the correct recipient chat ID?

### To check logs in real-time

```bash
openclaw logs 2>&1 | grep -i "smart-surprise\|telegram\|cron.*deliver"
```

---

## Uninstallation

To completely remove Smart Surprise:

```bash
# Step 1: Stop and remove all Smart Surprise cron jobs
openclaw cron list | grep -i surprise
openclaw cron rm <job-id>   # repeat for each job found

# Step 2: Remove the skill directory
rm -rf ~/.openclaw/workspace/skills/smart-surprise

# Step 3: Optionally remove runtime state
rm -f ~/.openclaw/workspace/skills/smart-surprise/next_run.json
```

This fully removes Smart Surprise from your system.
