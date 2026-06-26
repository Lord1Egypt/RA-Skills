---
name: gifgrep
description: Search, preview, download, and process GIFs from Tenor and Giphy
author: steipete
author-url: https://github.com/steipete/gifgrep
version: 1.0.0
tags: ["gif", "media", "search", "images"]
metadata: {
  "requires": {
    "bins": ["gifgrep"],
    "env": ["GIPHY_API_KEY", "TENOR_API_KEY"]
  },
  "install": [
    {
      "type": "homebrew",
      "package": "steipete/tap/gifgrep",
      "label": "Install GifGrep CLI (Homebrew)"
    },
    {
      "type": "go",
      "package": "github.com/steipete/gifgrep/cmd/gifgrep@latest",
      "label": "Install GifGrep CLI (Go)"
    }
  ]
}
---

# GifGrep GIF Search Skill

## Overview
Search, preview, download, and process GIFs from Tenor and Giphy providers. Supports CLI output, interactive TUI with previews, static frame extraction, and frame sheet generation.

## Configuration
| Environment Variable | Description |
|----------------------|-------------|
| `GIPHY_API_KEY` | Optional for Giphy provider (uses demo key if not set) |
| `TENOR_API_KEY` | Optional for Tenor provider (uses demo key if not set) |

## Usage Examples

### Search for GIFs
```json
{
  "tool": "gifgrep_search",
  "parameters": {
    "query": "excited reaction",
    "limit": 5,
    "format": "url"
  }
}
```

### Search and download top GIF
```json
{
  "tool": "gifgrep_search",
  "parameters": {
    "query": "happy birthday",
    "limit": 1,
    "download": true,
    "output_path": "/workspace/downloads/birthday.gif"
  }
}
```

### Extract static frame from GIF
```json
{
  "tool": "gifgrep_extract_frame",
  "parameters": {
    "input_path": "/workspace/downloads/birthday.gif",
    "time": "1.5s",
    "output_path": "/workspace/output/frame.png"
  }
}
```

### Generate frame sheet
```json
{
  "tool": "gifgrep_generate_sheet",
  "parameters": {
    "input_path": "/workspace/downloads/birthday.gif",
    "frames": 9,
    "columns": 3,
    "output_path": "/workspace/output/sheet.png"
  }
}
```

## Supported Providers
- `auto` (default): Uses Giphy if API key is set, otherwise Tenor
- `tenor`: Tenor GIF provider
- `giphy`: Giphy GIF provider (requires API key for higher rate limits)
