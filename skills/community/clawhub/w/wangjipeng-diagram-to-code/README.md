# Diagram To Code

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> user provides architecture diagram and needs infrastructure as code or component code

## What Problem This Solves

Brief paragraph explaining the specific engineering problem this skill solves.
When triggered: [trigger condition].

## Features

- Transforms diagram to code input into structured output
- Handles user provides architecture diagram and needs infrastructu...
- Preserves data integrity — no silent drops or fabrication

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install Diagram To Code

# Or manually
cp -r Diagram To Code ~/.openclaw/skills/
```

### Usage

```bash
# Mode 1
clawhub run Diagram To Code --mode read

# Mode 2
clawhub run Diagram To Code --mode write --input ./data.json
```

## Directory Structure

```
Diagram To Code/
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