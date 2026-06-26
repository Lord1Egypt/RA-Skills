# Automations — Agent Routines & Push Notifications

Wayve automations come in two flavors:

1. **Agent Routines** (`agent_routine`) — Playbooks your AI agent can follow. Stored in Wayve, executed by copying to your agent. NOT executed server-side.
2. **Push Notifications** — Server-executed scheduled notifications delivered via Telegram, Discord, Slack, email, or pull.

## How It Works

### Agent Routines
```
User creates agent routine via wayve automations create or Wayve app
    → Stored in wayve.automations (DB) with automation_type = 'agent_routine'
    → Visible in Automation Registry under "Agent Routines" tab
    → User copies instructions to their AI agent (or exports as JSON)
    → NOT executed by the server timer
```

### Push Notifications
```
User configures push notification via wayve automations create
    → Stored in wayve.automations (DB)
    → Azure timer function checks every 5 minutes
    → Builds message from template + live data
    → Delivers via configured channel (Telegram, Discord, Slack, email, or pull)
```

No VPS, no bash scripts, no cron jobs needed. Everything runs server-side.

## App Deep Links

Always include the relevant link when directing the user to take action in the Wayve app. Base URL: `https://gowayve.com`

| Action | URL |
|--------|-----|
| Dashboard | https://gowayve.com/dashboard |
| Weekly Planning | https://gowayve.com/week |
| Calendar | https://gowayve.com/calendar |
| Life Pillars | https://gowayve.com/buckets |
| Projects | https://gowayve.com/projects |
| Time Locks | https://gowayve.com/time-locks |
| Review Hub | https://gowayve.com/review |
| Wrap Up Ritual | https://gowayve.com/wrap-up |
| Fresh Start Ritual | https://gowayve.com/fresh-start |
| Account Settings | https://gowayve.com/account |

## Available Types

### Agent Routine Type

| Type | Default Schedule | Purpose |
|------|-----------------|---------|
| `agent_routine` | `0 9 * * 1-5` | AI agent playbook — stores instructions, skills, and schedule. Not executed server-side. |

### Push Notification Types

| Type | Default Schedule | What it sends |
|------|-----------------|---------------|
| `morning_brief` | `30 7 * * *` | Today's activity count + dashboard link |
| `evening_winddown` | `0 21 * * *` | Completed/total activities today |
| `wrap_up_reminder` | `0 19 * * 0` | Sunday wrap-up nudge |
| `fresh_start_reminder` | `30 8 * * 1` | Monday planning nudge with carryover count |
| `mid_week_pulse` | `30 12 * * 3` | Mid-week progress summary |
| `friday_check` | `0 15 * * 5` | Uncompleted activities count |
| `frequency_tracker` | `0 20 * * *` | Pillar frequency alert (silent when on track) |
| `monthly_audit` | `0 11 1 * *` | Monthly review prompt |
| `time_audit_checkin` | `0 */2 * * *` | Time audit check-in (per audit config) |

## Delivery Channels

| Channel | What you need | How it works |
|---------|---------------|--------------|
| `telegram` | Bot token + chat ID | Direct Telegram Bot API call |
| `discord` | Webhook URL | POST to Discord webhook |
| `slack` | Incoming webhook URL | POST to Slack webhook |
| `email` | Email address | Via Azure Communication Services |
| `openclaw` | Gateway URL + hook token | POST to /hooks/wake + direct channel delivery |
| `openclaw_whatsapp` | Gateway URL + hook token | POST to /hooks/agent with WhatsApp delivery |
| `pull` | Nothing | Messages stored in DB, retrieved via SessionStart hook |

### Channel Setup Details

**Telegram:**
1. Create a bot via @BotFather, get the bot token
2. Start a chat with your bot, send a message
3. Get your chat_id via `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Pass via CLI:
```bash
wayve automations create morning_brief --cron "30 7 * * *" --timezone Europe/Amsterdam --channel telegram --delivery-config '{"bot_token":"YOUR_TOKEN","chat_id":"YOUR_CHAT_ID"}' --json
```

**Discord:**
1. In your Discord server: Server Settings > Integrations > Webhooks > New Webhook
2. Copy the webhook URL
3. Pass via CLI:
```bash
wayve automations create morning_brief --cron "30 7 * * *" --timezone Europe/Amsterdam --channel discord --delivery-config '{"webhook_url":"https://discord.com/api/webhooks/..."}' --json
```

**Slack:**
1. Create an Incoming Webhook at api.slack.com/apps
2. Copy the webhook URL
3. Pass via CLI:
```bash
wayve automations create morning_brief --cron "30 7 * * *" --timezone Europe/Amsterdam --channel slack --delivery-config '{"webhook_url":"https://hooks.slack.com/services/..."}' --json
```

**Email:**
```bash
wayve automations create morning_brief --cron "30 7 * * *" --timezone Europe/Amsterdam --channel email --delivery-config '{"email":"you@example.com"}' --json
```

**Pull (no setup needed):**
Messages are stored server-side and automatically presented when you start a new Claude Code session (via the SessionStart hook). No `--delivery-config` needed.

## Setup Flow

When offering automations to the user:

1. **Ask what they want**: "I can set up proactive notifications. Want the Starter Bundle (morning brief + weekly rituals) or the Full Bundle?"
2. **Ask timezone**: "What's your timezone? (e.g., Europe/Amsterdam)"
3. **Ask delivery channel**: "Where should I send notifications — Telegram, Discord, Slack, email, or just show them when you start a session?"
4. **Ask explicit permission before collecting credentials**: Explain exactly what data you need (e.g., bot token + chat ID for Telegram), why you need it (to deliver notifications), and how it's stored (encrypted with AES-256-GCM, deletable anytime by removing the automation). **Never collect or pass credentials without the user explicitly confirming.** If the user declines, offer the `pull` channel instead (no credentials needed).
5. **Collect channel credentials** if the user agreed — guide them through getting the token/webhook (see Channel Setup Details above)
6. **Create the bundle or individual automations** via CLI commands, passing `--delivery-config` with the credentials
7. **Confirm**: Show what was created with schedules

### Example: Create an agent routine
```bash
wayve automations create agent_routine --cron "0 9 * * 1" --timezone Europe/Amsterdam --channel pull --name "Weekly Content Research" --config '{"description": "Research trending topics in my niche", "agent_instructions": "Every Monday at 9am, research the top 10 trending topics in solopreneur AI tools. Summarize each with a one-line hook and report via Telegram.", "skills": ["research", "content"], "pillar_id": "..."}' --json
```

Note: `delivery_channel` defaults to "pull" for agent routines. No credentials needed.

### Example: Create a starter bundle (push notifications)
```bash
wayve automations bundle starter --timezone Europe/Amsterdam --channel telegram --delivery-config '{"bot_token":"YOUR_TOKEN","chat_id":"YOUR_CHAT_ID"}' --json
```

## Bundles

### Starter Bundle
- Morning Brief (7:30 daily)
- Wrap Up Reminder (Sunday 19:00)
- Fresh Start Reminder (Monday 8:30)

### Full Bundle
Everything in Starter, plus:
- Evening Wind Down (21:00 daily)
- Mid-Week Pulse (Wednesday 12:30)
- Friday Check (Friday 15:00)
- Frequency Tracker (20:00 daily)
- Monthly Audit (1st of month 11:00)

## Managing Automations

| User says | Action |
|-----------|--------|
| "List my automations" | `wayve automations list --json` |
| "Pause my morning briefs" | `wayve automations update ID --enabled false --json` |
| "Resume morning briefs" | `wayve automations update ID --enabled true --json` |
| "Change morning brief to 8:00" | `wayve automations update ID --cron "0 8 * * *" --json` |
| "Delete all automations" | List, then delete each |
| "Switch to Discord" | Update each automation with new delivery_channel + delivery_config |

Always update the knowledge base when automations change.

## When to Suggest Automations

| Moment | Suggested Automations |
|--------|----------------------|
| After **onboarding** completes | Starter bundle |
| After first **Wrap Up** | wrap_up_reminder if not set |
| After first **Fresh Start** | fresh_start_reminder if not set |
| User starts a **Time Audit** | time_audit_checkin for audit duration |
| User says "remind me" | Suggest creating an automation |

Frame it naturally: "Want me to send you a morning brief at 7:30 every day? I can also nudge you Sunday evening for your Wrap Up."

## Security Constraints

- **User approval required** — every automation must be explicitly approved
- **Predefined types only** — only the 10 types listed above are accepted (9 push + agent_routine)
- **No arbitrary code execution** — push messages are fixed templates filled with live data; agent routines are stored playbooks, NOT executed server-side
- **Delivery credentials encrypted** — AES-256-GCM at rest, never returned via API
- **User can stop at any time** — "stop all reminders" must be respected immediately
