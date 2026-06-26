# WeryAI Image Generator

Use this package when the task is official WeryAI image generation through the WeryAI API.

Preferred entry points:

- `node {baseDir}/scripts/submit-text-image.js`
- `node {baseDir}/scripts/submit-image-to-image.js`
- `node {baseDir}/scripts/status-image.js`
- `node {baseDir}/scripts/wait-image.js`
- `node {baseDir}/scripts/models-image.js`
- `node {baseDir}/scripts/balance-image.js`

Default execution policy:

- In agent environments, prefer completing the request to visible image output when the workflow allows it.
- Use the matching `submit-*` command as the default entry point.
- Treat `taskId` or `batchId` as tracking data only.
- After submit, default to polling for final results with `status-image.js`.
- Continue polling until images are ready or the maximum timeout of 5 minutes (300 seconds) is reached.
- Do not run unbounded polling loops; always enforce a timeout ceiling.
- Use `node {baseDir}/scripts/status-image.js` for both default polling and user-requested progress checks.
- Use `node {baseDir}/scripts/wait-image.js` only when the user explicitly asks for one-shot submit-and-wait behavior.

Route intents this way:

- prompt only -> text-to-image
- `image` or `images` -> image-to-image
- `taskId` or `batchId` -> status query, not a new paid submission
- model or parameter question -> run `models-image.js` first

Delivery rules:
- When an image or image set is ready, send/display the actual image output to the user immediately.
- If image URLs are available, return at least one user-visible link (for example `[Image](https://...)`) or inline image rendering when supported. If multiple images are generated, render all of them using markdown image syntax consecutively.
- `taskId` / `batchId` can be included as metadata but must not be the only deliverable unless the user explicitly asked for IDs first.
- If timeout is reached before completion, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.
- Never stop at a filename or local file path alone. If the environment supports file sending, send the file. If it supports inline rendering, render inline. Otherwise provide a usable download URL.

Read `SKILL.md` first for trigger language, defaults, workflow, and constraints.
Read `references/api-models.md` when you need exact model capabilities or parameter support.
Read `references/error-codes.md` when debugging failures or retry behavior.
