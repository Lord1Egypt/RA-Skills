---
name: qywx-notify
description: A skill for sending notifications via WeChat Work.
---

# WeCom Notification Skill

## Overview
Send notifications to group chats via WeCom robot Webhook, supporting text, images (Markdown format), and Markdown rich text.

## Quick Start

### Installation
```bash
# Copy to OpenClaw Skills directory
cp -r qywx-notify ~/.openclaw/skills/

# Install dependencies
cd ~/.openclaw/skills/qywx-notify
npm install
```

### Usage
```bash
# Send text notification
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "Hello, this is a test notification"

# Send notification with image
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "Please check the image" \
  --image "https://example.com/image.jpg"

# Send Markdown format notification
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "## Important Notice\n\n- Project update\n- Meeting reminder" \
  --msgtype "markdown" \
  --title "Daily Briefing"
```

## Features

- ✅ Text notifications
- ✅ Image notifications (Markdown format)
- ✅ Markdown rich text
- ✅ @all mention support
- ✅ Automatic retry on failure
- ✅ Complete error handling
- ✅ Both CLI and code-based invocation

## Webhook URL Format
```
https://{your-domain}/weai-core/v1/qywx/webhook-messages/bot/{bot-token}
```

### 2. Call in Code
```javascript
const QywxNotifySkill = require('./index.js');
const skill = new QywxNotifySkill(config);

// Send notification
const result = await skill.send({
  webhook: "your-webhook-url",
  content: "System is running normally",
  image: "https://example.com/status.jpg",
  mentionAll: true
});

console.log(result);
```

### 3. Message Format Examples

**Text message:**
```json
{
  "msgtype": "text",
  "text": {
    "content": "Hello, please check the image: ![image](https://example.com/image.jpg)",
    "mentioned_list": ["@all"]
  }
}
```

**Markdown message:**
```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "# Important Notice\n\n- Project update\n- Meeting reminder\n\n![image](https://example.com/image.jpg)"
  }
}
```

## Examples

### Example 1: Send Simple Notification
```bash
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "Maintenance Notice: System upgrade tonight from 20:00-22:00. Please save your work in advance."
```

### Example 2: Send Notification with Image
```bash
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "Monthly report has been generated, please review:" \
  --image "https://example.com/reports/202503/report.jpg" \
  --mentionAll true
```

### Example 3: Send Markdown Format Notification
```bash
openclaw skill qywx-notify send \
  --webhook "your-webhook-url" \
  --content "## Project Progress\n\n✅ Completed:\n- Requirements analysis\n- Prototype design\n\n⏳ In progress:\n- Development\n\n📅 Next week plan:\n- Testing and acceptance" \
  --msgtype "markdown" \
  --title "Weekly Project Report"
```

## Error Handling

### Common Errors
1. **Invalid Webhook URL**: Check if the URL format is correct
2. **Network connection failure**: Check network connectivity and firewall settings
3. **Insufficient permissions**: Check if the robot has permission to send messages
4. **Content too long**: WeCom message content limit is 2048 characters

### Error Response
```json
{
  "success": false,
  "message": "Send failed: WeCom API error: invalid webhook url (code: 400)",
  "error": {
    "errcode": 400,
    "errmsg": "invalid webhook url"
  }
}
```

## Testing

### Test Connection
```bash
openclaw skill qywx-notify test --webhook "your-webhook-url"
```

### View Configuration
```bash
openclaw skill qywx-notify config
```

## Integration with Other Skills

### Call from Python
```python
import subprocess
import json

def send_qywx_notification(webhook, content, image=None):
    """Send WeCom notification"""
    cmd = ["openclaw", "skill", "qywx-notify", "send"]
    cmd.extend(["--webhook", webhook])
    cmd.extend(["--content", content])
    
    if image:
        cmd.extend(["--image", image])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Send failed: {e.stderr}")
        return None
```

## Security Considerations

1. **Protect Webhook URL**: The Webhook URL contains sensitive information. Do not share it publicly.
2. **Access control**: Set minimum required permissions for the robot.
3. **Content moderation**: Avoid sending sensitive or inappropriate content.
4. **Rate limiting**: Comply with WeCom's message sending rate limits.
