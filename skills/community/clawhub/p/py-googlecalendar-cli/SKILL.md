---
name: google-calendar
description: Tiny and short Python CLI tool to manage Google Calendar events from the command line -- list, add, update, delete events via the Calendar API.
license: MIT
homepage: https://github.com/xwings/py-googlecalendar-cli
compatibility: Requires Python 3.6+. Network access to Google Calender
metadata: {"author": "xwings", "openclaw": {env: ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN", "GOOGLE_CALENDAR_ID"], "bins": ["python3 {baseDir}/scripts/google-calendar-cli.py"]}}
---

# Google Calendar CLI

A single-file CLI for Google Calendar using only Python 3 standard library.

## Setup

1. Create a Google Cloud project and enable the **Google Calendar API**.
2. Create **OAuth 2.0 credentials** (Desktop app). Note the client ID and secret.
3. Obtain a refresh token via the OAuth consent flow.
4. Export credentials:
   ```bash
   export GOOGLE_CLIENT_ID=...
   export GOOGLE_CLIENT_SECRET=...
   export GOOGLE_REFRESH_TOKEN=...
   export GOOGLE_CALENDAR_ID=primary  # optional, defaults to "primary"
   ```

## Usage

```
google-calendar-cli.py <command> [options]
```

| Command  | Description              |
|----------|--------------------------|
| `list`   | List upcoming events     |
| `today`  | Show today's events      |
| `add`    | Create a new event       |
| `update` | Update an existing event |
| `delete` | Delete an event          |

Credentials can also be passed as flags (`--client-id`, `--client-secret`, `--refresh-token`, `--calendar-id`).

Use `--json` for raw JSON output. Run with `-h` for full help.

## Examples

```bash
# List next 10 events
python3 {baseDir}/scripts/google-calendar-cli.py list

# Today's events
python3 {baseDir}/scripts/google-calendar-cli.py today

# Events in a date range
python3 {baseDir}/scripts/google-calendar-cli.py list --from 2025-06-01T00:00:00Z --to 2025-06-30T23:59:59Z

# Add an event
python3 {baseDir}/scripts/google-calendar-cli.py add --title "Meeting" \
    --start 2025-06-01T09:00:00-07:00 --end 2025-06-01T10:00:00-07:00

# Update an event
python3 {baseDir}/scripts/google-calendar-cli.py update --event-id EVENT_ID --title "New Title"

# Delete an event
python3 {baseDir}/scripts/google-calendar-cli.py delete --event-id EVENT_ID
```
