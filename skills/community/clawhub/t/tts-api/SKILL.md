---
name: tts
description: "Use this skill whenever the user wants to convert text to speech, generate audio from text, create voiceovers, or produce spoken audio files. Triggers include: any mention of 'text to speech', 'TTS', 'read aloud', 'voice synthesis', 'generate speech', 'voiceover', 'narration audio', 'speak this text', or requests to turn written content into an audio/MP3 file. Also use when the user wants to pick a voice, adjust speech emotion/style, change speech rate or pitch, or compare TTS providers (Azure, Volcengine, Edge). If the user asks to 'make an audio version' of any text, 'record' a script, or produce '.mp3' output from text, use this skill. Do NOT use for speech-to-text, audio transcription, music generation, or sound effects."
---

# Text-to-Speech (TTS) via tts.102465.xyz

Convert text into spoken audio using a hosted TTS API that supports multiple providers, voices, emotions, and tuning parameters.

## API Base URL

```
https://tts.102465.xyz
```

All endpoints are under the `/api` prefix.

## Quick Reference

| Task | Endpoint | Method |
|------|----------|--------|
| Generate speech audio | `/api/tts` | POST or GET |
| List available voices | `/api/voices?provider=<name>` | GET |
| List available providers | `/api/providers` | GET |

## Generating Speech

Two equivalent ways to call the TTS endpoint:

### POST (recommended for longer text or programmatic use)

```bash
curl -X POST https://tts.102465.xyz/api/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"你好世界","voice":"晓晓","emotion":"温柔","provider":"azure"}' \
  --output output.mp3
```

### GET (convenient for short text or browser-playable links)

```
https://tts.102465.xyz/api/tts?text=你好世界&voice=晓晓&provider=azure
```

The response is an audio file (MP3). Save it with `--output` in curl, or open the GET URL directly in a browser to play.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `text` | Text to synthesize (**required**) | — |
| `voice` | Voice name (Chinese label or English ID) | Provider default |
| `emotion` | Emotion or speaking style (Azure only) | — |
| `rate` | Speech rate adjustment, percentage (Azure/Edge) | 0 |
| `pitch` | Pitch adjustment, percentage (Azure/Edge) | 0 |
| `provider` | TTS backend: `azure`, `volcengine`, or `edge` | `azure` |

## Providers at a Glance

- **azure** — Default provider. Richest feature set: many voices, emotion/style control, rate and pitch tuning.
- **volcengine** — Alternative Chinese-language voices including specialty voices (e.g. film narration).
- **edge** — Microsoft Edge TTS voices including regional dialect options (e.g. Liaoning dialect). Supports rate and pitch.

## Choosing a Voice and Emotion

Before generating speech, query the available voices for a provider:

```bash
curl https://tts.102465.xyz/api/voices?provider=azure
```

This returns a JSON list of voices and, for Azure, their supported emotions/styles. Use the voice's Chinese label (e.g. `晓晓`) or English ID in the `voice` parameter, and pick an emotion from the voice's supported list for the `emotion` parameter.

## Workflow

1. **Clarify requirements** — Ask the user what text they want spoken, in what language, and whether they have a preference for voice gender, style, or emotion.
2. **Pick a provider** — Default to `azure` unless the user needs a specialty voice from another provider. If unsure, query `/api/providers` and `/api/voices?provider=<name>` to browse options.
3. **Generate the audio** — Call `/api/tts` with the chosen parameters. For programmatic use, POST with JSON body; for a quick shareable link, construct a GET URL.
4. **Deliver the result** — If using curl/POST, save the MP3 to `/mnt/user-data/outputs/` and present it to the user. If constructing a GET link, provide the URL so the user can play it in-browser.

## Example GET URLs

**Azure with emotion:**
```
https://tts.102465.xyz/api/tts?text=今天天气真不错&provider=azure&voice=晓晓&emotion=温柔
```

**Volcengine specialty voice:**
```
https://tts.102465.xyz/api/tts?text=在遥远的东方，有一个古老的传说&provider=volcengine&voice=影视男解说%20中英混
```

**Edge dialect voice:**
```
https://tts.102465.xyz/api/tts?text=今天咱们唠唠嗑&provider=edge&voice=晓北%20辽宁%20女
```

## Tips

- URL-encode Chinese characters and spaces when constructing GET URLs (e.g. `%20` for space).
- The `emotion` parameter only works with Azure. Other providers ignore it.
- `rate` and `pitch` are percentages — positive values speed up / raise pitch, negative values slow down / lower pitch. They work with Azure and Edge.
- If the user doesn't specify a voice, omit the `voice` parameter to use the provider's default.
- When generating audio files programmatically, save as `.mp3`.
