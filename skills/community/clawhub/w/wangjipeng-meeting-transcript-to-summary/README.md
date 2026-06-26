# Meeting Transcript To Summary

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> user pastes meeting transcript and needs structured summary with action items and decision owners

## What Problem This Solves

Brief paragraph explaining the specific engineering problem this skill solves.
When triggered: [trigger condition].

## Features

- Transforms meeting transcript to summary input into structured output
- Handles user pastes meeting transcript and needs structured summa...
- Preserves data integrity — no silent drops or fabrication

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install Meeting Transcript To Summary

# Or manually
cp -r Meeting Transcript To Summary ~/.openclaw/skills/
```

### Usage

```bash
# Mode 1
clawhub run Meeting Transcript To Summary --mode read

# Mode 2
clawhub run Meeting Transcript To Summary --mode write --input ./data.json
```

## Directory Structure

```
Meeting Transcript To Summary/
├── SKILL.md          # Entry point
├── LICENSE           # MIT
├── README.md         # This file
├── README_zh.md      # Chinese version
├── CONTRIBUTING.md    # Contribution guide
├── .gitignore
├── references/       # Templates and schemas
│   └── ...
└── scripts/          # Helper scripts (if any)
    └── ...
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | API key for the service |

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

Powered by [MiniMax](https://minimax.io).