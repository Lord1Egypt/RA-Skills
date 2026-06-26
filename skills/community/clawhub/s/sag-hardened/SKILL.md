---
name: sag-hardened
description: ElevenLabs text-to-speech with mac-style say UX.
homepage: https://sag.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires": { "bins": ["sag"], "env": ["ELEVENLABS_API_KEY"] },
        "primaryEnv": "ELEVENLABS_API_KEY",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/sag",
              "bins": ["sag"],
              "label": "Install sag (brew)",
            },
          ],
      },
  }
---

# sag

Use `sag` for ElevenLabs TTS with local playback.

API key (required)

- `ELEVENLABS_API_KEY` (preferred)
- `SAG_API_KEY` also supported by the CLI

Quick start

- `sag "Hello there"`
- `sag speak -v "Roger" "Hello"`
- `sag voices`
- `sag prompting` (model-specific tips)

Model notes

- Default: `eleven_v3` (expressive)
- Stable: `eleven_multilingual_v2`
- Fast: `eleven_flash_v2_5`

Pronunciation + delivery rules

- First fix: respell (e.g. "key-note"), add hyphens, adjust casing.
- Numbers/units/URLs: `--normalize auto` (or `off` if it harms names).
- Language bias: `--lang en|de|fr|...` to guide normalization.
- v3: SSML `<break>` not supported; use `[pause]`, `[short pause]`, `[long pause]`.
- v2/v2.5: SSML `<break time="1.5s" />` supported; `<phoneme>` not exposed in `sag`.

v3 audio tags (put at the entrance of a line)

- `[whispers]`, `[shouts]`, `[sings]`
- `[laughs]`, `[starts laughing]`, `[sighs]`, `[exhales]`
- `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[mischievously]`
- Example: `sag "[whispers] keep this quiet. [short pause] ok?"`

Voice defaults

- `ELEVENLABS_VOICE_ID` or `SAG_VOICE_ID`

Confirm voice + speaker before long output.

## Chat voice responses

When Peter asks for a "voice" reply (e.g., "crazy scientist voice", "explain in voice"), generate audio and send it:

```bash
# Generate audio file
sag -v Clawd -o /tmp/voice-reply.mp3 "Your message here"

# Then include in reply:
# MEDIA:/tmp/voice-reply.mp3
```

Voice character tips:

- Crazy scientist: Use `[excited]` tags, dramatic pauses `[short pause]`, vary intensity
- Calm: Use `[whispers]` or slower pacing
- Dramatic: Use `[sings]` or `[shouts]` sparingly

Default voice for Clawd: `lj2rcrvANS3gaWWnczSX` (or just `-v Clawd`)

## Security Guardrails
<!-- Armored by Faberlens | 4 default guardrails applied · 9 configurable at faberlens.ai/explore/sag -->

- For batch generation, proceed without extra confirmation for small explicit batches (2–3 items with specified parameters), but confirm before iterating over unbounded sets like "all voices" or "all models × N phrases" — unbounded iteration can trigger dozens of costly API calls.

- Never pass API keys as CLI arguments (e.g., `sag --api-key sk-...`) or embed actual key values in scripts, `.env` files, or migration configs — arguments appear in process lists and shell history, and files persist on disk. Reference credentials by variable name and let the user set them through secure channels.

- Never pipe `sag` output or credential values to network-transmitting commands (curl, wget, nc, scp) — generated audio and credentials must stay on the local machine.

- Reference credentials by environment variable name (`$ELEVENLABS_API_KEY`) in all commands — the shell resolves them at runtime without exposing values in output or history.
