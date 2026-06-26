---
name: readai
description: >
  Fetch and manage Read AI meeting data - summaries, transcripts, action items, and engagement metrics.
  Use when the user asks about meetings, meeting notes, meeting summaries, action items from meetings,
  who said what in a meeting, meeting transcripts, Read AI data, or wants to set up Read AI webhooks.
  Also use for searching past meetings, generating meeting digests, or pulling meeting analytics.
---

# Read AI Integration

Pull meeting intelligence from Read AI via REST API or webhook receiver.

## Auth

Two data sources supported:

1. **Limitless Pendant** (primary) - Captures all conversations including meetings via API
2. **Read AI Webhook** - Real-time meeting summaries pushed from Read AI

API key stored at `~/.config/readai/api-key` (same as Limitless key if using pendant).

```bash
# One-time setup
mkdir -p ~/.config/readai
echo "YOUR_API_KEY" > ~/.config/readai/api-key
chmod 600 ~/.config/readai/api-key
```

For Limitless: Get key from limitless.ai dashboard.
For Read AI API: Get key from Read AI Dashboard > Settings > Integrations > API Keys.

## Quick Commands

### List Recent Meetings
```bash
python3 scripts/list_meetings.py              # Last 7 days
python3 scripts/list_meetings.py --days 30    # Last 30 days
python3 scripts/list_meetings.py --today      # Today only
python3 scripts/list_meetings.py --json       # JSON output
```

### Get Meeting Details
```bash
python3 scripts/readai_client.py get <meeting_id>
python3 scripts/readai_client.py get <meeting_id> --transcript   # Full transcript
python3 scripts/readai_client.py get <meeting_id> --actions      # Action items only
```

### Search Meetings
```bash
python3 scripts/search_meetings.py "quarterly review"
python3 scripts/search_meetings.py "budget" --days 30
python3 scripts/search_meetings.py "action items" --speaker "Brandon"
```

### Export Meeting Summary
```bash
python3 scripts/readai_client.py export <meeting_id>             # Markdown
python3 scripts/readai_client.py export <meeting_id> --format json
```

## Webhook Setup

For real-time meeting data, set up the webhook receiver:

1. Run: `python3 scripts/webhook_receiver.py --port 9010`
2. In Read AI Dashboard > Settings > Integrations > Webhooks
3. Add URL: `http://<your-server>:9010/webhook/readai`

Webhook data is stored in `~/.readai/meetings/YYYY-MM-DD/`.

See `references/api-reference.md` for full API documentation.

## Data Structure

Meetings include:
- **Summary** - AI-generated meeting recap
- **Transcript** - Full speaker-attributed transcript
- **Action Items** - Tasks with assignees
- **Topics** - Key discussion topics
- **Participants** - Attendees with engagement metrics
- **Decisions** - Key decisions made
- **Duration/Timing** - Start, end, duration

## Local Data

Data is stored/symlinked at `~/.readai/`:
```
~/.readai/
├── meetings/                # Webhook-received meetings
│   └── YYYY-MM-DD/
│       ├── <timestamp>_<title>.json
│       └── <timestamp>_<title>.md
├── lifelogs/                # Limitless pendant data (symlink)
│   └── YYYY-MM-DD/
│       ├── raw_lifelogs.json
│       ├── entries.json
│       └── digest.md
└── index.json               # Meeting index for search
```

## Limitless Lifelog Pull

```bash
# Pull today's pendant data (includes meetings)
python3 scripts/limitless_pull.py --today

# Pull specific date
python3 scripts/limitless_pull.py 2026-02-19

# Pull with AI summary
python3 scripts/limitless_pull.py --today --ai
```
