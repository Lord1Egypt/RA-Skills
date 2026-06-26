---
name: senseaudio-ai-rapper
description: Create and debug SenseAudio rap, hip-hop, or vocal song generation workflows using the `/v1/song/lyrics/create`, `/v1/song/lyrics/pending/:task_id`, `/v1/song/music/create`, and `/v1/song/music/pending/:task_id` APIs. Use this whenever the user wants rap lyrics, AI songs, style-controlled hip-hop tracks, or help polling async music-generation jobs.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://nightly.senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key for SenseAudio Open Platform
      env_var: SENSEAUDIO_API_KEY
homepage: https://nightly.senseaudio.cn
---

# SenseAudio AI Rapper

Use this skill for SenseAudio music-generation tasks focused on rap, hip-hop, and other vocal-song creation requests.

## Read First

- `references/music.md`

Load the reference only when you need exact endpoint, parameter, polling, or response-shape details.

## When To Use

Use this skill when the user wants to:

- generate rap or hip-hop lyrics from a prompt,
- turn lyrics into a full song with vocals,
- control song style, title, vocal gender, or instrumental mode,
- poll async lyric or song generation tasks,
- debug errors around SenseAudio music-generation requests.

## Default Workflow

1. Confirm the target output:
- lyrics only,
- full song from user-provided lyrics,
- or full song with platform-generated lyrics.

2. Start with the minimal valid request:
- lyrics generation requires `prompt` and `provider: sensesong`.
- song generation requires `model: sensesong`.

3. Treat both pipelines as potentially asynchronous:
- if create returns `task_id`, poll the matching `pending` endpoint,
- wait for `status == SUCCESS` before reading payload data,
- surface `FAILED` clearly instead of assuming empty data.

4. Add creative controls only when needed:
- `lyrics`, `title`, `style`, `style_weight`, `negative_tags`, `vocal_gender`, `instrumental`.

5. Return production-ready output:
- one minimal `curl` example,
- one requested-language example,
- polling logic,
- and safe response parsing for `audio_url`, `cover_url`, `lyrics`, and `duration`.

## Rap-Specific Guidance

- For rap requests, make the prompt explicit about theme, tone, pacing, and era, such as trap, boom bap, drill, conscious rap, or melodic rap.
- If the user already has bars or a chorus, skip lyric generation and call song creation directly with `lyrics`.
- Use `style` for positive steering and `negative_tags` for exclusions.
- Use `vocal_gender: "m"` or `"f"` only when the user asks or when matching a clear creative brief.
- Use `instrumental: true` only for beat-only output; otherwise omit it.

## Implementation Rules

- Keep API keys in environment variables; never hardcode secrets.
- Prefer `curl` first for reproducibility, then provide Python or JavaScript if useful.
- Do not invent extra request fields or undocumented endpoints.
- Do not assume lyric tags beyond what the docs examples show; if structure syntax matters, mirror the documented examples closely.
- When the docs show semicolon-separated section markers in lyrics, preserve that formatting unless the user provides a different valid lyric format.

## Response Parsing Rules

- Lyrics polling success shape: `response.data[0].text` and optional `response.data[0].title`.
- Song polling success shape: `response.data[0].audio_url`, `cover_url`, `duration`, `id`, `lyrics`, `title`.
- Guard every array/object access because `response` or `data` may be absent before success.

## Output Checklist

When producing an answer with this skill, include:

1. which endpoint(s) are used,
2. the minimal valid request body,
3. whether polling is required,
4. the final fields the caller should read,
5. and any rap-specific prompt/style suggestions relevant to the user’s brief.
