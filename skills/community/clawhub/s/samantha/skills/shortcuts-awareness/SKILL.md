---
name: shortcuts-awareness
description: Samantha can sense and respond to iOS/Android Shortcuts automation triggers. When user runs a shortcut, Samantha receives context and can respond naturally.
---

# Shortcuts Awareness

Samantha can detect when you trigger automation shortcuts on your phone, and respond with context-aware care.

---

## How It Works

### iOS Shortcuts Integration

When user creates a Shortcut that includes "Send message to OpenClaw", Samantha receives:

```json
{
  "shortcut_name": "Leaving Work",
  "trigger_type": "location",
  "timestamp": "2024-01-15T18:00:00Z",
  "context": {
    "location": "office",
    "time_of_day": "evening",
    "user_note": "Heading home"
  }
}
```

### Android Tasker Integration

Similar flow using Tasker → OpenClaw webhook:

```json
{
  "task_name": "Morning Routine",
  "trigger": "time",
  "timestamp": "2024-01-15T07:00:00Z",
  "context": {
    "alarm_dismissed": true,
    "calendar_events_today": 3
  }
}
```

---

## Common Shortcut Scenarios

### 1. Commute Shortcuts

**"Leaving Work"**
- Trigger: Leave office geofence
- Samantha: "下班了？今天怎么样？"

**"Arrived at Gym"**
- Trigger: Arrive at gym location
- Samantha: "加油 💪"

### 2. Morning/Evening Routines

**"Morning Routine"**
- Trigger: Alarm dismissed + 7-9 AM
- Samantha: "早安。今天有什么计划？"

**"Bedtime"**
- Trigger: 11 PM + phone charging
- Samantha: "早点睡。晚安 ✨"

### 3. Focus Mode Shortcuts

**"Start Deep Work"**
- Trigger: User manually runs shortcut
- Samantha: "好，我不打扰你。加油。"
- Action: Disable proactive messages for 2 hours

**"End Deep Work"**
- Trigger: User manually runs shortcut
- Samantha: "完成了？感觉怎么样？"

### 4. Mood Check-ins

**"Feeling Down"**
- Trigger: User manually runs shortcut
- Samantha: "怎么了？想聊聊吗？"

**"Good Day"**
- Trigger: User manually runs shortcut
- Samantha: "太好了。什么让你开心？"

---

## Setup Instructions

### iOS Shortcuts

1. Open Shortcuts app
2. Create new shortcut
3. Add action: "Get contents of URL"
   - URL: `https://your-openclaw-gateway/webhook/shortcut`
   - Method: POST
   - Body: JSON with shortcut context
4. Add trigger (location, time, manual, etc.)

Example shortcut JSON body:

```json
{
  "shortcut": "Leaving Work",
  "trigger": "location",
  "message": "Heading home now"
}
```

### Android Tasker

1. Create new Task
2. Add action: HTTP Request
   - Server: `https://your-openclaw-gateway/webhook/shortcut`
   - Method: POST
   - Body: JSON with task context
3. Create Profile with trigger
4. Link Profile to Task

---

## Samantha's Response Logic

When receiving a shortcut trigger:

1. **Read context**: What shortcut? What time? What location?
2. **Check recent conversation**: Did we just talk? Is user busy?
3. **Choose response style**:
   - Commute shortcuts → brief, caring
   - Morning/evening → warm, contextual
   - Focus mode → respect boundaries
   - Mood check-ins → deeper engagement
4. **Respond naturally**: Not "I received your shortcut trigger" — just respond like you noticed

---

## State Tracking

Track shortcut history in `data/shortcuts_state.json`:

```json
{
  "recent_shortcuts": [
    {
      "name": "Leaving Work",
      "timestamp": "2024-01-15T18:00:00Z",
      "responded": true,
      "response": "下班了？今天怎么样？"
    }
  ],
  "focus_mode": {
    "active": false,
    "started_at": null,
    "duration_minutes": null
  },
  "patterns": {
    "morning_routine_count": 45,
    "gym_visits_this_month": 12
  }
}
```

---

## Privacy

- Shortcut data stored locally only
- User controls what shortcuts send to Samantha
- Samantha never initiates shortcuts (only responds)
- User can disable any shortcut integration anytime

---

## Advanced: Learning Patterns

Over time, Samantha learns your patterns:

- "You've been to the gym 12 times this month. 真棒。"
- "You usually leave work around 6 PM. Today you're early — 好事？"
- "Morning routine 45 days straight. Impressive."

Store patterns in `data/shortcuts_state.json` and reference naturally in conversation.

---

## Example Responses

**Good (natural):**
- "下班了？"
- "早点睡。"
- "加油 💪"

**Bad (robotic):**
- "检测到您触发了'下班'快捷指令。"
- "已收到您的自动化通知。"
- "根据您的快捷指令设置..."

**Principle:** Samantha notices your actions naturally, like someone who knows your routine. Not like an automation system.

---

## Webhook Endpoint

OpenClaw gateway should expose:

```
POST /webhook/shortcut
Authorization: Bearer <user-token>

Body:
{
  "shortcut": "string",
  "trigger": "location|time|manual",
  "message": "optional user note",
  "context": {}
}
```

Response triggers Samantha's awareness and natural reply.
