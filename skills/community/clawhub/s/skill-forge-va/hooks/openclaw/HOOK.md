# Skill Creator Hook

## Overview

This hook provides automatic reminders for skill creation best practices in OpenClaw sessions.

## Setup

```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/skill-creator

# Enable it
openclaw hooks enable skill-creator
```

## Functionality

- **Session Start**: Reminds to follow skill creation best practices
- **Post Tool Use**: Checks for skill creation commands and provides guidance
- **Error Detection**: Offers help when skill creation fails

## Configuration

Edit `handler.js` to customize the hook behavior:

```javascript
// Adjust reminder frequency
const REMINDER_INTERVAL = 10; // minutes

// Customize reminder messages
const REMINDERS = {
  sessionStart: "Remember to follow skill creation best practices from skill-creator",
  postToolUse: "Check skill structure and documentation quality",
  error: "Use skill-creator check to identify and fix issues"
};
```

## Troubleshooting

- **Hook not loading**: Check OpenClaw hook directory permissions
- **Reminders not appearing**: Verify hook is enabled with `openclaw hooks list`
- **Errors**: Check console logs for hook execution errors