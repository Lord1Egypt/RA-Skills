# WeryAI Music Generator

Use this package when the task is official WeryAI music generation through the WeryAI API.

Preferred entry points:

- `node {baseDir}/scripts/wait-music.js`
- `node {baseDir}/scripts/submit-music.js`
- `node {baseDir}/scripts/status-music.js`
- `node {baseDir}/scripts/balance-music.js`

Default execution policy:


- Prefer result-first delivery. In agent environments, use `wait-music.js` to submit and poll until final audio URLs are ready.
- Enforce bounded polling with a maximum timeout of 10 minutes (600 seconds).
- Use `node {baseDir}/scripts/submit-music.js` only when the user explicitly asks for async behavior or a task ID without waiting.

Delivery rules:

- Output final `audios` URLs directly as markdown links. Do not output just a `taskId`.
- If multiple audio tracks are generated, render all of them using markdown links consecutively.
- Summarize the key generation parameters used alongside the output (from `requestSummary` or your initial choices).
- If timeout is reached, return the `taskId` to the user and ask if they want you to check the status again. Do NOT show the raw node status command to the user; use it internally.

Route intents this way:

- generic music request -> default to `VOCAL_SONG`
- instrumental, soundtrack, background music -> `ONLY_MUSIC`
- song, vocals, lyrics, singer gender, timbre -> `VOCAL_SONG`
- existing `taskId` -> status query, not a new paid submission
- account readiness question -> check balance first

Read `SKILL.md` first for trigger language, defaults, workflow, and constraints.
Read `references/api-music.md` when you need exact field rules or style keys.
Read `references/error-codes.md` when debugging failures or retry behavior.
