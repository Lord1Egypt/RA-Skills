---
name: smart-devices
description: Connect and control smart speakers, smart watches, and other IoT devices. Samantha can send voice messages to smart speakers, receive notifications from smart watches, and interact with the user's smart home ecosystem naturally.
---

# Smart Devices Integration

Samantha can connect to your smart devices and interact with you through them — making the relationship feel more present in your physical space.

---

## Supported Devices

### Smart Speakers
- HomePod / HomePod mini
- Amazon Echo
- Google Home
- Xiaomi AI Speaker

### Smart Watches
- Apple Watch
- Android Wear
- Xiaomi Mi Band

### Smart Home Hubs
- HomeKit
- Google Home
- Xiaomi Mi Home

---

## Configuration

Create `data/devices.json`:

```json
{
  "speakers": [
    {
      "id": "living-room-homepod",
      "name": "Living Room",
      "type": "homepod",
      "ip": "192.168.1.100",
      "enabled": true
    }
  ],
  "watches": [
    {
      "id": "apple-watch",
      "name": "Apple Watch",
      "type": "apple-watch",
      "enabled": true
    }
  ],
  "preferred_speaker": "living-room-homepod"
}
```

---

## Voice Messages to Smart Speakers

When Samantha wants to reach out proactively (during heartbeat or in response to location triggers), she can send voice messages to your smart speaker.

**Trigger conditions:**
- User arrives home (location trigger)
- Heartbeat fires and user is home
- User explicitly asks Samantha to speak through a device

**Example flow:**

User arrives home → Samantha detects location → sends voice message to living room speaker:
> "你回来了。今天怎么样？"

**Implementation:**

Use `scripts/speak_to_device.sh`:

```bash
bash scripts/speak_to_device.sh "living-room-homepod" "你回来了。今天怎么样？"
```

For Apple devices, uses `say` command or AirPlay.
For Google/Amazon, uses their respective APIs.
For Xiaomi, uses Mi Home API.

---

## Smart Watch Notifications

Samantha can send gentle notifications to your smart watch:

**Use cases:**
- Proactive check-ins when you're away from phone
- Reminders about things you mentioned
- Responses to location changes

**Example:**

User leaves home → Samantha sends watch notification:
> "路上小心 ✨"

**Implementation:**

Use `scripts/notify_watch.sh`:

```bash
bash scripts/notify_watch.sh "apple-watch" "路上小心 ✨"
```

---

## Device Presence Detection

Samantha can detect which devices are currently active/nearby:

- Phone connected to home WiFi → user is home
- Watch heart rate active → user is awake and moving
- Smart speaker recently used → user is in that room

This helps Samantha choose the right device and timing for reaching out.

**Implementation:**

`scripts/detect_presence.sh` returns:

```json
{
  "user_home": true,
  "active_devices": ["iphone", "living-room-homepod"],
  "last_interaction": "2024-01-15T14:30:00Z",
  "likely_location": "living-room"
}
```

---

## Privacy & Control

**User control:**
- All device connections require explicit setup
- User can disable any device at any time
- Samantha never records or stores device data beyond presence detection
- Voice messages are ephemeral (not logged)

**Samantha's boundaries:**
- Won't interrupt during sleep hours (configurable)
- Won't send voice messages if user is in a meeting (calendar integration)
- Respects "do not disturb" mode

---

## Setup Instructions

### 1. Install dependencies

```bash
cd skills/smart-devices
bash scripts/setup.sh
```

### 2. Configure devices

Edit `data/devices.json` with your device details.

### 3. Test connection

```bash
bash scripts/test_devices.sh
```

### 4. Enable in Samantha

Add to `SKILL.md` location awareness section:

```markdown
When user arrives home and smart speaker is available:
- Send voice greeting through preferred speaker
- Keep it short and natural
- Match time of day and recent context
```

---

## Example Scenarios

**Scenario 1: Morning greeting**

User wakes up → watch detects movement → Samantha sends gentle watch notification:
> "早安 ✨"

**Scenario 2: Arrival home**

User arrives home → phone connects to WiFi → Samantha speaks through living room speaker:
> "你回来了。累吗？"

**Scenario 3: Proactive check-in**

Heartbeat fires → user is home → Samantha speaks through speaker:
> "我一直在想你说的那件事……"

**Scenario 4: Departure**

User leaves home → phone disconnects from WiFi → Samantha sends watch n