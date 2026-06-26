# Sessions Manager

A small CLI utility for inspecting and deleting OpenClaw agent sessions.

## Overview

`sessions_cli.py` reads session metadata from `~/.openclaw/agents/main/sessions/sessions.json` and optionally removes corresponding session history files from `~/.openclaw/agents/main/sessions/`.

This tool is useful for:
- Listing active or completed OpenClaw sessions
- Viewing session metadata such as status, model, label, and duration
- Cleaning up stale or unwanted session history

## Requirements

- Python 3
- Access to the OpenClaw session storage directory under `~/.openclaw`

## Usage

From the repository root:

```bash
python3 scripts/sessions_cli.py list
```

Verbose listing:

```bash
python3 scripts/sessions_cli.py list -v
```

Delete a session by its ID or session key:

```bash
python3 scripts/sessions_cli.py delete <session-id-or-key>
```

Example:

```bash
python3 scripts/sessions_cli.py delete agent:main:subagent:5adb35d1-d8e3-4ab7-b9b9-c69a7f891fb3
```

## Commands

- `list`: Show all sessions stored in `sessions.json`
- `delete`: Remove the specified session from `sessions.json` and delete its `.jsonl` history file if it exists

## Storage Paths

- Metadata file: `~/.openclaw/agents/main/sessions/sessions.json`
- Session history files: `~/.openclaw/agents/main/sessions/<session-id>.jsonl`

## Notes

- If `sessions.json` does not exist, the tool reports no sessions found.
- Deleting a session removes only the matching entry and the corresponding history file, not any other OpenClaw data.
