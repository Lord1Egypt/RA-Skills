# WeryAI Podcast Generator

Use this package when the task is official WeryAI podcast generation rather than music-only generation or general text chat.

Preferred entry points:

- `node {baseDir}/scripts/speakers.js`
- `node {baseDir}/scripts/submit-text.js`
- `node {baseDir}/scripts/generate-audio.js`
- `node {baseDir}/scripts/status.js`
- `node {baseDir}/scripts/wait.js`

Route intents this way:

- podcast voices or speaker lookup -> `speakers.js`
- create a podcast from a topic -> `wait.js`
- text generation only -> `submit-text.js`
- audio generation for an existing task -> `generate-audio.js`
- inspect podcast task state -> `status.js`

Default execution policy:


- Prefer result-first delivery. In agent environments, use `wait.js` for end-to-end podcast generation and delivery.
- Enforce bounded polling with a maximum timeout of 30 minutes (1800 seconds).

Delivery rules:

- Output final `audios` URLs directly as markdown links. Do not output just a `taskId`.
- If multiple audio tracks are generated, render all of them using markdown links consecutively.
- Summarize the key generation parameters used alongside the output (from `requestSummary` or your initial choices).
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally to check the status when asked.

Read `SKILL.md` first for defaults, mode rules, and paid-run workflow.
Read `references/podcast-api.md` when you need the exact endpoint contract.
