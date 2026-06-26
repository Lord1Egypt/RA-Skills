# OpenClaw Session File Format

## Overview

OpenClaw stores session data in JSONL (JSON Lines) format. Each line is a valid JSON object representing a single event in the session.

## File Location

```
~/.claude/projects/<project-name>/<session-uuid>.jsonl
```

## Entry Types

### 1. Message Entry

The most common type, representing a conversation message.

```json
{
  "type": "message",
  "message": {
    "id": "chatcmpl-xxx",
    "type": "message",
    "role": "assistant",  // or "user"
    "content": [
      {
        "type": "text",
        "text": "Hello!"
      },
      {
        "type": "thinking",
        "thinking": "Internal thought process"
      }
    ],
    "model": "claude-sonnet-4-6",
    "provider": "anthropic",
    "usage": {
      "input_tokens": 1000,
      "output_tokens": 500,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 200,
      "prompt_tokens": 1000,
      "completion_tokens": 500
    },
    "stop_reason": "end_turn",
    "durationMs": 2500
  },
  "timestamp": "2026-03-16T07:12:47.060Z",
  "uuid": "xxx"
}
```

### 2. Progress Entry

Represents a hook or progress event.

```json
{
  "type": "progress",
  "data": {
    "type": "hook_progress",
    "hookEvent": "SessionStart",
    "hookName": "SessionStart:clear",
    "command": "..."
  },
  "timestamp": "2026-03-16T07:12:47.060Z"
}
```

### 3. File History Snapshot

Snapshot of file state.

```json
{
  "type": "file-history-snapshot",
  "messageId": "xxx",
  "snapshot": {...}
}
```

## Usage Fields

| Field | Description |
|-------|-------------|
| `input_tokens` | Tokens in the input/prompt |
| `output_tokens` | Tokens in the output/completion |
| `cache_creation_input_tokens` | Tokens written to cache |
| `cache_read_input_tokens` | Tokens read from cache |
| `prompt_tokens` | Alias for input_tokens |
| `completion_tokens` | Alias for output_tokens |
| `total` | Total tokens (if available) |

## Tool Calls

Tool calls appear in assistant messages:

```json
{
  "message": {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "toolu_xxx",
        "type": "tool_use",
        "name": "Read",
        "input": {"file_path": "/path/to/file"}
      }
    ]
  }
}
```

## Cost Calculation

Costs are estimated using these rates per 1K tokens:

- Input: $0.003
- Output: $0.015
- Cache Read: $0.0003
- Cache Write: $0.00375

Note: These are approximate rates and may vary by model and provider.
