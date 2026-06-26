---
name: "seedance-video-gen-1-2.0"
version: 1.0.0
description: "Multi-version Seedance video generation on WeryAI (Seedance 2.0, 1.5 Pro, 1.0 Pro / Fast / Lite): text-to-video and image-to-video with version-aware limits. Defaults to Seedance 2.0 (SEEDANCE_2_0). Use when you need a Seedance clip and may switch lineage for aspect ratios, duration cap, audio, negatives, or multi-image / first-last-frame support. SEO: Seedance multi-version video; Seedance 2.0 default video-gen."

tags: [seedance, seedance-2, seedance-1-5, seedance-1, multi-version, text-to-video, image-to-video, video-gen]

metadata: { "openclaw": { "emoji": "🎬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Seedance multi-version generator (default 2.0)

Generate video with **Seedance 2.0**, **Seedance 1.5 Pro**, or **Seedance 1.0** variants on WeryAI. **`model` is required** in every JSON body—**default `model_key` is `SEEDANCE_2_0`** unless the user explicitly picks another row in **`## Model and API constraints`**.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. When you run the CLI, **`{baseDir}/scripts/video_gen.js`** must exist; **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** must exist under **`{baseDir}/resources/`** (publish or pre-use assembly). Full commands and JSON fields: see **`resources/WERYAI_VIDEO_API.md`**. **No other Cursor skills required.**

## Choosing a Seedance version (quick map)

| User intent (examples) | `model_key` | Typical reason |
|------------------------|-------------|----------------|
| Default / “Seedance” / “2.0” / best motion + audio | **`SEEDANCE_2_0`** | Up to **15s**, **generated audio**, multi-image + first/last on **image** path |
| “1.5 Pro” / wider aspect set / **1080p** text or image | **`DOUBAO_1_5_PRO`** | Rich **aspect_ratios**, **1080p**; image path: **first/last** yes, **single image only** (`upload_image_limit` 1) |
| “1.0 Pro” / classic Pro | **`DOUBAO`** | **1080p**; image path: **single** ref, **no** multi-image / first-last in metadata |
| “1.0 Fast” / cheaper draft | **`DOUBAO_1_PRO_FAST`** | **1080p**, fast tier; image: **single** ref |
| “1.0 Lite” / multi-image on **1.x** line | **`DOUBAO_1_LITE`** | Image path: **multi-image** up to **3**; **no** first/last in metadata |

Always re-check **`duration`**, **`aspect_ratio`**, **`resolution`**, **`generate_audio`**, and **whether `negative_prompt` is allowed** for the **selected `model_key` and channel** (text vs image)—see frozen tables below.

## Prerequisites

- `WERYAI_API_KEY` **must be set** before running `video_gen.js`.
- Node.js **18+**; reference URLs **must** be public **`https`** (no local paths).
- **`model` is mandatory** in `wait --json`. If the user does not specify a version, use **`SEEDANCE_2_0`**.
- Each `wait` run may consume credits; re-run creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Child skills must not document or rely on URL environment-variable overrides—only **`WERYAI_API_KEY`** is read from the environment.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use.

## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short brief into a **full English production `prompt`**.

**When:** Input is short or vague. **Exception:** The user supplies a finished long prompt within **`prompt_length_limit`** and explicitly asks you **not** to rewrite—still show the **full** text in the confirmation table.

**Always add:** shot size and angle; camera move or lock-off; lighting and mood; motion paced to **`duration`**; one clear payoff; framing for **`aspect_ratio`**; if **`generate_audio`** is **true**, describe ambience/SFX in generic words (no copyrighted music).

**`negative_prompt`:** Send **only** when the frozen row for that **`model_key`** and **channel** shows **Yes**. Otherwise **omit** the field.

**Length:** Stay within the selected row's **`prompt_length_limit`** (all listed: **2000**).

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`**, **`model`**, and every field you will send.

## Workflow

1. Detect whether the job is **text-to-video** or **image-to-video** (including multi-image / first-last).
2. **Pick `model_key`:** default **`SEEDANCE_2_0`**; if the user names another Seedance line, map with **`## Choosing a Seedance version`** and the frozen tables.
3. **Validate features vs model:** e.g. do **not** send **`images`** with more than one URL for models with **`support_multiple_images: false`** or **`upload_image_limit: 1`**.
4. **Expand prompt (mandatory)** per above.
5. Show the confirmation table (full `prompt`, `model`, `duration`, `aspect_ratio`, `resolution`, `generate_audio`, optional `negative_prompt`, URLs).
6. Run `node {baseDir}/scripts/video_gen.js wait --json '...'`.
7. Return **`videos`** as **`[Video](url)`** Markdown links—**not** inside code fences.

## CLI reference

~~~sh
node {baseDir}/scripts/video_gen.js models --mode text_to_video
node {baseDir}/scripts/video_gen.js models --mode image_to_video
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user gets a playable **[Video](url)** link or a clear error with a parameter fix. The submitted payload **must** match the **selected `model_key`** row. Default version behavior: **`SEEDANCE_2_0`** when unspecified.

## Boundaries (out of scope)

- Do not send **`negative_prompt`** when the frozen row says **No** for that model and channel.
- Do not exceed **`upload_image_limit`** or use multi-image when **`support_multiple_images`** is **false**.
- Do not use local file paths for media; do not embed **`WERYAI_API_KEY`** values in files.
- Do not link to `weryai-model-capabilities.md` or arbitrary `../references/` paths; use **`resources/WERYAI_VIDEO_API.md`** for CLI/API details.
- Do not wrap user-facing playable URLs in Markdown code fences.

### Example prompts

- `Default Seedance vertical: rainy alley, slow push-in, 10s` → **`SEEDANCE_2_0`**
- `Use Seedance 1.5 Pro, 1080p, 3:4, text-only` → **`DOUBAO_1_5_PRO`**
- `Seedance 1.0 Lite, three product photos in order` → **`DOUBAO_1_LITE`** + `images` (≤3 URLs)
- `First and last frame transition, best quality` → prefer **`SEEDANCE_2_0`**; **`DOUBAO_1_5_PRO`** only if user insists on 1.5 and accepts **single** reference constraints (see table)

---

## Model and API constraints (frozen for this skill)

> From `node {baseDir}/scripts/video_gen.js models` (`text_to_video` + `image_to_video`) at authoring time. Re-run after upgrades. **`multi_image_to_video` mode returned `[]` on the authoring run**—use **`image_to_video`** rows below for image counts and flags.

### Text-to-video

| model_key | Title (API) | durations | aspect_ratios | resolutions | Audio | negative_prompt | prompt limit |
|-----------|-------------|-----------|---------------|-------------|-------|-----------------|--------------|
| `SEEDANCE_2_0` | Seedance 2.0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | 2000 |
| `DOUBAO_1_5_PRO` | Seedance 1.5 Pro | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | Yes | No | 2000 |
| `DOUBAO_1_PRO_FAST` | Seedance 1.0 Pro Fast | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | No | 2000 |
| `DOUBAO_1_LITE` | Seedance 1.0 Lite | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p | No | No | 2000 |
| `DOUBAO` | Seedance 1.0 Pro | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | No | 2000 |

### Image-to-video

| model_key | durations | aspect_ratios | resolutions | Audio | negative_prompt | Multi-image | First/last frame | upload_image_limit |
|-----------|-----------|---------------|-------------|-------|-----------------|------------|------------------|-------------------|
| `SEEDANCE_2_0` | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | No | Yes | Yes | 3 |
| `DOUBAO_1_5_PRO` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | Yes | Yes | No | Yes | 1 |
| `DOUBAO_1_LITE` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p | No | Yes | Yes | No | 3 |
| `DOUBAO` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | Yes | No | No | 1 |
| `DOUBAO_1_PRO_FAST` | 5, 10 | 9:16, 16:9, 4:3, 3:4, 1:1, 21:9 | 480p, 720p, 1080p | No | Yes | No | No | 1 |

---

## Recommended defaults (when user is silent)

| Field | Value |
|-------|--------|
| `model` | **`SEEDANCE_2_0`** |
| `aspect_ratio` | **`9:16`** (must be allowed for that model) |
| `duration` | **`10`** |
| `resolution` | **`720p`** (use **1080p** only when the model lists it and the user wants max sharpness) |
| `generate_audio` | **`true`** for **`SEEDANCE_2_0`** defaults; **`false`** for 1.0 variants unless the row allows audio and the user wants it |

---

## Scenario notes

- **Text-only:** Any row in the text table; default **`SEEDANCE_2_0`**.
- **Single `image`:** Any image row; respect **`upload_image_limit`**.
- **Several images / storyboard:** Prefer **`SEEDANCE_2_0`** or **`DOUBAO_1_LITE`**—never send multi-image payloads to models with **Multi-image = No**.
- **First + last frame:** **`SEEDANCE_2_0`** or **`DOUBAO_1_5_PRO`** per image metadata; confirm against **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** field names (`first_frame` / `last_frame`, `image` / `last_image`, or ordered `images`).

> Pack: `seedance-video-gen-1-2.0`.
