# WeryAI Video Generator

Use this package when the task is official WeryAI video generation through the WeryAI API.

Preferred entry points:

- `node {baseDir}/scripts/wait-video.js`
- `node {baseDir}/scripts/submit-text-video.js`
- `node {baseDir}/scripts/submit-image-video.js`
- `node {baseDir}/scripts/submit-multi-image-video.js`
- `node {baseDir}/scripts/status-video.js`
- `node {baseDir}/scripts/models-video.js`
- `node {baseDir}/scripts/balance-video.js`

Default execution policy:

- In agent environments, default to result-first delivery for generation requests.
- For generation tasks, use `node {baseDir}/scripts/wait-video.js` by default so polling continues until videos are ready or timeout is reached.
- Enforce bounded polling with mode-aware timeout classes (`short`: 10 minutes, `long`: 30 minutes), unless explicitly overridden by environment.
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.
- Use `submit-*` when the user explicitly asks for task creation without waiting.
- Use `node {baseDir}/scripts/status-video.js` for progress checks on existing tasks.

Route intents this way:

- text brief -> text-to-video
- `image` -> image-to-video
- `first_frame` + `last_frame`, or `image` + `last_image` -> ordered multi-image transition flow
- `images` -> multi-image-to-video
- `taskId` or `batchId` -> status query, not a new paid submission

Delivery rules:
- If video URLs are available, return at least one playable Markdown link (for example `[Video](https://...)`). If multiple videos are generated, render all of them using markdown links consecutively.
- Alongside video output, include key generation parameters when available: `model`, `duration`, `aspect_ratio`, `resolution`, `generate_audio`.
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.

Read `SKILL.md` first for trigger language, defaults, workflow, and constraints.
Read `references/api-models.md` when you need exact model capabilities or parameter support.
Read `references/error-codes.md` when debugging failures or retry behavior.
