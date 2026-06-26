---
name: ticktick
description: Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling.
---

# TickTick CLI Skill

Manage TickTick tasks and projects from the command line.

## Setup

### 1. Install dependencies

```bash
pip install -e .
# or just: pip install requests
```

### 2. Register a TickTick Developer App

1. Go to [TickTick Developer Center](https://developer.ticktick.com/manage)
2. Create a new application
3. Set the redirect URI to `http://localhost:8080`
4. Note your `Client ID` and `Client Secret`

### 3. Authenticate

```bash
# Set credentials and start OAuth flow
python -m ticktick.cli auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# Check authentication status
python -m ticktick.cli auth --status

# Logout (clear tokens, keep credentials)
python -m ticktick.cli auth --logout
```

If installed via `pip install -e .`, you can also use:
```bash
ticktick auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

### Headless / Manual Authentication

```bash
# Use manual mode on headless servers
python -m ticktick.cli auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --manual
```

This prints an authorization URL. Open it in a browser, approve access, then copy the full redirect URL (it looks like `http://localhost:8080/?code=XXXXX&state=STATE`) and paste it back into the CLI.

Tokens are stored in `~/.clawdbot/credentials/ticktick-cli/config.json`.

## Commands

### List Tasks

```bash
# List all tasks
python -m ticktick.cli tasks

# List tasks from a specific project
python -m ticktick.cli tasks --list "Work"

# Filter by status
python -m ticktick.cli tasks --status pending
python -m ticktick.cli tasks --status completed

# JSON output
python -m ticktick.cli tasks --json
```

### Create Task

```bash
# Basic task creation
python -m ticktick.cli task "Buy groceries" --list "Personal"

# With description and priority
python -m ticktick.cli task "Review PR" --list "Work" --content "Check the new auth changes" --priority high

# With due date
python -m ticktick.cli task "Submit report" --list "Work" --due tomorrow
python -m ticktick.cli task "Plan vacation" --list "Personal" --due "in 7 days"
python -m ticktick.cli task "Meeting" --list "Work" --due "2024-12-25"

# With tags
python -m ticktick.cli task "Research" --list "Work" --tag research important

# With start and due date (creates a time block)
python -m ticktick.cli task "Meeting" --list "Work" --start "2026-04-26T14:00:00+02:00" --due "2026-04-26T15:30:00+02:00"
```

### Update Task

```bash
# Update by task name or ID
python -m ticktick.cli task "Buy groceries" --update --priority medium
python -m ticktick.cli task "abc123" --update --due tomorrow --content "Updated notes"

# Rename a task
python -m ticktick.cli task "Old Name" --update --new-title "New Name"

# Limit search to specific project
python -m ticktick.cli task "Review PR" --update --list "Work" --priority low

# Update with start and due date (time block)
python -m ticktick.cli task "Meeting" --update --start "2026-04-26T14:00:00+02:00" --due "2026-04-26T15:30:00+02:00"
```

### Complete Task

```bash
# Mark task as complete
python -m ticktick.cli complete "Buy groceries"

# Complete with project filter
python -m ticktick.cli complete "Review PR" --list "Work"
```

### Abandon Task (Won't Do)

```bash
# Mark task as won't do
python -m ticktick.cli abandon "Old task"

# Abandon with project filter
python -m ticktick.cli abandon "Obsolete item" --list "Do"
```

### Batch Abandon (Multiple Tasks)

```bash
# Abandon multiple tasks in a single API call
python -m ticktick.cli batch-abandon <taskId1> <taskId2> <taskId3>

# With JSON output
python -m ticktick.cli batch-abandon abc123def456... xyz789... --json
```

Note: `batch-abandon` requires task IDs (24-character hex strings), not task names. Use `tasks --json` to get task IDs first.

### Attach File to Task

```bash
# Attach a file by task name
python -m ticktick.cli attach "Buy groceries" /path/to/file.pdf --list "Personal"

# Attach by task ID
python -m ticktick.cli attach abc123def456789012345678 /path/to/image.png

# JSON output
python -m ticktick.cli attach "Report" /tmp/report.pdf --list "Work" --json
```

**Note:** Attachment upload requires `sessionCookie` and `v2DeviceId` in the credentials config file. These use the TickTick web session API, not OAuth. If uploads fail with 401/403, the session cookie has expired — get a fresh `t` cookie from your browser.

### List Projects

```bash
# List all projects
python -m ticktick.cli lists

# JSON output
python -m ticktick.cli lists --json
```

### Create Project

```bash
# Create new project
python -m ticktick.cli list "New Project"

# With color
python -m ticktick.cli list "Work Tasks" --color "#FF5733"
```

### Update Project

```bash
# Rename project
python -m ticktick.cli list "Old Name" --update --new-name "New Name"

# Change color
python -m ticktick.cli list "Work" --update --color "#00FF00"
```

## Options Reference

### Priority Levels
- `none` - No priority (default)
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

### Start / Due Date Formats
- `today` - Today
- `tomorrow` - Tomorrow
- `in N days` - In N days (e.g., "in 3 days")
- `next monday` - Next occurrence of weekday
- ISO date with timezone - `2026-04-26T17:00:00+02:00` (preferred for precision)
- ISO date - `YYYY-MM-DD` or full ISO format

**Important:** Always use explicit timezone offsets (e.g. `+02:00`) for ISO dates to avoid UTC conversion issues.

### Global Options
- `--json` - Output results in JSON format (useful for scripting)
- `--help` - Show help for any command

## Agent Usage Tips

When using this skill as an AI agent:

1. **Always use `--json` flag** for machine-readable output
2. **List projects first** with `lists --json` to get valid project IDs
3. **Use project IDs** rather than names when possible for reliability
4. **Check task status** before completing to avoid errors

Example agent workflow:
```bash
# 1. Get available projects
python -m ticktick.cli lists --json

# 2. Create a task in a specific project
python -m ticktick.cli task "Agent task" --list "PROJECT_ID" --priority high --json

# 3. Later, mark it complete
python -m ticktick.cli complete "Agent task" --list "PROJECT_ID" --json
```

## Configuration

Tokens are stored in `~/.clawdbot/credentials/ticktick-cli/config.json`:
```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "accessToken": "...",
  "refreshToken": "...",
  "tokenExpiry": 1234567890000,
  "redirectUri": "http://localhost:8080"
}
```

Note: Credentials are stored in plaintext. The CLI sets file permissions to 700/600; treat this file as sensitive.

The CLI automatically refreshes tokens when they expire.

## Troubleshooting

### "Not authenticated" error
Run `python -m ticktick.cli auth` to authenticate.

### "Project not found" error
Use `python -m ticktick.cli lists` to see available projects and their IDs.

### "Task not found" error
- Check the task title matches exactly (case-insensitive)
- Try using the task ID instead
- Use `--list` to narrow the search to a specific project

### Token expired errors
The CLI auto-refreshes tokens. If issues persist, run `python -m ticktick.cli auth` again.

## File Attachments

The CLI supports file attachments via the `attach` command. Attachments use a **different API** (`/api/v1/`, NOT `/open/v1/`) and require a session cookie — not OAuth.

### Requirements
- **Session cookie** (`t` cookie from ticktick.com browser login) — stored in config as `sessionCookie`
- **X-Device header** — JSON with `platform`, `version`, `id` fields
- OAuth tokens do NOT work for attachments

### Manual curl upload (alternative to `attach` command)

```bash
# Read credentials
CONFIG="$HOME/.clawdbot/credentials/ticktick-cli/config.json"
COOKIE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['sessionCookie'])")
DEVICE_ID=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('v2DeviceId','clawagent00000000000001'))")
XDEVICE="{\"platform\":\"web\",\"version\":6430,\"id\":\"$DEVICE_ID\"}"

# Generate attachment ID (24-char hex)
ATT_ID=$(python3 -c "import secrets; print(secrets.token_hex(12))")

# Upload
curl -s -X POST \
  "https://api.ticktick.com/api/v1/attachment/upload/{PROJECT_ID}/{TASK_ID}/$ATT_ID" \
  -H "Cookie: t=$COOKIE" \
  -H "X-Device: $XDEVICE" \
  -H "User-Agent: Mozilla/5.0 (rv:145.0) Firefox/145.0" \
  -H "Origin: https://ticktick.com" \
  -H "Referer: https://ticktick.com/webapp/" \
  -F "file=@/path/to/file.pdf;type=application/pdf;filename=myfile.pdf"
```

### Upload endpoint details
- **URL:** `https://api.ticktick.com/api/v1/attachment/upload/{projectId}/{taskId}/{attachmentId}`
- **Method:** POST multipart/form-data
- **Auth:** Cookie `t={sessionCookie}` + `X-Device` header (JSON)
- **File field:** `file` (standard multipart)
- **Response:** JSON with `id`, `refId`, `path`, `size`, `fileName`, `fileType`, `createdTime`
- **fileType values:** `IMAGE`, `PDF`, `OTHER` (auto-detected by server)

### Important notes
- The `attachmentId` is client-generated (24-char hex, e.g. `secrets.token_hex(12)`)
- **Session cookies expire.** When you get 401/403/access_forbidden on attachment uploads, the cookie is dead. Ask the user for a fresh `t` cookie from their browser (ticktick.com → DevTools → Application → Cookies → `t`). Update `sessionCookie` in config. **Never ask for the user's password.**
- The V1 API (`/open/v1/`) does NOT return attachments in task responses
- V2 batch endpoint (`/api/v2/batch/task`) needs session cookie + X-Device header to work

## API Notes

This CLI uses the [TickTick Open API v1](https://developer.ticktick.com/api).

### Rate Limits
- **100 requests per minute**
- **300 requests per 5 minutes**

The CLI makes multiple API calls per operation (listing projects to find a task), so bulk operations can hit limits quickly.

### Batch Endpoint
The CLI supports TickTick's batch endpoint for bulk operations:
```
POST https://api.ticktick.com/open/v1/batch/task
{
  "add": [...],
  "update": [...],
  "delete": [...]
}
```
Use `batch-abandon` to abandon multiple tasks in one API call.

### Other Limitations
- Maximum 500 tasks per project
- Some advanced features (focus time, habits) not supported by the API
