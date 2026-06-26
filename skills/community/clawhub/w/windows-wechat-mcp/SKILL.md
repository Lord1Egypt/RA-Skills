---
name: windows-wechat-mcp
description: Windows WeChat message monitoring and sending. Achieved through window automation: screenshot, search contacts, send messages. Use when needing to send messages to WeChat contacts, check WeChat window status, or perform WeChat-related automation tasks.
---

# Windows WeChat MCP

Windows desktop WeChat message monitoring and sending, achieved through window automation.

## Prerequisites

1. The WeChat window must remain open
2. Python dependencies installed:
   ```bash
   pip install pyautogui pygetwindow pillow pyperclip opencv-python
   ```

## Features

| Feature | Description |
|---------|-------------|
| Screenshot | Capture a screenshot of the WeChat window |
| Search Contacts | Search for and open a contact's chat window |
| Send Messages | Send messages to a specified contact |
| Detached Windows | Support identification of detached chat windows (Dragon windows) |

## Usage

### 1. Send a Message to a Specified Contact

```python
from scripts.server import send_message_to_contact

# Complete flow: Search -> Open chat -> Send
send_message_to_contact("Contact Name", "Message content")
```

### 2. Send a Message to the Current Chat Window

```python
from scripts.server import send_message_to_current

send_message_to_current("Message content")
```

### 3. Get WeChat Status

```python
from scripts.server import get_wechat_status

status = get_wechat_status()
# Returns: {'status': 'running', 'title': 'WeChat', 'position': {'x': 0, 'y': 0}, 'size': {'width': 1920, 'height': 1080}}
```

## MCP Tools

When called via the MCP protocol, the following tools are provided:

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `wechat_get_status` | Get the WeChat window status | None |
| `wechat_send_message` | Send a message to the current chat window | `message`: Message content |

## Notes

1. The WeChat window is automatically activated when sending messages
2. Chinese input requires the system's Chinese input method to function properly
3. Supports sending messages to detached chat windows (separately opened Dragon windows)