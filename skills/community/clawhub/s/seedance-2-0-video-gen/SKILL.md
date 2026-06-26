---
name: seedance-2.0-video-gen
version: 1.0.0
description: "Generate Seedance 2.0 videos through WeryAI for text-to-video, image-to-video, multi-image video, and first-frame/last-frame transitions. Use when you need a Seedance 2.0 video generator, want to animate an HTTPS image, create a storyboard-to-video clip, migrate `image + last_image` workflows, or generate controlled start/end frame video with your WeryAI API key."

tags: [seedance, seedance-2, video-gen, text-to-video, image-to-video, multi-image-video, storyboard, start-frame, end-frame]

metadata: { "openclaw": { "emoji": "🎬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Seedance 2.0 video generator

Generate Seedance 2.0 videos through WeryAI with one focused skill: text-to-video, image-to-video, multi-image video, and first-frame/last-frame transition control. This skill is intentionally strict about secret declaration and input safety: the only runtime secret is `WERYAI_API_KEY`, and reference media must be public `https` URLs rather than ad-hoc local uploads.

**Dependencies:** `scripts/video_gen.js` in this directory + `WERYAI_API_KEY` + Node.js 18+. No other Cursor skills are required.

## Authentication and first-time setup

Before the first real generation run:

1. Create a WeryAI account.
2. Open the API key page at `https://www.weryai.com/api/keys`.
3. Create a new API key and copy the secret value.
4. Add it to the required environment variable `WERYAI_API_KEY`.
5. Make sure the WeryAI account has available balance or credits before paid generation.

### OpenClaw-friendly setup

- This skill already declares `WERYAI_API_KEY` in `metadata.openclaw.requires.env` and `primaryEnv`.
- After installation, if the installer or runtime asks for required environment variables, paste the key into `WERYAI_API_KEY`.
- If you are configuring the runtime manually, export it before running commands:

```sh
export WERYAI_API_KEY="your_api_key_here"
```

### Quick verification

Use one safe check before the first paid run:

```sh
node {baseDir}/scripts/video_gen.js models --mode text_to_video
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"A glowing koi swims through ink clouds","duration":5}' --dry-run
```

- `models` confirms that the key is configured and the models endpoint is reachable.
- `--dry-run` confirms the request shape locally without spending credits.
- Real `wait` or `submit-*` commands still require available WeryAI balance.

## Quick summary

- Main jobs: Seedance 2.0 text-to-video, single-image animation, multi-image video, start/end-frame transition video
- Main inputs: `prompt`, `image`, `images`, `first_frame`, `last_frame`, `last_image`
- Main outputs: `taskId`, `videos`, task status, model capability checks
- Main trust signals: declared `WERYAI_API_KEY`, no local-file upload requirement, dry-run support, explicit paid-task warning

## Example prompts

- `Generate a Seedance 2.0 text-to-video clip: a silver train exits a tunnel into sunrise mist, 9:16 vertical`
- `Animate this HTTPS portrait with Seedance 2.0 image-to-video and keep the face consistent`
- `Turn these three storyboard images into one coherent product reveal video with consistent lighting`
- `Use these first and last frames to generate a smooth transition video with the same character`
- `Migrate this WaveSpeed Seedance flow that uses image plus last_image into the WeryAI version`

## Prerequisites

- `WERYAI_API_KEY` **must be set** before running `video_gen.js`.
- Node.js **18+** is required.
- `image`, `images`, `first_frame`, `last_frame`, and `last_image` inputs **must** be public `https` URLs. Do not pass local files.
- Every real `wait` or `submit-*` run creates a paid WeryAI task.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat it as a secret. Configure it only in the runtime environment; never write the secret value into the skill files.
- **Optional URL overrides** (`WERYAI_BASE_URL`, `WERYAI_MODELS_BASE_URL`): `video_gen.js` defaults to **`https://api.weryai.com`** and **`https://api-growth-agent.weryai.com`**. Only override them for trusted environments.
- **Higher assurance**: Run paid jobs in a short-lived shell or isolated environment, and review `scripts/video_gen.js` before production use.

## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts for you. Before every paid call, turn the user's short brief into a complete production prompt in English unless they already gave you a final long prompt and explicitly asked you not to rewrite it.

For advanced prompt design patterns, read [references/seedance-prompt-optimization.md](references/seedance-prompt-optimization.md) before drafting the final API `prompt`.

**Always add:**

- Shot scale, angle, and lens feel.
- Camera movement or a clear lock-off choice.
- Lighting direction, material response, and overall mood.
- Subject motion paced to the selected `duration`.
- One clear visual payoff in the final shot.
- Output framing such as `9:16 vertical` when using the default aspect ratio.

**Mode-specific additions:**

- **Text-to-video**: define the scene, motion beat, and ending reveal.
- **Single image**: preserve identity, composition, and palette from the reference image; keep the motion plausible.
- **Multi-image**: describe the transition path across the image sequence instead of treating the images as unrelated shots.
- **First-frame / last-frame**: explicitly describe how the opening frame evolves into the ending frame while preserving the same subject, scene logic, and temporal continuity.

**Length:** Current frozen Seedance rows in this document use a `prompt` limit of **2000 chars** where documented. If you re-check live metadata with `models`, trust the live value.

**Confirmation:** Always show the **full expanded prompt** and all selected parameters in a table, then wait for the user to reply **`confirm`** or request edits.

### Prompt optimization workflow

Use this sequence whenever the user asks for stronger Seedance prompt quality or tighter control:

1. Pick the mode first: text-only, single-image, multi-image, or first/last-frame.
2. Map each asset to a role: identity anchor, first frame, waypoint, or ending frame.
3. Break the clip into 2 to 4 timecoded beats based on `duration`.
4. Write one primary action arc and one clear final payoff.
5. Add only the negative constraints that directly help this request.

If the request is complex, structure the prompt plan internally as:

- `Mode`
- `Asset mapping`
- `Timeline beats`
- `Final prompt`
- `Negative constraints`
- `Generation settings`

## Input shapes

| Use case | Accepted fields | Notes |
|----------|-----------------|-------|
| Text-to-video | `prompt`, `duration`, optional `aspect_ratio`, `resolution`, `generate_audio` | Default model is `SEEDANCE_2_0`. |
| Single-image animation | `image` + `prompt` | Keeps the reference composition and identity. |
| Multi-image video | `images` + `prompt` | Ordered list, trimmed to the model limit. |
| Start/end-frame guidance | `first_frame` + `last_frame` + `prompt` | Internally normalized to ordered `images`. |
| WaveSpeed-style migration | `image` + `last_image` + `prompt` | Supported as a compatibility alias for end-frame workflows. |

## Migration notes

- If you are coming from a WaveSpeed-style Seedance workflow, map `last_image` to this skill's end-frame path. This skill accepts `image + last_image` as a compatibility alias and normalizes it to the ordered multi-image route.
- Do **not** rely on local file uploads. Convert or host your references first and pass public `https` URLs only.
- This skill's metadata correctly declares the required secret (`WERYAI_API_KEY`) so installers and reviewers can see the runtime contract up front.

## Prompt engineering recipes

When the user asks for "better Seedance prompts" rather than just API execution:

- Use the mode table, timeline planning, and prompt skeletons in `references/seedance-prompt-optimization.md`.
- Prefer timecoded beats over long adjective-heavy paragraphs.
- For `first_frame` / `last_frame` or `image` + `last_image`, explicitly describe the bridge action between start and end state.
- For `images`, treat them as ordered waypoints of one coherent shot, not unrelated inspirations.
- For product, character, transformation, or storyboard prompts, use the scenario-specific recipes from the reference file before writing the final prompt.

## Workflow

1. Decide which path fits the request: `text`, `image`, `multi-image`, or `first-frame/last-frame`.
2. Collect the user's brief, `duration`, optional `aspect_ratio`, optional `resolution`, and required HTTPS image URLs if the mode uses references.
3. Expand the prompt with the rules from `## Prompt expansion (mandatory)`. If the request needs tighter control, read `references/seedance-prompt-optimization.md` and explicitly decide mode, asset mapping, timeline beats, and negative constraints before writing the final prompt.
4. If you are unsure about current multi-image support or field limits, run `node {baseDir}/scripts/video_gen.js models --mode multi_image_to_video` before a paid request.
5. Show a confirmation table with the **full expanded prompt**, model, duration, aspect ratio, resolution, audio choice, and any image URLs.
6. After explicit confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'`.
7. Return the JSON result. On success, surface the video URLs. On failure, report `errorCode` and `errorMessage` and suggest the likely parameter fix.

## CLI reference

```sh
# Check live model metadata
node {baseDir}/scripts/video_gen.js models
node {baseDir}/scripts/video_gen.js models --mode text_to_video
node {baseDir}/scripts/video_gen.js models --mode image_to_video
node {baseDir}/scripts/video_gen.js models --mode multi_image_to_video

# Text-to-video
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"A paper crane unfolds into a real bird, cinematic lighting, 9:16 vertical","duration":5}'

# Single image to video
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"Animate this portrait with subtle hair and cloth movement","image":"https://example.com/frame.png","duration":5,"aspect_ratio":"9:16","resolution":"720p"}'

# Multi-image to video
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"Turn these storyboard frames into one coherent reveal shot","images":["https://example.com/1.png","https://example.com/2.png","https://example.com/3.png"],"duration":5,"aspect_ratio":"9:16"}'

# First-frame / last-frame guided video
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"Start on the first frame and transition naturally to the last frame with the same subject and environment","first_frame":"https://example.com/start.png","last_frame":"https://example.com/end.png","duration":5,"aspect_ratio":"9:16"}'

# WaveSpeed-style compatibility alias
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"Transition smoothly from the start image to the end image","image":"https://example.com/start.png","last_image":"https://example.com/end.png","duration":5,"aspect_ratio":"9:16"}'

# Preview without spending credits
node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"A glowing koi swims through ink clouds","duration":5}' --dry-run

# Poll an existing task
node {baseDir}/scripts/video_gen.js status --task-id <task-id>
```

## Definition of done

Done when the user receives at least one playable video URL, or a clear failure with `errorCode` / `errorMessage` and a concrete next step. The submitted payload must stay within the selected model's supported field set.

## Boundaries (out of scope)

- Do not use local file paths for references; only public `https` URLs are supported.
- Do not invent undocumented API fields beyond the JSON surface in this skill.
- Do not assume multi-image or first/last-frame support without checking live metadata when the behavior matters.
- Do not store the secret value of `WERYAI_API_KEY` inside the repository.
- Do not copy parameter names blindly from another provider without checking the normalized fields in this document.

## Model & API constraints (frozen for this skill)

> Frozen from the repository's current WeryAI capability snapshots. Re-run `node {baseDir}/scripts/video_gen.js models` after platform upgrades.

### Text-to-video (`SEEDANCE_2_0`)

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | Prompt max |
|-----------|-----------|---------------|-------------|-------|-----------------|------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | 2000 |

### Image-to-video (`SEEDANCE_2_0`)

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | upload_image_limit |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | 3 |

### Multi-image and first-frame / last-frame

- Use the `images` array for multi-image generation.
- Use either `images` with ordered URLs, `first_frame` + `last_frame`, or `image` + `last_image` for start/end-frame control.
- Before a paid submission where multi-image support matters, run `node {baseDir}/scripts/video_gen.js models --mode multi_image_to_video` and confirm `support_multiple_images`, `support_first_last_frame`, `upload_image_limit`, and allowed output fields on the live account.
- If the live registry says the model cannot take multiple images, the runtime falls back to the first image only.

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | `SEEDANCE_2_0` |
| Aspect ratio | `9:16` |
| Duration | `5` |
| Resolution | `720p` |
| Audio | `false` by default; enable only when you want generated ambience |
| Prompt style | concise cinematic English prompt with one clear motion beat and one final payoff |

---

## Text brief -> Seedance video

Use this when the user has only an idea and wants Seedance 2.0 to generate the clip from scratch.

**Need from the user:**

- Subject or scene
- Motion beat
- Preferred aspect ratio or platform
- Optional duration and resolution

**Flow:**

1. Expand the brief into a full English prompt.
2. Keep `model` at `SEEDANCE_2_0` unless the user explicitly wants another model.
3. Show a confirmation table:

   > 📋 **Ready to generate - please confirm**
   >
   > | Field | This run | Notes |
   > |-------|----------|-------|
   > | `model` | `SEEDANCE_2_0` | Override only if the user explicitly requests another model |
   > | `aspect_ratio` | `9:16` | Must stay inside the Seedance row |
   > | `duration` | `5` | Allowed: 5 / 10 / 15 |
   > | `resolution` | `720p` | Allowed: 480p / 720p |
   > | `generate_audio` | `false` | Turn on only if the user wants generated ambience |
   > | `prompt` | **full expanded prompt** | Never show only a summary |

4. After confirmation, run:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"...","duration":5,"aspect_ratio":"9:16","resolution":"720p"}'
   ```

---

## Single HTTPS image -> Seedance motion

Use this when the user already has one reference image and wants subtle or medium motion while preserving the subject.

**Need from the user:**

- One public `https` image URL
- Desired motion direction
- Optional duration, aspect ratio, and audio

**Flow:**

1. Expand the prompt around preservation plus motion.
2. Add `image` to the JSON body.
3. Confirm parameters and URL, then run:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"...","image":"https://example.com/input.png","duration":5,"aspect_ratio":"9:16","resolution":"720p"}'
   ```

---

## Multiple HTTPS images -> Seedance storyboard clip

Use this when the user wants several frames turned into one coherent shot or short sequence.

**Need from the user:**

- Ordered public `https` image URLs
- Desired transition logic
- Optional duration and aspect ratio

**Flow:**

1. Treat the image order as meaningful story order.
2. If support is uncertain, check `models --mode multi_image_to_video` first.
3. Confirm the final prompt plus ordered `images`, then run:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"...","images":["https://example.com/1.png","https://example.com/2.png","https://example.com/3.png"],"duration":5,"aspect_ratio":"9:16"}'
   ```

---

## First frame + last frame -> controlled transition

Use this when the user wants tighter motion control from a known opening frame to a known ending frame.

**Need from the user:**

- One public `https` start frame
- One public `https` end frame
- A prompt that explains the in-between action

**Flow:**

1. Expand the prompt so it explicitly bridges the first frame to the last frame.
2. Use either `first_frame` / `last_frame`, `image` / `last_image`, or pass the same two URLs through `images` in order.
3. Confirm both URLs and the full prompt, then run:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"prompt":"...","first_frame":"https://example.com/start.png","last_frame":"https://example.com/end.png","duration":5,"aspect_ratio":"9:16"}'
   ```

4. If the live registry rejects multi-image routing, reduce expectations: the runtime will fall back to single-image behavior with the first frame.
