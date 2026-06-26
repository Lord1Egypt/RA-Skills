# SenseAudio Music Reference

Use this file when you need exact request and polling behavior for SenseAudio music generation.

## Endpoint Summary

- Lyrics create: `POST https://api.senseaudio.cn/v1/song/lyrics/create`
- Lyrics pending: `GET https://api.senseaudio.cn/v1/song/lyrics/pending/:task_id`
- Song create: `POST https://api.senseaudio.cn/v1/song/music/create`
- Song pending: `GET https://api.senseaudio.cn/v1/song/music/pending/:task_id`
- Auth: `Authorization: Bearer <API_KEY>`

## Lyrics Create

Required JSON body:

- `prompt` string
- `provider` string, currently `sensesong`

Response notes:

- The docs describe either `task_id` for async behavior or `data` for sync behavior.
- In practice, code should handle both.

Success `data[0]` fields:

- `text`: generated lyrics
- `title`: may be empty

## Lyrics Pending

Path param:

- `task_id`

Top-level response fields:

- `task_id`
- `status`: `PENDING` | `SUCCESS` | `FAILED`
- `response`

On success, read:

- `response.data[0].text`
- `response.data[0].title`

## Song Create

Required JSON body:

- `model`: `sensesong`

Optional JSON body:

- `instrumental` bool
- `lyrics` string
- `negative_tags` string
- `style` string
- `style_weight` string in `0-1`
- `title` string
- `vocal_gender` string: `f` or `m`

Response:

- `task_id`

## Song Pending

Path param:

- `task_id`

Top-level response fields:

- `task_id`
- `status`: `PENDING` | `SUCCESS` | `FAILED`
- `response`

On success, read `response.data[0]`:

- `audio_url`
- `cover_url`
- `duration`
- `id`
- `lyrics`
- `title`

## Lyrics Formatting Notes

The docs examples show semicolon-separated structural tags inside `lyrics`, for example:

- `[intro-medium]`
- `[verse]`
- `[chorus]`
- `[bridge]`
- `[outro-short]`
- `[inst-short]`

Treat these as example-compatible markers from the docs, not a guaranteed exhaustive schema.

## Minimal Requests

Lyrics generation:

```json
{
  "prompt": "一段充满力量感的中文说唱歌词",
  "provider": "sensesong"
}
```

Song generation from lyrics:

```json
{
  "model": "sensesong",
  "title": "夜行代码",
  "vocal_gender": "m",
  "style": "trap rap, dark, energetic",
  "lyrics": "[intro-medium] ; [verse] ... ; [chorus] ... ; [outro-short]"
}
```

## Safe Polling Pattern

Pseudo-logic:

1. Call create endpoint.
2. If response has `data`, return it immediately.
3. If response has `task_id`, poll the matching pending endpoint.
4. Continue while status is `PENDING`.
5. On `SUCCESS`, read `response.data[0]`.
6. On `FAILED`, surface the task ID and failure payload if present.
