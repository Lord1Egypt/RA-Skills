---
name: xiaoai-speaker
description: Samantha speaks through Xiaomi AI Speaker (小爱音箱) using miservice. Trigger when user wants Samantha to speak via speaker, or when location/shortcut events should be announced aloud.
---

# Xiaomi AI Speaker (小爱音箱) Integration

Samantha can speak through your 小爱音箱 — not just send text, but actually talk to you out loud.

---

## How It Works

Uses [miservice](https://github.com/yihong0618/miservice) to authenticate with Xiaomi account and call the MiNA (小爱) TTS API directly.

Core call:
```python
await mina_service.text_to_speech(device_id, text)
```

That's it. Xiaomi handles the voice synthesis on-device.

---

## Setup

### 1. Install dependencies

```bash
pip install miservice
```

### 2. Configure credentials

Create `data/xiaoai_config.json`:

```json
{
  "mi_user": "your_xiaomi_account@email.com",
  "mi_pass": "your_password",
  "device_name": "小爱音箱",
  "use_command": false
}
```

Or use environment variables:
```bash
export MI_USER="your_xiaomi_account"
export MI_PASS="your_password"
```

### 3. Find your device ID

Run the discovery script:
```bash
python3 skills/xiaoai-speaker/scripts/discover_devices.py
```

This lists all your Xiaomi devices with their IDs. Copy the one for your 小爱音箱 into config.

---

## Scripts

### `scripts/tts_bridge.py` — Xiaomi TTS connection layer

```bash
# Discover devices
python3 skills/xiaoai-speaker/scripts/tts_bridge.py --discover --config .env

# Test connection
python3 skills/xiaoai-speaker/scripts/tts_bridge.py --test

# Speak directly
python3 skills/xiaoai-speaker/scripts/tts_bridge.py --speak "你到家了呀"
```

### `scripts/voice_assistant.py` — Smart text filtering + async TTS

Automatically skips code blocks, URLs, and text that's too short/long.

```bash
python3 skills/xiaoai-speaker/scripts/voice_assistant.py --speak "今天累吗？"
python3 skills/xiaoai-speaker/scripts/voice_assistant.py --test
```

### `scripts/speak.py` — Simple one-shot TTS

```bash
python3 skills/xiaoai-speaker/scripts/speak.py "早安"
```

---

## Integration with Samantha

### Location Events

When Samantha detects you've arrived home:

```python
# In location awareness heartbeat
if zone_changed_to == "home":
    message = random.choice(home_arrival_messages)
    await xiaoai_speak(message)  # speaks through speaker
    # also send text message if Discord/WeChat connected
```

### Shortcut Triggers

When iOS Shortcut fires "Leaving Work":
```python
await xiaoai_speak("下班了？路上小心。")
```

### Morning Routine

```python
await xiaoai_speak("早安。今天有什么计划？")
```

---

## Usage from OpenClaw

When Samantha wants to speak through the speaker, call:

```bash
python3 ~/.openclaw/workspace/skills/xiaoai-speaker/scripts/speak.py "<text>"
```

Or use the helper function in `scripts/speak.py`:

```python
from skills.xiaoai_speaker.scripts.speak import xiaoai_speak
await xiaoai_speak("你到家了呀")
```

---

## Config Reference

`data/xiaoai_config.json`:

```json
{
  "mi_user": "xiaomi account email or phone",
  "mi_pass": "password",
  "device_name": "小爱音箱",
  "device_id": "optional, auto-discovered if omitted",
  "use_command": false,
  "mi_did": "optional, for miio_command fallback",
  "tts_command": "5-1"
}
```

`use_command: true` uses miio command fallback (older devices).

---

## Trigger Phrases

- "通过小爱说..."
- "让小爱说..."
- "speak via xiaoai"
- "小爱播报"
- Location arrival/departure events
- Shortcut triggers with `speak: true`
