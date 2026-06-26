---
name: telegram-send-file
description: Send local files and documents to a Telegram user via bot. Use when user asks to "send", "发", "发给我", "发送" a file, note, or document via Telegram. Handles files from iCloud Drive paths or local paths. Handles files up to 50MB (auto-zips if over limit). Triggers on: "发送文件", "发笔记", "send me", "send file", "发给我这个文件", "把xxx发过来", "send document".
metadata:
  homepage: https://clawhub.ai/skills/telegram-file-sender
---

# Telegram File Sender

Send files to a Telegram user via bot, handling workspace path restrictions and Telegram's 50MB file size limit.

## What This Skill Does

This skill enables an AI agent to send files from the local filesystem (including iCloud Drive paths) to a Telegram user through a bot account. It handles:

- **Path resolution**: Accepts iCloud paths and local absolute paths
- **Size limits**: Telegram caps documents at 50MB; this skill auto-compresses files over that limit
- **Workspace isolation**: Files outside allowed directories are copied to a temporary location before sending
- **Multiple bots**: Supports any bot accountId configured in OpenClaw

## When to Use This Skill

- User asks to "send me the file" or "发给我"
- User wants a note or document forwarded to Telegram
- User requests a specific file be delivered via the bot
- Any request that involves transferring a file from the agent's filesystem to Telegram

## Prerequisites

The agent must have:
1. A configured Telegram bot account in OpenClaw
2. The target user's Telegram chat ID
3. The file path (or enough info to locate the file)

If any of these are missing, ask the user before proceeding.

## Core Workflow

### Step 1: Identify the File

If the user didn't specify a path, ask them.  
Accepted formats:
- Any absolute path: `/Users/you/Documents/file.any`
- Path with `~` expansion: `~/path/to/file`
- Relative path from workspace root
- Any file extension (`.md`, `.txt`, `.pdf`, `.zip`, images, etc.)

### Step 2: Run the Helper Script

```bash
python3 skills/telegram-send-file/scripts/send_file.py "<source_path>" "<target_user_id>" [caption] [accountId]
```

Arguments:
| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| `source_path` | Yes | — | Absolute path to the file |
| `target_user_id` | Yes | — | Telegram chat ID (e.g. `123456789`) |
| `caption` | No | `""` | Text caption shown before the file |
| `accountId` | No | (first bot) | Bot accountId configured in OpenClaw |

### Step 3: Parse Script Output

The script outputs key-value lines on stdout:

```
SEND_PATH=/tmp/xyz/file.md
SEND_FILENAME=file.md
TARGET=123456789
CAPTION=📄 My Document
ACCOUNT_ID=your_bot_account
READY
```

Extract `SEND_PATH`, `TARGET`, `ACCOUNT_ID` from the output.

### Step 4: Send via Message Tool

```json
{
  "action": "send",
  "channel": "telegram",
  "target": "<TARGET from output>",
  "accountId": "<ACCOUNT_ID from output>",
  "filePath": "<SEND_PATH from output>",
  "asDocument": true
}
```

Use `filePath` (absolute path), not `path` or relative paths.

### Step 5: Clean Up Temp Files

After message tool returns `ok: true`, delete the temp file:

```bash
rm <SEND_PATH>
rm -rf <parent_tmp_dir>
```

## Size Handling Rules

| File size | Behavior |
|-----------|----------|
| ≤ 50MB | Copied to tmp, sent as-is |
| > 50MB | Auto-zipped; sent if result ≤ 50MB |
| > 50MB after zip | Prints `FAIL` + suggestion; does not send |

The suggestion will be either:
- "Split the file into smaller parts"
- "Send a summary + external link"

## Common Usage Patterns

### Send Any File Type

```bash
python3 skills/telegram-send-file/scripts/send_file.py \
  "/Users/you/Documents/report.pdf" \
  "123456789" \
  "📄 Report" \
  "your_bot_account"
```

Works with any extension: `.md`, `.txt`, `.pdf`, `.zip`, `.png`, `.jpg`, `.json`, etc.

### Send a Large File (Auto-zipped)

If a file exceeds 50MB, the script auto-zips it. If the zip is ≤ 50MB, it sends the zip automatically.

### Send from a Different Bot

```bash
python3 skills/telegram-send-file/scripts/send_file.py \
  "/Users/you/path/to/file.png" \
  "123456789" \
  "🖼 Image" \
  "another_bot_account"
```

## Edge Cases

### File Not Found
The script exits with `FAIL: Source file not found`. Ask the user to verify the path.

### Permission Denied
If the file exists but cannot be read, the script will fail. Check file permissions.

### Empty File
Allowed. The script sends it normally.

### Binary File
Allowed. The script handles any file type, not just text.

### Very Long Filename
Telegram handles filenames up to 255 chars. The script preserves the original basename.

## Security Notes

- Files are only copied to tmp and deleted after sending
- No external command execution (uses Python's built-in `zipfile` module only)
- Only OpenClaw's Telegram bot credentials are used (configured server-side)
- The script does not log or persist file contents

## Debugging

If sending fails:

1. **Check file size**: `ls -lh <path>`
2. **Verify path exists**: `ls <path>`
3. **Test temp copy manually**: `cp <path> /tmp/`
4. **Check bot config**: Confirm `accountId` is correct in OpenClaw config
5. **Check user ID**: Confirm the target chat ID is correct

## Relationship to OpenClaw Message Tool

This skill wraps the `message` tool's `send` action with file-document support. The workflow is:

1. Helper script prepares the file and resolves path/size
2. Agent calls `message` tool with the prepared absolute path
3. OpenClaw handles the Telegram API call

The skill exists because:
- OpenClaw requires absolute paths for file sending
- Files may need to be copied from iCloud to a reachable location
- Size limits require compression as a pre-processing step
