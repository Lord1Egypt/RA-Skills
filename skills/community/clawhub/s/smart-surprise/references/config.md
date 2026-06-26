# Smart Surprise — Configuration Reference

Complete schema and field-by-field documentation for `config.json`.

## Config File Location

```
~/.openclaw/workspace/skills/smart-surprise/config.json
```

## Full Schema

```json
{
  "timezone": "Asia/Shanghai",
  "location": "Beijing",
  "quietHoursStart": "22:00",
  "quietHoursEnd": "08:00",
  "minIntervalMinutes": 60,
  "maxIntervalMinutes": 480,
  "channel": "telegram",
  "channelTarget": "YOUR_CHANNEL_TARGET",
  "characteristics": "warm, casual, playful"
}
```

## Field Reference

### timezone

**Type:** string  
**Default:** `"Asia/Shanghai"`  
**Format:** IANA timezone identifier (e.g., `Asia/Shanghai`, `America/New_York`, `Europe/London`)

Determines:
- Time-of-day context for greetings (morning/afternoon/evening)
- Quiet hours window calculation
- Day-of-week labels in messages

### location

**Type:** string  
**Default:** none (required for weather topic)  
**Format:** City name (e.g., `Beijing`, `New York`, `London`)

Required for the `weather` topic to fetch accurate local weather data.

Used in: `https://wttr.in/{location}?format=j1`

### quietHoursStart / quietHoursEnd

**Type:** string (HH:MM, 24-hour)  
**Defaults:** `"22:00"` / `"08:00"`

No messages are sent during this window.

**Behavior:**
- If a scheduled trigger lands inside quiet hours → skip it entirely
- If the next random delay would land inside quiet hours → push to `quietHoursEnd` instead
- Quiet hours **do not** count toward the minimum interval wait

---

### minIntervalMinutes / maxIntervalMinutes

**Type:** integer (minutes)  
**Defaults:** `60` / `480` (1 hour / 8 hours)

The random range for the next trigger delay. Each completed run picks a uniformly random value in this range.

| Profile | min | max | Feel |
|---------|-----|-----|------|
| Default | 60 | 480 | Moderate surprise |
| Frequent | 30 | 240 | More surprises |
| Relaxed | 120 | 1440 | Less intrusive |

---

### channelTarget

**Type:** string  
**Required:** Yes

Recipient ID on your configured channel. Used for `openclaw message send --target <channelTarget>`.

**How to find your Telegram chat ID:**
- Message `@userinfobot` on Telegram — it replies with your user ID
- Or check OpenClaw logs: `openclaw sessions list`

---

### channel

**Type:** string  
**Required:** Yes  
**Supported:** `telegram`, `discord`, `slack`, `whatsapp`, `signal`, `msteams`

The delivery channel. Must be configured and enabled in your OpenClaw setup.

### characteristics

**Type:** string (free text)  
**Default:** `"warm, casual, playful"`  

A natural language description of the user's preferred communication style. The agent reads this on every run and uses it to guide the tone, word choice, and personality of every message generated.

The agent also updates this field after interactions if the user expresses a preference for a different style.

**Example values:**
- `"warm, casual, playful"` — friendly, informal, a bit cute
- `"calm, thoughtful, professional"` — measured, reflective, serious tone
- `"gentle, caring, encouraging"` — soft, supportive, warm
- `"witty, funny, light-hearted"` — humorous, entertaining
- `"brief, direct, efficient"` — short, to-the-point, minimal fluff

Free text is intentional — any description the user gives in plain language works.

---

## Runtime State File

**Location:** `~/.openclaw/workspace/skills/smart-surprise/next_run.json`

Written by each run to communicate scheduling info to the next agent. **Do not edit manually.**

---

## Environment-Specific Notes

### Telegram

```json
{
  "channel": "telegram",
  "channelTarget": "YOUR_CHANNEL_TARGET"
}
```

### Discord

```json
{
  "channel": "discord",
  "channelTarget": "YOUR_CHANNEL_TARGET"
}
```



### Google Calendar Integration

⚠️ **Credentials required for this topic.** If enabled, the skill will read:
1. Google OAuth credentials at `~/.openclaw/secrets/google-calendar.json`, or
2. The helper script at `~/.openclaw/scripts/google-calendar.py`

These files contain sensitive tokens — only provide access if you understand what they contain and trust the skill.

If credentials are not configured, the `calendar` topic silently produces no output (no error is shown to the user).

### Weather

The `weather` topic requires `location` to be set in this config file.

---

## Complete Example Configurations

### Example 1: Default (Beijing user)

```json
{
  "timezone": "Asia/Shanghai",
  "location": "Beijing",
  "quietHoursStart": "22:00",
  "quietHoursEnd": "08:00",
  "minIntervalMinutes": 60,
  "maxIntervalMinutes": 480,
  "channel": "telegram",
  "channelTarget": "YOUR_CHANNEL_TARGET",
  "characteristics": "warm, casual, playful"
}
```

### Example 2: New York User (Evening Focus)

```json
{
  "timezone": "America/New_York",
  "location": "New York",
  "quietHoursStart": "23:00",
  "quietHoursEnd": "07:00",
  "minIntervalMinutes": 120,
  "maxIntervalMinutes": 720,
  "channel": "telegram",
  "channelTarget": "YOUR_CHANNEL_TARGET",
  "characteristics": "calm, thoughtful, professional"
}
```
