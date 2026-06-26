---
name: wechat-send
description: "Automate sending text messages and images/files in the macOS WeChat desktop app by controlling the UI via AppleScript and JXA. This is NOT a WeChat chat channel for OpenClaw — it controls the WeChat GUI on your Mac to send messages on your behalf. Use when: (1) user asks to send a WeChat message to someone, (2) notifying a WeChat contact, (3) batch messaging multiple contacts. Requires: WeChat for Mac installed, logged in, and window visible. macOS Accessibility permission granted to node. NOT for: reading or receiving WeChat messages, group chat management (beyond sending), or using WeChat as a conversation channel with OpenClaw."
metadata: {"openclaw": {"os": ["darwin"], "author": "ryan_dream", "email": "ryanyang5@gmail.com"}}
---

# WeChat Send

Send messages to WeChat contacts by automating the macOS WeChat desktop app.

## Prerequisites

- WeChat for Mac installed and **logged in**
- macOS **Accessibility permission** granted to `node` (System Settings → Privacy & Security → Accessibility)
- WeChat window must be **open** (not minimized to dock)

## Usage

Run the scripts:

```bash
# Send text
bash scripts/wechat_send.sh "<contact_name>" "<message>"

# Send an image (or any file attachable by WeChat)
bash scripts/wechat_send_image.sh "<contact_name>" "/path/to/image.png"
```

### Examples

```bash
# Send a simple message
bash scripts/wechat_send.sh "Ryan" "你好！"

# Send a longer message
bash scripts/wechat_send.sh "Ellison" "明天下午3点开会，别忘了带文件"

# Send a screenshot
bash scripts/wechat_send_image.sh "Family" "/Users/you/Desktop/screen.png"
```

## How It Works

1. Activates WeChat and opens search (Cmd+F)
2. Types the contact name, selects the first result (Enter), closes search (Escape)
3. Clicks the message input field using JXA CGEvent mouse simulation
4. Pastes the message from clipboard (Cmd+V) and sends (Enter)

## Limitations

- Contact name must **exactly match** a WeChat contact (first search result is selected)
- Image/file sending depends on WeChat accepting paste-from-clipboard as an attachment (works for common formats like PNG/JPG)
- Cannot read incoming messages
- WeChat window position affects click coordinates (auto-calculated from window bounds)
- If the contact search returns wrong results, the message goes to the wrong person — use specific names
- Only one message at a time; for multiple recipients, call the script multiple times

## Troubleshooting

- **Message not sent**: Ensure WeChat window is visible (not minimized) and the correct contact was found
- **Accessibility error**: Re-grant node permission in System Settings → Accessibility, then restart the gateway
- **Wrong contact**: Use a more specific name to avoid ambiguous search results
