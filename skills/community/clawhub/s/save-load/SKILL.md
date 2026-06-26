---
name: save-load
description: Save and load OpenClaw conversation context with /save and /load slash commands
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw"] },
      },
  }
---

# Save/Load Context Plugin

An OpenClaw plugin that adds `/save` and `/load` slash commands for persisting and restoring conversation context across sessions.

## Problem

OpenClaw conversations are ephemeral — when you start a new session or reset, all context is lost. This plugin lets you save any conversation to disk and reload it later, preserving full context continuity.

## Commands

| Command | Description |
|---------|-------------|
| `/save [label]` | Save the current conversation context with an optional label. If no label is provided, the save is named "unnamed". |
| `/load` | List all previously saved conversation contexts with their labels, message counts, and save dates. |
| `/load <name>` | Load a saved context by label or index number. This replaces the current session transcript with the saved conversation. After loading, the agent receives a system event with the save file path so it can restore full context. |
| `/load --delete <name>` | Permanently delete a saved context file. |

## How It Works

### Saving
1. When `/save` is invoked, the plugin reads the session transcript (JSONL format)
2. It identifies the conversation boundary — messages since the last `/new`, `/reset`, or `/load`
3. Only `user` and `assistant` messages are extracted (tool calls and results are excluded)
4. The messages are written to `~/.openclaw/saves/<timestamp>_<label>.json`
5. An index file (`index.json`) is updated for fast listing

### Loading
1. `/load <name>` finds the save file by label or index
2. The saved messages are written as a new session transcript
3. A system event is injected via `enqueueSystemEvent()` containing the save file path and message count
4. The agent receives this event and can use the `read` tool to load the full context from the save file

### Save File Format

```json
{
  "version": 1,
  "label": "project-discussion",
  "savedAt": "2026-03-30T15:38:00+08:00",
  "messageCount": 42,
  "sourceSession": "telegram:2074807638",
  "messages": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." }
  ]
}
```

## Installation

### Via OpenClaw Plugin Manager
```bash
openclaw plugins install save-load
```

### Manual Installation
1. Copy the plugin directory to `~/.openclaw/extensions/save-load/`
2. Ensure `openclaw.plugin.json` and `package.json` are present
3. Add `"save-load"` to the `plugins.enabled` array in `~/.openclaw/openclaw.json`
4. Restart the OpenClaw gateway: `openclaw gateway restart`

## Storage

Save files are stored in `~/.openclaw/saves/`. There is no limit on the number or size of saves — only disk space applies.

## Requirements

- OpenClaw 2026.3.30 or later
- Node.js (included with OpenClaw)

## Source Code

https://github.com/jkyotnfjfbjnknh/openclaw-save-load
