# Video models

Text-to-video, image-to-video and reference-to-video.

All of these are called with `POST /api/generate-video` using the `mode` and `generation_type` shown. Params marked 💲 change the price — get the exact cost with `POST /api/quote` before generating. Defaults are what the API uses when the field is omitted (not always what the website preselects).

## Index

- Google Veo 3.1 — `veo3`: `text-to-video`, `image-to-video`, `reference-to-video`
- Grok Imagine — `grok-imagine`: `text-to-video`, `image-to-video`
- Kling 2.6 — `kling-2-6`: `text-to-video`, `image-to-video`
- Kling 3.0 — `kling-3`: `text-to-video`, `image-to-video`
- LTX 2.5 — `ltx-2-5`: `text-to-video`, `image-to-video`
- LTX 2.3 — `ltx-2-3`: `text-to-video`, `image-to-video`
- Wan Animate — `wan-animate`: `image-to-video`
- Veevid 2.0 Pro — `veevid-2.0-pro`: `text-to-video`, `image-to-video`
- Veevid 2.5 Pro — `veevid-2.5-pro`: `text-to-video`, `image-to-video`
- Seedance 2.0 — `seedance-2.0`: `text-to-video`, `image-to-video`, `reference-to-video`
- Seedance 2.5 — `seedance-2.5`: `text-to-video`, `image-to-video`, `reference-to-video`
- Wan 2.6 — `wan-2-6`: `text-to-video`, `image-to-video`, `reference-to-video`
- Wan 2.7 — `wan-2.7`: `text-to-video`, `image-to-video`, `reference-to-video`
- Wan 3.0 — `wan-3.0`: `text-to-video`, `image-to-video`, `reference-to-video`
- MiniMax H3 — `minimax-h3`: `text-to-video`, `image-to-video`, `reference-to-video`
- MiniMax H3 Max — `minimax-h3-max`: `text-to-video`, `image-to-video`, `reference-to-video`
- MiniMax H3 Max Camera Controls — `minimax-h3-max-camera`: `camera-controls`
- MiniMax H3 Max Lip Sync — `minimax-h3-max-lip-sync`: `lip-sync`
- Gemini Omni — `gemini-omni`: `text-to-video`, `image-to-video`, `reference-to-video`
- Boreal — `creatify-boreal`: `text-to-video`, `image-to-video`

## Google Veo 3.1 — `veo3`

### `veo3` · `text-to-video`

Generates a 4-8 second video with native audio from a text prompt using Google Veo 3.1 (Lite / Fast / Quality tiers).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Scene description (required, non-empty, max 20000 characters). |
| `video_quality` 💲 | string | "lite", "standard", "pro" | "standard" | Tier: lite = Lite, standard = Fast, pro = Quality. Always send `video_quality`. |
| `resolution` 💲 | string | "720p", "1080p", "4k" | "720p" | Output resolution. |
| `duration` | string | "4", "6", "8" | "8" | Seconds: "4", "6" or "8" (default 8). |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" | 16:9 (landscape) or 9:16 (portrait). |
| `watermark` | string |  |  | Optional custom watermark text (max 200 characters). |

Rules:
- resolution, when sent, must be 720p, 1080p or 4k (422 otherwise).
- duration, when sent, must be '4', '6' or '8' (400 otherwise); omitted duration becomes '8'.
- Send lite, standard or pro: any other accepted video_quality value (e.g. "1080p") is treated as the Quality (pro) tier — set the output size with `resolution`.
- Price depends only on the video_quality tier and resolution; duration and aspect_ratio do not change the price.

Example body:

```json
{"mode": "veo3", "generation_type": "text-to-video", "prompt": "A golden retriever running through sunflowers, cinematic lighting", "video_quality": "standard", "resolution": "720p", "duration": "8", "aspect_ratio": "16:9"}
```

### `veo3` · `image-to-video`

Animates a first frame (optionally to a last frame) into a 4-8 second Veo 3.1 video with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Motion/scene description (required, non-empty, max 20000 characters). |
| `images` **required** | string[] |  |  | [first_frame_url] or [first_frame_url, last_frame_url]. A single `image` string is also accepted. |
| `video_quality` 💲 | string | "lite", "standard", "pro" | "standard" | Tier: lite = Lite, standard = Fast, pro = Quality. Always send `video_quality`. |
| `resolution` 💲 | string | "720p", "1080p", "4k" | "720p" | Output resolution; same price table as text-to-video. |
| `duration` | string | "4", "6", "8" | "8" | Seconds: "4", "6" or "8" (default 8). |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" | 16:9 (landscape) or 9:16 (portrait). |
| `watermark` | string |  |  | Optional custom watermark text (max 200 characters). |

Input files:
- `images`: 1-2 image URLs: first frame, optional last frame (max 10MB per image)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-veo3`

Rules:
- image or a non-empty images array is required (400 'Image is required for image-to-video generation').
- Send 1 or 2 images: the first frame and an optional last frame.
- resolution must be 720p/1080p/4k (422) and duration 4/6/8 (400) when sent.
- Send lite, standard or pro: any other accepted video_quality value (e.g. "1080p") is treated as the Quality (pro) tier — set the output size with `resolution`.
- Price depends only on the video_quality tier and resolution.
- To guide generation with reference images (rather than first/last frames), use generation_type reference-to-video.

Example body:

```json
{"mode": "veo3", "generation_type": "image-to-video", "prompt": "The woman slowly turns toward the camera and smiles", "images": ["https://example.com/first-frame.jpg"], "video_quality": "standard", "resolution": "720p", "duration": "8", "aspect_ratio": "16:9"}
```

### `veo3` · `reference-to-video`

Generates an 8-second Veo 3.1 video that keeps subjects consistent with 1-3 reference images.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Scene description (required, non-empty). |
| `images` **required** | string[] |  |  | 1-3 reference image URLs. |
| `video_quality` 💲 | string | "lite", "standard" | "standard" | Only the Lite (lite) and Fast (standard) tiers accept reference images. |
| `resolution` 💲 | string | "720p", "1080p", "4k" | "720p" |  |
| `duration` | string | "8" | "8" | Locked to 8 seconds. |
| `aspect_ratio` | string | "16:9" | "16:9" | Send 16:9; reference mode supports 16:9 only. |
| `watermark` | string |  |  | Optional custom watermark text (max 200 characters). |

Input files:
- `images`: 1-3 reference image URLs (max 10MB per image)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-veo3`

Rules:
- images must contain 1-3 URLs (400 'Reference-to-video requires 1-3 images').
- video_quality, when sent, must be lite or standard; the Quality tier is rejected with 422.
- duration, when sent, must be '8' (422).
- resolution must be 720p/1080p/4k (422) when sent.

Example body:

```json
{"mode": "veo3", "generation_type": "reference-to-video", "prompt": "The character from the reference walks through a neon-lit street at night", "images": ["https://example.com/character.png"], "video_quality": "standard", "resolution": "720p", "duration": "8", "aspect_ratio": "16:9"}
```

## Grok Imagine — `grok-imagine`

### `grok-imagine` · `text-to-video`

Generate a 6-30 second video with synchronized audio from a text prompt using xAI Grok Imagine.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty). |
| `duration` 💲 | string | 6–30 | "6" | Integer seconds sent as a string, 6-30. |
| `video_quality` 💲 | string | "480p", "720p" | "720p" | Output resolution: 480p or 720p. Always send `video_quality`. |
| `grokMode` | string | "fun", "normal", "spicy" | "normal" | Grok style mode: fun, normal or spicy. |
| `aspect_ratio` | string | "2:3", "3:2", "1:1", "9:16", "16:9" | "16:9" | Output aspect ratio; use one of the listed values. Always send `aspect_ratio` explicitly (16:9 is used when omitted). |

Rules:
- duration must be an integer string between 6 and 30 (400 otherwise); omitted duration defaults to 6.
- video_quality, when sent, must be 480p or 720p (400 otherwise).
- grokMode must be fun, normal or spicy; aspect_ratio must be one of the listed values.
- prompt must be non-empty.

Example body:

```json
{"mode": "grok-imagine", "generation_type": "text-to-video", "prompt": "A cat DJ spinning records in a neon club, crowd cheering", "duration": "6", "video_quality": "480p", "aspect_ratio": "1:1", "grokMode": "normal"}
```

### `grok-imagine` · `image-to-video`

Animate one or more images into a 6-30 second video with audio using xAI Grok Imagine.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty). |
| `duration` 💲 | string | 6–30 | "6" | Integer seconds sent as a string, 6-30. |
| `video_quality` 💲 | string | "480p", "720p" | "720p" | Output resolution: 480p or 720p. Always send `video_quality`. |
| `grokMode` | string | "fun", "normal", "spicy" | "normal" | Grok style mode: fun, normal or spicy. |
| `aspect_ratio` | string | "2:3", "3:2", "1:1", "9:16", "16:9" |  | Output aspect ratio; use one of the listed values. When omitted, a single-image request follows the image and a multi-image request uses 16:9. |
| `images` | array |  |  | Optional array of all image URLs when more than one image is used (the first one also goes in `image`). |
| `image` | string |  |  | First image URL. Required unless you send it as images[0]. |

Input files:
- `image`: First image URL.
- `images`: Optional array of up to 7 image URLs when more than one image is used (jpg/png/webp, max 10MB each).

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-grok-imagine`

Rules:
- image-to-video requires image or images (400).
- Send at most 7 images.
- aspect_ratio only applies when more than one image is used; with a single image the output follows the image.
- duration must be an integer string between 6 and 30 (400 otherwise); omitted duration defaults to 6.
- video_quality, when sent, must be 480p or 720p (400 otherwise).
- grokMode must be fun, normal or spicy; aspect_ratio must be one of the listed values.
- prompt must be non-empty.

Example body:

```json
{"mode": "grok-imagine", "generation_type": "image-to-video", "prompt": "She turns toward the camera and laughs as the wind blows her hair", "image": "https://example.com/portrait.jpg", "duration": "6", "video_quality": "480p", "aspect_ratio": "1:1", "grokMode": "normal"}
```

## Kling 2.6 — `kling-2-6`

### `kling-2-6` · `text-to-video`

Generates a cinematic video with optional synced native audio from a text prompt using Kling 2.6.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty, max 20000 characters). |
| `negative_prompt` | string |  |  | Optional things to avoid (max 2000 characters). |
| `duration` 💲 | string | "5", "10" | "5" | Seconds, sent as a string: "5" or "10". |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | "16:9" | Output aspect ratio. |
| `generate_audio` 💲 | boolean |  | true | Generate native audio. |

Rules:
- duration must be '5' or '10'; aspect_ratio must be one of 16:9, 9:16, 1:1.

Example body:

```json
{"mode": "kling-2-6", "generation_type": "text-to-video", "prompt": "A red fox running through a snowy forest at sunrise, cinematic", "duration": "5", "aspect_ratio": "16:9", "generate_audio": true}
```

### `kling-2-6` · `image-to-video`

Animates a start image into a video guided by a text prompt, with optional synced native audio, using Kling 2.6.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt describing the motion (required, non-empty). |
| `image` **required** | string |  |  | Public URL of the start frame image. |
| `negative_prompt` | string |  |  | Optional things to avoid (max 2000 characters). |
| `duration` 💲 | string | "5", "10" | "5" | Seconds, sent as a string: "5" or "10". |
| `aspect_ratio` | string | "16:9" | "16:9" | Send 16:9; the output follows the input image's aspect ratio. |
| `generate_audio` 💲 | boolean |  | true | Generate native audio. |

Input files:
- `image`: 1 image URL used as the start frame (JPEG/PNG/WebP, max 10MB)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-kling26`

Rules:
- image (or images[0]) is required for image-to-video, otherwise 400 'Image is required for image-to-video generation'.
- Only one image is used (start frame); there is no end-frame support for Kling 2.6.
- duration must be '5' or '10'.

Example body:

```json
{"mode": "kling-2-6", "generation_type": "image-to-video", "prompt": "The woman slowly turns her head and smiles", "image": "https://cdn.veevid.ai/sample/motion-control-image-1.webp", "duration": "5", "aspect_ratio": "16:9", "generate_audio": true}
```

## Kling 3.0 — `kling-3`

### `kling-3` · `text-to-video`

Generates a 3-15 second video with optional native audio from a text prompt or a multi-shot prompt list using Kling 3.0 Standard/Pro.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Single text prompt. Required unless `multi_prompt` is used; send either `prompt` or `multi_prompt`, not both (send `prompt` as an empty string when using `multi_prompt`). |
| `multi_prompt` | array |  |  | Multi-shot prompts: array of {prompt: string (max 5000 characters), duration: string seconds 3-15}. Set `duration` to the sum of item durations. |
| `model_version` 💲 | string | "kling-3-standard", "kling-3-pro" | "kling-3-standard" | Standard or Pro quality tier. |
| `duration` 💲 | string | 3–15 | "5" | Total seconds as a string, integer step 1. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | "16:9" | Output aspect ratio. |
| `generate_audio` 💲 | boolean |  | false | Native audio. When omitted the video is generated without audio (and priced as silent); the website sends true. |
| `shot_type` | string | "customize", "intelligent" | "customize" | 'customize' or 'intelligent'. |
| `cfg_scale` | number | 0–1 | 0.5 | Prompt adherence, 0-1 (step 0.01). |
| `negative_prompt` | string |  |  | Optional things to avoid (max 2000 characters). |

Rules:
- duration must be an integer 3-15.
- aspect_ratio must be one of 16:9, 9:16, 1:1 when provided.
- model_version must be kling-3-standard or kling-3-pro, otherwise 400.
- prompt and multi_prompt must not both be non-empty; with multi_prompt, set `duration` to the sum of item durations.

Example body:

```json
{"mode": "kling-3", "generation_type": "text-to-video", "prompt": "A drone shot flying over a neon-lit city at night, rain reflections", "model_version": "kling-3-standard", "duration": "5", "aspect_ratio": "16:9", "generate_audio": true, "shot_type": "customize", "cfg_scale": 0.5}
```

### `kling-3` · `image-to-video`

Animates a start frame (optionally to an end frame) into a 3-15 second video with optional native audio (Kling 3.0 Standard or Pro).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Text prompt. Required unless multi_prompt is used; never send both non-empty. |
| `image` | string |  |  | Public URL of the start frame. If images is also sent, images[0] takes precedence. |
| `images` | array |  |  | [start_frame_url] or [start_frame_url, end_frame_url]. images[0] is the start frame (takes precedence over image), images[1] the optional end frame. |
| `multi_prompt` | array |  |  | Array of {prompt, duration} for multi-shot generation. Do not combine with an end frame. |
| `model_version` 💲 | string | "kling-3-standard", "kling-3-pro" | "kling-3-standard" |  |
| `duration` 💲 | string | 3–15 | "5" | Total seconds as a string. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | "16:9" |  |
| `generate_audio` 💲 | boolean |  | false | Native audio. When omitted the video is generated without audio (and priced as silent); the website sends true. |
| `shot_type` | string | "customize" | "customize" | Send 'customize'. |
| `cfg_scale` | number | 0–1 | 0.5 |  |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars); omit when empty. |

Input files:
- `image`: 1 image URL (start frame); JPEG/PNG/WebP, max 10MB
- `images`: 1-2 image URLs: [start_frame] or [start_frame, end_frame]; only the first two are used

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-kling3`, images → `video-generator-kling3`

Rules:
- image or images[0] is required, otherwise 400 'Image is required for image-to-video generation'.
- duration must be an integer 3-15; aspect_ratio one of 16:9, 9:16, 1:1; model_version kling-3-standard or kling-3-pro.
- images[1] is used as the end frame; an end frame cannot be combined with multi_prompt.

Example body:

```json
{"mode": "kling-3", "generation_type": "image-to-video", "prompt": "The character walks toward the camera as the wind blows her hair", "image": "https://cdn.veevid.ai/sample/motion-control-image-1.webp", "images": ["https://cdn.veevid.ai/sample/motion-control-image-1.webp"], "model_version": "kling-3-pro", "duration": "5", "aspect_ratio": "16:9", "generate_audio": true, "shot_type": "customize", "cfg_scale": 0.5}
```

## LTX 2.5 — `ltx-2-5`

### `ltx-2-5` · `text-to-video`

Generates a 720p-4K video with native audio from a text prompt using LTX 2.5 Fast or Pro; with a driving audio file it animates a scene to that audio (audio-to-video).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty). |
| `model_version` 💲 | string | "ltx-2.5-fast", "ltx-2.5-pro" | "ltx-2.5-fast" | Fast or Pro tier. Fast: 720p-2160p, 6-20s. Pro: 720p/1080p, 6/8/10s. |
| `duration` 💲 | string | "6", "8", "10", "12", "14", "16", "18", "20" | "6" | Seconds, sent as a string. Pro supports only 6/8/10; 12-20 require ltx-2.5-fast. Ignored when `audio` is sent (the clip is as long as the audio). |
| `video_quality` 💲 | string | "720p", "1080p", "1440p", "2160p" | "1080p" | Output resolution. Pro supports only 720p/1080p. Fast longer than 10s supports only 720p/1080p. Ignored when `audio` is sent (always 1080p). |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" | 16:9 or 9:16 ('auto' is also accepted when `audio` is sent). 16:9 when omitted. |
| `target_fps` | number | 24, 25, 48, 50 | 25 | Frames per second. Pro: 24, 25 or 50. Fast: 24, 25, 48 or 50; Fast longer than 10s only 24 or 25. Ignored when `audio` is sent. |
| `generate_audio` | boolean |  | true | Generate a native audio track. Same price either way. Ignored when `audio` is sent. |
| `camera_motion` | string | "dolly_in", "dolly_out", "dolly_left", "dolly_right", "jib_up", "jib_down", "static", "focus_shift" |  | Optional camera move. Omit to let the prompt decide. Not allowed together with `audio` (400). |
| `audio` 💲 | string |  |  | Optional driving audio (2-20s; Pro 2-10s). Switches to audio-to-video: the clip follows the audio and is as long as it, always at 1080p. The price then depends on the audio length. Must be a file uploaded with `POST /api/storage/upload` to folder 'ltx25/audio'; any other URL is rejected with 400 before charging. |
| `input_audio_duration` 💲 | number | 2–20 |  | Length of the driving audio in seconds. The server measures the uploaded file and uses the measured length (your value is used only when it is within 0.15s of the measurement). Needed only to quote before uploading the audio. |
| `guidance_scale` | number | 1–50 |  | Audio-to-video only (400 without `audio`). Omit to use the model default. |

Input files:
- `audio`: Optional: 1 driving audio file (2-20s, Pro 2-10s; max 15MB), uploaded to folder 'ltx25/audio'

Upload folders (`folder` for `POST /api/storage/upload`): audio → `ltx25/audio`

Rules:
- text-to-video does not accept images (400); use image-to-video.
- duration must be one of '6','8','10' for ltx-2.5-pro and '6'-'20' (even) for ltx-2.5-fast (400 otherwise).
- video_quality must be 720p or 1080p for ltx-2.5-pro; 720p, 1080p, 1440p or 2160p for ltx-2.5-fast (400 otherwise).
- ltx-2.5-fast longer than 10s supports only 720p/1080p and 24/25 fps (400 otherwise).
- Invalid combinations are rejected with 400 before charging; nothing is silently downgraded.
- `audio` must be uploaded first with `POST /api/storage/upload` (folder 'ltx25/audio'); external URLs and files in other folders are rejected with 400 before charging.
- If the server cannot read the length of the uploaded audio file, the request is rejected with 400; re-encode it as MP3 or WAV and upload again.
- Audio must be 2-20s long (Pro: 2-10s), measured on the server (400 otherwise).
- With `audio`: duration, video_quality, target_fps and generate_audio are ignored; camera_motion and an end image are rejected (400).
- To quote audio-to-video, send the uploaded `audio` URL (the quote measures the file). Before uploading, send `has_audio_input: true` and `input_audio_duration` instead.
- Generation is async; poll by generation_id.

Example body:

```json
{"mode": "ltx-2-5", "generation_type": "text-to-video", "prompt": "A slow cinematic dolly shot through a neon-lit rainy street at night", "model_version": "ltx-2.5-fast", "duration": "6", "video_quality": "720p", "aspect_ratio": "16:9", "target_fps": 25, "generate_audio": true}
```

### `ltx-2-5` · `image-to-video`

Animates a start image (optionally toward an end image) into a 720p-4K video with native audio using LTX 2.5 Fast or Pro; with a driving audio file it animates the image to that audio (audio-to-video).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Text prompt describing the motion. Required unless `audio` is sent. |
| `image` | string |  |  | Public URL of the start (first-frame) image. Required unless you send it as images[0]; when both are sent they are merged (image first, duplicates removed). |
| `images` | string[] |  |  | [start_url] or [start_url, end_url]. The second image is used as the end frame (not allowed with `audio`). More than 2 images is rejected (400). |
| `model_version` 💲 | string | "ltx-2.5-fast", "ltx-2.5-pro" | "ltx-2.5-fast" | Fast or Pro tier. Fast: 720p-2160p, 6-20s. Pro: 720p/1080p, 6/8/10s. |
| `duration` 💲 | string | "6", "8", "10", "12", "14", "16", "18", "20" | "6" | Seconds, sent as a string. Pro supports only 6/8/10; 12-20 require ltx-2.5-fast. Ignored when `audio` is sent (the clip is as long as the audio). |
| `video_quality` 💲 | string | "720p", "1080p", "1440p", "2160p" | "1080p" | Output resolution. Pro supports only 720p/1080p. Fast longer than 10s supports only 720p/1080p. Ignored when `audio` is sent (always 1080p). |
| `aspect_ratio` | string | "auto", "16:9", "9:16" | "16:9" | 'auto' follows the start image; otherwise 16:9 or 9:16. 16:9 when omitted (send 'auto' to keep the image's framing). |
| `target_fps` | number | 24, 25, 48, 50 | 25 | Frames per second. Pro: 24, 25 or 50. Fast: 24, 25, 48 or 50; Fast longer than 10s only 24 or 25. Ignored when `audio` is sent. |
| `generate_audio` | boolean |  | true | Generate a native audio track. Same price either way. Ignored when `audio` is sent. |
| `camera_motion` | string | "dolly_in", "dolly_out", "dolly_left", "dolly_right", "jib_up", "jib_down", "static", "focus_shift" |  | Optional camera move. Omit to let the prompt decide. Not allowed together with `audio` (400). |
| `audio` 💲 | string |  |  | Optional driving audio (2-20s; Pro 2-10s). Switches to audio-to-video: the clip follows the audio and is as long as it, always at 1080p. The price then depends on the audio length. Must be a file uploaded with `POST /api/storage/upload` to folder 'ltx25/audio'; any other URL is rejected with 400 before charging. |
| `input_audio_duration` 💲 | number | 2–20 |  | Length of the driving audio in seconds. The server measures the uploaded file and uses the measured length (your value is used only when it is within 0.15s of the measurement). Needed only to quote before uploading the audio. |
| `guidance_scale` | number | 1–50 |  | Audio-to-video only (400 without `audio`). Omit to use the model default. |

Input files:
- `image`: 1 image URL used as the first frame
- `images`: Optional: [start, end] - 2 image URLs; the second is used as the last frame
- `audio`: Optional: 1 driving audio file (2-20s, Pro 2-10s; max 15MB), uploaded to folder 'ltx25/audio'

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-ltx25`, end image → `video-generator-ltx25-end`, audio → `ltx25/audio`

Rules:
- image-to-video requires a start image in image or images (400 'LTX 2.5 image-to-video requires a start image').
- Start frame = first image; end frame = second image if present. End image does not change the price.
- duration must be one of '6','8','10' for ltx-2.5-pro and '6'-'20' (even) for ltx-2.5-fast (400 otherwise).
- video_quality must be 720p or 1080p for ltx-2.5-pro; 720p, 1080p, 1440p or 2160p for ltx-2.5-fast (400 otherwise).
- ltx-2.5-fast longer than 10s supports only 720p/1080p and 24/25 fps (400 otherwise).
- Invalid combinations are rejected with 400 before charging; nothing is silently downgraded.
- `audio` must be uploaded first with `POST /api/storage/upload` (folder 'ltx25/audio'); external URLs and files in other folders are rejected with 400 before charging.
- If the server cannot read the length of the uploaded audio file, the request is rejected with 400; re-encode it as MP3 or WAV and upload again.
- Audio must be 2-20s long (Pro: 2-10s), measured on the server (400 otherwise).
- With `audio`: duration, video_quality, target_fps and generate_audio are ignored; camera_motion and an end image are rejected (400).
- To quote audio-to-video, send the uploaded `audio` URL (the quote measures the file). Before uploading, send `has_audio_input: true` and `input_audio_duration` instead.
- Generation is async; poll by generation_id.

Example body:

```json
{"mode": "ltx-2-5", "generation_type": "image-to-video", "prompt": "The woman turns toward the camera and smiles as the wind moves her hair", "image": "https://example.com/start.jpg", "images": ["https://example.com/start.jpg"], "model_version": "ltx-2.5-fast", "duration": "6", "video_quality": "1080p", "aspect_ratio": "auto", "target_fps": 25, "generate_audio": true}
```

## LTX 2.3 — `ltx-2-3`

### `ltx-2-3` · `text-to-video`

Generates a high-resolution (1080p-2160p) video with optional native audio from a text prompt using LTX 2.3 or LTX 2.3 Fast.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty, max 20000 chars). |
| `model_version` 💲 | string | "ltx-2.3", "ltx-2.3-fast" | "ltx-2.3" | Standard or Fast variant. Use one of the listed values. |
| `duration` **required** 💲 | string | "6", "8", "10", "12", "14", "16", "18", "20" |  | Seconds, sent as a string. Standard ('ltx-2.3') only supports 6/8/10; 12-20 require 'ltx-2.3-fast'. Always send it explicitly. |
| `video_quality` 💲 | string | "1080p", "1440p", "2160p" | "1080p" | Output resolution. Forced to 1080p when model_version is 'ltx-2.3-fast' and duration > 10. |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" | 16:9 or 9:16 for text-to-video. |
| `target_fps` | number | 24, 25, 48, 50 | 24 | Frames per second: 24, 25, 48 or 50. Send it explicitly (24 is used when omitted). Forced to 25 when model_version is 'ltx-2.3-fast' and duration > 10. |
| `generate_audio` | boolean |  | true | Generate native audio track. |

Rules:
- Always send `duration`; it must be one of '6','8','10','12','14','16','18','20' (400 otherwise).
- model_version 'ltx-2.3' supports only duration 6/8/10; 'ltx-2.3-fast' supports 6-20 (even). Other combinations make the generation fail.
- video_quality must be one of 1080p, 1440p, 2160p (400 otherwise); defaults to 1080p.
- target_fps must be 24, 25, 48 or 50; other values make the generation fail.
- With ltx-2.3-fast and duration > 10, output is always 1080p at 25 fps and priced at 1080p.
- aspect_ratio: use one of the listed values.
- Generation is async; poll by generation_id.

Example body:

```json
{"mode": "ltx-2-3", "generation_type": "text-to-video", "prompt": "A slow cinematic dolly shot through a neon-lit rainy street at night", "model_version": "ltx-2.3", "duration": "6", "video_quality": "1080p", "aspect_ratio": "16:9", "target_fps": 25, "generate_audio": true}
```

### `ltx-2-3` · `image-to-video`

Animates a start image (optionally toward an end image) into a high-resolution video with optional native audio using LTX 2.3 or LTX 2.3 Fast.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt describing the motion (required, non-empty, max 20000 chars). |
| `image` | string |  |  | Public URL of the start (first-frame) image. Required unless you send images; when both are sent, images[0] is used. |
| `images` | string[] |  |  | [start_url] or [start_url, end_url]. images[1], if present, is used as the end frame. |
| `model_version` 💲 | string | "ltx-2.3", "ltx-2.3-fast" | "ltx-2.3" | Standard or Fast variant. Use one of the listed values. |
| `duration` **required** 💲 | string | "6", "8", "10", "12", "14", "16", "18", "20" |  | Seconds, sent as a string. Standard only supports 6/8/10; 12-20 require 'ltx-2.3-fast'. Always send it explicitly. |
| `video_quality` 💲 | string | "1080p", "1440p", "2160p" | "1080p" | Output resolution. Forced to 1080p when Fast and duration > 10. |
| `aspect_ratio` | string | "auto", "16:9", "9:16" | "16:9" | 'auto' follows the input image; otherwise 16:9 or 9:16. |
| `target_fps` | number | 24, 25, 48, 50 | 24 | Frames per second: 24, 25, 48 or 50. Send it explicitly (24 is used when omitted). Forced to 25 when Fast and duration > 10. |
| `generate_audio` | boolean |  | true | Generate native audio track. |

Input files:
- `image`: 1 image URL used as the first frame (JPEG/PNG/GIF, max 10MB)
- `images`: Optional: [start, end] - 2 image URLs; the second is used as the last frame

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-ltx23`, end image → `video-generator-ltx23-end`

Rules:
- image-to-video requires image or a non-empty images array (400 'Image is required for image-to-video generation').
- Start frame = image (or images[0] if image is absent); end frame = images[1] if present.
- Always send `duration`; it must be one of '6','8','10','12','14','16','18','20' (400 otherwise).
- model_version 'ltx-2.3' supports only duration 6/8/10; 'ltx-2.3-fast' supports 6-20 (even). Other combinations make the generation fail.
- video_quality must be one of 1080p, 1440p, 2160p (400 otherwise); defaults to 1080p.
- target_fps must be 24, 25, 48 or 50; other values make the generation fail.
- With ltx-2.3-fast and duration > 10, output is always 1080p at 25 fps and priced at 1080p.
- aspect_ratio: use one of the listed values.
- End image does not change the price.

Example body:

```json
{"mode": "ltx-2-3", "generation_type": "image-to-video", "prompt": "The woman turns toward the camera and smiles as the wind moves her hair", "image": "https://example.com/start.jpg", "images": ["https://example.com/start.jpg"], "model_version": "ltx-2.3", "duration": "6", "video_quality": "1080p", "aspect_ratio": "16:9", "target_fps": 25, "generate_audio": true}
```

## Wan Animate — `wan-animate`

### `wan-animate` · `image-to-video`

Animates a character image with the motion of a reference video (animate), or replaces the person in the reference video with the character (replace).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `image` **required** | string |  |  | Public URL of the character image. |
| `video` **required** | string |  |  | Public URL of the reference (driving) video, up to 120 seconds. |
| `animationMode` | string | "animate", "replace" | "animate" | 'animate' = character performs the reference video's motion; 'replace' = character replaces the person in the reference video. |
| `video_quality` **required** 💲 | string | "480p", "720p" |  | Output resolution. Always send it ('480p' or '720p'). |
| `duration` 💲 | string | 1–120 | "5" | Reference video length in whole seconds (rounded up), as a string. Send the real length of the reference video; it determines the price (5 when omitted). |
| `prompt` | string |  |  | Optional text guidance, max 5000 characters; may be empty. |
| `aspect_ratio` | string |  |  | Optional; can be omitted (output follows the inputs). |

Input files:
- `image`: 1 character image URL (JPEG/PNG/GIF, max 10MB)
- `video`: 1 reference video URL, max 120 seconds (max 200MB)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator`, video → `wan-animate/reference-videos`

Rules:
- image is required (400 'Character image is required for wan-animate generation').
- video is required (400 'Reference video is required for wan-animate generation').
- When sent, duration must be an integer > 0 and <= 120 (400).
- prompt, if sent, must be <= 5000 characters (400).
- generation_type must be 'image-to-video'.
- Always send `video_quality` ('480p' or '720p').
- animationMode must be 'animate' or 'replace'; defaults to 'animate'.
- Send `duration` equal to the reference video length in whole seconds (rounded up).
- Generation is async; poll by generation_id.

Example body:

```json
{"mode": "wan-animate", "generation_type": "image-to-video", "prompt": "", "image": "https://example.com/character.png", "video": "https://example.com/dance.mp4", "duration": "8", "video_quality": "480p", "aspect_ratio": "", "animationMode": "animate"}
```

## Veevid 2.0 Pro — `veevid-2.0-pro`

### `veevid-2.0-pro` · `text-to-video`

Veevid 2.0 Pro text-to-video, 4-15s, Mini/Fast/Standard tiers up to 4K with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Required for text-to-video. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality tier: Mini, Fast or Standard ('seedance-2.0'). Always send `model_version`; when omitted, Standard is used. Mini/Fast support only 480p/720p. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds as an integer string; values outside 4-15 are clamped to 4-15. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution. 1080p/4k are available only with Standard ('seedance-2.0'); with Mini/Fast they are reduced to 720p and priced as 720p. Defaults to 480p; use one of the listed values. |
| `aspect_ratio` | string | "auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | Output aspect ratio; 'auto' adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate native audio. Does not change price. |
| `seed` | integer |  | -1 | Random seed; -1 means random. |

Rules:
- duration is clamped to 4-15 seconds (for both price and output); no range error is returned.
- Always send `model_version`; values other than the Mini/Fast tiers are treated as Standard ('seedance-2.0').
- generate_audio and seed do not affect price.

Example body:

```json
{"mode": "veevid-2.0-pro", "generation_type": "text-to-video", "prompt": "A chef flips a pancake in a sunlit kitchen, slow motion, warm tones", "model_version": "seedance-2.0-fast", "duration": "5", "aspect_ratio": "16:9", "video_quality": "480p", "generate_audio": true, "seed": -1}
```

### `veevid-2.0-pro` · `image-to-video`

Veevid 2.0 Pro image-to-video with first/optional last frame, 4-15s, Mini/Fast/Standard tiers up to 4K with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Optional text prompt (max 20000 chars). |
| `image` | string |  |  | Public https URL of the first-frame image. Required unless you send it as images[0]. |
| `images` | array<string> |  |  | Optional [first_frame_url, last_frame_url]; when 2+ entries are sent, the last one is used as the last frame. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality tier: Mini, Fast or Standard ('seedance-2.0'). Always send `model_version`; when omitted, Standard is used. Mini/Fast support only 480p/720p. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds as an integer string; values outside 4-15 are clamped to 4-15. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution. 1080p/4k are available only with Standard ('seedance-2.0'); with Mini/Fast they are reduced to 720p and priced as 720p. Defaults to 480p; use one of the listed values. |
| `aspect_ratio` | string | "auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | Output aspect ratio; 'auto' adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate native audio. Does not change price. |
| `seed` | integer |  | -1 | Random seed; -1 means random. |

Input files:
- `image`: 1 image URL used as first frame (JPEG/PNG/WebP, max 30MB)
- `images`: optional [first,last] to add a last frame

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance20`

Rules:
- duration is clamped to 4-15 seconds (for both price and output); no range error is returned.
- Always send `model_version`; values other than the Mini/Fast tiers are treated as Standard ('seedance-2.0').
- generate_audio and seed do not affect price.

Example body:

```json
{"mode": "veevid-2.0-pro", "generation_type": "image-to-video", "prompt": "A chef flips a pancake in a sunlit kitchen, slow motion, warm tones", "model_version": "seedance-2.0-fast", "duration": "5", "aspect_ratio": "auto", "video_quality": "480p", "generate_audio": true, "seed": -1, "image": "https://example.com/first-frame.jpg", "images": ["https://example.com/first-frame.jpg"]}
```

## Veevid 2.5 Pro — `veevid-2.5-pro`

### `veevid-2.5-pro` · `text-to-video`

Veevid 2.5 Pro text-to-video, one-take videos 4-30s up to 1080p with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). A prompt or at least one image is required. |
| `duration` 💲 | string | 4–30 | "5" | Output length: integer string 4-30, or '-1' to let the model choose the length. Anything else returns 400. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution (1080p is 10-bit HEVC). Defaults to 480p; use one of the listed values. |
| `aspect_ratio` | string | "auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | Output aspect ratio; 'auto' adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `output_format` | string | "mp4", "mov" | "mp4" | Container. mov = H.264 yuv444p + PCM audio (poor browser playback). Only mp4/mov are valid for this mode. |
| `generate_audio` | boolean |  | true | Generate native audio. Does not change price. |
| `seed` | integer |  | -1 | Random seed; -1 means random. |

Rules:
- duration must be a pure integer string 4-30 or '-1'; otherwise 400.
- output_format must be mp4 or mov for this mode; image formats (PNG/JPEG) return 400.
- output_format, generate_audio and seed do not affect price.
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.

Example body:

```json
{"mode": "veevid-2.5-pro", "generation_type": "text-to-video", "prompt": "A lighthouse keeper climbs the spiral stairs at dusk, one continuous take", "duration": "5", "aspect_ratio": "16:9", "video_quality": "480p", "output_format": "mp4", "generate_audio": true, "seed": -1}
```

### `veevid-2.5-pro` · `image-to-video`

Veevid 2.5 Pro image-to-video with first/optional last frame, one-take videos 4-30s up to 1080p with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Text prompt (max 20000 chars). A prompt or at least one image is required. |
| `image` | string |  |  | Public https URL of the first-frame image. Required unless you send it as images[0]. |
| `images` | array<string> |  |  | Optional [first_frame_url, last_frame_url]; images[0] is used as first frame and the last entry (when 2+) as last frame. |
| `duration` 💲 | string | 4–30 | "5" | Output length: integer string 4-30, or '-1' to let the model choose the length. Anything else returns 400. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution (1080p is 10-bit HEVC). Defaults to 480p; use one of the listed values. |
| `aspect_ratio` | string | "auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "auto" | Not applied for image-to-video: the output follows the first frame's aspect ratio. Send 'auto'. |
| `output_format` | string | "mp4", "mov" | "mp4" | Container. mov = H.264 yuv444p + PCM audio (poor browser playback). Only mp4/mov are valid for this mode. |
| `generate_audio` | boolean |  | true | Generate native audio. Does not change price. |
| `seed` | integer |  | -1 | Random seed; -1 means random. |

Input files:
- `image`: 1 image URL used as first frame (JPEG/PNG/WebP, max 30MB)
- `images`: optional [first,last] to add a last frame

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance25`

Rules:
- image (or images) is required for image-to-video, else 400.
- For image-to-video the aspect ratio always follows the first frame, regardless of aspect_ratio.
- duration must be a pure integer string 4-30 or '-1'; otherwise 400.
- output_format must be mp4 or mov for this mode; image formats (PNG/JPEG) return 400.
- output_format, generate_audio and seed do not affect price.
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.

Example body:

```json
{"mode": "veevid-2.5-pro", "generation_type": "image-to-video", "prompt": "A lighthouse keeper climbs the spiral stairs at dusk, one continuous take", "duration": "5", "aspect_ratio": "auto", "video_quality": "480p", "output_format": "mp4", "generate_audio": true, "seed": -1, "image": "https://example.com/first-frame.jpg", "images": ["https://example.com/first-frame.jpg"]}
```

## Seedance 2.0 — `seedance-2.0`

### `seedance-2.0` · `text-to-video`

Generates a 4-15s video with optional native audio from a text prompt using ByteDance Seedance 2.0 (Mini/Fast/Standard tiers).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Required for text-to-video. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality tier: 'seedance-2.0-mini', 'seedance-2.0-fast' or 'seedance-2.0' (Standard). Always send `model_version`; when omitted, Standard is used. Mini and Fast support only 480p/720p. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution ('4K' is also accepted as 4k). Defaults to 480p; use one of the listed values. 1080p and 4k are only available with 'seedance-2.0'; with Mini/Fast they fall back to 720p. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds as an integer string (e.g. "5"), 4-15. Out-of-range values are clamped to 4-15; non-numeric values fall back to 5. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | Output aspect ratio; 'auto' (or 'adaptive') adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate native audio track. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |

Rules:
- duration must be a JSON string (e.g. "5"); a number returns 400.
- duration is clamped to 4-15 seconds (for both price and output) instead of being rejected.
- Always send `model_version`; values other than seedance-2.0 / seedance-2.0-fast / seedance-2.0-mini are treated as seedance-2.0 (Standard).
- seedance-2.0-fast and seedance-2.0-mini support only 480p/720p; requested 1080p/4k is reduced to 720p and priced as 720p.
- Credits are deducted at submission (402 if insufficient); unused credits are refunded automatically if the generation fails.

Example body:

```json
{"mode": "seedance-2.0", "generation_type": "text-to-video", "prompt": "A red fox running through fresh snow at sunrise, cinematic tracking shot", "model_version": "seedance-2.0-fast", "video_quality": "480p", "duration": "5", "aspect_ratio": "16:9", "generate_audio": true, "seed": -1}
```

### `seedance-2.0` · `image-to-video`

Animates a first-frame image (optionally with a last-frame image) into a 4-15s video with Seedance 2.0.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Optional text prompt (max 20000 chars) when image or reference inputs are given. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality tier: 'seedance-2.0-mini', 'seedance-2.0-fast' or 'seedance-2.0' (Standard). Always send `model_version`; when omitted, Standard is used. Mini and Fast support only 480p/720p. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution ('4K' is also accepted as 4k). Defaults to 480p; use one of the listed values. 1080p and 4k are only available with 'seedance-2.0'; with Mini/Fast they fall back to 720p. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds as an integer string (e.g. "5"), 4-15. Out-of-range values are clamped to 4-15; non-numeric values fall back to 5. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | Output aspect ratio; 'auto' (or 'adaptive') adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate native audio track. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |
| `image` | string |  |  | First-frame image URL. Required unless you send it as images[0]. |
| `images` | array<string> |  |  | [first] or [first, last]. images[0] is used as first frame (overrides image), and the last element becomes the last frame when length > 1. |

Input files:
- `image`: 1 public image URL used as first frame (JPEG/PNG/WebP, max 30MB)
- `images`: optional [first_frame_url, last_frame_url] for first+last-frame mode

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance20`

Rules:
- duration must be a JSON string (e.g. "5"); a number returns 400.
- duration is clamped to 4-15 seconds (for both price and output) instead of being rejected.
- Always send `model_version`; values other than seedance-2.0 / seedance-2.0-fast / seedance-2.0-mini are treated as seedance-2.0 (Standard).
- seedance-2.0-fast and seedance-2.0-mini support only 480p/720p; requested 1080p/4k is reduced to 720p and priced as 720p.
- Credits are deducted at submission (402 if insufficient); unused credits are refunded automatically if the generation fails.
- aspect_ratio is applied as sent for image-to-video.
- Price is the same as text-to-video (images do not add cost).

Example body:

```json
{"mode": "seedance-2.0", "generation_type": "image-to-video", "prompt": "The woman turns toward the camera and smiles", "image": "https://example.com/first.jpg", "images": ["https://example.com/first.jpg"], "model_version": "seedance-2.0-fast", "video_quality": "720p", "duration": "5", "aspect_ratio": "auto", "generate_audio": true, "seed": -1}
```

### `seedance-2.0` · `reference-to-video`

Generates a 4-15s video guided by multimodal references (up to 9 images, 3 videos, 3 audio clips) with Seedance 2.0 omni reference.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Optional text prompt (max 20000 chars) when image or reference inputs are given. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality tier: 'seedance-2.0-mini', 'seedance-2.0-fast' or 'seedance-2.0' (Standard). Always send `model_version`; when omitted, Standard is used. Mini and Fast support only 480p/720p. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution ('4K' is also accepted as 4k). Defaults to 480p; use one of the listed values. 1080p and 4k are only available with 'seedance-2.0'; with Mini/Fast they fall back to 720p. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds as an integer string (e.g. "5"), 4-15. Out-of-range values are clamped to 4-15; non-numeric values fall back to 5. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | Output aspect ratio; 'auto' (or 'adaptive') adapts to the content. Use one of the listed values; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate native audio track. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |
| `images` | array<string> |  |  | Reference image URLs (role reference_image). Max 9; extras are ignored. |
| `videos` 💲 | array<string> |  |  | Reference video URLs (role reference_video), mp4/mov. Max 3; extras are ignored. |
| `input_video_duration` 💲 | number | 0–15 |  | Total seconds of all reference videos (rounded up). Required when videos are sent; must equal the total reference video length. >15 is rejected with 400; values below 2 are priced as 2. |
| `audio` | string |  |  | Optional; if sent, set it to the first reference audio URL (audios[0]). |
| `audios` | array<string> |  |  | Reference audio URLs (role reference_audio). Max 3, .wav/.mp3, total <= 15s; extras are ignored. Audio cannot be the only reference: at least one image or video is required. |

Input files:
- `images`: 0-9 reference image URLs (JPEG/PNG/WebP; max 30MB each)
- `videos`: 0-3 reference video URLs (mp4/mov, max 50MB each, total <= 15s)
- `audios`: 0-3 reference audio URLs (wav/mp3, max 15MB each, total <= 15s); requires at least one image or video

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance20`, video → `seedance20/reference-videos`, audio → `seedance20/audio`

Rules:
- duration must be a JSON string (e.g. "5"); a number returns 400.
- duration is clamped to 4-15 seconds (for both price and output) instead of being rejected.
- Always send `model_version`; values other than seedance-2.0 / seedance-2.0-fast / seedance-2.0-mini are treated as seedance-2.0 (Standard).
- seedance-2.0-fast and seedance-2.0-mini support only 480p/720p; requested 1080p/4k is reduced to 720p and priced as 720p.
- Credits are deducted at submission (402 if insufficient); unused credits are refunded automatically if the generation fails.
- At least one reference image or video is required (audio-only is not allowed); otherwise the generation fails.
- When sending videos, send `input_video_duration` equal to the total reference video length in seconds (rounded up); > 15 is rejected with 400.
- Send at most 9 images, 3 videos and 3 audios; extras are ignored.
- Without reference videos (images/audio only), price equals the text-to-video price.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send reference videos (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.0", "generation_type": "reference-to-video", "prompt": "The character from image 1 dances in the style of video 1", "images": ["https://example.com/character.png"], "videos": ["https://example.com/dance.mp4"], "input_video_duration": 6, "model_version": "seedance-2.0-fast", "video_quality": "480p", "duration": "5", "aspect_ratio": "auto", "generate_audio": true, "seed": -1}
```

## Seedance 2.5 — `seedance-2.5`

### `seedance-2.5` · `text-to-video`

Generates a 4-30s one-take video with optional native audio from a text prompt using ByteDance Seedance 2.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Required for text-to-video. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution; always send `video_quality` explicitly. 1080p is 10-bit HEVC (may not play in some browsers). '4k'/'4K'/'2160p' are treated as 1080p. |
| `duration` 💲 | string | 4–30 | "5" | Output seconds as a string containing a plain integer from 4 to 30, or "-1" to let the model choose the length. Anything else (e.g. "3", "31", "5.0", "0x10") is rejected with 400. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | Output aspect ratio; 'auto' lets the model choose. Send `aspect_ratio` explicitly and use one of the listed values. |
| `output_format` | string | "mp4", "mov" | "mp4" | Output container. mov = H.264 yuv444p with PCM audio (often not playable in browsers). Any other value is rejected with 400. |
| `generate_audio` | boolean |  | true | Generate a native audio track. Default true. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |

Rules:
- duration must be a JSON string matching /^-?\d+$/ and equal -1 or 4-30, otherwise 400
- output_format must be mp4 or mov (400 otherwise)
- Always send `video_quality` as 480p, 720p or 1080p ('4k' is treated as 1080p)
- No model_version parameter (single tier)
- Price can be previewed with POST /api/quote; /api/generate-video returns 402 if credits are insufficient. Credits for failed generations are refunded automatically.
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.

Example body:

```json
{"mode": "seedance-2.5", "generation_type": "text-to-video", "prompt": "A lighthouse keeper climbs the spiral stairs at dusk, one continuous shot", "video_quality": "480p", "duration": "5", "aspect_ratio": "16:9", "output_format": "mp4", "generate_audio": true, "seed": -1}
```

### `seedance-2.5` · `image-to-video`

Animates a first-frame image (optionally to a last-frame image) into a 4-30s video with Seedance 2.5; aspect ratio follows the input image.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Text prompt (max 20000 chars). Optional when a first-frame image is given. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution; always send `video_quality` explicitly. 1080p is 10-bit HEVC (may not play in some browsers). '4k'/'4K'/'2160p' are treated as 1080p. |
| `duration` 💲 | string | 4–30 | "5" | Output seconds as a string containing a plain integer from 4 to 30, or "-1" to let the model choose the length. Anything else (e.g. "3", "31", "5.0", "0x10") is rejected with 400. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "auto" | Ignored for image-to-video: the output aspect ratio follows the first-frame image. |
| `output_format` | string | "mp4", "mov" | "mp4" | Output container. mov = H.264 yuv444p with PCM audio (often not playable in browsers). Any other value is rejected with 400. |
| `generate_audio` | boolean |  | true | Generate a native audio track. Default true. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |
| `image` | string |  |  | First-frame image URL (or provide images[0]). |
| `images` | array<string> |  |  | [first_frame_url] or [first_frame_url, last_frame_url]. images[0] is the first frame (overrides image); when there is more than one entry, the last element is used as the last frame. |

Input files:
- `image`: 1 public image URL used as the first frame (JPEG/PNG/WEBP; max 30MB)
- `images`: optional [first_frame_url, last_frame_url]

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance25`

Rules:
- duration must be a JSON string matching /^-?\d+$/ and equal -1 or 4-30, otherwise 400
- output_format must be mp4 or mov (400 otherwise)
- Always send `video_quality` as 480p, 720p or 1080p ('4k' is treated as 1080p)
- No model_version parameter (single tier)
- Price can be previewed with POST /api/quote; /api/generate-video returns 402 if credits are insufficient. Credits for failed generations are refunded automatically.
- image-to-video requires `image` or `images` (400 'Image is required for image-to-video generation')
- aspect_ratio has no effect for image-to-video; the output follows the first-frame image
- Price is the same as text-to-video (images do not add cost)
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.

Example body:

```json
{"mode": "seedance-2.5", "generation_type": "image-to-video", "prompt": "The camera slowly pushes in as leaves drift past", "image": "https://example.com/first.jpg", "images": ["https://example.com/first.jpg", "https://example.com/last.jpg"], "video_quality": "720p", "duration": "8", "aspect_ratio": "auto", "output_format": "mp4", "generate_audio": true, "seed": -1}
```

### `seedance-2.5` · `reference-to-video`

Generates a 4-30s video guided by up to 30 reference images, 10 reference videos and 10 reference audio clips (audio-only allowed) with Seedance 2.5.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Text prompt (max 20000 chars). Optional when reference assets are given; can refer to them (e.g. 'image 1', 'video 1'). |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution; always send `video_quality` explicitly. 1080p is 10-bit HEVC (may not play in some browsers). '4k'/'4K'/'2160p' are treated as 1080p. |
| `duration` 💲 | string | 4–30 | "5" | Output seconds as a string containing a plain integer from 4 to 30, or "-1" to let the model choose the length. Anything else (e.g. "3", "31", "5.0", "0x10") is rejected with 400. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | Output aspect ratio; 'auto' lets the model choose. Send `aspect_ratio` explicitly and use one of the listed values. |
| `output_format` | string | "mp4", "mov" | "mp4" | Output container. mov = H.264 yuv444p with PCM audio (often not playable in browsers). Any other value is rejected with 400. |
| `generate_audio` | boolean |  | true | Generate a native audio track. Default true. |
| `seed` | integer |  | -1 | Random seed; -1 = random. |
| `images` | array<string> |  |  | Reference image URLs. Max 30. |
| `videos` 💲 | array<string> |  |  | Reference video URLs (mp4/mov). Max 10, total length <= 30s. Including reference videos switches to reference-video pricing. |
| `input_video_duration` 💲 | number | 0–30 |  | Total length in seconds of all reference videos (round the sum up to a whole second). Max 30; larger values are rejected with 400. Send it equal to the total reference video length whenever `videos` is sent. Minimum billed input length is 2s. |
| `audio` | string |  |  | Optional single reference audio URL; may be the same as audios[0]. |
| `audios` | array<string> |  |  | Reference audio URLs (wav/mp3). Max 10, total length <= 30s. Audio-only reference is allowed. |

Input files:
- `images`: 0-30 reference image URLs (JPEG/PNG/WEBP; max 30MB each)
- `videos`: 0-10 reference video URLs (mp4/mov, max 50MB each, total <= 30s)
- `audios`: 0-10 reference audio URLs (wav/mp3, max 15MB each, total <= 30s)

Upload folders (`folder` for `POST /api/storage/upload`): image → `seedance25`, video → `seedance25/reference-videos`, audio → `seedance25/audio`

Rules:
- duration must be a JSON string matching /^-?\d+$/ and equal -1 or 4-30, otherwise 400
- output_format must be mp4 or mov (400 otherwise)
- Always send `video_quality` as 480p, 720p or 1080p ('4k' is treated as 1080p)
- No model_version parameter (single tier)
- Price can be previewed with POST /api/quote; /api/generate-video returns 402 if credits are insufficient. Credits for failed generations are refunded automatically.
- At least one reference image, video or audio is required; the generation fails otherwise
- Send `input_video_duration` equal to the total reference video length (seconds) whenever `videos` is sent; values > 30 are rejected with 400
- aspect_ratio is honored for reference-to-video
- Without reference videos (images/audio only), price equals text-to-video price
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send reference videos (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.5", "generation_type": "reference-to-video", "prompt": "The product from image 1 rotates on a marble table, lit like video 1", "images": ["https://example.com/product.png"], "videos": ["https://example.com/lighting.mp4"], "input_video_duration": 8, "video_quality": "480p", "duration": "10", "aspect_ratio": "9:16", "output_format": "mp4", "generate_audio": true, "seed": -1}
```

## Wan 2.6 — `wan-2-6`

### `wan-2-6` · `text-to-video`

Generates a 5-15 second video with synchronized audio from a text prompt using Wan 2.6.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `duration` 💲 | string | "5", "10", "15" | "5" | Output seconds, sent as a string. |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution. Use one of the listed values. |
| `seed` | integer |  | -1 | Random seed; -1 = random, otherwise 0-2147483647. |
| `enable_prompt_expansion` | boolean |  | true | Let the model rewrite/expand the prompt. |
| `shot_type` | string | "single", "multi" | "single" | multi = multi-shot video. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio. Use one of the listed values. |
| `audio` | string |  |  | Optional driving/background audio URL (mp3/ogg/wav/m4a/aac, max 15MB) for audio-visual sync. |

Input files:
- `audio`: optional 1 audio URL (mp3/ogg/wav/m4a/aac)

Upload folders (`folder` for `POST /api/storage/upload`): audio → `wan26/audio`

Rules:
- duration must be one of 5, 10, 15 (default 5)
- video_quality and aspect_ratio are not validated; always send one of the listed values

Example body:

```json
{"mode": "wan-2-6", "generation_type": "text-to-video", "prompt": "A red fox running through fresh snow at sunrise, cinematic", "duration": "5", "video_quality": "720p", "aspect_ratio": "16:9"}
```

### `wan-2-6` · `image-to-video`

Animates a single image into a 5-15 second video with Wan 2.6.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `image` **required** | string |  |  | Public https URL of the source image (used as the first frame). |
| `duration` 💲 | string | "5", "10", "15" | "5" | Output seconds, sent as a string. |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution. Use one of the listed values. |
| `seed` | integer |  | -1 | Random seed; -1 = random, otherwise 0-2147483647. |
| `enable_prompt_expansion` | boolean |  | true | Let the model rewrite/expand the prompt. |
| `shot_type` | string | "single", "multi" | "single" | multi = multi-shot video. |
| `audio` | string |  |  | Optional driving/background audio URL (mp3/ogg/wav/m4a/aac, max 15MB) for audio-visual sync. |

Input files:
- `image`: 1 image URL (first frame); jpg/png/webp, max 10MB
- `audio`: optional 1 audio URL (mp3/ogg/wav/m4a/aac)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator`, audio → `wan26/audio`

Rules:
- image (or images[0]) is required
- aspect_ratio is not used for image-to-video; the output follows the image
- duration must be one of 5, 10, 15

Example body:

```json
{"mode": "wan-2-6", "generation_type": "image-to-video", "prompt": "The character turns and smiles at the camera", "image": "https://example.com/input.jpg", "duration": "5", "video_quality": "720p"}
```

### `wan-2-6` · `reference-to-video`

Generates a new video guided by 1-3 reference videos (subject/motion reference) with Wan 2.6.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `videos` **required** | array<string> |  |  | 1-3 reference video URLs. |
| `video` | string |  |  | Optional single reference video URL; either `video` or `videos` satisfies the requirement. |
| `duration` 💲 | string | "5", "10" | "5" | Output seconds: 5 or 10 (15 is rejected for reference-to-video). |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution. Use one of the listed values. |
| `seed` | integer |  | -1 | Random seed; -1 = random, otherwise 0-2147483647. |
| `enable_prompt_expansion` | boolean |  | true | Let the model rewrite/expand the prompt. |
| `shot_type` | string | "single", "multi" | "single" | multi = multi-shot video. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio. Use one of the listed values. |

Input files:
- `videos`: 1-3 reference video URLs (mp4/mov/mkv; max 10MB each)

Upload folders (`folder` for `POST /api/storage/upload`): video → `wan26/reference-videos`

Rules:
- At least one reference video (video or videos) is required
- At most 3 reference videos
- duration 15 is rejected (only 5 or 10)
- Audio input is not supported for reference-to-video; do not send `audio`

Example body:

```json
{"mode": "wan-2-6", "generation_type": "reference-to-video", "prompt": "The character from the reference video dances in a neon-lit street", "videos": ["https://example.com/ref.mp4"], "duration": "5", "video_quality": "720p", "aspect_ratio": "16:9"}
```

## Wan 2.7 — `wan-2.7`

### `wan-2.7` · `text-to-video`

Generates a 2-15 second video from a text prompt with Wan 2.7 (smoother motion, better scene fidelity).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `duration` 💲 | string | 2–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio. |
| `enable_prompt_expansion` | boolean |  | true | Let the model expand the prompt. |
| `audio` | string |  |  | Optional audio URL to drive the video (mp3/ogg/wav/m4a/aac, max 15MB). |
| `seed` | integer |  | -1 | Random seed; -1 = random. |

Input files:
- `audio`: optional 1 audio URL (mp3/ogg/wav/m4a/aac)

Upload folders (`folder` for `POST /api/storage/upload`): audio → `wan27/audio`

Rules:
- duration must be an integer 2-15 (default 5)
- video_quality, if sent, must be 720p or 1080p
- aspect_ratio, if sent, must be one of 16:9, 9:16, 1:1, 4:3, 3:4

Example body:

```json
{"mode": "wan-2.7", "generation_type": "text-to-video", "prompt": "A paper boat drifting down a rain-soaked city gutter, macro shot", "duration": "5", "video_quality": "720p", "aspect_ratio": "16:9"}
```

### `wan-2.7` · `image-to-video`

Animates a start image (optionally to an end frame) into a 2-15 second video with Wan 2.7.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `image` | string |  |  | Start-frame image URL. Required unless you send it as images[0]. |
| `images` | array<string> |  |  | Only for first/last-frame mode: [start_image_url, end_image_url]; images[1] becomes the end frame. |
| `duration` 💲 | string | 2–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution. |
| `enable_prompt_expansion` | boolean |  | true | Let the model expand the prompt. |
| `audio` | string |  |  | Optional audio URL to drive the video (mp3/ogg/wav/m4a/aac, max 15MB). |
| `seed` | integer |  | -1 | Random seed; -1 = random. |

Input files:
- `image`: 1 start-frame image URL (jpg/png/webp, max 20MB)
- `images`: optional [start, end] pair for first/last-frame interpolation
- `audio`: optional 1 audio URL

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-wan27`, audio → `wan27/audio`

Rules:
- image (or images[0]) is required
- aspect_ratio is not needed for image-to-video (the output follows the image); if sent it must be one of the listed values
- duration must be an integer 2-15

Example body:

```json
{"mode": "wan-2.7", "generation_type": "image-to-video", "prompt": "Gentle wind moves the hair, camera slowly pushes in", "image": "https://example.com/start.jpg", "duration": "5", "video_quality": "720p"}
```

### `wan-2.7` · `reference-to-video`

Generates a video guided by up to 3 reference images and/or up to 3 reference videos with Wan 2.7.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `negative_prompt` | string |  |  | Optional negative prompt (max 2000 chars). Omit when empty. |
| `images` | array<string> |  |  | 0-3 reference image URLs. |
| `videos` | array<string> |  |  | 0-3 reference video URLs. |
| `video` | string |  |  | Optional single reference video URL; may be the same as videos[0]. |
| `duration` 💲 | string | 2–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "720p", "1080p" | "720p" | Output resolution; 720p when omitted. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio. |
| `shot_type` | string | "single", "multi" | "single" | single or multi-shot output. |
| `seed` | integer |  | -1 | Random seed; -1 = random (values >= 0 fix the seed). |

Input files:
- `images`: 0-3 reference image URLs (jpg/png/webp, max 20MB)
- `videos`: 0-3 reference video URLs (mp4/mov, max 100MB each)

Upload folders (`folder` for `POST /api/storage/upload`): image → `video-generator-wan27`, video → `wan27/reference-videos`

Rules:
- At least one reference image or video is required
- At most 3 reference images and at most 3 reference videos
- duration must be an integer 2-15
- audio and enable_prompt_expansion are not supported for reference-to-video

Example body:

```json
{"mode": "wan-2.7", "generation_type": "reference-to-video", "prompt": "The woman from the reference image walks through a sunflower field", "images": ["https://example.com/ref.jpg"], "duration": "5", "video_quality": "720p", "aspect_ratio": "16:9", "shot_type": "single"}
```

## Wan 3.0 — `wan-3.0`

### `wan-3.0` · `text-to-video`

Generates a 2-30 second video with optional native audio from a text prompt using Wan 3.0.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. Required for text-to-video. |
| `duration` 💲 | string | 2–30 | "5" | Output seconds as an integer string (2-30); -1 (smart duration) is rejected. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "720p" | Resolution. Use one of the listed values ('4k' is treated as 1080p). |
| `aspect_ratio` | string | "adaptive", "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio; 'adaptive' lets the model choose. Send `aspect_ratio` explicitly and use one of the listed values. |
| `generate_audio` | boolean |  | true | Generate a synchronized soundtrack (default true; send false to turn it off). Does not change the price. |
| `seed` | integer |  |  | Accepted but currently not passed to the model. |

Rules:
- duration must be an integer 2-30; -1 (smart duration) is rejected
- generate_audio does not change the price

Example body:

```json
{"mode": "wan-3.0", "generation_type": "text-to-video", "prompt": "A drone shot over a misty mountain lake at dawn, birds taking off", "duration": "5", "video_quality": "720p", "aspect_ratio": "adaptive", "generate_audio": true}
```

### `wan-3.0` · `image-to-video`

Animates a first frame (optionally to a last frame) into a 2-30 second video with Wan 3.0.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Motion/scene prompt (optional for image-to-video). |
| `image` | string |  |  | First-frame image URL. Required unless you send it as images[0]. |
| `images` | array<string> |  |  | [first_frame] or [first_frame, last_frame]; images[0] is the first frame and the last element (when 2 or more) is the last frame. |
| `duration` 💲 | string | 2–30 | "5" | Output seconds as an integer string (2-30); -1 (smart duration) is rejected. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "720p" | Resolution. Use one of the listed values ('4k' is treated as 1080p). |
| `aspect_ratio` | string | "adaptive", "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio; 'adaptive' lets the model choose. Send `aspect_ratio` explicitly and use one of the listed values. |
| `generate_audio` | boolean |  | true | Generate a synchronized soundtrack (default true; send false to turn it off). Does not change the price. |
| `seed` | integer |  |  | Accepted but currently not passed to the model. |

Input files:
- `image`: 1 first-frame image URL (jpg/png/webp/bmp/tiff, max 20MB)
- `images`: optional [first, last] frame pair

Upload folders (`folder` for `POST /api/storage/upload`): image → `wan30`

Rules:
- image or images is required
- files (document) and links (webpage) cannot be combined with image-to-video
- duration must be an integer 2-30; -1 rejected

Example body:

```json
{"mode": "wan-3.0", "generation_type": "image-to-video", "prompt": "The cat slowly opens its eyes and yawns", "image": "https://example.com/first.jpg", "images": ["https://example.com/first.jpg"], "duration": "5", "video_quality": "720p", "aspect_ratio": "adaptive", "generate_audio": true}
```

### `wan-3.0` · `reference-to-video`

Generates a 2-30 second video from any mix of reference images, videos, audio, one document (document-to-video) or one webpage (webpage-to-video) with Wan 3.0.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | Instruction describing how to use the references (e.g. refer to 'Image 1', 'Video 1'). |
| `images` | array<string> |  |  | 0-10 reference image URLs. |
| `videos` | array<string> |  |  | 0-5 reference video URLs, total length <= 15s. Always pass reference videos in `videos` (plural), together with `input_video_duration`. |
| `input_video_duration` 💲 | number | 0–15 |  | Total seconds of all reference videos (round the sum up to a whole second; max 15). Send it equal to the total reference video length whenever `videos` is sent. |
| `audios` | array<string> |  |  | 0-5 reference audio URLs (wav/mp3), total <= 15s. |
| `audio` | string |  |  | Single reference audio URL; used only when `audios` is absent. |
| `files` | array<string> |  |  | Document-to-video: at most 1 document URL (.doc .docx .xls .xlsx .ppt .pptx .pdf .txt .md .key .pages .numbers; <=100MB, <=50 pages). Mutually exclusive with links. |
| `links` | array<string> |  |  | Webpage-to-video: at most 1 public webpage URL. Mutually exclusive with files. |
| `duration` 💲 | string | 2–30 | "5" | Output seconds as an integer string (2-30); -1 (smart duration) is rejected. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "720p" | Resolution. Use one of the listed values ('4k' is treated as 1080p). |
| `aspect_ratio` | string | "adaptive", "16:9", "9:16", "1:1", "4:3", "3:4" | "16:9" | Output aspect ratio; 'adaptive' lets the model choose. Send `aspect_ratio` explicitly and use one of the listed values. |
| `generate_audio` | boolean |  | true | Generate a synchronized soundtrack (default true; send false to turn it off). Does not change the price. |
| `seed` | integer |  |  | Accepted but currently not passed to the model. |

Input files:
- `images`: 0-10 image URLs (jpg/png/webp/bmp/tiff, max 20MB each)
- `videos`: 0-5 video URLs (mp4/mov, max 100MB each), combined <= 15s
- `audio`: 0-5 audio URLs via audios (wav/mp3, max 15MB each), combined <= 15s
- `files`: 0-1 document URL (100MB, 50 pages max)
- `links`: 0-1 webpage URL

Upload folders (`folder` for `POST /api/storage/upload`): image → `wan30`, video → `wan30/reference-videos`, audio → `wan30/audio`, document → `wan30/documents`

Rules:
- At most 10 images, 5 videos, 5 audios, 1 file, 1 link (exceeding returns 400, never truncated)
- files and links cannot be sent together
- Provide at least one reference image, video, audio, document or webpage
- input_video_duration must be <= 15, and input_video_duration + duration must be <= 30 (400 otherwise)
- Always pass reference videos in `videos` (plural) and send `input_video_duration` equal to their total length (seconds)
- duration must be an integer 2-30; -1 rejected
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send reference videos (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "wan-3.0", "generation_type": "reference-to-video", "prompt": "Turn this product page into a 10 second promo video", "links": ["https://example.com/product"], "duration": "10", "video_quality": "720p", "aspect_ratio": "16:9", "generate_audio": true}
```

## MiniMax H3 — `minimax-h3`

### `minimax-h3` · `text-to-video`

Generates a 4-15 second video from a text prompt with MiniMax H3 (Hailuo 03) at 768P or 2K.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (max 20000 chars). Always send a non-empty prompt. |
| `duration` 💲 | string | 4–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "768p", "2k" | "768p" | Resolution. '2K', '1440p', '2160p' are treated as 2k. Use one of the listed values. |
| `aspect_ratio` | string | "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | Output aspect ratio. 'adaptive' is not supported for text-to-video; use one of the listed values. |

Rules:
- duration must be an integer between 4 and 15 (400 otherwise); sent as a string
- Seed, negative prompt and audio options are not supported for this model

Example body:

```json
{"mode": "minimax-h3", "generation_type": "text-to-video", "prompt": "A red fox running through fresh snow at sunrise, cinematic tracking shot", "duration": "5", "aspect_ratio": "16:9", "video_quality": "768p"}
```

### `minimax-h3` · `image-to-video`

Animates a first-frame image (optionally toward a last frame) into a 4-15 second MiniMax H3 video at 768P or 2K.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt describing the motion. Always send a non-empty prompt. |
| `duration` 💲 | string | 4–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "768p", "2k" | "768p" |  |
| `image` | string |  |  | First frame image URL. Either image or images[0] must be present. |
| `images` 💲 | string[] |  |  | [first_frame] or [first_frame, last_frame]. images[0] is the first frame; with 2 or more entries the LAST element is used as the last frame. Max 9. |
| `aspect_ratio` | string | "adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "adaptive" | Ignored for image-to-video; the output follows the first frame. |

Input files:
- `image`: 1 public image URL used as the first frame (jpg/png/webp, max 20MB)
- `images`: Optional array [first_frame_url, last_frame_url]; only the first and last entries are used

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3`

Rules:
- image-to-video requires image or a non-empty images array (400 'Image is required for image-to-video generation')
- duration must be an integer 4-15
- At most 9 images
- The last frame is taken from the last element of images only when images has 2 or more entries
- Only the first and last images are used, but every image after the 5th is charged: send at most 2. When quoting with `/api/quote`, send `input_image_count`.

Example body:

```json
{"mode": "minimax-h3", "generation_type": "image-to-video", "prompt": "The woman turns toward the camera and smiles as wind moves her hair", "duration": "5", "aspect_ratio": "adaptive", "video_quality": "768p", "image": "https://example.com/first-frame.jpg", "images": ["https://example.com/first-frame.jpg"]}
```

### `minimax-h3` · `reference-to-video`

Generates a MiniMax H3 video guided by up to 9 reference images, 3 reference videos and 3 reference audio clips.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt; can refer to the reference assets. Always send a non-empty prompt. |
| `duration` 💲 | string | 4–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "768p", "2k" | "768p" |  |
| `aspect_ratio` | string | "adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | 'adaptive' lets the model choose from the references. Use one of the listed values. |
| `images` 💲 | string[] |  |  | Reference image URLs, max 9. |
| `videos` 💲 | string[] |  |  | Reference video URLs, max 3, total duration <= 15s. Singular 'video' is accepted as a fallback when 'videos' is absent. |
| `input_video_duration` 💲 | number | 0–15 |  | Total seconds of the reference videos (max 15). Send it equal to the total reference video length whenever videos are sent. |
| `audios` | string[] |  |  | Reference audio URLs, max 3 (free). |
| `audio` | string |  |  | Singular reference audio; used only if 'audios' is absent. |

Input files:
- `images`: 0-9 reference image URLs (jpg/png/webp/bmp/tiff, 20MB each)
- `video`: 0-3 reference video URLs via 'videos' (mp4/mov, 100MB each, total <= 15s)
- `audio`: 0-3 reference audio URLs via 'audios' (wav/mp3, 15MB each); cannot be the only reference

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3`, video → `minimax-h3/reference-videos`, audio → `minimax-h3/audio`

Rules:
- At most 9 reference images, 3 reference videos, 3 reference audio files (400 if exceeded, no silent truncation)
- At least one reference image or video is required; reference audio cannot be used alone
- input_video_duration must be <= 15 seconds in total
- Send `input_video_duration` equal to the total reference video length (seconds) whenever videos are sent
- duration must be an integer 4-15
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send reference videos (the quote endpoint does not read video URLs, so the price would come out too low). Also send `input_image_count` (number of reference images).

Example body:

```json
{"mode": "minimax-h3", "generation_type": "reference-to-video", "prompt": "The character from image 1 walks into the room from video 1 and waves", "duration": "5", "aspect_ratio": "adaptive", "video_quality": "768p", "images": ["https://example.com/character.png"], "videos": ["https://example.com/room.mp4"], "input_video_duration": 6}
```

## MiniMax H3 Max — `minimax-h3-max`

### `minimax-h3-max` · `text-to-video`

Fast (turbo) MiniMax H3 Max text-to-video, 5-15 seconds at 480P/768P/1080P.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. Required; always send a non-empty prompt. |
| `duration` 💲 | string | 5–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "480p", "768p", "1080p" | "768p" | Use one of the listed values (2k is not supported). |
| `aspect_ratio` | string | "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | 'adaptive' is not supported for text-to-video. Use one of the listed values. |
| `prompt_expansion_mode` | string | "disabled", "fast", "balanced", "quality" | "balanced" | Prompt rewriting strength. Values outside the list are rejected with 400. |
| `seed` | integer |  |  | Optional; a value >= 0 fixes the random seed. |

Rules:
- generation_type must be text-to-video, image-to-video or reference-to-video for this mode (400 otherwise)
- duration must be an integer between 5 and 15

Example body:

```json
{"mode": "minimax-h3-max", "generation_type": "text-to-video", "prompt": "A paper boat drifting down a rainy city gutter, macro shot", "duration": "5", "aspect_ratio": "16:9", "video_quality": "768p", "prompt_expansion_mode": "balanced"}
```

### `minimax-h3-max` · `image-to-video`

Fast MiniMax H3 Max image-to-video from a first frame (optional end frame), 5-15 seconds.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Motion prompt. Required; always send a non-empty prompt. |
| `duration` 💲 | string | 5–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "480p", "768p", "1080p" | "768p" |  |
| `image` | string |  |  | First frame URL (image or images[0] required). |
| `images` | string[] |  |  | [first_frame] or [first_frame, end_frame]. With 2 or more entries, the last one is used as the end frame. |
| `aspect_ratio` | string | "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | Ignored for image-to-video; the output follows the first frame. |
| `prompt_expansion_mode` | string | "disabled", "fast", "balanced", "quality" | "balanced" | Prompt rewriting strength. |
| `seed` | integer |  |  | Optional; a value >= 0 fixes the random seed. |

Input files:
- `image`: 1 public image URL used as the first frame
- `images`: Optional [first_frame_url, end_frame_url]

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3-max`

Rules:
- image-to-video requires a first frame (image or images[0]); 400 otherwise
- duration must be an integer 5-15

Example body:

```json
{"mode": "minimax-h3-max", "generation_type": "image-to-video", "prompt": "The camera slowly pushes in as the dog tilts its head", "duration": "5", "aspect_ratio": "16:9", "video_quality": "768p", "prompt_expansion_mode": "balanced", "image": "https://example.com/dog.jpg", "images": ["https://example.com/dog.jpg"]}
```

### `minimax-h3-max` · `reference-to-video`

Fast MiniMax H3 Max video guided by reference images, videos and audio (up to 12 files total).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt. Required; always send a non-empty prompt. |
| `duration` 💲 | string | 5–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "480p", "768p", "1080p" | "768p" |  |
| `aspect_ratio` | string | "adaptive", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "16:9" | 'adaptive' is available only for reference-to-video. Use one of the listed values. |
| `prompt_expansion_mode` | string | "disabled", "fast", "balanced", "quality" | "balanced" | Prompt rewriting strength. |
| `images` 💲 | string[] |  |  | Reference image URLs, max 9. Resize images so the long edge is <= 1024 px. |
| `videos` 💲 | string[] |  |  | Reference video URLs, max 3, each 2-15s, total <= 15s. Singular 'video' accepted as fallback. |
| `audios` 💲 | string[] |  |  | Reference audio URLs, max 3, each 2-15s, total <= 15s. Singular 'audio' accepted as fallback. |
| `input_video_duration` 💲 | number | 0–15 |  | Total reference video seconds (max 15). Send it equal to the total reference video length whenever videos are sent. |
| `input_audio_duration` 💲 | number | 0–15 |  | Total reference audio seconds (max 15). Send it equal to the total reference audio length whenever audios are sent. |
| `seed` | integer |  |  | Optional; a value >= 0 fixes the random seed. |

Input files:
- `images`: 0-9 reference image URLs (jpg/png/webp, 20MB, long edge <= 1024 px)
- `video`: 0-3 reference video URLs via 'videos' (mp4/mov, 100MB each, 2-15s each, total <= 15s)
- `audio`: 0-3 reference audio URLs via 'audios' (wav/mp3, 15MB each, 2-15s each, total <= 15s); cannot be the only reference

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3-max`, video → `minimax-h3-max/reference-videos`, audio → `minimax-h3-max/audio`

Rules:
- At least one reference image, video or audio is required
- Reference audio cannot be used alone; add at least one image or video
- Max 9 images, 3 videos, 3 audio files, and max 12 files in total
- Reference videos and reference audio each total <= 15s (two separate limits); each clip must be at least 2s
- Send `input_video_duration` / `input_audio_duration` equal to the total reference video / audio length (seconds)
- duration must be an integer 5-15
- Resize reference images so the long edge is <= 1024 px
- When quoting with `/api/quote`, describe the references with `input_image_count`, `has_video_input` + `input_video_count` + `input_video_duration`, and `has_audio_input` + `input_audio_count` + `input_audio_duration` (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "minimax-h3-max", "generation_type": "reference-to-video", "prompt": "The product from image 1 rotates on a marble table, soft studio light", "duration": "5", "aspect_ratio": "adaptive", "video_quality": "768p", "prompt_expansion_mode": "balanced", "images": ["https://example.com/product.jpg"]}
```

## MiniMax H3 Max Camera Controls — `minimax-h3-max-camera`

### `minimax-h3-max-camera` · `camera-controls`

Turns a single image into a 5-15 second video with a scripted camera move (orbit, dolly, crane, etc.) using MiniMax H3 Max.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `image` | string |  |  | Source image URL (`image` or `images[0]`). Output aspect ratio follows the image. |
| `images` | string[] |  |  | Optional; if sent, must contain at most 1 entry (the source image). No end frame. |
| `camera_preset` | string | "orbit-360", "birds-eye", "whip-spin", "hero-reveal", "dolly-in", "dolly-out", "arc-left", "arc-right", "worms-eye" | "orbit-360" | Named trajectory. Unknown names are rejected (400). Ignored when camera_trajectory is provided. Defaults to orbit-360 when both are omitted. |
| `camera_trajectory` | array |  |  | Explicit keyframes. Array of 2-12 objects {time: number 0..1 strictly increasing, azimuth: degrees (signed, multi-turn allowed), elevation: number -90..90, distance: number > 0}. Total \|azimuth\| travel <= 11520 degrees (32 turns). Takes precedence over camera_preset. |
| `prompt` | string |  |  | Optional. If empty, the default instruction 'The entire scene is frozen. Only the camera moves.' is used. |
| `duration` 💲 | string | 5–15 | "5" | Output seconds as an integer string. |
| `video_quality` 💲 | string | "480p", "768p", "1080p" | "768p" | Use one of the listed values. |
| `prompt_expansion_mode` | string | "disabled", "fast", "balanced", "quality" | "balanced" | Prompt rewriting strength. |
| `seed` | integer |  |  | Optional non-negative integer for reproducible results; omit for random. |

Input files:
- `image`: Exactly 1 public image URL (source image / first frame); no end frame, no reference videos or audio

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3-max`

Rules:
- generation_type must be 'camera-controls' (image-to-video is rejected with 400)
- A source image is required; more than 1 image, any video, or any audio is rejected with 400
- duration must be an integer 5-15
- camera_preset must be one of the 9 preset ids unless camera_trajectory is given
- camera_trajectory: 2-12 keyframes, time in [0,1] strictly increasing, elevation in [-90,90], distance > 0, total azimuth travel <= 11520 degrees
- aspect_ratio has no effect (output follows the source image)

Example body:

```json
{"mode": "minimax-h3-max-camera", "generation_type": "camera-controls", "prompt": "", "duration": "5", "video_quality": "768p", "prompt_expansion_mode": "balanced", "image": "https://example.com/statue.jpg", "images": ["https://example.com/statue.jpg"], "camera_preset": "orbit-360"}
```

## MiniMax H3 Max Lip Sync — `minimax-h3-max-lip-sync`

### `minimax-h3-max-lip-sync` · `lip-sync`

Makes a portrait photo speak in sync with an audio track (5 seconds to 15 minutes) using MiniMax H3 Max; output length follows the audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `image` | string |  |  | Portrait image URL (`image` or `images[0]`). Image aspect ratio (width/height) must be between 0.4 and 2.5. |
| `images` | string[] |  |  | Optional; if sent, must contain at most 1 entry (the portrait image). |
| `audios` **required** | string[] |  |  | Exactly 1 driving audio URL. Singular `audio` is accepted as a fallback if `audios` is absent. |
| `input_audio_duration` 💲 | number | 5–900 |  | Audio length in seconds. Always send it, equal to the audio length: the server measures the uploaded file and returns 409 (nothing charged) if the value is missing or the measured length costs more. Billed seconds = ceil(audio length), min 5. Over 15 seconds the whole clip costs 1.2x. Under 5s or over 900s is rejected. |
| `video_quality` 💲 | string | "480p", "768p", "1080p", "2k" | "768p" | Use one of the listed values. |
| `enable_transcription` | boolean |  | true | Transcribe the audio to guide mouth shapes. Defaults to true. |
| `seed` | integer |  |  | Optional non-negative integer for reproducible results; omit for random. |

Input files:
- `image`: 1 public portrait image URL (aspect ratio 0.4-2.5)
- `audio`: 1 audio file stored on Veevid, sent via 'audios': upload it to folder 'minimax-h3-max/audio' (wav/mp3/m4a, up to 15MB) or use a Veevid text-to-speech result; 5 seconds to 15 minutes; URLs on other hosts are rejected (400)

Upload folders (`folder` for `POST /api/storage/upload`): image → `minimax-h3-max`, audio → `minimax-h3-max/audio`

Rules:
- generation_type must be 'lip-sync' (400 otherwise)
- Requires one portrait image and one audio track; more than 1 image, more than 1 audio, or any video input is rejected (400)
- Portrait image aspect ratio (width/height) must be between 0.4 and 2.5
- Send input_audio_duration equal to the audio length; audio must be 5s to 15 minutes (400). The clip is as long as the audio, with no clipping
- prompt, duration, aspect_ratio and prompt_expansion_mode have no effect for this mode
- Cannot re-sync an existing video; image-to-video lip sync only
- If input_audio_duration is missing or the measured audio costs more than it, the request returns 409 with measured_duration and required_credits and nothing is charged; resend with measured_duration to confirm. If the output runs more than 0.5s past the billed length, or a smaller overrun takes it past 15 seconds, the difference is charged after generation. If an overrun of more than 0.5s cannot be covered by the balance, the video is not delivered and the credits are not refunded.

Example body:

```json
{"mode": "minimax-h3-max-lip-sync", "generation_type": "lip-sync", "image": "https://example.com/portrait.jpg", "images": ["https://example.com/portrait.jpg"], "audios": ["https://example.com/speech.mp3"], "input_audio_duration": 8.4, "video_quality": "768p", "enable_transcription": true}
```

## Gemini Omni — `gemini-omni`

### `gemini-omni` · `text-to-video`

Google Gemini Omni text-to-video with native audio, 4-10s, optionally guided by one reference video.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt (required, non-empty), max 20000 characters. |
| `duration` 💲 | string | "4", "6", "8", "10" | "8" | Seconds. Ignored (and not billed) when a video is supplied; output length then follows the input video clip (max 10s). |
| `video_quality` 💲 | string | "720p", "1080p", "4k" | "1080p" | Output resolution. The `resolution` field with the same values is also accepted and takes precedence. |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" | Only landscape or portrait. |
| `videos` 💲 | string[] |  |  | Optional, at most 1 video URL used as motion/style reference. |
| `input_video_duration` | number | 0–30 |  | Length of the supplied input video in seconds. Send it whenever a video is supplied; the output covers the first min(input_video_duration, 10) seconds. |
| `seed` | integer | 0–2147483647 |  | Optional, 0-2147483647; omit for random. |

Input files:
- `videos`: optional, max 1 video URL (mp4/mov, up to 100MB; input video must be <= 30s)

Upload folders (`folder` for `POST /api/storage/upload`): video → `gemini-omni/reference-videos`

Rules:
- duration must be one of 4, 6, 8, 10 (omitted defaults to 8)
- video_quality (if sent) must be 720p, 1080p or 4k; aspect_ratio (if sent) must be 16:9 or 9:16
- at most 1 video; asset quota images + 2*videos <= 7
- input_video_duration must be <= 30s
- prompt is required, max 20000 characters
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send a video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "gemini-omni", "generation_type": "text-to-video", "prompt": "A golden retriever surfing a wave at sunset, cinematic, with ocean sounds", "duration": "8", "video_quality": "1080p", "aspect_ratio": "16:9"}
```

### `gemini-omni` · `image-to-video`

Google Gemini Omni image-to-video: animates up to 7 input images into a 4-10s video with native audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, max 20000 characters. |
| `images` **required** | string[] |  |  | 1-7 image URLs. A single `image` field is also accepted. |
| `duration` 💲 | string | "4", "6", "8", "10" | "8" | Seconds. Ignored and not billed when a video is supplied. |
| `video_quality` 💲 | string | "720p", "1080p", "4k" | "1080p" | Output resolution; `resolution` is also accepted and takes precedence. |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" |  |
| `videos` 💲 | string[] |  |  | Optional, at most 1 video URL. |
| `input_video_duration` | number | 0–30 |  | Length of the input video in seconds. Send it whenever a video is supplied; the output covers the first min(input_video_duration, 10) seconds. |
| `seed` | integer | 0–2147483647 |  |  |

Input files:
- `images`: 1-7 image URLs (up to 20MB each)
- `videos`: optional, max 1 video URL (mp4/mov, <= 30s, up to 100MB)

Upload folders (`folder` for `POST /api/storage/upload`): image → `gemini-omni`, video → `gemini-omni/reference-videos`

Rules:
- image-to-video requires `image` or a non-empty `images`
- max 7 images and max 1 video; images + 2*videos <= 7 (so with a video, at most 5 images)
- video_quality must be 720p, 1080p or 4k; aspect_ratio must be 16:9 or 9:16
- input_video_duration must be <= 30s
- same price table as text-to-video
- duration must be 4, 6, 8 or 10, also when a video is supplied (it is then ignored).
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send a video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "gemini-omni", "generation_type": "image-to-video", "prompt": "The woman in the photo turns toward the camera and smiles as wind moves her hair", "images": ["https://example.com/portrait.jpg"], "duration": "6", "video_quality": "1080p", "aspect_ratio": "9:16"}
```

### `gemini-omni` · `reference-to-video`

Google Gemini Omni reference-to-video: generates a video guided by up to 7 reference images and/or 1 reference video.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Text prompt, max 20000 characters. |
| `images` | string[] |  |  | 0-7 reference image URLs. At least one image or one video is required. |
| `videos` 💲 | string[] |  |  | 0-1 reference video URL. |
| `input_video_duration` | number | 0–30 |  | Length of the reference video in seconds; output length = min(this, 10). Send it whenever a video is supplied. |
| `duration` 💲 | string | "4", "6", "8", "10" | "8" | Only used/billed when no video is supplied. |
| `video_quality` 💲 | string | "720p", "1080p", "4k" | "1080p" |  |
| `aspect_ratio` | string | "16:9", "9:16" | "16:9" |  |
| `seed` | integer | 0–2147483647 |  |  |

Input files:
- `images`: 0-7 reference image URLs (up to 20MB each)
- `videos`: 0-1 reference video URL (mp4/mov, <= 30s; only the first 10s is used)

Upload folders (`folder` for `POST /api/storage/upload`): image → `gemini-omni`, video → `gemini-omni/reference-videos`

Rules:
- at least one reference image or video is required
- reference quota: images <= 7, videos <= 1, images + 2*videos <= 7
- input_video_duration must be <= 30s
- same price table as text-to-video
- duration must be 4, 6, 8 or 10, also when a video is supplied (it is then ignored).
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send a reference video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "gemini-omni", "generation_type": "reference-to-video", "prompt": "The character from the reference images walks through a neon-lit Tokyo street at night", "images": ["https://example.com/character-front.png", "https://example.com/character-side.png"], "duration": "8", "video_quality": "1080p", "aspect_ratio": "16:9"}
```

## Boreal — `creatify-boreal`

### `creatify-boreal` · `text-to-video`

Creatify Boreal text-to-video for ads, UGC and presenter clips with native synced speech, 1-20s, optionally driven by an uploaded audio track.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Prompt; may optionally be structured with section headers [VISUAL], [SPEECH], [SOUNDS], [TEXT] (dialogue in quotes). |
| `duration` 💲 | string | 1–20 | "10" | Integer seconds. |
| `video_quality` 💲 | string | "720p", "1080p", "2k" | "720p" | Output resolution ('2K' uppercase also accepted). |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4" | "auto" |  |
| `audio` | string |  |  | Optional driving audio URL; if given, the audio track is kept and the model lip-syncs to it instead of generating speech. |

Input files:
- `audio`: optional, 1 audio URL (.mp3/.ogg/.wav/.m4a/.aac)

Upload folders (`folder` for `POST /api/storage/upload`): audio → `creatify-boreal/audio`

Rules:
- generation_type must be text-to-video or image-to-video
- duration must be an integer between 1 and 20 (omitted defaults to 10)
- video_quality must be 720p, 1080p, 2k or 2K; aspect_ratio must be auto, 16:9, 9:16, 1:1, 4:3 or 3:4
- prompt is required

Example body:

```json
{"mode": "creatify-boreal", "generation_type": "text-to-video", "prompt": "[VISUAL]\nA young woman holds a can of sparkling water in a sunny kitchen and talks to the camera.\n\n[SPEECH]\n\"This is the only drink I grab after my workout.\"", "duration": "10", "video_quality": "720p", "aspect_ratio": "9:16"}
```

### `creatify-boreal` · `image-to-video`

Creatify Boreal image-to-video: turns a product or presenter image into an ad/UGC clip with native synced speech, optionally driven by audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Prompt; optional [VISUAL]/[SPEECH]/[SOUNDS]/[TEXT] sections. |
| `image` **required** | string |  |  | 1 image URL used as the starting image (`images[0]` is also accepted). |
| `duration` 💲 | string | 1–20 | "10" | Integer seconds. |
| `video_quality` 💲 | string | "720p", "1080p", "2k" | "720p" |  |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4" | "auto" | 'auto' follows the input image. |
| `audio` | string |  |  | Optional driving audio URL; the model lip-syncs to it instead of generating speech. |

Input files:
- `image`: 1 image URL
- `audio`: optional, 1 audio URL (.mp3/.ogg/.wav/.m4a/.aac)

Upload folders (`folder` for `POST /api/storage/upload`): image → `creatify-boreal`, audio → `creatify-boreal/audio`

Rules:
- image-to-video requires `image` or non-empty `images`
- duration integer 1-20; video_quality 720p/1080p/2k/2K; aspect_ratio auto/16:9/9:16/1:1/4:3/3:4

Example body:

```json
{"mode": "creatify-boreal", "generation_type": "image-to-video", "prompt": "[VISUAL]\nThe presenter picks up the product and shows it to the camera.\n\n[SPEECH]\n\"Meet the lightest headphones we've ever made.\"", "image": "https://example.com/presenter.jpg", "duration": "8", "video_quality": "1080p", "aspect_ratio": "auto"}
```
