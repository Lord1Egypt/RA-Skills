# Google Calendar CLI

A command-line tool to manage Google Calendar events. Zero external dependencies — uses only Python 3 standard library.

## Setup

1. Create a [Google Cloud project](https://console.cloud.google.com/) and enable the **Google Calendar API**.
2. Create **OAuth 2.0 credentials** (Desktop app).
3. Complete the OAuth consent flow to obtain a refresh token.
4. Export your credentials:

```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REFRESH_TOKEN="your-refresh-token"
export GOOGLE_CALENDAR_ID="primary"  # optional, defaults to "primary"
```

Credentials can also be passed as CLI flags (`--client-id`, `--client-secret`, `--refresh-token`, `--calendar-id`).

## Usage

```bash
python3 scripts/google-calendar-cli.py <command> [options]
```

### Commands

| Command  | Description              |
|----------|--------------------------|
| `list`   | List upcoming events     |
| `today`  | Show today's events      |
| `add`    | Create a new event       |
| `update` | Update an existing event |
| `delete` | Delete an event          |

### Examples

```bash
# List next 10 events
python3 scripts/google-calendar-cli.py list

# Today's events
python3 scripts/google-calendar-cli.py today

# Events in a date range
python3 scripts/google-calendar-cli.py list --from 2025-06-01T00:00:00Z --to 2025-06-30T23:59:59Z

# Search events
python3 scripts/google-calendar-cli.py list --query "standup"

# Add an event
python3 scripts/google-calendar-cli.py add --title "Meeting" \
    --start 2025-06-01T09:00:00+08:00 --end 2025-06-01T10:00:00+08:00

# Add an all-day event
python3 scripts/google-calendar-cli.py add --title "Holiday" \
    --start 2025-06-01 --end 2025-06-02

# Update an event
python3 scripts/google-calendar-cli.py update --event-id EVENT_ID --title "New Title"

# Delete an event
python3 scripts/google-calendar-cli.py delete --event-id EVENT_ID

# Raw JSON output
python3 scripts/google-calendar-cli.py --json list
```

Run `python3 scripts/google-calendar-cli.py -h` for full help.

## License

MIT
