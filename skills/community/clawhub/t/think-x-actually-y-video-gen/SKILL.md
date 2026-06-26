---
name: think-x-actually-y-video-gen
version: 1.0.1
description: "Create vertical three-beat debunks: you think X, actually Y, but Z—timed English captions on three segments (WeryAI). Use for mindset ladders, hot-take templates, or layered arguments. Use when the user wants think/actually/but structure. SEO: think X actually Y video; debunk template video."

tags: [debunk, mindset, template, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "🔀", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# You think X, actually Y (three-beat ladder)

**Template (segment lengths assume `duration` 10 → 30% / 30% / 40%; rescale for 5 or 15):** **Beat 1** *YOU THINK {X}*; **Beat 2** *ACTUALLY: IT’S {Y}*; **Beat 3** *BUT WHAT REALLY DECIDES IS {Z}* — **X / Y / Z** come from the user’s brief (you **compress each to ≤6 words** for on-screen legibility). **Hard cuts** and **kinetic** energy between beats. **English subtitles** with **exact windows**. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**. Prefer public **`https`** image URLs; if the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
- Non-empty `model` in every `submit-*` / `wait` JSON.
- Each **successful** task submission may consume credits; re-submit creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; never commit.
- **API hosts** fixed in `video_gen.js`.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Prefer a short-lived or isolated environment; review `scripts/video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Pre-submit gate (mandatory)

⚠️ **No paid submit without explicit user confirmation.** Do **not** call `submit-text`, `submit-image`, `submit-multi-image`, or `wait` until the user has **explicitly approved** the parameter table (including **full expanded `prompt`** with **X / Y / Z** filled and **timed caption windows**). Never infer consent from silence or vague “continue.” **Explicit** means clear intent such as **confirm** / **go** / **approved** / **yes, generate** (or equivalent).

**Parameter confirmation table (before any submit):** `model`, `duration`, `aspect_ratio`, `resolution` (Seedance only), `generate_audio`, `negative_prompt` (Kling only), **`image` / `images`** (if used), and the **entire** expanded `prompt` (not a summary).

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested.
- **Timeline scaling:** Keep **30% / 30% / 40%** of total runtime for the three beats (adjust seconds in the written prompt); or another **explicit** split the user approves.

**User must supply (or approve) X, Y, Z concepts**—if they only give a topic, **propose** three beats in the confirmation table before submit.

**Visuals:** **Three distinct looks** per beat (e.g. office runner → chess flip → neon brain schematic); **arrows reversing**, **color grade shift** each beat; **motion** throughout.

**Typography:** Bold sans, outline, lower third; **ALL CAPS** optional for punch—keep lines **short**.

**Negatives (Kling):** illegible text, watermark.

**Confirmation:** The **full** `prompt` including **filled X/Y/Z** inside the timed block appears **only** in the pre-submit table; see **`## Pre-submit gate (mandatory)`** — **wait for explicit approval** before `submit-*` or `wait`.

### Niche checklist

- Avoid **demeaning** groups; critique **ideas**, not people.
- If user’s Z is vague, default to **SKILL / LUCK / COGNITION** style abstractions **they confirm**.

## Workflow

1. Choose path: **text-to-video**, **single image**, or **multi-image** (**SEEDANCE_2_0** only, ≤3 URLs).
2. Extract or **draft X, Y, Z**; if the user only gave a topic, **propose** three beats and get their OK on concepts **before** expanding the full cinematic prompt.
3. **Expand prompt (mandatory):** Build the full production `prompt` (three distinct looks, motion, timed English captions per beat, negatives for Kling). Validate length against `prompt_length_limit` for the chosen `model`.
4. **Pre-submit gate:** Show the **parameter confirmation table** with the **complete** expanded `prompt`. **Stop** until the user **explicitly confirms** or requests edits.
5. **Submit (async, default):** After explicit confirmation, run **`submit-text`**, **`submit-image`**, or **`submit-multi-image`** (same JSON shape as `wait`; see **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**). Do **not** start a long blocking `wait` in the same turn unless the user **already** asked to block until the video is ready.
6. **Immediate notify:** On successful accept (e.g. **`taskId`** / **`batchId`** returned), **immediately** tell the user the id(s), short status (e.g. queued), and **ask** whether to continue with **`status`** polling or **`wait`** (block-until-done).
7. **Continue (user-driven):** Only after they agree, poll `status --task-id <id>` at reasonable intervals **or** run `wait --json '…'` with the **same** payload — per user choice.
8. Return results: **`[Video](url)`** when URLs exist; otherwise explain `errorCode` / `errorMessage`. **Never** wrap playable links in code fences.

## CLI reference

**After confirmation** — async submit, then `status` (user opts in to polling):

~~~sh
node scripts/video_gen.js submit-text --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, watermark, garbled captions"}'
node scripts/video_gen.js submit-image --json '{"model":"SEEDANCE_2_0","prompt":"…","image":"https://…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
node scripts/video_gen.js status --task-id <TASK_ID>
~~~

**Block until done** — only if the user explicitly chose `wait`:

~~~sh
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference** (`submit-multi-image`, stdout fields, errors): **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or a clear error. **Pre-submit:** **full** expanded `prompt` with **three non-overlapping time ranges** (scaled to `duration`) and **concrete English** for each beat was **explicitly** user-confirmed before submit. **After submit:** user was **notified** with task id(s) and **chose** `status` vs blocking `wait`. Playable URLs **must** be **`[label](url)`** only — not inside code blocks.

## Boundaries (out of scope)

- Not financial or medical advice—**rhetorical template** only.
- **`resources/WERYAI_VIDEO_API.md`** for CLI; no `negative_prompt` on Seedance.
- **Multi-image** only **SEEDANCE_2_0**, max **3**.

### Example prompts

- `X effort success, Y choices, Z cognition—office to chess to abstract mind`
- `X cheap price, Y hidden fees, Z trust—ecommerce vibes`
- `Product hero image URL → three-beat reversal with same windows`
- `X free time, Y discipline, Z identity—gym / calendar / mirror visual metaphors`

---

## Model and API constraints (frozen for this skill)

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | prompt limit |
|-----------|-----------|---------------|-------------|-------|-----------------|--------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | 2000 |

### Image-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | image slots |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | up to **3** `images` |

## Recommended models

| Tier | model_key | Default duration |
|------|-----------|------------------|
| ⭐ Best | KLING_V3_0_PRO | 10 |
| 👍 Good | KLING_V3_0_STA | 10 |
| ⚡ Fast | SEEDANCE_2_0 | 10 (`resolution`: **720p**) |

## Default parameters

| Field | Value |
|-------|--------|
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | true |
| resolution | 720p (Seedance) |
| negative_prompt | Kling: `illegible text, garbled captions, watermark` |

## Text-to-video (primary)

Lock **X/Y/Z** with user → expand **timed** caption block → **pre-submit table** → **`submit-text`** → notify **task id** → user picks **`status`** or **`wait`**.

## Image-to-video (optional)

Single hero → **three visual skins** across beats → **`submit-image`** (or **`submit-multi-image`** for Seedance, ≤3) → same **notify → user-driven** polling as above.

## Tips

- **Translate** Chinese user input to **English** captions unless they specify on-screen language.
- **Z** lands best when it feels **one level meta** above Y.

> Packaged as **`think-x-actually-y-video-gen`**.
