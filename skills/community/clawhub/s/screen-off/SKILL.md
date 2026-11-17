---
name: screen-off
description: "Toggle any macOS display on/off by ID, name, or index."
version: 1.0.0
author: mfang0126
license: MIT
metadata:
  hermes:
    tags: [macos, display, screen, toggle, cli, hardware]
  platforms: [macos]
---

# screen-off

macOS display toggle CLI — turn any screen on/off by ID, name, or index. Zero dependencies, Python 3.8+.

Based on [zy0816/ScreenOff](https://github.com/zy0816/ScreenOff) (MIT). Uses CoreGraphics/SkyLight private API.

## When to Use

- You have external monitors and want to turn off a specific screen
- Multi-display setup management
- Quick screen toggle from terminal/agent

## Quick Start

```bash
git clone https://github.com/mfang0126/screen-off.git
alias screen-off='python3 /path/to/screen-off/screen-off.py'
```

## Usage

```bash
screen-off --status          # List all displays
screen-off --off 3           # Turn off by ID (stable)
screen-off --on 3            # Turn on by ID
screen-off --off #2          # Turn off by index (changes)
screen-off --off main        # Turn off main display
screen-off --off "S2700"     # Fuzzy match by name
screen-off --off 3 --force   # Force (even if only screen)
screen-off --off 3 --permanent  # Survive reboot
```

## Requirements

- macOS (SkyLight/CoreGraphics framework)
- Python 3.8+ (system built-in)
