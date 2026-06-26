---
name: brave-search-custom
description: "A custom tool for web searching using Brave Search API."
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": { "bins": ["python3"] }
    }
  }
---

# Brave Search Custom Skill

A lightweight skill for searching the web with the Brave Search API.

## Installation

1. Create a folder named `brave-search-custom` in your OpenClaw `skills/` directory.
2. Put `brave_search.py` and `SKILL.md` inside it.
3. Make sure `brave_search.py` is executable: `chmod +x brave_search.py`.

## Configuration

Set your Brave Search API key as an environment variable:

```bash
export BRAVE_API_KEY="your_brave_api_key_here"
```

## Usage

Ask your OpenClaw agent to search for anything, and it will use this script to fetch real-time data from the web.
