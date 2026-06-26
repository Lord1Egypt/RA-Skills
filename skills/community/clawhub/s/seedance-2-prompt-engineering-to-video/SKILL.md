---
name: seedance-2-prompt-engineering-video-gen
version: 1.1.1
description: "Design production English prompts for Seedance 2.0 then generate text-to-video or image-to-video on WeryAI (`SEEDANCE_2_0`), using bundled recipes (A–K), mode-to-JSON mapping, camera vocabulary, and pre-flight checklists. Use when you need JiMeng-grade prompt control translated to WeryAI submit-* flows with explicit pre-submit confirmation. SEO: Seedance 2.0 prompt engineering; Seedance text and image to video; recipe library."

tags: [seedance, seedance-2, prompt-engineering, text-to-video, image-to-video, video-gen]

metadata: { "openclaw": { "emoji": "🎬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Seedance 2.0 prompt engineering to video

**Display name:** Seedance 2.0 prompt engineering to video · **Package folder:** `seedance-2-prompt-engineering-to-video`

Combine **high-control Seedance-style prompt design** (modes, asset roles, timeline beats, IP-safe language) with **direct WeryAI generation** for **`SEEDANCE_2_0`** **text-to-video** and **image-to-video** (single image by default; optional multi-image / first–last frame within model limits).

**Resource library (prompt guidance — under `resources/` next to `WERYAI_VIDEO_API.md` after sync):**

| Doc | Role |
|-----|------|
| **[`resources/seedance2-prompt-engineering-playbook.md`](resources/seedance2-prompt-engineering-playbook.md)** | Hub: 60s workflow, @→JSON map, quick beats |
| **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md)** | Modes, WeryAI field mapping, dialogue/sound, multi-segment, pitfalls, **pre-flight checklist** |
| **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)** | **A–K** production recipes (adventure, extend, IP-safe, toy, product, drama, one-take, 30s plan) |
| **[`resources/camera-and-styles.md`](resources/camera-and-styles.md)** | Shot, movement, angle, lighting, palette, render vocabulary |

**Dependencies:** `WERYAI_API_KEY` + Node.js **18+**. After assembly, **`scripts/video_gen.js`** and **`resources/`** must include **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** (your publish/sync pipeline copies the API doc from the WeryAI video skill creator; prompt guides ship in-repo). Full JSON fields and commands: **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set** before running `video_gen.js`.
- Node.js **18+**. Prefer public **`https`** URLs for `image`, `images`, `first_frame`, `last_frame`, and `last_image`. If the bundled runtime supports local file paths, **review** `scripts/video_gen.js`, **verify** read-and-upload behavior, and obtain **explicit user consent** before using local paths.
- **`model` is mandatory** in every `submit-*` and `wait` JSON body. This skill **only** documents **`SEEDANCE_2_0`**. If `model` is missing or blank, the CLI exits with **`MISSING_PARAM`** (no default model in the script).
- Each successful **`submit-*`** / **`wait`** may consume credits; retries create new paid tasks.
- **`SEEDANCE_2_0` does not support API `negative_prompt`** on text or image paths—do **not** send that field for this model.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret; never commit its value inside the skill package. OpenClaw metadata declares **`primaryEnv`** / **`requires.env`** so installers see the runtime contract.
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Do not rely on undocumented URL overrides.
- **Local image disclosure**: Prefer **`https`**. If the runtime can read local files and upload them to WeryAI for a public URL, require review, verification, and **explicit consent** before that path.
- **Higher assurance**: Use an isolated or short-lived environment; review `scripts/video_gen.js` before production paid use.

## Pre-submit gate (mandatory)

⚠️ **No paid submit without explicit user confirmation.** Do **not** call `submit-text`, `submit-image`, `submit-multi-image`, or `wait` until the user has **explicitly approved** the full parameter table below, including the **entire expanded `prompt`**. **Never** infer consent from silence or vague “continue”. **Explicit** means **confirm** / **go** / **approved** / **yes, generate** (or clear equivalent in the user’s language).

**Parameter confirmation table (show before any submit):** `model`, `duration`, `aspect_ratio`, `resolution`, `generate_audio`, reference URLs (if any), and **full expanded `prompt` (complete text, not a summary)**.

## Workflow

1. Confirm the user wants **Seedance 2.0** on WeryAI and whether the path is **text-only** or uses **reference image(s)**.
2. Collect the brief, optional **`https`** URLs, target **`duration`** (5–15 s, integer), **`aspect_ratio`**, **`resolution`**, and whether **`generate_audio`** should be **true** or **false**.
3. **Prompt engineering (mandatory):** Use the **resource library** above. Start from **[`resources/seedance2-prompt-engineering-playbook.md`](resources/seedance2-prompt-engineering-playbook.md)**; for mode and JSON mapping use **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md)**; match a scenario from **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)** when helpful; sharpen wording with **[`resources/camera-and-styles.md`](resources/camera-and-styles.md)**. Choose mode, map each URL to a role, draft timecoded beats, then compress into one API **`prompt`**. The API does not use `@image1` tokens; roles belong in prose while URLs sit in JSON. Unless the user supplied a finished long prompt and asked **not** to rewrite, **always** expand short input into a production English prompt.
4. Validate **`prompt`** length against **`prompt_length_limit`** (**2000**); trim lower-priority clauses if over limit.
5. **Pre-submit gate:** Show the confirmation table; **stop** until the user explicitly confirms or edits.
6. **Submit (async, default):** After confirmation, run **`submit-text`** or **`submit-image`** (or **`submit-multi-image`** when using multiple URLs), using the **same** JSON shape as `wait` (see **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**). **Do not** start a long blocking **`wait`** in the same turn unless the user already asked to block until the video is ready.
7. **Immediate notify:** On success, report **`taskId`** / **`batchId`** (or documented id fields), short status (e.g. queued), and **ask** whether to poll **`status`** or use blocking **`wait`** next. **Do not** run long invisible polling without that choice.
8. **Continue (user-driven):** Only after the user agrees, use **`status --task-id …`** at reasonable intervals **or** **`wait --json '…'`** with the **same** payload.
9. On completion, return playable URLs as **Markdown inline links** only—e.g. `[Video](https://…)`—**not** inside fenced code blocks.

## Prompt expansion (mandatory)

`video_gen.js` does **not** auto-expand prompts.

- **When:** The user gives a short or vague brief. **Exception:** They provide a final long prompt within **2000** characters and explicitly opt out of rewriting—still show the **full** text in the pre-submit table.
- **What to add:** Mode; asset mapping (for each URL); timecoded beats for the chosen **`duration`**; shot scale, angle, camera move (see **[`resources/camera-and-styles.md`](resources/camera-and-styles.md)**); lighting and materials; one clear payoff; framing for **`aspect_ratio`**; if **`generate_audio`** is **true**, describe ambience/SFX in generic, non-copyrighted terms; dialogue/sound as separate labeled lines when needed (see **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md) §4**).
- **IP / moderation:** **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md) §8** and recipe blocks in **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)** (D, E, F).
- **Length:** Stay within **2000** characters for **`prompt`**.
- **Confirmation:** The pre-submit table **must** include the **full** expanded **`prompt`**.

## CLI reference

**After confirmation — async submit, then optional `status`:**

~~~sh
node scripts/video_gen.js submit-text --json '{"model":"SEEDANCE_2_0","prompt":"<expanded English prompt>","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
node scripts/video_gen.js submit-image --json '{"model":"SEEDANCE_2_0","prompt":"<expanded English prompt>","image":"https://example.com/ref.png","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
node scripts/video_gen.js status --task-id <TASK_ID>
~~~

**Blocking until done** — only if the user explicitly chooses **`wait`:**

~~~sh
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Multi-image or first/last frame** — use **`submit-multi-image`** or the field names documented in **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**; keep **`images`** length ≤ **3** for **`SEEDANCE_2_0`**.

**Full CLI and API:** **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user receives at least one playable **[Video](url)** link or a clear error with a fix. **Pre-submit:** full **`prompt`** and parameters were **explicitly** confirmed. **Post-submit:** the user was notified with task id(s) and **chose** **`status`** vs **`wait`**. Submitted **`prompt`** must be the engineered production string unless the user opted out. **Do not** wrap user-facing video URLs in code fences.

## Boundaries (out of scope)

- Do **not** send **`negative_prompt`** for **`SEEDANCE_2_0`** (unsupported on this model’s rows).
- Do **not** exceed **`upload_image_limit`** (**3**) or claim multi-image support for other models inside **this** skill—**this skill documents only `SEEDANCE_2_0`**.
- Do not embed **`WERYAI_API_KEY`** values in files. Do not link to `weryai-model-capabilities.md` or arbitrary paths outside this skill package for shared capability docs.
- Do not use local image paths as the default; if supported by the bundled script, disclose upload behavior and require explicit consent.
- This skill does not run JiMeng-native UIs; it targets **WeryAI** JSON + `video_gen.js` only.

### Example prompts

- `Plan a 10s 9:16 Seedance 2.0 clip from a one-line cyberpunk alley idea, then generate on WeryAI after I confirm`
- `I have an https product still—map it as identity anchor, expand the prompt with beats, then image-to-video with SEEDANCE_2_0`
- `Help me write an IP-safe fantasy creature prompt and submit text-to-video with audio on`

---

## Model and API constraints (frozen for this skill)

> Derived from `node scripts/video_gen.js models` (`text_to_video` + `image_to_video`) at authoring time. Re-run after platform upgrades. **This skill uses only `SEEDANCE_2_0`.**

### Text-to-video

| model_key | durations (s) | aspect_ratios | resolutions | Audio (`generate_audio`) | negative_prompt (API) | prompt_length_limit |
|-----------|---------------|---------------|-------------|--------------------------|-------------------------|---------------------|
| `SEEDANCE_2_0` | 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | 9:16, 1:1, 16:9 | 480p, 720p | Yes | **Not supported** — omit field | 2000 |

### Image-to-video

| model_key | durations (s) | aspect_ratios | resolutions | Audio | negative_prompt (API) | Multi-image | First/last frame | upload_image_limit | prompt_length_limit |
|-----------|---------------|---------------|-------------|-------|----------------------|-------------|------------------|-------------------|---------------------|
| `SEEDANCE_2_0` | 5–15 (integers as above) | 9:16, 1:1, 16:9 | 480p, 720p | Yes | **Not supported** — omit field | Yes | Yes | 3 | 2000 |

---

## Recommended models

| Tier | model_key | Notes |
|------|-----------|--------|
| Default | `SEEDANCE_2_0` | Only model covered by this skill; text + image paths |

---

## Default parameters (when the user is silent)

| Field | Value |
|-------|--------|
| `model` | `SEEDANCE_2_0` |
| `aspect_ratio` | `9:16` |
| `duration` | `10` (must be one of the allowed integers) |
| `resolution` | `720p` |
| `generate_audio` | `true` unless the user wants silent motion |

---

## Scenario: Text-to-video with prompt engineering

1. Read **[`resources/seedance2-prompt-engineering-playbook.md`](resources/seedance2-prompt-engineering-playbook.md)** and pick a matching recipe from **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)** if applicable; set **Text-only** mode; draft beats for the chosen **`duration`**.
2. Build one English **`prompt`**; keep within **2000** characters.
3. **Pre-submit gate** with full **`prompt`** and numeric fields.
4. After explicit confirmation:

~~~sh
node scripts/video_gen.js submit-text --json '{"model":"SEEDANCE_2_0","prompt":"<expanded>","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

5. Notify task id; offer **`status`** vs **`wait`**. Return final URLs as **`[Video](url)`**.

---

## Scenario: Image-to-video (single reference)

1. Obtain one **`https`** image URL (or local path only with script review + explicit consent).
2. Plan **single-image** mode and **asset mapping** (identity, composition, palette to preserve); see **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md) §2.3** and recipes **F** / **H** in **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)**.
3. Expand **`prompt`** with motion beats and camera; merge dialogue/sound lines if needed.
4. **Pre-submit gate** including the image URL and full **`prompt`**.
5. After explicit confirmation:

~~~sh
node scripts/video_gen.js submit-image --json '{"model":"SEEDANCE_2_0","prompt":"<expanded>","image":"https://example.com/input.png","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

6. Same notify / poll / link rules as above.

---

## Scenario (advanced): Multi-image or first/last frame

Use only when the user supplies multiple references or explicit start/end frames and agrees to **`SEEDANCE_2_0`** limits (**≤ 3** uploads). Map order with **[`resources/modes-and-weryai-mapping.md`](resources/modes-and-weryai-mapping.md) §2.4 / §6** and recipe **J** in **[`resources/recipes-weryai.md`](resources/recipes-weryai.md)**; then use **`submit-multi-image`** and field names from **[`resources/WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **Pre-submit gate** must list **every** URL and the full **`prompt`**.

> Pack: `seedance-2-prompt-engineering-to-video` · slug: `seedance-2-prompt-engineering-video-gen`.
