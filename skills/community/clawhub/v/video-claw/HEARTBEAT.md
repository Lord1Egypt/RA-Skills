# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## Content Calendar Cron Manager

Manages one-shot reminder crons for upcoming planned calendar events. Runs on every heartbeat cycle (~30 min).

**Goal:** Ensure every planned item with a future reminderFiresAt has a corresponding one-shot cron. Do not send any messages directly — that is the cron's job.

Steps:

1. Read `~/.videoclaw_personal_mcp_token` → extract `pat` (full file content, trimmed). Use baseUrl `app.humeo.com`.
2. Read `~/.openclaw/workspace/USER.md` → find the `## Notifications` section and extract the `Preferred reminder channel` value. Store it as `notifyChannel`. If the section is missing or the value is not set, **do not create the cron** — instead alert the user in the main session and ask them which channel they want reminders on before proceeding.
3. Call `GET /api/mcp/calendar/list?status=planned&limit=100` on the baseUrl with `Authorization: Bearer <pat>`.
4. For each item in the response:
   a. Skip if `targetDate` is null.
   b. Compute `reminderFiresAt = new Date(targetDate) - reminderMinutes * 60000`. Skip if already in the past.
   c. If `cronJobId` is already set, skip — cron exists.
   d. Create a one-shot cron using `CronCreate`. Use the actual `notifyChannel` value from step 2 as the `channel` — not a placeholder string:
      ```json
      {
        "name": "VideoClaw Reminder",
        "schedule": { "kind": "at", "at": "<reminderFiresAt>" },
        "sessionTarget": "isolated",
        "wakeMode": "now",
        "payload": {
          "kind": "agentTurn",
          "lightContext": true,
          "timeoutSeconds": 120,
          "message": "You are a one-shot VideoClaw reminder agent.\n1. Read ~/.videoclaw_personal_mcp_token — extract PAT (full file content, trimmed). Use baseUrl app.humeo.com.\n2. Read ~/.openclaw/workspace/USER.md — extract user name (default: 'there').\n3. Call GET /api/mcp/calendar/<ITEM_ID> on the baseUrl with Authorization: Bearer <pat>.\n4. If item is missing, not planned/scripted, or targetDate has passed beyond usefulness, stop.\n5. If handoffReady is false, call POST /api/mcp/calendar/<ITEM_ID>/prepare on the baseUrl with same auth.\n6. Send one warm message to BOTH channels: (a) deliver via Telegram announce (handled by cron delivery config), (b) also call sessions_send with sessionKey 'agent:main:main' to post the same message to webchat. Include topic, recordingMode (capitalised), reminderMinutes, and handoffUrl as a clickable link.\n7. Call POST /api/mcp/calendar/<ITEM_ID>/reminded on the baseUrl with same auth."
        },
        "delivery": { "mode": "announce", "channel": "<notifyChannel>", "to": "last", "bestEffort": true }
      }
      ```
      Substitute: `<reminderFiresAt>` → computed ISO time. `<ITEM_ID>` → item id (3 places in message). `<notifyChannel>` → the actual channel value read from USER.md (e.g. `telegram`).
   e. Call `PATCH /api/mcp/calendar/<item id>` with `{ "cronJobId": "<returned cron id>" }`.
5. If no new crons were created, return `HEARTBEAT_OK`.
