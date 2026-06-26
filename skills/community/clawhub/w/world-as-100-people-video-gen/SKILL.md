---
name: world-as-100-people-video-gen
version: 1.0.1
description: "Create ‘world as 100 people’ verticals: shrink hook, stat morphs, punchline, timed English captions and motion graphics (WeryAI). Use for infographic TikToks, demographic explainers, or icon-driven stats. Use when the user names the 100-people metaphor. SEO: 100 people world video; demographic hook video."

tags: [infographic, demographics, data, icons, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "👥", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# World as 100 people (icons + stat race + punchline)

**Template (assume `duration` 10 unless scaled):** **0–2s** *shrink the world to 100 people*; **2–9s** **rapid visual changes** (wealth split, gender, access to water/internet, etc.—user picks **themes**); **9–10s** **one shocking or memorable stat line** (user-themed). **English on-screen text** with **exact windows**. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**. Prefer public **`https`** image URLs; if the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
- Non-empty `model` in JSON.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; never commit.
- **API hosts** fixed in `video_gen.js` as in sibling skills—only the key is read from env.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Prefer a short-lived or isolated environment; review `scripts/video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested.
- **Timeline scaling:** Rescale hook / middle / punchline segments proportionally; keep **hook → three middle beats → final punchline** order.

**Locked rhythm (example for duration 10):**

- **0.0–2.0s** — Hook: e.g. *SHRINK EARTH TO 100 PEOPLE*.
- **2.0–4.0s**, **4.0–6.0s**, **6.0–9.0s** — **Three** rotating **stat / theme** lines (user brief): e.g. *WEALTH SHIFTS* / *GENDER* / *WHO GETS WHAT*—keep labels **short**; pair each with **icon morph**, **pie wipe**, or **counter tick**.
- **9.0–10.0s** — **Punchline stat** (one short English line the user intends—e.g. *ONLY X HAVE Y*).

**Visuals:** Isometric or flat UI icons, **glow**, **snappy** transitions (~1s); **no** tiny unreadable numbers unless the **caption** carries the readable stat.

**Typography:** Bold sans, outline, lower third; **English only** unless user requests otherwise.

**Audio:** Light digital ticks / whoosh if audio on.

**Negatives (Kling):** garbled numbers, illegible text, watermark.

**Confirmation:** Full expanded `prompt` in table.

### Niche checklist

- Prefer **one clear metaphor** per middle window.
- Punchline must be **one screenful**—no paragraph.

## Workflow

1. Text / image / multi-image (**SEEDANCE_2_0** only, ≤3 URLs).
2. Collect **which stats or angles** to imply (user may give Chinese—**translate** lines to English on screen).
3. Expand with **timed captions** + motion graphics language.
4. Validate JSON vs frozen tables.
5. Confirm → `wait`.
6. **`[Video](url)`** only for playable links.

## CLI reference

~~~sh
node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, garbled numbers, watermark"}'
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or error; `prompt` includes **0–2 / 2–4 / 4–6 / 6–9 / 9–10** (or user-approved adjustment) subtitle schedule.

## Boundaries (out of scope)

- **Not** verified census data—**illustrative** motion; user owns factual claims.
- No `negative_prompt` on Seedance; no unsupported fields.
- **`resources/WERYAI_VIDEO_API.md`** for CLI details.

### Example prompts

- `Focus: internet access, education, wealth—punchline about inequality`
- `Climate + water + energy icons, last line about renewable share`
- `Three chart images URLs → Seedance multi-image, same caption windows`
- `Healthcare access vs wealth percentiles—punchline about who gets left out`

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

User lists **themes** → you **assign lines + seconds** → confirm → `wait`.

## Image-to-video (optional)

Charts / icons stills → animate under same windows.

## Tips

- If user gives **too many themes**, merge into **three** middle beats.
- Punchline hits harder with a **contrast number** (still short).

> Packaged as **`world-as-100-people-video-gen`**.
