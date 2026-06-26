---
name: scarcest-not-money-video-gen
version: 1.0.0
description: "Create vertical scarcity-mystery shorts: not money, option teases, final reveal, timed English captions (WeryAI). Use for guess-the-answer hooks or motivational mystery series. Use when the user asks what is scarcer than money. SEO: scarcest resource video; scarcity reveal video."

tags: [scarcity, motivation, mystery, series, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "💎", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Scarcest thing isn’t money (tease options → reveal)

**Template (assume `duration` 10 unless scaled):** **0–3s** *THE SCARCEST THING ISN’T MONEY*; **3–8s** **two or three quick option teases** on screen—e.g. **3–5** *ATTENTION?*, **5–6.5** *TRUST?*, **6.5–8** *TIME?* (user can swap candidates); **8–10s** **reveal** line naming the **one answer** they want (e.g. *IT’S ATTENTION*—**must** be **≤6 words**). **English subtitles** with **exact windows**. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**. Prefer public **`https`** image URLs; if the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
- Non-empty `model`.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; **`requires.env`** / **`primaryEnv`**.
- **API hosts** fixed in `video_gen.js`.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Prefer a short-lived or isolated environment; review `scripts/video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested.
- **Timeline scaling:** Rescale **0–3 / 3–8 / 8–10** and internal tease splits proportionally; keep **thesis → teases → reveal** order.

**Visuals:** **Coins dissolving** to sand, **hourglass**, **eye macro**, **handshake silhouette**, **clock abstraction**—**luxury** grade, **warm gold** accents optional; **morphs** every ~1.5s.

**Typography:** Bold sans, outline, lower third; **question marks** on tease lines.

**Audio:** Soft tick + **reveal sting** if `generate_audio` true.

**Negatives (Kling):** illegible text, watermark.

**User must confirm the final reveal word** before submit if you inferred it.

**Confirmation:** Full expanded `prompt`.

### Niche checklist

- **Teases** should be **distinct concepts**, not synonyms.
- **Reveal** should feel **earned**—visual points at the answer **as it appears**.

## Workflow

1. Text / image / multi-image (**SEEDANCE_2_0**, ≤3).
2. Collect **candidate list** + **final answer** (or you propose both for approval).
3. Expand → validate → confirm → `wait`.
4. **`[Video](url)`**.

## CLI reference

~~~sh
node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, watermark, garbled captions"}'
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or error; `prompt` includes **scaled second ranges** for thesis, tease block (with sub-splits), and reveal.

## Boundaries (out of scope)

- Not a finance or therapy authority—**hook content** only.
- **`resources/WERYAI_VIDEO_API.md`** for CLI; no `negative_prompt` on Seedance.
- **Multi-image** only **SEEDANCE_2_0**, max **3**.

### Example prompts

- `Tease attention trust time—reveal attention`
- `Tease sleep discipline focus—reveal discipline`
- `Gold coins still life URL → morph sequence with same caption rhythm`
- `Tease sleep, focus, energy—reveal discipline as the scarcest resource`

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

Agree **teases + reveal** → timed captions → `wait`.

## Image-to-video (optional)

Object still → **symbol morph** under same windows.

## Tips

- **Series:** end with *NEXT EP?* only if user wants; default is **clean reveal**.
- **Translate** Chinese brief to **English** on-screen lines unless user opts out.

> Packaged as **`scarcest-not-money-video-gen`**.
