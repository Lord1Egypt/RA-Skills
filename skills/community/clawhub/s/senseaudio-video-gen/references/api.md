# SenseAudio API Reference

Use `SENSEAUDIO_API_KEY` as the Bearer token for SenseAudio media APIs. If it is not exported, the CLI also checks AudioClaw's local workspace credential files for `SENSEAUDIO_API_KEY`.

## LLM Planning

Use `DEEPSEEK_API_KEY` as a Bearer token for OpenAI-compatible chat completions.

- Default base URL: `https://api.deepseek.com`
- Chat path: `/chat/completions`
- Default model: `deepseek-v4-pro`
- Override model/base URL with env vars or command flags.

AudioClaw planning is a separate OpenAI-compatible LLM route. It uses `AUDIOCLAW_LLM_API_KEY`, `AUDIOCLAW_LLM_BASE_URL`, and `AUDIOCLAW_LLM_MODEL`, or the local AudioClaw config file when `--provider audioclaw` or `--llm audioclaw` is selected. The config entry supplies `api_base`, `api_key`, and `model`; LiteLLM-style prefixes such as `volcengine/` are removed for `platform.senseaudio.cn`. Do not reuse `SENSEAUDIO_API_KEY` as the AudioClaw LLM key.

The skill uses the selected LLM only for creative planning: title, headline, narration, visual style, and storyboard JSON. Generated video copy defaults to Chinese (`zh-CN`) unless the brief explicitly requests another language. SenseAudio remains the media provider for TTS, ASR, images, and model video.

## One-Pass Website Pipeline

`site-video` is the recommended website-to-video path. It orchestrates URL/site evidence ingestion, AudioClaw or DeepSeek planning, real screenshot capture, optional SenseAudio TTS/ASR, audio-reactive data extraction, local render, `motion-audit`, and `motion-map`. `--llm-fallback` is enabled by default so transient model/API failures degrade to heuristic planning instead of aborting the whole run. Add `--vision-audit` when an OpenRouter/OpenAI-compatible vision model should review inspect frames.

`site-ingest` adds `semantic_sections`, `primary_roles`, and role-tagged evidence. Supported roles include `hero`, `product`, `research`, `safety`, `developer`, `enterprise`, `customer`, `pricing`, and `cta`. `compose` uses these roles to avoid repetitive generic sections and to choose richer shot grammar.

`site-vision-plan` adds `visual_plan` crop directives before rendering. Each item includes `screenshot_id`, `role`, `crop.x`, `crop.y`, `crop.zoom`, and `crop.pan`; `compose` writes these into screenshot CSS variables such as `--crop-x`, `--crop-y`, and `--crop-zoom`. The `heuristic` provider is deterministic; `openrouter` can be used to ask a VL model for the same crop plan when screenshots are available.

## Video Generation

- Create: `POST https://api.senseaudio.cn/v1/video/create`
- Status: `GET https://api.senseaudio.cn/v1/video/status?id=<task_id>`
- Models: `Seedance-2.0-Fast`, `Seedance-2.0`, `Seedance-Pro-1.5`
- Status values: `pending`, `processing`, `completed`, `failed`

Core request fields: `model`, `content`, `duration`, `resolution`, `ratio`, `watermark`, `provider_specific`.

Content item types:

- `{"type":"text","text":"..."}`
- `{"type":"image","url":"https://... or data:image/...","role":"first_frame|last_frame|reference"}`
- `{"type":"audio","audio_url":"https://..."}`
- `{"type":"video","video_url":"https://..."}`

Model guardrails:

- `Seedance-Pro-1.5`: `ratio` is `16:9` or `9:16`; `resolution` is `720p` or `1080p`; `duration` is 2–12 seconds; supports text and first/last-frame images.
- `Seedance-2.0` and `Seedance-2.0-Fast`: `ratio` is `16:9`, `4:3`, `1:1`, `3:4`, or `9:16`; `resolution` is `480p` or `720p`; `duration` is 4–15 seconds; supports first/last-frame mode or reference-material mode.
- Do not mix first/last-frame images with reference images in the same `Seedance-2.0` request.

## Image Generation

- Sync: `POST https://api.senseaudio.cn/v1/image/sync`
- Async: `POST https://api.senseaudio.cn/v1/image/async`
- Models: `senseaudio-image-1.0-260319`, `doubao-seedream-5-0-260128`

Fields: `model`, `prompt`, optional `reference`, optional `seed`, optional `size`.

Prefer sync when a downstream video needs a first frame immediately.

## Music Generation

- Create: `POST https://api.senseaudio.cn/v1/music/song/create`
- Status: `GET https://api.senseaudio.cn/v1/music/song/pending/<task_id>`
- Model: `senseaudio-music-1.0-260319`
- Auth: `Authorization: Bearer SENSEAUDIO_API_KEY`

Fields: `model`, `lyrics`, optional `custom_mode`, optional `instrumental`, optional `negative_tags`, optional `style`, optional `style_weight`, optional `title`, optional `vocal_gender`.

For stable instrumental beds, prefer structured music tags rather than free-form prompt text:

```text
[intro-medium] ; [inst-medium] ; [outro-short]
```

The official status response nests the generated audio at `response.data[].audio_url`. If the task remains `PENDING` without an `audio_url`, `site-video --music-fallback` can create a local ambient bed and continue the render while preserving the SenseAudio task manifest for later inspection.

## Text To Speech

- Endpoint: `POST https://api.senseaudio.cn/v1/t2a_v2`
- Model: `senseaudio-tts-1.5-260319`
- Output: `data.audio` is hex-encoded audio bytes.

`voice_setting`: `voice_id`, `speed` `[0.5,2.0]`, `vol` `[0.01,10.0]`, `pitch` `[-12,12]`, `latex_read`.

`audio_setting`: `format` `mp3|wav|pcm|flac`, `sample_rate`, `bitrate`, `channel`.

## Speech Recognition

- Endpoint: `POST https://api.senseaudio.cn/v1/audio/transcriptions`
- Content-Type: `multipart/form-data`
- Models: `senseaudio-asr-lite-1.5-260319`, `senseaudio-asr-1.5-260319`, `senseaudio-asr-pro-1.5-260319`, `senseaudio-asr-deepthink-1.5-260319`

For captions, use `senseaudio-asr-1.5-260319` or `senseaudio-asr-pro-1.5-260319` with `response_format=verbose_json` and `timestamp_granularities[]=word`.

## Voice Listing

- Endpoint: `POST https://api.senseaudio.cn/v1/get_voice`
- Body: `{"voice_type":"all"}`

Use this before picking a voice when the user has not provided a known `voice_id`.
