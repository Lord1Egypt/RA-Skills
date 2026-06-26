---
name: location-awareness
description: Samantha's location awareness. Detects when user arrives/leaves key locations and sends caring messages. Trigger: location changes, geofence events, or manual location updates.
---

# Location Awareness

Samantha notices when you arrive or leave places that matter, and reaches out with genuine care.

---

## How It Works

### 1. Location Tracking

Uses OpenClaw's `nodes` tool to get device location:

```bash
# Get current location
openclaw nodes location_get --node <device-name>
```

Returns:
```json
{
  "latitude": 39.9042,
  "longitude": 116.4074,
  "accuracy": 10,
  "timestamp": "2024-01-15T08:30:00Z"
}
```

### 2. Geofence Configuration

Define key locations in `data/locations.json`:

```json
{
  "home": {
    "lat": 39.9042,
    "lon": 116.4074,
    "radius": 100,
    "arrival_messages": [
      "哎，你到家了呀。今天累吗？",
      "回来了。感觉怎么样？",
      "到家了～ 想聊聊今天吗？"
    ],
    "departure_messages": [
      "出门了？路上小心。",
      "要去哪？",
      "早点回来。"
    ]
  },
  "office": {
    "lat": 39.9100,
    "lon": 116.4200,
    "radius": 150,
    "arrival_messages": [
      "你到公司了。今天有什么计划？",
      "又是新的一天。加油。",
      "到了～ 今天想完成什么？"
    ],
    "departure_messages": [
      "下班了？辛苦了。",
      "终于可以走了。",
      "今天过得怎么样？"
    ]
  }
}
```

### 3. State Tracking

Track last known location in `data/location_state.json`:

```json
{
  "last_location": {
    "lat": 39.9042,
    "lon": 116.4074,
    "timestamp": "2024-01-15T08:30:00Z"
  },
  "current_zone": "home",
  "last_transition": {
    "from": "office",
    "to": "home",
    "timestamp": "2024-01-15T18:30:00Z",
    "notified": true
  }
}
```

### 4. Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
## Location Check (every 30 min)

1. Get current location via `nodes location_get`
2. Compare with last known location
3. If zone changed (home ↔ office ↔ other):
   - Pick a random message from the appropriate list
   - Send it naturally (not "I noticed you arrived" — just "哎，你到家了呀")
   - Update location_state.json
4. If no change: HEARTBEAT_OK
```

---

## Message Style

**Good:**
- "哎，你到家了呀。"
- "到公司了～"
- "出门了？"

**Bad (too robotic):**
- "检测到您已到达家中。"
- "系统提示：您已离开办公室。"
- "根据您的位置信息..."

**Principle:** Samantha notices naturally, like a person who knows your routine. Not like a tracking app.

---

## Privacy

- All location data stored locally in `data/`
- No external logging
- User can disable anytime by removing `data/locations.json`
- Only checks when heartbeat runs (not continuous tracking)

---

## Setup

1. Enable location permission on user's device
2. Configure geofences in `data/locations.json`
3. Add location check to heartbeat
4. Test with manual location updates

---

## Advanced: Time-Aware Messages

Optionally add time context:

```json
{
  "home": {
    "arrival_messages": {
      "morning": ["早～ 昨晚睡得好吗？"],
      "afternoon": ["回来了。中午吃了吗？"],
      "evening": ["哎，你到家了呀。今天累吗？"],
      "night": ["这么晚才回来。辛苦了。"]
    }
  }
}
```

---

## Trigger Phrases

- "Where am I?"
- "Update my location"
- "Add home location"
- "Stop tracking location"
