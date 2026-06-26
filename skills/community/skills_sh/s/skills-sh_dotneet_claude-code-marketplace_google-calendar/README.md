# Google Calendar + Tasks CLI

This skill provides a lightweight Python CLI for Google Calendar and Google Tasks API access using OAuth 2.0.
It is useful for listing/creating/updating events and tasks without using the MCP server.

## Requirements

- Python 3.9+ recommended
- Google Cloud project with the **Google Calendar API** and **Google Tasks API** enabled
- OAuth client credentials (Desktop app)

Install dependencies (venv recommended):

```bash
python3 -m venv ~/.config/google-calendar/venv
~/.config/google-calendar/venv/bin/pip install -r <skill_dir>/scripts/requirements.txt
```

The wrapper scripts (`gcal`, `gcal-auth`) automatically use the venv at `~/.config/google-calendar/venv` if it exists.

## Credentials (OAuth client)

1. Open Google Cloud Console and select/create a project.
2. Enable **Google Calendar API** and **Google Tasks API**.
3. Configure the OAuth consent screen (External or Internal).
4. Create credentials:
   - **Create Credentials** → **OAuth client ID** → **Desktop app**
5. Download the JSON file (client secret) and save it to `~/.config/google-calendar/credentials.json`.

Keep this file out of git and in a secure location.

## Authentication (token)

Authenticate and store a token:

- Calendar only:

```bash
<skill_dir>/scripts/gcal-auth
```

- Tasks only:

```bash
<skill_dir>/scripts/gcal-auth \
  --scopes https://www.googleapis.com/auth/tasks
```

- Calendar + Tasks (single token):

```bash
<skill_dir>/scripts/gcal-auth \
  --scopes https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/tasks
```

By default, the token is stored at:

```
~/.config/google-calendar/token.json
```

You can override the token path with either:

- `--token /custom/path/token.json`
- `GCAL_TOKEN_PATH=/custom/path/token.json`

**Token management tips**

- Use different token files for different Google accounts.
- Remove the token file to force re-authentication.
- Tokens contain refresh tokens; keep them secure and out of version control.

## Environment variables

- `GCAL_CREDENTIALS`: path to the client secret JSON (default: `~/.config/google-calendar/credentials.json`).
- `GCAL_TOKEN_PATH`: default path for the OAuth token JSON.

## Common commands

List calendars:

```bash
<skill_dir>/scripts/gcal list-calendars
```

List events:

```bash
<skill_dir>/scripts/gcal list-events \
  --calendar-id primary \
  --time-min 2026-01-01T00:00:00-08:00 \
  --time-max 2026-02-01T00:00:00-08:00
```

Create an event:

```bash
<skill_dir>/scripts/gcal create-event \
  --calendar-id primary \
  --summary "Review" \
  --start 2026-01-22T10:00:00-08:00 \
  --end 2026-01-22T11:00:00-08:00
```

List task lists:

```bash
<skill_dir>/scripts/gcal list-tasklists
```

List tasks:

```bash
<skill_dir>/scripts/gcal list-tasks \
  --tasklist <tasklist_id>
```

Create a task:

```bash
<skill_dir>/scripts/gcal create-task \
  --tasklist <tasklist_id> \
  --title "Buy milk" \
  --due 2026-01-22T10:00:00-08:00
```

## Date/time rules

- Timed events/tasks use RFC3339 (e.g., `2026-01-22T10:00:00-08:00`).
- All-day events use `YYYY-MM-DD` and end on the next day (exclusive).
- Use `--time-zone` when the datetime lacks an offset.

## Safety

- Confirm intent before creating/updating/deleting events or tasks.
- Keep OAuth credentials and token files out of git.
