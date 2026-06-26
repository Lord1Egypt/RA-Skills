---
name: slack-member-fetch
description: Fetch Slack member information from a workspace or a specific Slack channel using the Slack Web API. Use when the user asks to list Slack members, get member profiles, fetch users from a channel, or export Slack member info. Supports workspace-wide lookup and channel-specific lookup. Not for sending Slack messages or editing Slack users.
metadata: openclaw
---

# Slack Member Fetch

This skill fetches member information from Slack.

## What it can do

- List members from the whole Slack workspace
- List members from a specific Slack channel by channel ID
- List members from a specific Slack channel by channel name
- Return structured JSON for downstream automation

## Required environment variable

```bash
export SLACK_BOT_TOKEN="xoxb-..."
```

## Recommended Slack scopes

- `users:read`
- `users:read.email`
- `conversations:read`

## Usage

Fetch all workspace members:

```bash
python3 scripts/fetch_slack_members.py --workspace
```

Fetch members from a channel by ID:

```bash
python3 scripts/fetch_slack_members.py --channel C0123456789
```

Fetch members from a channel by name:

```bash
python3 scripts/fetch_slack_members.py --channel-name general
```

Save output:

```bash
python3 scripts/fetch_slack_members.py --channel-name sales --out members.json
```

## Output shape

```json
{
  "ok": true,
  "source": "channel",
  "channel_id": "C0123456789",
  "channel_name": "sales",
  "count": 2,
  "members": [
    {
      "user_id": "U123",
      "username": "jane",
      "real_name": "Jane Doe",
      "display_name": "Jane",
      "email": "jane@example.com",
      "title": "Operations Manager",
      "timezone": "Asia/Manila",
      "is_admin": false,
      "is_owner": false,
      "is_bot": false,
      "deleted": false
    }
  ]
}
```

## Notes

- If email is missing, confirm the app has `users:read.email`
- If channel lookup fails, confirm the app has access to that channel and `conversations:read`
- For large workspaces, the script follows Slack cursor pagination automatically
