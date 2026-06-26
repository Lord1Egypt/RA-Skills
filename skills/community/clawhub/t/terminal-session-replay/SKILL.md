---
name: terminal-session-replay
description: Record and replay terminal sessions for debugging, documentation, or sharing procedures with teammates.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - script
---

# Terminal Session Replay

## What This Does

A CLI tool to record, replay, and export terminal sessions. Captures commands, outputs, and timing for later review, documentation, or sharing with teammates. Wraps the standard `script` command with a simpler interface and additional features.

Key features:
- **Record sessions** - Start recording terminal session with a simple command
- **Replay sessions** - Play back recorded sessions with original timing
- **Export to markdown** - Convert sessions to readable documentation
- **Session management** - List, view, and delete recorded sessions
- **Metadata support** - Add titles, descriptions, and tags to sessions
- **Timing control** - Adjust playback speed or skip timing for quick review

## How To Use

### Record a session:
```bash
./scripts/main.py record --output session1
```

### Replay a session:
```bash
./scripts/main.py replay --input session1
```

### Export to markdown:
```bash
./scripts/main.py export --input session1 --output session1.md
```

### List recorded sessions:
```bash
./scripts/main.py list
```

### Full command reference:
```bash
./scripts/main.py help
```

## Commands

- `record`: Start recording a terminal session
  - `--output`: Session name (default: timestamp-based)
  - `--title`: Session title for metadata
  - `--desc`: Session description
  - `--tags`: Comma-separated tags
  
- `replay`: Replay a recorded session
  - `--input`: Session name to replay
  - `--speed`: Playback speed multiplier (default: 1.0)
  - `--no-timing`: Skip timing, display immediately
  
- `export`: Export session to markdown
  - `--input`: Session name to export
  - `--output`: Output markdown file (default: session_name.md)
  - `--include-timing`: Include timing information in export
  
- `list`: List all recorded sessions
  - `--filter-tags`: Filter by tags
  
- `info`: Show session metadata
  - `--input`: Session name
  
- `delete`: Delete a session
  - `--input`: Session name to delete

## Output

Sessions are stored in `~/.terminal-sessions/` by default:
- `session_name.typescript`: Raw terminal recording (script output)
- `session_name.timing`: Timing data for replay
- `session_name.meta.json`: Metadata (title, description, tags, timestamp)

Export produces markdown like:
```markdown
# Terminal Session: Setting up Project

**Recorded:** 2026-03-11 10:30:00  
**Duration:** 2 minutes 15 seconds

```bash
$ git clone https://github.com/example/project
Cloning into 'project'...
remote: Enumerating objects: 100, done.
remote: Counting objects: 100% (100/100), done.
remote: Compressing objects: 100% (80/80), done.
remote: Total 100 (delta 20), reused 80 (delta 15), pack-reused 0
Receiving objects: 100% (100/100), 1.5 MiB | 3.5 MiB/s, done.
Resolving deltas: 100% (20/20), done.

$ cd project
$ npm install
...
```

## Limitations

- Requires `script` command (available on Linux/macOS, not on Windows without WSL/Cygwin)
- Cannot record GUI applications or mouse interactions
- Very fast terminal output may not be captured perfectly
- Sessions can be large if recording for long periods
- Color and formatting may not be preserved in markdown export
- Requires terminal with proper support for script command

## Examples

Record a debugging session:
```bash
./scripts/main.py record --output debug-session --title "Debugging API issue" --tags "debug,api"
# ... work in terminal ...
exit  # or Ctrl+D to end recording
```

Replay at 2x speed:
```bash
./scripts/main.py replay --input debug-session --speed 2.0
```

Export for documentation:
```bash
./scripts/main.py export --input debug-session --output DEBUGGING.md
```

## Installation Notes

The `script` command is typically pre-installed on Linux and macOS systems. On Windows, use WSL or Cygwin.

The tool creates `~/.terminal-sessions/` directory to store recordings.