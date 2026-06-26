# WeryAI Video Tools Matrix

Use this file when you need the exact parameter surface for a video editing tool instead of relying on memory.

## Shared Contract

- Base URL: `https://api.weryai.com`
- Auth: `Authorization: Bearer <WERYAI_API_KEY>`
- Task model: async submit -> `task_id` / `task_ids` -> poll task status
- Status values: `waiting`, `processing`, `succeed`, `failed`
- Result field: `videos`

## Tool Summary

### `anime-replace`

- Endpoint: `/v1/generation/video-anime-replace`
- Use for: replace or move an element in a video with anime-style processing
- Required:
  - `video_url`
  - `image_url`
- Optional:
  - `type`: `move` | `replace`
  - `resolution`: `480p` | `580p` | `720p`
- Defaults in this skill:
  - `type=replace`
  - `resolution=720p`

### `background-remove`

- Endpoint: `/v1/generation/video-background-remove`
- Use for: remove background or replace it with a solid color
- Required:
  - `video_url`
- Optional:
  - `background_color`: `TRANSPARENT`, `BLACK`, `WHITE`, `GRAY`, `RED`, `GREEN`, `BLUE`, `YELLOW`, `CYAN`, `MAGENTA`, `ORANGE`
- Default in this skill:
  - `background_color=BLACK`

### `extend`

- Endpoint: `/v1/generation/video-extend`
- Use for: continue or lengthen a source video
- Required:
  - `video_url`
  - `prompt`
- Optional:
  - `style`: `anime` | `3d_animation` | `cyberpunk` | `comic`
  - `resolution`: `360p` | `540p` | `720p` | `1080p`
  - `duration`: `5` | `8`
- Defaults in this skill:
  - `style=anime`
  - `resolution=720p`
  - `duration=5`

### `face-change`

- Endpoint: `/v1/generation/video-face-change`
- Use for: swap the face in a source video
- Required:
  - `video_url`
  - `image_url`

### `lips-change`

- Endpoint: `/v1/generation/video-lips-change`
- Use for: lip-sync a video to a provided audio file
- Required:
  - `video_url`
  - `audio_url`

### `magic-style`

- Endpoint: `/v1/generation/video-magic`
- Use for: style-transfer a source video
- Required:
  - `video_url`
- Optional:
  - `video_style`: `realistic_2` | `anime_style_3` | `anime_style_4`
- Default in this skill:
  - `video_style=anime_style_3`

### `subtitle-erase`

- Endpoint: `/v1/generation/video-subtitle-erase`
- Use for: remove subtitle text from a video
- Required:
  - `video_url`
- Optional:
  - `rect_vo_list`
- Region shape:
  - `lt_x`, `lt_y`, `rb_x`, `rb_y`
  - normalized to `0~1`
- If no region is provided, the API uses auto-detection.

### `subtitle-translate`

- Endpoint: `/v1/generation/video-subtitle-translate`
- Use for: translate subtitles to another language
- Required:
  - `video_url`
  - `target_language`
- Common language codes:
  - `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`

### `upscaler`

- Endpoint: `/v1/generation/video-upscaler`
- Use for: upscale a source video
- Required:
  - `video_url`
- Optional:
  - `resolution`: `1080p` | `2k` | `4k`
- Default in this skill:
  - `resolution=1080p`

### `watermark-remove`

- Endpoint: `/v1/generation/video-watermark-remove`
- Use for: remove watermark overlays from a video
- Required:
  - `video_url`
- Optional:
  - `rect_vo_list`
- Region shape:
  - `lt_x`, `lt_y`, `rb_x`, `rb_y`
  - normalized to `0~1`
- If no region is provided, the API uses auto-detection.

## Guidance Rules

- Ask for the smallest missing parameter set; do not dump every field at once.
- Prefer defaults only when the API clearly supports them.
- Ask before paid execution if the user has not confirmed the final tool choice or irreversible processing settings.
- Keep all asset URLs public `https://` URLs.
