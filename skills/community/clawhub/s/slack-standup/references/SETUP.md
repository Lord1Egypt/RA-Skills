# Slack Bot Setup

## 1. Create App
- Visit api.slack.com/apps → "Create New App" → From scratch
- Name: "Standup Bot"

## 2. Permissions
- OAuth & Permissions → Add scopes:
  - `chat:write` | `chat:write.public` | `channels:read`

## 3. Install
- "Install to Workspace" → Copy Bot Token (xoxb-*)

## 4. Add to Channel
```bash
/invite @StandupBot
```

## 5. Configure
```
SLACK_BOT_TOKEN=xoxb-...
```

## 6. Test
```bash
/standup test
```

**Security:** Never commit tokens. Rotate every 90 days.
