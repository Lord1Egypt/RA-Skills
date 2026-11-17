# Video tools & effects

Upscale, resize, edit, extend, insert, character swap, lip-sync, motion control, hug/kiss effects.

All of these are called with `POST /api/generate-video` using the `mode` and `generation_type` shown. Params marked 💲 change the price — get the exact cost with `POST /api/quote` before generating. Defaults are what the API uses when the field is omitted (not always what the website preselects).

## Index

- Kling 3.0 Motion Control — `motion-control-standard`: `motion-control`
- Kling 3.0 Motion Control — `motion-control-pro`: `motion-control`
- AI Hug Video Generator — `ai-hug`: `ai-hug`
- AI Kissing Video Generator — `ai-kissing`: `ai-kissing`
- AI Video Upscaler — `upscale`: `video-upscale`
- AI Video Resizer — `reframe`: `video-reframe`
- Wan 2.7 Edit — `wan-2.7-edit`: `edit-video`
- Wan 3.0 — `wan-3.0`: `edit-video`, `video-extend`
- Seedance 2.0 — `seedance-2.0`: `edit-video`, `video-extend`
- Seedance 2.5 — `seedance-2.5`: `edit-video`, `video-extend`
- LTX 2.3 — `ltx-2-3`: `video-extend`
- MiniMax H3 Max — `minimax-h3-max-extend`: `video-extend`
- MiniMax H3 Max — `minimax-h3-max-insert`: `video-insert`
- MiniMax H3 Max — `minimax-h3-max-recast`: `character-swap`
- Video Lip Sync — `video-lip-sync`: `lip-sync`
- Google Veo 3.1 — `veo3`: `video-extend`
- Grok Imagine — `grok-imagine`: `video-extend`

## Kling 3.0 Motion Control — `motion-control-standard`

### `motion-control-standard` · `motion-control`

Transfers the motion from a driving video onto the character in a reference image (Kling 3.0 Motion Control, Standard).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `image` **required** | string |  |  | Public URL of the character image. |
| `video` **required** | string |  |  | Public URL of the driving (motion reference) video. |
| `duration` **required** 💲 | string (whole seconds) |  |  | Driving video length as a whole number of seconds, rounded up (e.g. "5"; decimals are rejected); it determines the price. When the driving video is on Veevid storage the server also measures it and charges by the measured length if that is longer. |
| `character_orientation` **required** | string | "image", "video" |  | 'image' keeps the character orientation from the image (video up to 10s); 'video' follows the video (up to 30s). |
| `model_version` 💲 | string | "motion-control-standard", "motion-control-pro" | "motion-control-standard" | Optional; the Pro tier is used when either mode or model_version is motion-control-pro. |
| `prompt` | string |  |  | Optional text guidance, e.g. 'No distortion, the character's movements are consistent with the video.' Omit if blank. |
| `keep_original_sound` | boolean |  | true | Keep the driving video's audio. |
| `elements` | array |  |  | At most 1 element: {frontal_image_url?: string, reference_image_urls: string[1-3]}. Only allowed when character_orientation is 'video'. Send [] when unused. |
| `aspect_ratio` | string | "original" |  | Send 'original'; output follows the inputs. |

Input files:
- `image`: 1 character image URL (JPEG/PNG/WebP, max 10MB)
- `video`: 1 driving video URL; up to 10s when character_orientation=image, up to 30s when =video (mp4/webm/mov, max 200MB)
- `images`: optional element images via elements[0].frontal_image_url and elements[0].reference_image_urls (1-3)

Upload folders (`folder` for `POST /api/storage/upload`): image → `kling-motion-control/reference-images`, video → `kling-motion-control/reference-videos`, images → `kling-motion-control/reference-images`

Rules:
- image, video and character_orientation are required (400 otherwise).
- elements are only allowed when character_orientation=video; at most 1 element with 1-3 reference_image_urls.
- Send `duration` equal to the driving video length in whole seconds (rounded up).
- duration must be a whole number of seconds (decimals are rejected); max 10 when character_orientation=image, max 30 when =video (400 otherwise).
- mode motion-control-standard / motion-control-pro must be used with generation_type motion-control, and vice versa (400 otherwise).
- If the output video is longer than the charged duration, the difference is charged after generation; if your balance cannot cover it, the result is not delivered and the generation fails without a refund.

Example body:

```json
{"mode": "motion-control-standard", "generation_type": "motion-control", "model_version": "motion-control-standard", "prompt": "No distortion, the character's movements are consistent with the video.", "image": "https://cdn.veevid.ai/sample/motion-control-image-1.webp", "video": "https://cdn.veevid.ai/sample/motion-control-video-1.mp4", "duration": "5", "aspect_ratio": "original", "character_orientation": "image", "keep_original_sound": true, "elements": []}
```

## Kling 3.0 Motion Control — `motion-control-pro`

### `motion-control-pro` · `motion-control`

Transfers the motion from a driving video onto the character in a reference image at Pro quality (Kling 3.0 Motion Control, Pro).

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `image` **required** | string |  |  | Public URL of the character image. |
| `video` **required** | string |  |  | Public URL of the driving (motion reference) video. |
| `duration` **required** 💲 | string (whole seconds) |  |  | Driving video length as a whole number of seconds, rounded up (e.g. "5"; decimals are rejected); it determines the price. When the driving video is on Veevid storage the server also measures it and charges by the measured length if that is longer. |
| `character_orientation` **required** | string | "image", "video" |  | 'image': video up to 10s; 'video': video up to 30s. |
| `model_version` 💲 | string | "motion-control-standard", "motion-control-pro" | "motion-control-pro" | Optional; the Pro tier is used when either mode or model_version is motion-control-pro. |
| `prompt` | string |  |  | Optional text guidance (omit if blank). |
| `keep_original_sound` | boolean |  | true | Keep the driving video's audio. |
| `elements` | array |  |  | At most 1 element: {frontal_image_url?: string, reference_image_urls: string[1-3]}; only with character_orientation='video'. Send [] when unused. |
| `aspect_ratio` | string | "original" |  | Send 'original'; output follows the inputs. |

Input files:
- `image`: 1 character image URL (JPEG/PNG/WebP, max 10MB)
- `video`: 1 driving video URL; up to 10s when character_orientation=image, up to 30s when =video (max 200MB)
- `images`: optional element images via elements[0].frontal_image_url and elements[0].reference_image_urls (1-3)

Upload folders (`folder` for `POST /api/storage/upload`): image → `kling-motion-control/reference-images`, video → `kling-motion-control/reference-videos`, images → `kling-motion-control/reference-images`

Rules:
- image, video and character_orientation are required (400 otherwise).
- elements are only allowed when character_orientation=video; at most 1 element with 1-3 reference_image_urls.
- Send `duration` equal to the driving video length in whole seconds (rounded up).
- duration must be a whole number of seconds (decimals are rejected); max 10 when character_orientation=image, max 30 when =video (400 otherwise).
- mode motion-control-standard / motion-control-pro must be used with generation_type motion-control, and vice versa (400 otherwise).
- If the output video is longer than the charged duration, the difference is charged after generation; if your balance cannot cover it, the result is not delivered and the generation fails without a refund.

Example body:

```json
{"mode": "motion-control-pro", "generation_type": "motion-control", "model_version": "motion-control-pro", "prompt": "No distortion, the character's movements are consistent with the video.", "image": "https://cdn.veevid.ai/sample/motion-control-image-1.webp", "video": "https://cdn.veevid.ai/sample/motion-control-video-1.mp4", "duration": "5", "aspect_ratio": "original", "character_orientation": "video", "keep_original_sound": true, "elements": []}
```

## AI Hug Video Generator — `ai-hug`

### `ai-hug` · `ai-hug`

Generates a video of two people (or a person and a pet) from two separate photos hugging in a described scene.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Only the scene sentence (max 500 chars). It is automatically wrapped in a fixed template that references the two photos as @Element1/@Element2; do not write the full prompt. |
| `images` **required** | string[] |  |  | Exactly 2 image URLs: [person A, person B]; images[0] = @Element1. |
| `resolution` 💲 | string | "720p", "1080p", "4k" | "720p" | Uses `resolution`, not video_quality. |
| `duration` 💲 | string | 3–15 | "5" | Integer seconds. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | "16:9" |  |
| `generate_audio` 💲 | boolean |  | false | Generate ambient audio. |

Input files:
- `images`: exactly 2 image URLs, one subject each (up to 10MB per photo)

Upload folders (`folder` for `POST /api/storage/upload`): image → `ai-hug`

Rules:
- mode and generation_type must both be 'ai-hug'
- images must contain exactly 2 URLs
- prompt (scene) is required and at most 500 characters
- resolution must be 720p, 1080p or 4k; duration integer 3-15; aspect_ratio 16:9, 9:16 or 1:1
- scene_template is rejected for this mode (only ai-kissing accepts it)

Example body:

```json
{"mode": "ai-hug", "generation_type": "ai-hug", "prompt": "They spot each other in a sunlit park, walk closer and share a warm, tight hug.", "images": ["https://example.com/person-a.jpg", "https://example.com/person-b.jpg"], "resolution": "720p", "duration": "5", "aspect_ratio": "16:9", "generate_audio": false}
```

## AI Kissing Video Generator — `ai-kissing`

### `ai-kissing` · `ai-kissing`

Generates a video of two adults kissing, either from two separate photos or from one photo of both people.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Only the scene sentence (max 500 chars); may refer to the two people only as @Element1 and @Element2 (exact spelling). It is automatically wrapped in a fixed template. |
| `images` **required** | string[] |  |  | 1 URL (one photo of both people, used as first frame) or 2 URLs ([person 1, person 2], images[0] = @Element1). Count selects the input mode. |
| `scene_template` | string | "default", "stylized" | "default" | 'stylized' for anime/3D style scenes (drops realism constraints). |
| `resolution` 💲 | string | "720p", "1080p", "4k" | "720p" | Uses `resolution`, not video_quality. |
| `duration` 💲 | string | 3–15 |  | Integer seconds. Default 5 with 2 photos, 8 with 1 photo. |
| `aspect_ratio` | string | "16:9", "9:16", "1:1" | "16:9" | No effect in one-photo mode (output follows the photo). |
| `generate_audio` 💲 | boolean |  | false |  |

Input files:
- `images`: 1 image URL (couple photo) or 2 image URLs (one per person); up to 10MB per photo

Upload folders (`folder` for `POST /api/storage/upload`): image → `ai-kissing`

Rules:
- mode and generation_type must both be 'ai-kissing' (legacy mode 'normal' is rejected)
- images must contain 1 or 2 URLs
- prompt (scene) is required, max 500 characters; only @Element1/@Element2 references allowed
- scene_template must be default or stylized
- resolution 720p/1080p/4k; duration integer 3-15; aspect_ratio 16:9, 9:16 or 1:1
- When quoting with `/api/quote`, send `images` or `input_image_count` (1 or 2) — the input mode decides the default duration (422 otherwise).

Example body:

```json
{"mode": "ai-kissing", "generation_type": "ai-kissing", "prompt": "Standing face to face in a sunlit park at golden hour, @Element1 tilts their head up and closes their eyes while @Element2 gently cups @Element1's face with one hand and leans in; they share a soft, tender kiss on the lips.", "images": ["https://example.com/person-1.jpg", "https://example.com/person-2.jpg"], "scene_template": "default", "resolution": "720p", "duration": "5", "aspect_ratio": "16:9", "generate_audio": false}
```

## AI Video Upscaler — `upscale`

### `upscale` · `video-upscale`

Upscales an existing video to 720p, 1080p or 4K and optionally raises its frame rate.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `video` **required** | string |  |  | URL of the source video (singular field). |
| `video_quality` **required** 💲 | string | "720p", "1080p", "4K" |  | Target resolution. Always send `video_quality`. |
| `target_fps` 💲 | number | 15–60 | 30 | Target frame rate. Above 30 fps costs more at 1080p and 4K. |
| `duration` 💲 | string |  | "5" | Source video length in whole seconds, as a string. Send the actual length of the source video; it determines the price (5 when omitted). |
| `video_source` | string | "upload", "url" |  | 'upload' for files uploaded with `POST /api/storage/upload`, 'url' for an external link. With 'url' the link must answer a HEAD request with a supported video type and be <=200MB. |
| `prompt` | string |  | "Upscale" | Optional; has no effect and can be omitted. |

Input files:
- `video`: 1 video URL (mp4, mov, webm, m4v, mkv, avi, wmv, ts, vob, mpg, flv, 3gp or gif), up to 200MB.

Upload folders (`folder` for `POST /api/storage/upload`): video → `upscale-input`

Rules:
- video is required (400 'Video is required for video-upscale generation').
- When sent, duration must be a positive integer (400).
- target_fps must be 15-60.
- With video_source 'url': the URL must answer a HEAD request within 5s, have a supported video content-type or file extension, and be <=200MB.
- Processing is asynchronous: the response has status 'processing' and a generation_id to poll.

Example body:

```json
{"mode": "upscale", "generation_type": "video-upscale", "prompt": "Upscale", "video": "https://cdn.veevid.ai/edit-video-samples/moto-source.mp4", "video_quality": "1080p", "target_fps": 30, "duration": "8", "video_source": "upload"}
```

## AI Video Resizer — `reframe`

### `reframe` · `video-reframe`

Changes a video's aspect ratio by using AI to extend the frame (outpainting) instead of cropping.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `video` **required** | string |  |  | URL of the source video (singular field). |
| `aspect_ratio` | string | "1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21" | "16:9" | Target aspect ratio; use one of the listed values (16:9 when omitted). |
| `duration` 💲 | string |  | "5" | Source video length in whole seconds, as a string. Send the actual length of the source video. |
| `prompt` | string |  | "Reframe Video" | Optional description of the scene to guide the extended areas. The literal 'Reframe Video' means no prompt. |
| `video_source` | string | "upload", "url" |  | Optional: 'upload' or 'url'. |
| `video_quality` | string |  | "standard" | Optional; has no effect (send 'standard' or omit). |

Input files:
- `video`: 1 video URL, up to 100MB and up to 30s.

Upload folders (`folder` for `POST /api/storage/upload`): video → `reframe-input`

Rules:
- video is required (400 'Video is required for video-reframe generation').
- Always send `duration` equal to the source video length (whole seconds).
- aspect_ratio must be one of the 7 listed values.
- The source video must be at most 30s and 100MB.
- Processing is asynchronous: poll the returned generation_id.

Example body:

```json
{"mode": "reframe", "generation_type": "video-reframe", "video": "https://cdn.veevid.ai/edit-video-samples/moto-source.mp4", "aspect_ratio": "9:16", "prompt": "Reframe Video", "duration": "8", "video_source": "upload", "video_quality": "standard"}
```

## Wan 2.7 Edit — `wan-2.7-edit`

### `wan-2.7-edit` · `edit-video`

Edits an existing 2-10s video according to a text instruction, with an optional reference image.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Editing instruction (required). |
| `video` **required** | string |  |  | Source video URL (singular field). MP4 or MOV, 2-10s, <=100MB. |
| `duration` **required** 💲 | string | 2–10 |  | Output length in whole seconds (2-10). To match the input, send the source length rounded up. |
| `video_quality` | string | "720p", "1080p" | "1080p" | Output resolution. Same price for both. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4" |  | Omit (or send 'auto') to keep the source ratio. |
| `audio_setting` | string | "auto", "origin" | "auto" | 'auto' lets the model generate audio; 'origin' keeps the source audio. |
| `video_source` | string | "upload", "url" |  | 'upload' for files uploaded with `POST /api/storage/upload`; 'url' for an external link, which must pass a HEAD check (supported video type, <=100MB). |
| `image` | string |  |  | Optional reference image URL (http/https) for the edit. |

Input files:
- `video`: 1 source video URL (MP4/MOV, 2-10s, <=100MB)
- `image`: optional 1 reference image URL (jpg/png/webp)

Upload folders (`folder` for `POST /api/storage/upload`): video → `edit-video-input`, image → `edit-video-ref`

Rules:
- Always send `duration`.
- duration must be an integer string 2-10 (400).
- video_quality, if sent, must be 720p or 1080p; aspect_ratio, if sent, must be auto, 16:9, 9:16, 1:1, 4:3 or 3:4 (400).
- video (singular) is required (400 'Video is required for edit-video generation').
- With video_source 'url' the link must pass a HEAD check (supported video type, <=100MB).
- Source videos uploaded to edit-video-input must be .mp4/.mov, up to 100MB.
- prompt is required.

Example body:

```json
{"mode": "wan-2.7-edit", "generation_type": "edit-video", "prompt": "Change the motorcycle to glossy red", "video": "https://cdn.veevid.ai/edit-video-samples/moto-source.mp4", "duration": "9", "video_quality": "720p", "audio_setting": "auto", "video_source": "upload"}
```

## Wan 3.0 — `wan-3.0`

### `wan-3.0` · `edit-video`

Edits a source video with a text instruction plus optional reference images and audio, and lets you pick the output length.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Editing instruction (required). It is automatically prefixed with 'Edit Video 1: ' when it lacks an edit intent. |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. Source seconds are billed together with output seconds. |
| `images` | string[] |  |  | Optional reference images, up to 10. |
| `audios` | string[] |  |  | Optional reference audio files, up to 5. |
| `duration` 💲 | string | 2–30 | "5" | Output length in whole seconds (2-30); -1 (smart duration) is rejected. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "720p" | Output resolution. |
| `aspect_ratio` | string | "adaptive", "16:9", "9:16", "1:1", "4:3", "3:4" | "adaptive" | Use one of the listed values; 'adaptive' keeps the source ratio. |
| `generate_audio` | boolean |  | true | Generate a soundtrack. |
| `input_video_duration` 💲 | number | 0–15 |  | Source video length in seconds, rounded up. Always send it with the source video. |
| `has_video_input` | boolean |  |  | Quote-only field: send `true` to `/api/quote` together with the source video length; `/api/generate-video` ignores it. |

Input files:
- `video`: 1 source video URL in videos[] (1-15s, up to 100MB)
- `images`: 0-10 reference image URLs (up to 20MB each)
- `audio`: 0-5 reference audio URLs in audios[]

Upload folders (`folder` for `POST /api/storage/upload`): video → `wan30/reference-videos`, image → `wan30`, audio → `wan30/audio`

Rules:
- Send input_video_duration equal to the source video length (seconds); values > 15 are rejected (400).
- duration must be an integer 2-30; -1 is rejected (400).
- input_video_duration + duration must be <= 30 (400).
- At most 10 images, 5 videos and 5 audios (400).
- videos[] must contain the source video (400 'Video is required for edit-video generation').
- prompt is required.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "wan-3.0", "generation_type": "edit-video", "prompt": "Replace the rider with a short-haired woman in a yellow raincoat", "videos": ["https://cdn.veevid.ai/edit-video-samples/moto-source.mp4"], "duration": "5", "video_quality": "720p", "aspect_ratio": "adaptive", "generate_audio": true, "input_video_duration": 9}
```

### `wan-3.0` · `video-extend`

Continues an uploaded video (up to 15s), keeping its characters, style and sound.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | What happens next. It is automatically prefixed with 'Extend Video 1 by N seconds.' when no extend intent is present. |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. No taskId needed. |
| `duration` 💲 | string | 2–30 | "5" | Length of the new footage in seconds. It must be <= 30 - source seconds. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "720p" | Output resolution. |
| `aspect_ratio` | string | "adaptive" | "16:9" | Send 'adaptive' so the output follows the source; when omitted, 16:9 is used. |
| `generate_audio` | boolean |  | true | Generate audio. |
| `input_video_duration` 💲 | number | 0–15 |  | Source length in seconds, rounded up. Always send it with the source video. |

Input files:
- `video`: 1 source video URL in videos[] (1-15s, up to 100MB)

Upload folders (`folder` for `POST /api/storage/upload`): video → `wan30-extend`

Rules:
- Send input_video_duration equal to the source video length (seconds); values > 15 are rejected (400).
- duration must be an integer 2-30; -1 is rejected; source + duration must be <= 30 (400).
- At most 5 videos, 10 images and 5 audios (400); only the source video is needed.
- A source video in videos[] is required.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "wan-3.0", "generation_type": "video-extend", "prompt": "The panther stops and looks straight at the camera", "videos": ["https://cdn.veevid.ai/sample/extend-video-3.mp4"], "duration": "5", "video_quality": "720p", "aspect_ratio": "adaptive", "generate_audio": true, "input_video_duration": 6}
```

## Seedance 2.0 — `seedance-2.0`

### `seedance-2.0` · `edit-video`

Edits a source video (up to 15s) using a prompt plus optional reference images and audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Editing instruction (required). |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. The source length is billed. |
| `images` | string[] |  |  | Optional reference images; up to 9 are used. |
| `audios` | string[] |  |  | Optional reference audio; up to 3 are used. |
| `duration` 💲 | string | 4–15 | "5" | Output length in seconds, 4-15. Out-of-range values are clamped to 4-15. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | Output resolution. 1080p and 4k require model_version 'seedance-2.0'; with mini or fast use 480p or 720p. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | 'auto' keeps the source ratio. Use one of the listed values. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality/price tier. Send `model_version` explicitly. |
| `generate_audio` | boolean |  | true | Generate audio. |
| `input_video_duration` 💲 | number | 0–15 |  | Source video length in seconds (billed as at least 2s). Always send it with the source video. |
| `has_video_input` | boolean |  |  | Quote-only field: send `true` to `/api/quote` together with the source video length; `/api/generate-video` ignores it. |

Input files:
- `video`: 1 source video URL in videos[] (up to 15s and 200MB)
- `images`: 0-9 reference image URLs (up to 30MB each)
- `audio`: 0-3 reference audio URLs in audios[] (.wav/.mp3, up to 15MB each, 15s total)

Upload folders (`folder` for `POST /api/storage/upload`): video → `seedance20-edit`, image → `seedance20`, audio → `seedance20-edit/audio`

Rules:
- Send input_video_duration equal to the source video length (seconds); values > 15 are rejected (400).
- Send `model_version` explicitly; with seedance-2.0-mini or seedance-2.0-fast use 480p or 720p.
- videos[] must contain the source video (400 'Video is required for edit-video generation').
- Only the first 9 images, 3 videos and 3 audios are used; duration is normalized to 4-15 rather than rejected.
- Not supported: output_format (mp4/mov is only valid for Seedance 2.5).
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.0", "generation_type": "edit-video", "prompt": "Make it snow in the scene", "videos": ["https://cdn.veevid.ai/edit-video-samples/moto-source.mp4"], "duration": "5", "video_quality": "480p", "aspect_ratio": "auto", "model_version": "seedance-2.0-fast", "generate_audio": true, "input_video_duration": 8.034}
```

### `seedance-2.0` · `video-extend`

Continues an uploaded video by 4-15s with optional reference images and audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | What happens next. |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. No taskId needed. |
| `images` | string[] |  |  | Optional reference images; up to 9 are used. |
| `audios` | string[] |  |  | Optional reference audio; up to 3 are used. |
| `duration` 💲 | string | 4–15 | "5" | Length of the new footage in seconds; clamped to 4-15. |
| `video_quality` 💲 | string | "480p", "720p", "1080p", "4k" | "480p" | 1080p and 4k require model_version 'seedance-2.0'; with mini or fast use 480p or 720p. |
| `aspect_ratio` | string | "auto", "16:9", "9:16", "1:1", "4:3", "3:4", "21:9" | "16:9" | 'auto' keeps the source ratio. |
| `model_version` 💲 | string | "seedance-2.0-mini", "seedance-2.0-fast", "seedance-2.0" | "seedance-2.0" | Quality/price tier. Send `model_version` explicitly. |
| `generate_audio` | boolean |  | true | Generate audio. |
| `input_video_duration` 💲 | number | 0–15 |  | Source length in seconds (billed as at least 2s). Always send it with the source video. |
| `has_video_input` | boolean |  |  | Quote-only field: send `true` to `/api/quote` together with the source video length; `/api/generate-video` ignores it. |

Input files:
- `video`: 1 source video URL in videos[] (<=15s; mp4/mov/webm up to 200MB)
- `images`: 0-9 reference image URLs
- `audio`: 0-3 reference audio URLs in audios[] (.wav/.mp3, up to 15MB each, 15s total)

Upload folders (`folder` for `POST /api/storage/upload`): video → `seedance20-extend`, image → `seedance20-extend`, audio → `seedance20-extend/audio`

Rules:
- Send input_video_duration equal to the source video length (seconds); values > 15 are rejected (400).
- Send `model_version` explicitly; with seedance-2.0-mini or seedance-2.0-fast use 480p or 720p.
- The source video is required in videos[].
- Only the first 9 images, 3 videos and 3 audios are used.
- Reference images uploaded to the seedance20-extend folder must be .jpg/.jpeg/.png/.tiff/.gif (not .webp).
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.0", "generation_type": "video-extend", "prompt": "The camera follows the panther as it stalks through the tall grass", "videos": ["https://cdn.veevid.ai/sample/extend-video-3.mp4"], "duration": "5", "video_quality": "480p", "aspect_ratio": "auto", "model_version": "seedance-2.0-fast", "generate_audio": true, "input_video_duration": 6}
```

## Seedance 2.5 — `seedance-2.5`

### `seedance-2.5` · `edit-video`

Edits a source video (up to 30s) with a prompt and optional references; the output keeps the source's length and aspect ratio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | Editing instruction. It is automatically prefixed with 'Edit the video: ' when no editing keyword (edit/add/remove/replace/change/...) is present. |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. |
| `images` | string[] |  |  | Optional reference images; up to 30 are used. |
| `audios` | string[] |  |  | Optional reference audio; up to 10 are used. |
| `duration` **required** 💲 | string | "-1" |  | Send "-1". Edit output always matches the source length. |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution. Use one of the listed values; 1080p output is 10-bit HEVC. |
| `aspect_ratio` | string | "auto" | "auto" | Send 'auto' or omit; edits always keep the source aspect ratio. |
| `generate_audio` | boolean |  | true | Generate audio. |
| `input_video_duration` 💲 | number | 0–30 |  | Source video length in seconds (billed as at least 2s). Always send it with the source video. |
| `output_format` | string | "mp4", "mov" | "mp4" | Optional output container: mp4 or mov. |
| `has_video_input` | boolean |  |  | Quote-only field: send `true` to `/api/quote` together with the source video length; `/api/generate-video` ignores it. |

Input files:
- `video`: 1 source video URL in videos[] (up to 30s and 200MB)
- `images`: 0-30 reference image URLs (up to 30MB each)
- `audio`: 0-10 reference audio URLs in audios[] (.wav/.mp3, up to 15MB each)

Upload folders (`folder` for `POST /api/storage/upload`): video → `seedance25-edit`, image → `seedance25`, audio → `seedance25-edit/audio`

Rules:
- duration must be an integer 4-30 or -1 (400); for edits send -1.
- Send input_video_duration equal to the source video length (seconds); values > 30 are rejected (400).
- output_format accepts only mp4 or mov (400 otherwise).
- videos[] must contain the source (400 'Video is required for edit-video generation').
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.5", "generation_type": "edit-video", "prompt": "Replace the motorcycle with a red vintage scooter", "videos": ["https://cdn.veevid.ai/edit-video-samples/moto-source.mp4"], "duration": "-1", "video_quality": "480p", "aspect_ratio": "auto", "generate_audio": true, "input_video_duration": 8.034}
```

### `seedance-2.5` · `video-extend`

Continues an uploaded video by 4-30s with optional reference images and audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | string |  |  | What happens next. It is automatically prefixed with 'Continue the video: ' when there is no extend keyword (extend/continue/continuation). |
| `videos` **required** 💲 | string[] |  |  | [source video URL]. No taskId needed. |
| `images` | string[] |  |  | Optional reference images; up to 30 are used. |
| `audios` | string[] |  |  | Optional reference audio; up to 10 are used. |
| `duration` 💲 | string | 4–30 | "5" | Length of the new footage in seconds. -1 lets the model choose and is billed as the source length (min 4). |
| `video_quality` 💲 | string | "480p", "720p", "1080p" | "480p" | Output resolution. |
| `output_format` | string | "mp4", "mov" | "mp4" | mov uses H.264 + PCM audio and usually cannot play in browsers. |
| `aspect_ratio` | string | "auto" | "auto" | The output follows the source aspect ratio. |
| `generate_audio` | boolean |  | true | Generate audio. |
| `input_video_duration` 💲 | number | 0–30 |  | Source length in seconds, rounded up (billed as at least 2s). Always send it with the source video. |
| `has_video_input` | boolean |  |  | Quote-only field: send `true` to `/api/quote` together with the source video length; `/api/generate-video` ignores it. |

Input files:
- `video`: 1 source video URL in videos[] (<=30s; mp4/mov/webm up to 200MB)
- `images`: 0-30 reference image URLs
- `audio`: 0-10 reference audio URLs in audios[] (.wav/.mp3, up to 15MB each, 30s total)

Upload folders (`folder` for `POST /api/storage/upload`): video → `seedance25-extend`, image → `seedance25-extend`, audio → `seedance25-extend/audio`

Rules:
- duration must be an integer 4-30 or -1 (400).
- Send input_video_duration equal to the source video length (seconds); values > 30 are rejected (400).
- output_format accepts only mp4 or mov (400).
- A source video in videos[] is required.
- Reference images uploaded to the seedance25-extend folder must be .jpg/.jpeg/.png/.tiff/.gif (not .webp).
- 480p results are usually drafts: the status response then includes `seedance25_draft`, and the draft can be upgraded once to a 1080p version within 7 days with `POST /api/video-generation/{id}/upgrade-draft`.
- When quoting with `/api/quote`, add `has_video_input: true` and `input_video_duration` if you send the source video (the quote endpoint does not read video URLs, so the price would come out too low).

Example body:

```json
{"mode": "seedance-2.5", "generation_type": "video-extend", "prompt": "Continue the video: the panther slips deeper into the misty jungle", "videos": ["https://cdn.veevid.ai/sample/extend-video-3.mp4"], "duration": "5", "video_quality": "480p", "output_format": "mp4", "aspect_ratio": "auto", "generate_audio": true, "input_video_duration": 6}
```

## LTX 2.3 — `ltx-2-3`

### `ltx-2-3` · `video-extend`

Extends an uploaded video by 1-20s at its start or end, with optional context length control.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `video` **required** | string |  |  | Source video URL (singular field). |
| `prompt` | string |  |  | Optional description of the extension. |
| `duration` 💲 | string | 1–20 | "5" | Seconds to add (1-20). Decimals are allowed (e.g. 0.5s steps). |
| `extend_mode` | string | "start", "end" | "end" | Where to add footage. |
| `context` | number | 1–20 |  | Seconds of the source to use as context. Omit to let the model maximize context. |
| `video_source` | string | "upload", "url" |  | 'upload' for files uploaded with `POST /api/storage/upload`; 'url' for an external link, which must pass a HEAD check (supported video type, <=200MB). |
| `aspect_ratio` | string | "original" | "original" | Optional; send 'original' or omit. Output keeps the source aspect ratio. |

Input files:
- `video`: 1 source video URL (mp4/mov/webm/m4v/gif, up to 20s and 200MB)

Upload folders (`folder` for `POST /api/storage/upload`): video → `video-generator-ltx23-extend`

Rules:
- duration must be a number between 1 and 20 (400).
- context, if sent, must be 1-20.
- video (singular) is required (400 'Video is required for LTX 2.3 extend generation').
- No taskId is used; model_version and video_quality have no effect for extends.

Example body:

```json
{"mode": "ltx-2-3", "generation_type": "video-extend", "prompt": "The panther keeps walking through the misty jungle", "video": "https://cdn.veevid.ai/sample/extend-video-3.mp4", "duration": "5", "extend_mode": "end", "aspect_ratio": "original", "video_source": "upload"}
```

## MiniMax H3 Max — `minimax-h3-max-extend`

### `minimax-h3-max-extend` · `video-extend`

Continues an uploaded clip (1.625-60s) by 5-15s at up to 2K resolution.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` **required** | string |  |  | What happens next (required). |
| `videos` **required** | string[] |  |  | [source video URL]; exactly one. The singular 'video' is also accepted. |
| `duration` 💲 | string | 5–15 | "5" | Seconds of new footage (whole seconds). |
| `video_quality` 💲 | string | "480p", "768p", "1080p", "2k", "2K" | "768p" | Output resolution. |
| `aspect_ratio` | string | "auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16" | "auto" | auto (or adaptive) follows the source. A fixed ratio crops the output. If omitted, auto is used, not 16:9. |
| `extend_output` | string | "extended", "continuation" | "extended" | 'extended' returns source + new footage; 'continuation' returns only the new footage plus ~1.6s of the source tail. |
| `prompt_expansion_mode` | string | "balanced", "disabled" | "balanced" | 'balanced' enables prompt expansion; 'disabled' turns it off. |
| `input_video_duration` | number | 1.625–60 |  | Source length in seconds (up to 2 decimals). Used for validation only; the source is not billed. |
| `seed` | number |  |  | Optional integer >= 0. |

Input files:
- `video`: 1 source video URL in videos[] (1.625-60s, <=50MB, aspect ratio 0.4-2.5; mp4/mov/webm/m4v)

Upload folders (`folder` for `POST /api/storage/upload`): video → `minimax-h3-max-extend`

Rules:
- The source length and extend_output do not affect price.
- generation_type must be video-extend; duration must be an integer 5-15 (400).
- Exactly one source video; prompt is required; images and audio are rejected (400).
- aspect_ratio must be auto/adaptive/21:9/16:9/4:3/1:1/3:4/9:16; video_quality must be 480p/768p/1080p/2k/2K (400).
- A declared input_video_duration must be 1.625-60s (400).
- The source video must be <=50MB with an aspect ratio between 0.4 and 2.5; out-of-spec sources fail during generation. Upload the source with POST /api/storage/upload (the upload only checks the 50MB size).

Example body:

```json
{"mode": "minimax-h3-max-extend", "generation_type": "video-extend", "prompt": "The panther leaps onto a fallen log and looks around", "videos": ["https://cdn.veevid.ai/sample/extend-video-3.mp4"], "duration": "5", "video_quality": "768p", "aspect_ratio": "auto", "extend_output": "extended", "prompt_expansion_mode": "balanced", "input_video_duration": 6}
```

## MiniMax H3 Max — `minimax-h3-max-insert`

### `minimax-h3-max-insert` · `video-insert`

Inserts a newly generated 5-13s scene between two time points of a source video.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `video` **required** | string |  |  | Source video URL (singular field; 'videos' means reference videos here). |
| `prompt` | string |  |  | Describes the new scene. Required unless images or videos are given. |
| `duration` 💲 | string | 5–13 | "5" | Length of the new scene in seconds; decimals allowed. |
| `video_quality` 💲 | string | "480p", "768p" | "768p" | Output resolution. |
| `start_time` **required** | number | 1.625–60 |  | Cut-out point in seconds (24 fps frame grid). |
| `resume_time` **required** | number | 1.667–60 |  | Resume point in seconds. It must be at least 1 frame (1/24s) after start_time and leave >= 33/24s (+0.25s safety margin) of the source after it. Source between start and resume is replaced. |
| `images` 💲 | string[] |  |  | Reference images for the new scene, up to 9. |
| `videos` 💲 | string[] |  |  | Reference videos, up to 3. Each must be >= 2s, <= 15s in total, and uploaded with POST /api/storage/upload. |
| `reference_video_duration` 💲 | number | 0–15 |  | Send the total reference-video length in seconds. The server also measures the files and bills the measured value if it is more than 0.5s longer; if it is omitted with reference videos, the 15-second maximum is billed. |
| `input_video_duration` | number | 0–60 |  | Source video length in seconds; used to validate resume_time. The source is not billed. |
| `color_match` | boolean |  | true | Match the new scene's color grading to the source. |
| `prompt_expansion_mode` | string | "balanced", "disabled" | "balanced" | Only 'disabled' turns prompt expansion off. |
| `seed` | number |  |  | Optional integer >= 0. |

Input files:
- `video`: 1 source video URL in 'video' (about 3.3-60s, <=50MB; mp4/mov/webm/m4v)
- `images`: 0-9 reference image URLs in 'images' (jpg/png/webp)
- `videos`: 0-3 reference video URLs in 'videos' (mp4/mov, each >=2s, total <=15s, <=100MB each, uploaded with POST /api/storage/upload)

Upload folders (`folder` for `POST /api/storage/upload`): video → `minimax-h3-max-insert`, images → `minimax-h3-max-insert/reference-images`, videos → `minimax-h3-max-insert/reference-videos`

Rules:
- When sending reference videos, always send reference_video_duration equal to their total length (seconds).
- generation_type must be video-insert; video_quality must be 480p or 768p (400).
- duration must be 5-13 (400).
- Exactly one source in 'video'. Reference images must use 'images'; a singular 'image' is rejected (400).
- A prompt, a reference image or a reference video is required; audio is rejected (400).
- Reference videos must be uploaded with POST /api/storage/upload first; external URLs are rejected (400). Each must be >= 2s, the total <= 15s, and at most 3 videos and 9 images.
- start_time must be 1.625-60. resume_time must be > start_time by >= 1/24s and <= 60. With a declared source length, resume_time must be <= floor((source - 1.375 - 0.25) x 24)/24 (400).
- A declared source length must be ~3.29-60s (400).
- When quoting, send `input_image_count` for reference images, and for reference videos add `has_video_input: true`, `input_video_count` and `reference_video_duration` (the quote endpoint does not read these files, so the price would come out too low).

Example body:

```json
{"mode": "minimax-h3-max-insert", "generation_type": "video-insert", "prompt": "A glowing blue spirit drifts out of the stone archway", "video": "https://cdn.veevid.ai/sample/extend-video-2.mp4", "duration": "5", "video_quality": "768p", "start_time": 3, "resume_time": 3.042, "input_video_duration": 10.04, "color_match": true, "prompt_expansion_mode": "balanced"}
```

## MiniMax H3 Max — `minimax-h3-max-recast`

### `minimax-h3-max-recast` · `character-swap`

Swaps the people in a 5-30s video with people from 1-4 reference photos, keeping motion, camera and original audio.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `video` **required** | string |  |  | Source video URL (singular field). Must be uploaded with POST /api/storage/upload, MP4/MOV, 5-30s, and no single shot over 15s. |
| `images` **required** | string[] |  |  | 1-4 reference photos, one per new person, mapped left to right by default. |
| `prompt` | string |  |  | Optional (<=2000 chars), e.g. which person becomes whom. |
| `video_quality` 💲 | string | "768p", "1080p" | "1080p" | Output resolution. Always send video_quality. |
| `input_video_duration` 💲 | number | 5–30 |  | Source length in seconds (up to 2 decimals). Send the actual length; the server measures the file and bills the measured length. |
| `seed` | number |  |  | Optional integer >= 0. |

Input files:
- `video`: 1 source video URL in 'video' (MP4/MOV, 5-30s, <=50MB, uploaded with POST /api/storage/upload)
- `images`: 1-4 reference photo URLs in 'images' (jpg/png/webp, <=20MB each)

Upload folders (`folder` for `POST /api/storage/upload`): video → `minimax-h3-max-recast`, images → `minimax-h3-max-recast/reference-images`

Rules:
- Seconds = server-measured source length (minimum 5). Reference photos are free.
- generation_type must be character-swap; video_quality must be 768p or 1080p (400). Always send video_quality.
- Input files must be uploaded with POST /api/storage/upload first (external URLs are rejected).
- If the source video's duration cannot be read from its MP4/MOV header, the request returns 422 and nothing is charged.
- A measured length outside 5-30s (+-0.1s) is rejected (400).
- If the measured length exceeds the declared input_video_duration by >0.1s, it returns 409 with measured_duration and required_credits and charges nothing; show the user the new required_credits and get a yes before resubmitting with input_video_duration = measured_duration.
- 1-4 images required; a singular 'image', reference videos or audio are rejected (400); prompt <= 2000 chars.
- Duration and aspect ratio are not inputs: the output matches the source.

Example body:

```json
{"mode": "minimax-h3-max-recast", "generation_type": "character-swap", "prompt": "Replace the woman in the video with the person in photo 1", "video": "https://cdn.veevid.ai/ai-character-swap/talking-vlog-original.mp4", "images": ["https://cdn.veevid.ai/ai-character-swap/talking-vlog-new-character.webp"], "video_quality": "768p", "input_video_duration": 6.6}
```

## Video Lip Sync — `video-lip-sync`

### `video-lip-sync` · `lip-sync`

Re-syncs the mouth movements in an existing video to a new voice track; output length equals the audio length.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `videos` **required** | string[] |  |  | [source video URL]; only the first is used. The singular 'video' is also accepted. Must be uploaded with POST /api/storage/upload. |
| `audios` **required** | string[] |  |  | [voice audio URL]; only the first is used. The singular 'audio' is also accepted. Must be uploaded with POST /api/storage/upload; use clean vocals. |
| `input_audio_duration` 💲 | number | 0–61 |  | Send the audio length in seconds. |
| `lip_sync_mode` | string | "lite", "basic" | "lite" | lite: single front-facing speaker, faster. basic: complex scenes, multiple shots. |
| `lip_sync_separate_vocal` | boolean |  | false | Isolate vocals / suppress background noise. |
| `lip_sync_open_scenedet` | boolean |  | true | Shot and speaker detection (basic only). |
| `lip_sync_align_audio` | boolean |  | true | Loop the video when the audio is longer (lite only; always on in basic). |
| `lip_sync_align_audio_reverse` | boolean |  | false | Loop by playing in reverse (lite only; requires align_audio). |
| `lip_sync_templ_start_seconds` | number | 0–3600 | 0 | Start offset in the source video, floored to whole seconds (lite only). |

Input files:
- `video`: 1 source video URL (mp4/mov, <=100MB, short side >=360p, uploaded with POST /api/storage/upload)
- `audio`: 1 voice audio URL (mp3/wav/m4a/aac/ogg, <=10MB, <=60s, uploaded with POST /api/storage/upload)

Upload folders (`folder` for `POST /api/storage/upload`): video → `video-lip-sync`, audio → `video-lip-sync/audio`

Rules:
- Always send input_audio_duration equal to the audio length (seconds); if it is omitted you are charged for the 60-second maximum. If the output is longer than declared, the difference is charged after processing (an over-declared length is not refunded).
- generation_type must be lip-sync (422).
- The video and audio must be uploaded with POST /api/storage/upload first; external URLs are rejected (422).
- input_audio_duration > 61 is rejected (422; the limit is 60s plus 1s tolerance).
- No prompt, duration or aspect ratio: the output length equals the audio and the resolution follows the source.

Example body:

```json
{"mode": "video-lip-sync", "generation_type": "lip-sync", "videos": ["https://cdn.veevid.ai/ai-character-swap/talking-vlog-original.mp4"], "audios": ["https://cdn.veevid.ai/lip-sync/lip-sync-voice-woman.mp3"], "input_audio_duration": 12.09, "lip_sync_mode": "lite", "lip_sync_separate_vocal": false, "lip_sync_open_scenedet": true, "lip_sync_align_audio": true, "lip_sync_align_audio_reverse": false, "lip_sync_templ_start_seconds": 0}
```

## Google Veo 3.1 — `veo3`

### `veo3` · `video-extend`

Extends a Veo 3.1 video you generated earlier, identified by its task ID.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `taskId` **required** 💲 | string |  |  | The provider_task_id of one of your own earlier Veo 3.1 generations (returned when it was created and by the status endpoint). |
| `prompt` **required** | string |  |  | What happens in the extension. Required. |
| `generation_mode` 💲 | string | "lite", "fast", "quality" | "fast" | Extension quality tier. |
| `watermark` | string |  |  | Optional custom watermark text, <=200 chars. |
| `duration` | string | "4", "6", "8" | "8" | Must be 4, 6 or 8 if sent; send "8". |
| `aspect_ratio` | string | "original" | "original" | Send "original" (the value is not used). |

Rules:
- taskId is required (400). It must match one of your generations (404 'Task not found') owned by you (403).
- The source must be a Veo 3.1 or Grok Imagine video (400). A Grok Imagine taskId is run and priced as a Grok Imagine extend.
- 1080p and 4k Veo sources can be extended.
- When taskId belongs to a Grok Imagine video, the request is run and billed as a Grok Imagine extend: send duration "6" or "10" (or omit it), not "8".

Example body:

```json
{"mode": "veo3", "generation_type": "video-extend", "taskId": "veo_task_abc123", "prompt": "The drone keeps flying over the city at night", "generation_mode": "fast", "duration": "8", "aspect_ratio": "original"}
```

## Grok Imagine — `grok-imagine`

### `grok-imagine` · `video-extend`

Extends a Grok Imagine video you generated earlier by 6 or 10 seconds from a chosen point.

| Param | Type | Values | Default | Notes |
|---|---|---|---|---|
| `taskId` **required** 💲 | string |  |  | The provider_task_id of one of your own earlier Grok Imagine generations. |
| `prompt` **required** | string |  |  | What happens in the extension. Required. |
| `duration` 💲 | string | "6", "10" | "6" | Seconds to add. |
| `extend_at` | number |  | 0 | Start position in seconds (>= 0); 0 extends from the end of the video. |
| `aspect_ratio` | string | "original" | "original" | Send "original" (the value is not used). |

Rules:
- duration must be '6' or '10' (400 'Grok Imagine Extend only supports 6s or 10s durations').
- taskId is required, must exist (404) and belong to you (403). The source must be a Grok Imagine or Veo 3.1 video; a Veo 3.1 taskId is run and priced as a Veo 3.1 extend.

Example body:

```json
{"mode": "grok-imagine", "generation_type": "video-extend", "taskId": "grok_task_abc123", "prompt": "The knight raises his sword as the dragon lands", "duration": "6", "extend_at": 0, "aspect_ratio": "original"}
```
