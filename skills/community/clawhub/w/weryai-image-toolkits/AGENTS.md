# WeryAI Image Toolkits

Use this package when the user wants WeryAI image editing or post-processing rather than text-to-image or image-to-image generation.

Preferred entry points:

- `node {baseDir}/scripts/image_toolkits.js tools`
- `node {baseDir}/scripts/image_toolkits.js submit --tool <tool-id> --json '{...}'`
- `node {baseDir}/scripts/image_toolkits.js wait --tool <tool-id> --json '{...}'`
- `node {baseDir}/scripts/image_toolkits.js status --task-id <task-id>`

Default execution policy:

- For async tools, default to `wait` so users receive final processed image output in the same turn.
- Enforce bounded polling with a maximum timeout of 5 minutes (300 seconds).
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.
- `submit` is for explicit task-creation requests or synchronous tools such as `image-to-prompt`.
- If output images are available, return user-visible image links and key parameters (`tool`, `model`, `aspect_ratio`, `image_number`, `resolution`) when present. If multiple images are generated, render all of them using markdown image syntax consecutively.

Route intents this way:

- analyze image into a prompt -> `image-to-prompt`
- replace or recolor background -> `background-change`
- remove background -> `background-remove`
- expand canvas -> `expand`
- face swap -> `face-swap`
- change aspect ratio -> `reframe`
- repair old photo -> `repair`
- erase text or watermark -> `text-erase`
- translate image text -> `translate`
- upscale image -> `upscale`

Read `SKILL.md` first for trigger language, defaults, missing-parameter guidance, and paid-run confirmation rules.
Read `references/image-tools-matrix.md` when you need exact required fields, defaults, or enum values.
