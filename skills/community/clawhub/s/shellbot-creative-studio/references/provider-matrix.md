# Provider Matrix

Use this matrix to pick providers and models quickly.

## Image generation

| Task | Primary | Secondary | Why |
|---|---|---|---|
| General purpose, consistency | Nano Banana 2 `gemini-3.1-flash-image-preview` | Freepik `seedream-v5-lite` | Best consistency across scenes, fast, cheap |
| Maximum quality stills | Nano Banana Pro `gemini-3-pro-image-preview` | Freepik `mystic` | Highest detail, best for hero shots |
| Fast concept ideation | Freepik `seedream-v5-lite` | fal `fal-ai/flux-2` | Fast iteration loops |
| Typography-heavy posters | Freepik `seedream-v4-5` | — | Best prompt-to-text rendering |
| Multi-image consistent edits | Nano Banana 2 (up to 14 ref images) | Freepik `seedream-v4-5-edit` | Strong instruction-following with references |
| Sub-second generation | Freepik `flux-2-klein` | — | When latency matters most |

## Video generation

| Task | Primary | Secondary | Why |
|---|---|---|---|
| Hero cinematic scenes | Freepik `kling-v3-omni-pro` | fal `fal-ai/kling-video/v2/image-to-video` | Best quality, multi-shot support |
| Fast video fallback | fal `fal-ai/minimax/video-01/image-to-video` | Freepik `kling-v3-omni-std` | Faster queue times |
| Text animations, branding | **Remotion** (not AI video) | — | Deterministic, precise |
| Scene transitions | **Remotion** (not AI video) | — | Deterministic, frame-accurate |

## Audio

| Task | Primary | Secondary | Why |
|---|---|---|---|
| Voiceover | Freepik ElevenLabs `elevenlabs-turbo-v2-5` | ElevenLabs direct | Clean integration |
| Background music | Freepik `music-generation` | ElevenLabs direct | Built-in marketing music |
| Sound effects | Freepik `sound-effects` | ElevenLabs direct | Prompt-guided SFX |

## Decision shortcuts

- **Need visual consistency across many scenes** → Nano Banana 2 (Flash) first
- **Need maximum quality hero shot** → Nano Banana Pro or Freepik Mystic
- **Need fast exploration** → Freepik Seedream v5 lite or fal Flux-2
- **Need text/typography in image** → Freepik Seedream v4-5
- **Need organic motion** → Kling (video command)
- **Need precise text/timing/branding** → Remotion (always)
- **Need final branded delivery** → always finish in Remotion

## Nano Banana 2 backends

Nano Banana 2 auto-detects the best available backend:

1. `GOOGLE_API_KEY` → Google Gemini API (preferred, full control over resolution/aspect)
2. `FAL_API_KEY` → fal.ai `fal-ai/nano-banana-2` endpoint (good fallback)
3. `OPENROUTER_API_KEY` → OpenRouter (largest model catalog, ShellBot default key)
4. `infsh` CLI → inference.sh (legacy fallback)

## OpenRouter image models

When using `--provider openrouter`, you can specify any model from the OpenRouter image catalog:

```bash
# Default: Nano Banana 2 via OpenRouter
bash scripts/image.sh --provider openrouter --prompt "..."

# Nano Banana Pro via OpenRouter
bash scripts/image.sh --provider openrouter --model pro --prompt "..."

# Any OpenRouter image model (use full model ID)
bash scripts/image.sh --provider openrouter --model "google/gemini-3.1-flash-image-preview" --prompt "..."
```

Browse available models: https://openrouter.ai/collections/image-models

## Environment variables

| Variable | Provider | Capabilities |
|---|---|---|
| `GOOGLE_API_KEY` | Nano Banana 2 (Google Gemini) | image, edit |
| `FAL_API_KEY` | fal.ai (+ Nano Banana 2 via fal) | image, edit, video |
| `OPENROUTER_API_KEY` | OpenRouter (+ Nano Banana 2 via OR) | image |
| `FREEPIK_API_KEY` | Freepik | image, edit, video, voice, music, sfx |
| `ELEVENLABS_API_KEY` | ElevenLabs | voice, music, sfx |
