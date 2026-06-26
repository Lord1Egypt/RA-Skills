# WeryAI Video Toolkits

Use this package when the user wants WeryAI video editing or post-processing rather than video generation.

Preferred entry points:

- `node {baseDir}/scripts/video_toolkits.js tools`
- `node {baseDir}/scripts/video_toolkits.js submit --tool <tool-id> --json '{...}'`
- `node {baseDir}/scripts/video_toolkits.js wait --tool <tool-id> --json '{...}'`
- `node {baseDir}/scripts/video_toolkits.js status --task-id <task-id>`

Default execution policy:


- For async tools, default to `wait` so users receive final processed image output in the same turn.
- Enforce bounded polling with a maximum timeout of 30 minutes (1800 seconds).
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.
- `submit` is for explicit task-creation requests.

Route intents this way:

- replace object in anime style -> `anime-replace`
- remove or recolor video background -> `background-remove`
- extend a short video -> `extend`
- swap face in a video -> `face-change`
- lip-sync video to audio -> `lips-change`
- transfer video style -> `magic-style`
- remove subtitles -> `subtitle-erase`
- translate subtitles -> `subtitle-translate`
- upscale video -> `upscaler`
- remove watermark -> `watermark-remove`

Delivery rules:
- If video URLs are available, return at least one playable Markdown link (for example `[Video](https://...)`). If multiple videos are generated, render all of them using markdown links consecutively.
- Alongside video output, include key parameters when available: `tool`, `style`, `duration`, `resolution`, `type`, `target_language`.
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.

Read `SKILL.md` first for trigger language, defaults, missing-parameter guidance, and paid-run confirmation rules.
Read `references/video-tools-matrix.md` when you need exact required fields, defaults, or enum values.
