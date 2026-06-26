# sleep-channel

A deterministic sleep-tracking skill for OpenClaw, designed for Discord channel-based logging.

Logs sleep events (bed, sleep, awake, up, rest) with source Discord metadata, rendering summaries from the real data file — never from conversational memory.

## Install

```bash
openclaw skill install sleep-channel
```

Or copy this directory into your workspace's `skills/` folder.

## Setup

1. Create a dedicated Discord channel for sleep tracking.
2. Set environment variables:

```bash
export SLEEP_TIMEZONE="America/Los_Angeles"  # your IANA timezone
export WORKSPACE="$HOME/.openclaw/workspace"  # optional, has default
```

3. Point your OpenClaw agent config to use this skill for the sleep channel.

## How It Works

- Users send natural language messages in the sleep channel (e.g. "going to bed", "awake now")
- The agent calls `scripts/tracker.py` with the raw message text and Discord metadata
- The tracker parses the event, logs it to CSV, and returns a confirmation
- No hallucinated timestamps — everything is grounded on source message metadata

## Tracker Commands

| Command | Description |
|---------|-------------|
| `add <text> <channel> <msg_id> <author> <ts>` | Log a new sleep event |
| `correct-latest <text> <channel> <msg_id> <author> <ts>` | Replace the latest entry |
| `delete-latest` | Remove the latest entry |
| `render` | Display the current sleep log |

## Requirements

- Python 3.10+ (uses `zoneinfo`, `dataclasses`)
- No external dependencies — stdlib only

## Data Files

Created at runtime under `$WORKSPACE/`:

- `data/sleep_log.csv` — all sleep events
- `state/sleep_summary_state.json` — summary computation state

## License

MIT
