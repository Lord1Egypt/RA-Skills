---
name: rust-restore-video
version: 1.0.2
description: "Generate vertical satisfying rust restoration shorts (WeryAI): text-to-video or rusty-object image to grind and polish motion. Use when you need rust restoration satisfying video, derust refresh clips, or users ask for scale flaking off, metal brightening, mirror finish. SEO: rust restore video; rust restoration video generation."

tags: [restoration, satisfying, asmr, craft, vintage, short-video]

metadata: { "openclaw": { "emoji": "🛠️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Rusty object restoration video generation

Rusty knives, blackened padlocks, vintage lighters—the moment the wheel touches, scale tears away and bare metal lights up along the grind path. “Junk reborn” is a high-completion lane for satisfying / men’s content; one line or one rust photo, straight to clip.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. When you run the CLI, **`scripts/video_gen.js`** must exist; **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** must exist under **`resources/`** (supply both via publish or pre-use assembly). Full commands and JSON fields: see **`resources/WERYAI_VIDEO_API.md`**. No other Cursor skills. **Default parameters** and model tiers are in the tables below; live API limits follow **weryai** models. Before installing or running, review the bundled `video_gen.js` to confirm it meets your requirements. Pay particular attention to how it handles local files if you choose to allow their usage, ensuring this behavior aligns with the skill's intended workflow for image-to-video requests.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, review and verify the script first, then get **explicit consent** before it reads a local image and uploads it to WeryAI to obtain a public URL.
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Only **`WERYAI_API_KEY`** is read from the environment—do not rely on URL-related environment variables.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.


## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Restore arc:** rust/oxidized → abrasive/polish/coat steps → **shine reveal**; macro metal texture.
- **Motion:** rotary tool, wipe, cloth buff—readable cause→effect; sparks optional if stylized safe.
- **Reflection:** final specular read proves the restore.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables in this document and **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node scripts/video_gen.js wait --json '…' --dry-run
node scripts/video_gen.js status --task-id <id>
```

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- We do not review platform compliance, copyright, or likeness; we do not warrant commercial usability of outputs.
- We do not provide offline rendering outside WeryAI, traditional NLE projects, or API field combinations not documented in this SKILL or **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
- Do not link to `weryai-model-capabilities.md` or shared `../references/` paths; use **`resources/WERYAI_VIDEO_API.md`** for CLI/API details.
- Do not hard-code absolute paths in this doc; run from the skill package root (next to `SKILL.md`) so `scripts/` and `resources/` paths resolve.

### Example prompts

- `Rusty wrench sanded and polished to mirror metal, vertical satisfying restore`
- `From this rusty pan: scale curls off, bottom brightens`
- `Old-tool restore vibe—each step readable, not too fast`
- `Rusty tool restoration 9:16, corrosion flakes off then mirror shine`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed, vertical short) |
| Duration | Short (`duration: 5`) |
| Look | Tight macro, dark workshop (wood bench / anvil), side light on metal texture, slow-mo sparks and rust dust (fixed) |
| Audio | On (wheel + metal friction ASMR is core) |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document and the API validity notes above; do not send unsupported fields such as `resolution`.

---

## Text-to-video: restore from description

Give object type (old knife / padlock / lighter / wrench / gear) and the beat to show (grind / polish / oil / reassembly); the skill fills visual detail.

**Flow:**

Collect object + action, pick the strongest phase (scale peel / shine appears / mirror finish) → build prompt → show parameters and wait for confirmation → run `node scripts/video_gen.js wait --json '…'`.

> Full parameters are shown before generate; wait for confirmation.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Rust vs. shine boundary is the main hook; grind path + wheel ASMR; mirror reflection as emotional peak.

---

## Rusty image → restoration motion

Provide a photo of a rusty object; generate motion from rusted surface to bright metal. Good for turning spare junk photos into content.

Prefer a public **`https`** image URL. If the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.

After the URL, optionally name the phase (grind / polish / oil); if omitted, pick the phase with strongest rust→clean contrast from the image.

**Flow:**

Confirm URL, infer object and rust level, choose angle for max contrast → show parameters and wait → run `node scripts/video_gen.js wait --json '…'` (JSON includes `image`).

> Full parameters are shown before generate; wait for confirmation.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User image URL |

**Sample prompt:**

> Starting from the rusty metal object in the image, a grinding wheel or abrasive pad moves methodically across the corroded surface, the rust layer is stripped away in one continuous slow-motion pass at 240fps revealing the bright original metal beneath, the clean-rust boundary line advances steadily through frame. Camera angle and framing match the image composition, single directional side light rakes across the surface to maximize texture contrast between corroded and polished areas. Rust powder and fine metallic sparks scatter in the air. ASMR grinding and metal friction sound.

**Expected outcome:** Grind direction matches rust coverage in the upload; strong return of true metal color.

---

## Prompt tips

**Rust texture**
- Rust surface: `heavy orange-brown corrosion pitting`, `flaking rust scale`, `uneven oxidation crust`, `rust powder suspended in air`
- Grind advance: `clean-rust boundary advances`, `bright metal exposed millimeter by millimeter`, `grinding path reveals polished steel`
- Polish finish: `mirror finish emerges`, `reflection sharpens as polishing progresses`, `surface transforms from matte to specular`

**Common notes**

- Smaller objects (lighter / knife): tighter macro—add `extreme close-up macro`
- Full arc (derust → polish → assembly): use `duration` **10** and say so at confirmation
- Prefer public **`https`** URLs; private hosts or in-app-only links may fail. If the runtime supports local paths, review `scripts/video_gen.js` and explicitly consent before local read-and-upload to WeryAI.

> **Note:** `KLING_V3_0_PRO` supports `negative_prompt` to exclude unwanted hands, tool occlusion, etc.—mention at confirmation if you want it added.
