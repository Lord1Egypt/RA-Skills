# WeryAI Podcast API

Use this file when you need the exact public contract for the WeryAI podcast endpoints wrapped by this skill.

## Endpoints

- `GET /v1/generation/podcast/speakers/list`
  - Required query: `language`
- `POST /v1/generation/podcast/generate/text`
  - Required body: `query`, `speakers`, `language`, `mode`
  - `mode` values: `quick`, `debate`, `deep`
  - `debate` requires exactly 2 speakers
- `POST /v1/generation/podcast/generate/{taskId}/audio`
  - Optional body: `scripts`, `webhook_url`, `caller_id`
  - If `scripts` is omitted, the API uses the generated default text from the task
- `GET /v1/generation/{taskId}/status`
  - Podcast tasks should be evaluated with `content_status`

## Podcast lifecycle

Podcast generation is a two-stage async workflow:

1. submit podcast text generation
2. poll task status until `content_status=text-success`
3. trigger audio generation
4. poll again until `content_status=audio-success`

Failure states called out in the docs:

- `text-fail`
- `audio-fail`

Use this skill for podcast generation only. Do not use it for generic chat, blog writing, or music-only generation.
