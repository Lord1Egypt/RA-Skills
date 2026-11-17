# Veevid API Reference — endpoints

Base URL `https://veevid.ai`. Every request needs `Authorization: Bearer <API_KEY>` (keys start with `vv_sk_`; at most 5 active keys per account; keys are managed only on the website). JSON in and out unless noted.

Per-model params live in the model files: [models-video.md](models-video.md), [models-image.md](models-image.md), [models-audio.md](models-audio.md), [models-tools.md](models-tools.md).

## POST /api/quote

Exact credit cost, without generating anything. Send the body you will send to `/api/generate-video`, including the prompt (GPT Image, Qwen Image, text-to-speech and music models check it). File URLs are only needed to quote `scribe-v2` and `veed-clean-audio` (the audio URL); other models can be quoted before uploading.

```json
{"mode": "kling-3", "generation_type": "text-to-video", "duration": "10", "model_version": "kling-3-standard", "generate_audio": true}
```

→ `{"required_credits": <n>, "current_balance": <n>, "sufficient": true}`

The quote endpoint does **not read video URLs** and, for some models, does not count the `images` array. Describe input files with these quote fields (each model's rules say which ones it needs):

| Quote field | Meaning |
|---|---|
| `input_image_count` | Number of images (0–16), for the models whose rules ask for it |
| `has_video_input` | Always `true` when you send reference videos, or a source video to edit or extend (not for character swap or the insert-shot source video) |
| `input_video_count` | Number of reference videos (also read by `minimax-h3-max` and `minimax-h3-max-insert`) |
| `input_video_duration` | Length in seconds of the input / reference video(s) |
| `reference_video_duration` | Total length of the reference videos for an inserted shot (`minimax-h3-max-insert`) |
| `has_audio_input`, `input_audio_count`, `input_audio_duration` | The same for audio inputs |

Seedance 2.5 draft upgrade price: `{"draft_upgrade_id": "<generation_id>"}` → also returns `upgradable` and, when it can't be upgraded, `reason`.

## POST /api/generate-video

Starts any generation (video, image, audio or tool). Credits are deducted on submission and refunded automatically if the job fails, unless the model's rules say otherwise.

Common params (each model has its own set — see the model files):

| Param | Type | Notes |
|---|---|---|
| `mode` | string | The model. Always send it (the server default is a legacy model) |
| `generation_type` | string | `text-to-video`, `image-to-video`, `reference-to-video`, `text-to-image`, `image-to-image`, `text-to-speech`, `video-upscale`, … (default `text-to-video`) |
| `prompt` | string | Max 20,000 characters (less for some models). Not auto-translated; keep the user's language unless they agree to a translation |
| `aspect_ratio`, `duration`, `video_quality`, `resolution`, `model_version` | string | Model-specific values. Omitted values fall back to server defaults, which are not always the website's — send what matters |
| `image` / `images` | URL / URL[] | First frame, reference images, images to edit |
| `video` / `videos` | URL / URL[] | Source video for tools / reference videos |
| `audio` / `audios` | URL / URL[] | Driving or reference audio, audio to transcribe |

Response:

```json
{"generation_id": "vg_abc123", "status": "processing", "video_url": null, "image_url": null, "provider_task_id": "...", "video_quality": "standard"}
```

A few jobs return `"status": "completed"` immediately with `video_url` (videos) or `image_url` (images) — use it directly instead of polling.

## GET /api/video-generation/{generation_id}/status

Works for every media kind. Poll every 5–10 seconds.

```json
{
  "id": "vg_abc123",
  "status": "completed",
  "media_kind": "image",
  "video_url": "https://cdn.veevid.ai/images/...jpg",
  "error_message": null,
  "credits_used": <n>,
  "created_at": "...",
  "completed_at": "...",
  "video_metadata": {"content_type": null, "file_name": null, "file_size": null},
  "provider_task_id": "...",
  "video_quality": "1K",
  "result_images": ["https://cdn.veevid.ai/images/...jpg"]
}
```

| Field | Meaning |
|---|---|
| `status` | `processing` → `completed` or `failed` |
| `media_kind` | `video`, `image` or `audio` |
| `video_url` | The result for every media kind (for images: the first image) |
| `result_images` | All output images |
| `error_message` | Why it failed |
| `lyrics` | Lyria song lyrics (raw markup) when the track has vocals |
| `transcript` | Scribe V2 transcript `{language, duration, speakers, text, cues: [{s, e, p, t}]}` |
| `timestamps` | Eleven v4 word timestamps, when requested |
| `seedance25_draft` | Seedance 2.5 / Veevid 2.5 Pro 480p drafts: `{upgradable, upgrade_credits, expires_at, upgrade_generation_id}` |

## POST /api/video-generation/{generation_id}/upgrade-draft

Seedance 2.5 and Veevid 2.5 Pro 480p results are usually drafts. A completed draft can be upgraded once, within 7 days, to 1080p with the same prompt, inputs and seed. No body. It spends credits: quote it first with `{"draft_upgrade_id": "<id>"}` and confirm with the user.

→ `{"generation_id": "vg_def456", "status": "processing", "credits_used": <n>, "draft_id": "vg_abc123"}` — poll the new id.

Errors: 400 not a Seedance 2.5 draft, 402 insufficient credits, 409 not completed yet / already upgraded, 410 expired, 502 could not be submitted (credits refunded).

## File uploads

### POST /api/storage/upload

`multipart/form-data` with `file` and `folder`. Use the upload folder listed for the model's input — the folder decides the accepted types and size (images JPEG/PNG/WebP, 10MB by default; video and audio folders allow more). Requests are capped at 100MB by the hosting platform, even where a folder or model allows more; pass a public https URL for bigger files if the model accepts one.

```bash
curl -X POST https://veevid.ai/api/storage/upload \
  -H "Authorization: Bearer $(cat ~/.config/veevid/api_key)" \
  -F "file=@./photo.jpg" -F "folder=image-generator"
```

→ `{"url": "https://cdn.veevid.ai/image-generator/...jpg", "key": "image-generator/...jpg"}` — pass `url` to the model.

### POST /api/storage/presign-upload

Like `/api/storage/upload`, this sends the user's file to Veevid's storage for processing by the model. Tell the user before uploading and ask first if the file is private or sensitive.

Direct upload for large files, only for `veed-clean-audio` (folder `remove-background-noise/input`, up to 512MB; .mp3 .wav .m4a .aac .ogg .opus .flac .mp4 .mov .m4v .webm).

1. `POST {"folder": "remove-background-noise/input", "filename": "talk.mp3", "size": <bytes>}` → `{"uploadUrl", "url", "key", "contentType"}` (402 if the balance is below one minute of audio)
2. `PUT` the raw file to `uploadUrl` with header `Content-Type: <contentType>` (exactly `size` bytes)
3. Pass `url` as `audio` to the model

## GET /api/user/creations

The user's generations, newest first. Query: `page` (default 1), `pageSize` (default 12, max 50), `generationType` (filter), `includeAudio=1` (audio is left out otherwise).

→ `{"creations": [{"id", "mode", "generationType", "status", "prompt", "videoUrl", "resultImages", "creditsUsed", "createdAt", "mediaKind", ...}], "totalPages", "currentPage", "totalCount", "hasMore"}` — note the camelCase field names; `resultImages` and `metadata` are JSON-encoded strings.

`GET /api/user/creations/{id}` returns one item with the same fields; `DELETE` permanently removes it with its result files and, for some models, the uploaded input audio → `{"success": true}`. Only delete when the user explicitly asks to delete that specific creation, and confirm which one first.

## GET /api/credits

→ `{"success": true, "credits": <n>, "balance": <n>}`

## Errors

Error bodies look like `{"error": "Insufficient credits. You need <n> credits but only have <m>.", "required": <n>, "balance": <m>}`.

| Code | Meaning |
|---|---|
| 400 | Invalid parameters |
| 401 | Invalid or missing API key |
| 402 | Insufficient credits (`required`, `balance`) |
| 403 | Account suspended |
| 404 | Generation not found |
| 409 | Character swap: the input video is longer than `input_video_duration` — nothing charged; the body has `measured_duration` and the new `required_credits`: get the user's yes to the new price, then resend with `input_video_duration = measured_duration`. Draft upgrade: not ready / already upgraded |
| 410 | Draft expired |
| 422 | Parameter combination not supported by the model |
| 500 | Server error — retry |
| 502 | Draft upgrade could not be submitted (credits refunded) |

## Limits

- No fixed per-key request rate limit today; poll status every 5–10 seconds rather than continuously.
- 5 active API keys per account.
