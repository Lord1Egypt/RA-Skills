# WhatsApp Whitelist Skill (Word Trigger)

Word-trigger flow (no HTTP API usage) that:

- Manages whitelist sets of phone numbers
- Sends WhatsApp messages only to whitelisted numbers
- Tracks message status by `messageId` (`sent`, `delivered`, `read`, `failed`, `unknown`)
- Verifies OpenClaw WhatsApp connectivity before sending

## Requirements

- OpenClaw CLI installed and logged in
- WhatsApp channel connected (`openclaw channels status --probe`)
- Node.js 18+ (works with your current Node 22)

## Start

```bash
cd /home/vignesh/.openclaw/workspace/skills/whatsapp-whitelist-api
node word-trigger.js "help"
```

## Word Triggers

Use:

```bash
node word-trigger.js "<phrase>"
```

Examples:

- `node word-trigger.js "check whatsapp"`
- `node word-trigger.js "create set demo_ops"`
- `node word-trigger.js "list sets"`
- `node word-trigger.js "show set demo_ops"`
- `node word-trigger.js "add +918657704479 to demo_ops"`
- `node word-trigger.js "update +918657704479 to +918657704480 in demo_ops"`
- `node word-trigger.js "remove +918657704480 from demo_ops"`
- `node word-trigger.js "send 'Hello team' to demo_ops"`
- `node word-trigger.js "send 'Invoice attached' with media /home/vignesh/file.pdf to demo_ops"`
- `node word-trigger.js "send media https://example.com/image.jpg to demo_ops"`
- `node word-trigger.js "status 3EB0F09EA29438B49F44F8"`

### Media Support

- `media` supports local file paths or URLs (image/video/document/audio)
- Caption-style text is passed via the message phrase
- At least one of message or media is required for send

## Notes

- Data is stored in:
  - `data/whitelist.json`
  - `data/message-store.json`
- WhatsApp `read/delivered` status depends on whether corresponding events are present in OpenClaw channel logs.

