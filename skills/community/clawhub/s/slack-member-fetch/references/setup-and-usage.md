# Setup and usage

## Slack app scopes

Add these bot token scopes:

- users:read
- users:read.email
- conversations:read

Then install or reinstall the app to the workspace.

## Example commands

Workspace:
```bash
python3 scripts/fetch_slack_members.py --workspace
```

Channel by ID:
```bash
python3 scripts/fetch_slack_members.py --channel C0123456789
```

Channel by name:
```bash
python3 scripts/fetch_slack_members.py --channel-name general
```

Write to file:
```bash
python3 scripts/fetch_slack_members.py --channel-name general --out members.json
```
