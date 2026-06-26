---
name: zalo-multi-send
description: Send multiple images or files in a single Zalo message using zca-js directly. Use when the user asks to send multiple photos/files to a Zalo contact or group at once, or when openclaw's built-in single-media send is not enough. Supports local file paths and URLs. Requires Zalo credentials already set up via openclaw zalouser channel.
---

# zalo-multi-send

Send multiple attachments in one Zalo message via `scripts/send.mjs`.

## Usage

```bash
node <skill-dir>/scripts/send.mjs \
  --to <userId_or_groupId> \
  --files "<path_or_url_1>,<path_or_url_2>,..." \
  [--caption "optional text"] \
  [--group] \
  [--profile default]
```

## Parameters

| Flag | Required | Description |
|---|---|---|
| `--to` | ✅ | Zalo user ID or group ID (numeric string) |
| `--files` | ✅ | Comma-separated local paths or https:// URLs |
| `--caption` | ❌ | Text message to send alongside the files |
| `--group` | ❌ | Add this flag if `--to` is a group ID |
| `--profile` | ❌ | Credential profile name (default: `"default"`) |

## Examples

```bash
# Send 2 local screenshots to a user
node scripts/send.mjs \
  --to 3484584962870495768 \
  --files "/home/tuan/Pictures/Screenshots/shot1.png,/home/tuan/Pictures/Screenshots/shot2.png"

# Send images from URLs with a caption
node scripts/send.mjs \
  --to 3484584962870495768 \
  --files "https://files.catbox.moe/abc.png,https://files.catbox.moe/def.png" \
  --caption "Đây nhé!"

# Send to a group
node scripts/send.mjs \
  --to 1234567890 \
  --group \
  --files "photo1.jpg,photo2.jpg"
```

## Notes

- Credentials are read from `~/.openclaw/credentials/zalouser/credentials.json` (managed by openclaw, no re-auth needed)
- ZCA_PATH is hardcoded to the openclaw-bundled zca-js. If openclaw is updated/reinstalled, the path may need updating in `scripts/send.mjs`
- Local files must be readable by the current user
- Zalo may have undocumented limits on number of attachments per message (tested up to ~10 without issues)
- Exit 0 = success, exit 1 = error
