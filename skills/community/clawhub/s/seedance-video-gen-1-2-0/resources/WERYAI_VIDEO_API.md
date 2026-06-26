# WeryAI video CLI & JSON (`video_gen.js`)

Shipped at **`{baseDir}/resources/WERYAI_VIDEO_API.md`** (next to `SKILL.md`). Run the CLI from **`{baseDir}/scripts/video_gen.js`**. Node.js **18+** required.

## Environment

- **`WERYAI_API_KEY`** (required for `models`, generation, and `status`, except `--dry-run`): bearer token for HTTPS requests. Never commit the value.
- **No other environment variables** are read by this script. API hosts and poll timing are fixed in `video_gen.js` source.

## API hosts (fixed)

- Video tasks: `https://api.weryai.com`
- Models registry: `https://api-growth-agent.weryai.com`

## `models` — fetch model metadata (JSON on stdout)

Run from the skill root (`{baseDir}`):

```sh
node {baseDir}/scripts/video_gen.js models
node {baseDir}/scripts/video_gen.js models --mode text_to_video
node {baseDir}/scripts/video_gen.js models --mode image_to_video
node {baseDir}/scripts/video_gen.js models --mode multi_image_to_video
```

Typical fields per model (names as returned by the API): `model_key`, `title`, `durations`, `aspect_ratios`, `resolutions`, `has_generate_audio`, `has_negative_prompt`, `prompt_length_limit`; image / multi-image modes may include `support_multiple_images`, `support_first_last_frame`, `upload_image_limit`, etc.

Use this output to fill **`## Model and API constraints`** in the skill’s `SKILL.md`. Do not send fields (e.g. `resolution`, `aspect_ratio`) that the chosen model does not support.

## `wait` — submit and block until done (polls status)

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"...","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '{"model":"...","prompt":"...","image":"https://...","duration":5}'
node {baseDir}/scripts/video_gen.js wait --json '{"model":"...","prompt":"...","images":["https://..."],"duration":5}'
node {baseDir}/scripts/video_gen.js wait --json '...' --dry-run
```

## `submit-*` — submit only (async; no wait)

```sh
node {baseDir}/scripts/video_gen.js submit-text --json '{"model":"…","prompt":"…","duration":5}'
node {baseDir}/scripts/video_gen.js submit-image --json '{"model":"…","prompt":"…","image":"https://…","duration":5}'
node {baseDir}/scripts/video_gen.js submit-multi-image --json '{"model":"…","prompt":"…","images":["https://…"],"duration":5}'
```

## `status` / `batch-status`

```sh
node {baseDir}/scripts/video_gen.js status --task-id <id>
node {baseDir}/scripts/video_gen.js batch-status --batch-id <id>
```

Task id / batch id can also be passed inside JSON for some flows; see `video_gen.js` usage text.

## Common JSON fields

| Field | Notes |
|--------|--------|
| `model` | Model key; **required** for `wait`, `submit-*`, and for `--dry-run` when `prompt` is present—if omitted or empty, the script returns `MISSING_PARAM` (no default model). **The script does not enforce** per-skill model rules from `SKILL.md`—callers must pass the model required by that skill. |
| `prompt` | Required for `wait` and `submit-*` |
| `duration` | Must be allowed for the model |
| `aspect_ratio` | Only if supported |
| `resolution` | Only if supported |
| `generate_audio` | Only if supported |
| `negative_prompt` | Only if supported |
| `image` | Public **https** URL (single image) |
| `images` | Array of public **https** URLs (multi-image) |

## Status response (conventions)

- HTTP OK with business `status === 0`: query succeeded.
- `data` may be a single object or an array of tasks; the script matches `task_id` or uses the first item.
- In progress: `phase` may be `running`, `inProgress: true`.
- Errors: stdout JSON with `ok: false`, `errorCode`, `errorMessage` (prefers API `message` / `desc`).

## Stdout JSON (generation / wait)

Common keys: `ok`, `phase`, `taskId`, `batchId`, `taskIds`, `videos` (`url`, `cover_url`), `tasks` (batch), `inProgress`, `errorCode`, `errorMessage`.

---

**Per-skill rules** in `SKILL.md` (prompt expansion, confirmation table, niche tables) still apply; this file only documents the **CLI and request shape**.
