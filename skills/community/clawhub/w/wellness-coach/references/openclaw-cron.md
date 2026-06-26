# OpenClaw Cron Setup

## Register 7AM Daily Briefing

The morning briefing cron fires at 7AM NYC time, runs both pipeline scripts,
and triggers Bianca (OpenClaw agent) to send the Telegram message.

### Via OpenClaw cron tool
```json
{
  "name": "wellness-morning-briefing",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/New_York" },
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "WELLNESS_BRIEFING_SEND: Run the morning wellness briefing pipeline: cd ~/wellness-coach && python3 cron/morning_context.py && python3 cron/send_briefing.py. Then send the formatted Telegram message to Andre."
  }
}
```

## HEARTBEAT.md Entry

Add this to your OpenClaw HEARTBEAT.md so the agent knows to handle the event:

```markdown
## Wellness Briefing Delivery
If a system event arrives with text starting with `WELLNESS_BRIEFING_SEND:` —
extract everything after the prefix and send it as a Telegram message to the user.
Do not add any extra commentary — just forward the formatted message as-is.
```

## Manual Test
```bash
python3 cron/morning_context.py && python3 cron/send_briefing.py
```
Always run both together — Tavus sessions expire in ~10 min.
