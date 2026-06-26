---
name: bluebubbles
description: Send and manage iMessages via BlueBubbles self-hosted macOS server
author: BlueBubbles
author-url: https://bluebubbles.app
version: 1.0.0
tags: ["imessage", "messaging", "communication"]
metadata: {
  "requires": {
    "config": ["channels.bluebubbles.server_url", "channels.bluebubbles.password"],
    "env": []
  }
}
---

# BlueBubbles iMessage Skill

## Overview
Use this skill to send and manage iMessage conversations through a self-hosted BlueBubbles server. Supports text messages, attachments, reactions, edits, unsend, and iMessage effects.

## Configuration
Add this to your gateway config:
```toml
[channels.bluebubbles]
server_url = "http://192.168.1.100:1234"  # Your BlueBubbles server URL
password = "your-server-password"
allowed_senders = ["*"]  # Allow all senders, or list specific handles
```

## Usage Examples

### Send a text message
```json
{
  "tool": "bluebubbles_send",
  "parameters": {
    "target": "+15551234567",
    "message": "Hello from your AI assistant!"
  }
}
```

### Send a message with iMessage effect
```json
{
  "tool": "bluebubbles_send",
  "parameters": {
    "target": "+15551234567",
    "message": "Congratulations! 🎉",
    "effect": "confetti"
  }
}
```

### Send an attachment
```json
{
  "tool": "bluebubbles_send_attachment",
  "parameters": {
    "target": "+15551234567",
    "file_path": "/workspace/output/report.pdf",
    "caption": "Here's the report you requested"
  }
}
```

### React to a message
```json
{
  "tool": "bluebubbles_react",
  "parameters": {
    "target": "+15551234567",
    "message_id": "msg_12345",
    "emoji": "👍"
  }
}
```

## Supported Effects
- slam, loud, gentle, invisible-ink
- balloons, confetti, lasers, fireworks, shooting-star
- celebration, echo, spotlight, love
