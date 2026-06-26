# Cron Setup — x-bookmark-triage

## OpenClaw Cron Registration

Register the bookmark poll to run at 9 AM and 5 PM daily:

```json
{
  "name": "knowledge-bookmark-poll",
  "schedule": { "kind": "cron", "expr": "0 9,17 * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the bookmark poll: `node /path/to/skills/x-bookmark-triage/scripts/bookmark-poll.js`. If it fails due to missing OAuth credentials, log the error and exit cleanly.",
    "model": "claude-haiku-4-5",
    "timeoutSeconds": 120
  },
  "delivery": { "mode": "none" },
  "enabled": true
}
```

Adjust the path to `bookmark-poll.js` to match your workspace. The cron payload runs as an isolated agent turn — it needs env vars (client ID, secret, refresh token) available to the gateway process.

## launchd Plist (macOS) — Manual Drop Poller

For the Discord channel drop handler (polls every 2 minutes):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.watson.knowledge-intake-poll</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/skills/x-bookmark-triage/scripts/run-poll.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>120</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/knowledge-intake-poll.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/knowledge-intake-poll.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>DISCORD_BOT_TOKEN</key><string>YOUR_BOT_TOKEN</string>
        <key>ANTHROPIC_DEFAULT_KEY</key><string>YOUR_ANTHROPIC_KEY</string>
        <key>X_OAUTH2_CLIENT_ID</key><string>YOUR_CLIENT_ID</string>
        <key>X_OAUTH2_CLIENT_SECRET</key><string>YOUR_CLIENT_SECRET</string>
        <key>X_OAUTH2_REFRESH_TOKEN</key><string>YOUR_REFRESH_TOKEN</string>
    </dict>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/ai.watson.knowledge-intake-poll.plist
```

Unload:
```bash
launchctl unload ~/Library/LaunchAgents/ai.watson.knowledge-intake-poll.plist
```

Check logs:
```bash
tail -f /tmp/knowledge-intake-poll.log
tail -f /tmp/knowledge-intake-poll.err
```

## systemd (Linux)

```ini
[Unit]
Description=Knowledge Intake Discord Poller

[Service]
Type=simple
ExecStart=/usr/bin/node /path/to/skills/x-bookmark-triage/scripts/poll-channel.js
Restart=always
RestartSec=120
Environment=DISCORD_BOT_TOKEN=...
Environment=ANTHROPIC_DEFAULT_KEY=...
Environment=X_OAUTH2_CLIENT_ID=...
Environment=X_OAUTH2_CLIENT_SECRET=...
Environment=X_OAUTH2_REFRESH_TOKEN=...

[Install]
WantedBy=multi-user.target
```
