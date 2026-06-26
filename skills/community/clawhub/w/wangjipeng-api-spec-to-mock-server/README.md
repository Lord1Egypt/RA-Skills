# Api Spec To Mock Server

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> user provides API spec in OpenAPI or Swagger format and needs a runnable mock server

## What Problem This Solves

Brief paragraph explaining the specific engineering problem this skill solves.
When triggered: [trigger condition].

## Features

- Transforms api spec to mock server input into structured output
- Handles user provides api spec in openapi or swagger format and n...
- Preserves data integrity — no silent drops or fabrication

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install Api Spec To Mock Server

# Or manually
cp -r Api Spec To Mock Server ~/.openclaw/skills/
```

### Usage

```bash
# Mode 1
clawhub run Api Spec To Mock Server --mode read

# Mode 2
clawhub run Api Spec To Mock Server --mode write --input ./data.json
```

## Directory Structure

```
Api Spec To Mock Server/
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