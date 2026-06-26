---
name: spotify-control
description: macOS Spotify control skill for OpenClaw. Supports playback, volume, position, and metadata retrieval via AppleScript.
version: 1.0.1
author: Antigravity
platform: macOS
---

# Spotify Control (macOS)

## Overview

Control Spotify on macOS using AppleScript. This skill provides a set of commands to manage playback, volume, and track information.

## Actions

### Playback Control

- **Play/Pause**: Toggle playback.
- **Next/Previous**: Jump to next or previous track.
- **Stop**: Pause playback.

### Volume & Position

- **Set Volume (0-100)**: Adjust Spotify internal volume.
- **Set Position (seconds)**: Jump to a specific time in the current track.

### Metadata & State

- **Get Info**: Retrieve current track name, artist, album, and Spotify URL.
- **Set Shuffle (on/off)**: Toggle shuffle mode.
- **Set Repeat (on/off)**: Toggle repeat mode.

## Usage

Agents should use the `scripts/spotify-control.py` wrapper for all commands.

### Examples

```sh
# Toggle play/pause
scripts/spotify-control.py playpause

# Get current track info
scripts/spotify-control.py get-info

# Set volume to 80%
scripts/spotify-control.py set-volume 80

# Seek to 1 minute (60s)
scripts/spotify-control.py set-position 60
```

## Guardrails

- Ensure Spotify is installed and running.
- All commands are one-shot AppleScript executions via a Python wrapper.
- Does not affect system-wide volume unless specified for fallback.
