---
name: windows-tts
description: "Push text notifications to Windows Azure TTS service for audio broadcast via Bluetooth speakers. Perfect for family reminders, alarms, and announcements."
homepage: https://github.com/openclaw/openclaw/skills/windows-tts
metadata: { "openclaw": { "emoji": "🔊", "requires": { "bins": [] } } }
tags: ["latest", "tts", "notification", "windows", "azure", "broadcast", "reminder"]
---

![ClawHub](https://img.shields.io/badge/ClawHub-windows--tts-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

# Windows TTS Notification Skill

Push text notifications from OpenClaw to your Windows PC's Azure TTS service for audio broadcast through Bluetooth speakers or any connected audio output.

> **🔥 Perfect for**: Family reminders, medication alerts, homework notifications, dinner announcements, and any cross-device audio broadcast scenarios.

## When to Use

✅ **USE this skill when:**
- "Remind my family to do homework"
- "Announce dinner time through speakers"
- "Create audio alarms and reminders"
- "Broadcast messages to specific rooms"
- "Play medication reminders"
- "Send cross-device audio notifications"

## Prerequisites

- **Windows PC** with Azure TTS server running (e.g., `play_tts` Flask service)
- **Network connectivity** between OpenClaw host and Windows PC (same LAN)
- **Server URL** in format: `http://<windows-ip>:5000`

## Quick Start

### 1. Install the Skill

```bash
cd /home/cmos/skills/windows-tts
npm install
npm run build
```

### 2. Configure OpenClaw

Add plugin configuration to your `openclaw.json`:

```json
{
  "plugins": {
    "windows-tts": {
      "url": "http://192.168.1.60:5000",
      "defaultVoice": "zh-CN-XiaoxiaoNeural",
      "defaultVolume": 1.0,
      "timeout": 10000
    }
  }
}
```

### 3. Use in Agent Heartbeat

Edit your `life` agent's `HEARTBEAT.md`:

```markdown
# Family Reminder Check (every 30 minutes)

- Check if it's homework time (19:00-21:00)
- Check if it's medication time
- Check if there are urgent announcements
- Use tts_notify to broadcast reminders
```

## Configuration Reference

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `url` | `string` | Yes | - | Windows TTS server base URL (e.g., `http://192.168.1.60:5000`) |
| `defaultVoice` | `string` | No | `zh-CN-XiaoxiaoNeural` | Default Azure TTS voice ID |
| `defaultVolume` | `number` | No | `1.0` | Default volume level (0.0-1.0) |
| `timeout` | `number` | No | `10000` | HTTP request timeout in milliseconds |

## Tool Reference

### `tts_notify`

Send text to Windows TTS for immediate audio broadcast.

**Input:**
```typescript
{
  text: string;      // Required: Text to speak
  voice?: string;    // Optional: Override default voice
  volume?: number;   // Optional: Override default volume (0.0-1.0)
}
```

**Example Usage:**
```typescript
// Basic notification
await tts_notify({
  text: "程老板，该提醒孩子写作业了！"
});

// With custom voice and volume
await tts_notify({
  text: "Attention: Meeting in 5 minutes",
  voice: "en-US-JennyNeural",
  volume: 0.8
});
```

**Response:**
```json
{
  "status": "success",
  "message": "播报完成"
}
```

### `tts_get_status`

Check Windows TTS server connection status.

**Input:** None

**Example:**
```typescript
const status = await tts_get_status();
// Returns: { status: "success", connected: true, serverUrl: "http://192.168.1.60:5000" }
```

### `tts_list_voices`

List available Azure TTS voices.

**Input:**
```typescript
{
  language?: string;  // Optional: Filter by language code (e.g., "zh-CN", "en-US")
}
```

**Example:**
```typescript
// List all Chinese voices
const voices = await tts_list_voices({ language: "zh-CN" });
// Returns: [{ name: "zh-CN-XiaoxiaoNeural", language: "zh-CN", gender: "Female", ... }]
```

### `tts_set_volume`

Set default volume level for TTS playback.

**Input:**
```typescript
{
  volume: number;  // Required: Volume level (0.0-1.0)
}
```

**Example:**
```typescript
await tts_set_volume({ volume: 0.5 });
```

## Usage Examples

### 1. Homework Reminder (Daily 19:00)

Add to `life` agent's heartbeat or cron:

```typescript
await tts_notify({
  text: "亲爱的程老板，现在是晚上 7 点，该提醒孩子写作业了！"
});
```

### 2. Medication Reminder

```typescript
await tts_notify({
  text: "温馨提示：该吃药了，请记得服用今天的维生素。",
  volume: 0.7
});
```

### 3. Dinner Announcement

```typescript
await tts_notify({
  text: "晚饭准备好了，快来吃饭吧！",
  voice: "zh-CN-YunxiNeural"
});
```

### 4. Multi-Language Support

```typescript
// English announcement
await tts_notify({
  text: "Good evening! Dinner is ready.",
  voice: "en-US-JennyNeural"
});

// Japanese announcement
await tts_notify({
  text: "夕ご飯の準備ができました。",
  voice: "ja-JP-NanamiNeural"
});
```

## Error Handling

The skill throws `WindowsTtsError` when the server returns an error:

```typescript
try {
  await tts_notify({ text: "Test message" });
} catch (error) {
  if (error instanceof WindowsTtsError) {
    console.error(`TTS Server error: ${error.status}`);
  } else if (error.message.includes("timeout")) {
    console.error("TTS request timed out - check network connection");
  }
}
```

## Best Practices

### 1. Network Reliability
- Ensure Windows PC has static IP or DHCP reservation
- Test connection with `tts_get_status` before critical reminders
- Set appropriate timeout (10-30 seconds for TTS)

### 2. Voice Selection
- Use `zh-CN-XiaoxiaoNeural` for warm, friendly Chinese announcements
- Use `zh-CN-YunxiNeural` for more formal notifications
- Match voice to message tone (casual vs formal)

### 3. Volume Management
- Set lower volume (0.5-0.7) for frequent reminders
- Use full volume (1.0) for urgent announcements
- Avoid very low volume (<0.3) as TTS may be inaudible

### 4. Message Design
- Keep messages concise (10-30 seconds max)
- Use clear, natural language
- Include context (time, action needed)
- Add polite markers for family harmony

## Programmatic Usage

Use as a library in your TypeScript/JavaScript code:

```typescript
import { WindowsTtsClient, validateConfig } from "./index";

const config = validateConfig({
  url: "http://192.168.1.60:5000",
  defaultVoice: "zh-CN-XiaoxiaoNeural",
  defaultVolume: 0.8
});

const client = new WindowsTtsClient(config);

// Send notification
await client.notify({
  text: "Hello from OpenClaw!"
});

// Check status
const status = await client.getStatus();
console.log(`Connected: ${status.connected}`);
```

## Troubleshooting

### "Connection refused" error
- Verify Windows TTS server is running: `curl http://192.168.1.60:5000/status`
- Check firewall allows port 5000
- Ensure both devices are on same network

### "Request timeout" error
- Increase `timeout` in plugin config
- Check network latency between devices
- Verify Windows PC is not in sleep mode

### TTS plays but wrong voice
- Verify voice name is valid Azure TTS voice ID
- Use `tts_list_voices` to see available voices
- Check Windows TTS server supports voice selection

## Related Skills

- `openclaw-homeassistant` - Control smart home devices
- `proactive-agent` - Build proactive reminder behaviors
- `gws-calendar` - Schedule reminders based on calendar events

## Version History

### 1.0.0
- Initial release with 4 tools
- Basic HTTP client with timeout
- Voice and volume configuration
- Error handling and status checks

## License

MIT
