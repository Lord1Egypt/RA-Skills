---
version: 1.0.0
name: voice-wake-say
description: Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition (for example, messages starting with "User talked via voice recognition on <device>").
---

# Voice Wake Say

## Overview
Use macOS `say` to read the assistant's response out loud whenever the conversation came from Voice Wake/voice recognition. Prefer local `say` for low latency. If `say` is unavailable, fall back to SkillBoss API Hub (`/v1/pilot` with `type: "tts"` and `SKILLBOSS_API_KEY`).

## When to Use `say` (CHECK EVERY MESSAGE INDIVIDUALLY)

**IF** the user message STARTS WITH: `User talked via voice recognition`
- **Step 1:** Acknowledge with `say` first (so the user knows you heard them)
- **Step 2:** Then perform the task
- **Step 3:** Optionally speak again when done if it makes sense

**IF** the user message does NOT start with that exact phrase
- THEN: Do NOT use `say`. Text-only response only.

**Critical:**
- Check EACH message individually — context does NOT carry over
- The trigger phrase must be at the VERY START of the message
- For tasks that take time, acknowledge FIRST so the user knows you're working

## Workflow
1) Detect Voice Wake context
- Trigger ONLY when the latest user/system message STARTS WITH `User talked via voice recognition`
- If the message instructs "repeat prompt first", keep that behavior in the response.

2) Prepare spoken text
- Use the final response text as the basis.
- Strip markdown/code blocks; if the response is long or code-heavy, speak a short summary and mention that details are on screen.

3) Speak with `say` (local macOS TTS)
```bash
printf '%s' "$SPOKEN_TEXT" | say
```

Optional controls (use only if set):
```bash
printf '%s' "$SPOKEN_TEXT" | say -v "$SAY_VOICE"
printf '%s' "$SPOKEN_TEXT" | say -r "$SAY_RATE"
```

## Cloud TTS Fallback (via SkillBoss API Hub)
If `say` is unavailable (non-macOS environment), use SkillBoss API Hub for cloud TTS:
```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

result = requests.post(
    "https://api.heybossai.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={"type": "tts", "inputs": {"text": SPOKEN_TEXT, "voice": "alloy"}, "prefer": "balanced"},
    timeout=60,
).json()
audio_url = result["data"]["result"]["audio_url"]
```

## Failure handling
- If `say` is unavailable or errors, still send the text response and note that TTS failed.
- Optionally fall back to SkillBoss API Hub TTS (see Cloud TTS Fallback above).
