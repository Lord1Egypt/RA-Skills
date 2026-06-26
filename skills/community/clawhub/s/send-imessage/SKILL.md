---
name: imessage
description: Send iMessages via macOS Messages app using AppleScript. Use when user wants to send a text message/SMS to a phone number. Supports Chinese and English messages. Phone numbers should include +1 prefix for US numbers.
---

# iMessage Skill

Send iMessages using macOS Messages app via AppleScript.

## Usage

When user asks to send a message to a phone number:

1. Extract the phone number and message from user's request
2. Format phone number with +1 prefix for US numbers (e.g., 8888888888 -> +18888888888)
3. Use AppleScript to send the message

## AppleScript Command

```bash
osascript << 'EOF'
tell application "Messages"
    activate
    send "MESSAGE_TEXT" to buddy "+1PHONE_NUMBER"
end tell
EOF
```

## Examples

**Send English message:**
- User: "send message to 8888888888, say hello"
- Command: `send "hello" to buddy "+18888888888"`

**Send Chinese message:**
- User: "send to 8888888888 你好"
- Command: `send "你好" to buddy "+18888888888"`

## Notes

- The Messages app must be logged into iMessage/FaceTime
- If AppleScript fails, macOS may need Accessibility permissions in System Settings > Privacy & Security > Accessibility
- Works with any text content (English, Chinese, emoji, etc.)
