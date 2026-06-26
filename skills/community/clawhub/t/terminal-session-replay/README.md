# Terminal Session Replay

A CLI tool to record, replay, and export terminal sessions for debugging, documentation, and sharing.

## Quick Start

```bash
# Record a session
./scripts/main.py record --output my-session

# Replay it
./scripts/main.py replay --input my-session

# Export to markdown
./scripts/main.py export --input my-session --output SESSION.md
```

## Features

- **Easy recording** - Simple command to start/stop recording
- **Accurate replay** - Play back with original timing
- **Documentation export** - Convert sessions to markdown
- **Session management** - List, view, delete recordings
- **Metadata** - Add titles, descriptions, tags

## Installation

This skill is installed via OpenClaw. Requires `script` command (available on Linux/macOS).

## Usage

### Recording
```bash
./scripts/main.py record --output session-name --title "Session Title"
```
Press Ctrl+D or type `exit` to stop recording.

### Replaying
```bash
./scripts/main.py replay --input session-name --speed 1.5
```
Use `--speed` to adjust playback speed.

### Exporting
```bash
./scripts/main.py export --input session-name --output documentation.md
```

### Listing Sessions
```bash
./scripts/main.py list
```

## Storage

Sessions are stored in `~/.terminal-sessions/`:
- `.typescript` - Terminal recording
- `.timing` - Timing data  
- `.meta.json` - Metadata

## Requirements

- Python 3.6+
- `script` command (usually pre-installed)
- Linux/macOS (Windows requires WSL/Cygwin)

## License

MIT