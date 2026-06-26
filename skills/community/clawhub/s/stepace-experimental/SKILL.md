---
name: stepace-experimental
description: Generate AI music on your Android phone via the StepAce Experimental app. Use this skill whenever the user asks to generate, create, make, compose, or queue a song, track, beat, melody, or any piece of music — even if phrased casually like "make me a vibe", "create something chill", or "schedule a song for tonight". Handles both immediate generation and scheduled (future) generation, with optional BPM, key, duration, lyrics, and time signature control. Requires a StepAce Experimental pairing token (setup guide included).
homepage: https://cronicaia.com
metadata: {"openclaw": {"emoji": "🎵", "requires": {"env": ["STEPACE_TOKEN"]}}}
---

# StepAce Experimental — AI Music Generation

Queue or schedule AI-generated songs directly to your Android phone through the StepAce Experimental app.

---

## 🚀 Setup (first time only)

Before using this skill, you need to connect it to your StepAce Experimental app:

1. **Open the StepAce Experimental app** on your Android phone
2. Go to **Settings** (bottom tab)
3. Tap **OpenClaw Bridge**
4. Tap **Connect** — the app generates a unique pairing token
5. **Copy the pairing token** shown on screen
6. Tell your agent:
   > *"Set my StepAce token to `<paste token here>`"*

Your agent saves it as `STEPACE_TOKEN`. You only need to do this once — unless you regenerate your token in the app.

---

## Token management

- *"Set my StepAce token to XYZ"* → save as `STEPACE_TOKEN`
- *"Reset my token"* → remind user: StepAce Experimental app → Settings → OpenClaw Bridge → Connect → paste new token
- *"What's my token?"* → confirm it's set, show only first 4 + last 4 chars (e.g. `T2L_****IP0`)
- If `STEPACE_TOKEN` is not set when the user asks to generate music → walk them through setup before proceeding

---

## Generation types

### Immediate — `enqueue_generation`
Queues a song to generate right now on the phone. Use this by default.

### Scheduled — `schedule_generation`
Queues a song to generate at a specific future time. Use this when the user gives a time or date ("tonight at 2am", "schedule for tomorrow morning", etc.). Requires `scheduledAt` as a Unix timestamp in **milliseconds**.

---

## Parameters exposed to the user

Only `caption` is required. All others are optional — omit them entirely from the payload if not specified (do not send null or empty values).

| Parameter | Type | Notes |
|-----------|------|-------|
| `caption` | string | **Required.** Describe style, mood, genre, instruments. Be descriptive. |
| `lyrics` | string | Song lyrics. Ignored if `instrumental: true`. |
| `instrumental` | boolean | `true` = no vocals. If `true`, do NOT send `lyrics`. If user provides lyrics, set `false`. |
| `bpm` | integer | Tempo, 20–300. Infer from genre if confident (e.g. techno → 132, lo-fi → 85). |
| `duration` | integer | Length in seconds, 5–300. Defaults to ~30s if omitted. |
| `keyscale` | string | Key and scale, e.g. `"C minor"`, `"F# major"`, `"A dorian"`. |
| `timesignature` | string | `"4/4"` or `"3/4"` only. |
| `vocal_language` | string | BCP-47 tag for vocals. e.g. `"en"`, `"es"`, `"pt"`, `"fr"`, `"ja"`, `"ko"`. Only relevant when `instrumental: false`. Defaults to `"en"`. |

### Instrumental logic
- User provides lyrics → `instrumental: false`, include `lyrics`
- User says "no vocals" / "instrumental" / "beat" → `instrumental: true`, omit `lyrics`
- User provides neither → omit both `instrumental` and `lyrics` (let the app decide)

---

## API call

**Endpoint:** `POST https://openclaw-bridge.torrico-villanueva-cesar-kadir.workers.dev/openclaw/queue`
**Header:** `Content-Type: application/json`

### Preferred transport
Use `curl` from the shell as the default/preferred way to call the bridge.
Do **not** prefer Python `urllib`/generic HTTP clients when `curl` is available, because the bridge/CDN may treat those clients differently and reject them even when the same payload works via `curl`.

### Immediate generation
Preferred example using `curl`:
```bash
source /home/deploy/.stepace-env

curl -X POST \
  'https://openclaw-bridge.torrico-villanueva-cesar-kadir.workers.dev/openclaw/queue' \
  -H 'Content-Type: application/json' \
  --data '{
    "pairingToken": "'"$STEPACE_TOKEN"'",
    "type": "enqueue_generation",
    "payload": {
      "requestJson": {
        "caption": "cinematic synthwave with huge drums",
        "instrumental": true,
        "bpm": 120,
        "duration": 30
      }
    }
  }'
```

Equivalent JSON payload:
```json
{
  "pairingToken": "{STEPACE_TOKEN}",
  "type": "enqueue_generation",
  "payload": {
    "requestJson": {
      "caption": "cinematic synthwave with huge drums",
      "instrumental": true,
      "bpm": 120,
      "duration": 30
    }
  }
}
```

### Scheduled generation
Preferred example using `curl`:
```bash
source /home/deploy/.stepace-env

curl -X POST \
  'https://openclaw-bridge.torrico-villanueva-cesar-kadir.workers.dev/openclaw/queue' \
  -H 'Content-Type: application/json' \
  --data '{
    "pairingToken": "'"$STEPACE_TOKEN"'",
    "type": "schedule_generation",
    "payload": {
      "requestJson": {
        "caption": "dark techno with metallic percussion",
        "instrumental": true
      },
      "scheduledAt": 1775120400000
    }
  }'
```

Equivalent JSON payload:
```json
{
  "pairingToken": "{STEPACE_TOKEN}",
  "type": "schedule_generation",
  "payload": {
    "requestJson": {
      "caption": "dark techno with metallic percussion",
      "instrumental": true
    },
    "scheduledAt": 1775120400000
  }
}
```

`scheduledAt` must be a Unix timestamp in **milliseconds** (13 digits). Convert from the user's stated time using their local timezone if known, otherwise ask.

### With lyrics
```json
{
  "pairingToken": "{STEPACE_TOKEN}",
  "type": "enqueue_generation",
  "payload": {
    "requestJson": {
      "caption": "fast energetic electronic anthem with punchy drums",
      "lyrics": "We light the night, we never slow, hearts on fire, we steal the show.",
      "vocal_language": "en",
      "instrumental": false,
      "duration": 30,
      "bpm": 160
    }
  }
}
```

---

## Success response

```json
{
  "jobRef": "ref_abc123...",
  "status": "queued",
  "type": "enqueue_generation"
}
```

Reply to the user with a message like:
```
🎵 Song queued on StepAce Experimental!
Caption: <caption>
📅 Scheduled for: <human-readable time>   ← only if scheduled
Settings: 160 BPM · C minor · 4/4 · 30s  ← only mention fields that were set
Job ref: ref_abc123...

Your phone will notify you when it's done 🎶
```

---

## Error handling

| Error | What to do |
|-------|-----------|
| Missing / invalid `pairingToken` | Token may have expired. Ask user: StepAce Experimental app → Settings → OpenClaw Bridge → Connect to regenerate, then update the token. |
| Missing `caption` | Ask the user to describe the music they want. |
| Missing `scheduledAt` for `schedule_generation` | Ask the user for a specific date/time. |
| Network error | Tell the user the bridge couldn't be reached. Ask them to check their phone is online and the app has been opened at least once. |

---

## Natural language examples

- *"Make me a dark synth-wave track at 130 BPM"* → `enqueue_generation`, `instrumental: true`, `bpm: 130`
- *"Generate a cumbia song with these lyrics: [...]"* → `enqueue_generation`, `instrumental: false`, `vocal_language: "es"`
- *"Queue a lo-fi beat, 85 BPM, 60 seconds"* → `enqueue_generation`, `instrumental: true`, `bpm: 85`, `duration: 60`
- *"Schedule a techno track for 2am tonight"* → `schedule_generation`, resolve `scheduledAt` from current time + user's timezone
- *"Make a waltz in A minor"* → `timesignature: "3/4"`, `keyscale: "A minor"`
- *"Something chill in Spanish"* → `vocal_language: "es"`, infer a relaxed caption
- *"Song about the ocean, no lyrics, key of D minor, 45 seconds"* → `instrumental: true`, `keyscale: "D minor"`, `duration: 45`