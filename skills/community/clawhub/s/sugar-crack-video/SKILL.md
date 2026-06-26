---
name: sugar-crack-video
version: 1.0.0
description: "Generate vertical satisfying sugar-shell crack & pour shorts (WeryAI): text-to-video or dessert image to shell shatter and flowing center motion—first-three-second hook. Use when you need food ASMR cut, caramel crack dessert clips, or users ask for shell snap, lava pour, jelly wobble. SEO: sugar crack video; sugar crack video generation."

tags: [food, asmr, satisfying, payoff, dessert-cut, short-video, video]

metadata: { "openclaw": { "emoji": "🍬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Sugar shell crack & pour video generation

Knife meets candied hawthorn shell—*crack*—shell splits, deep-red fruit pops—that frame loops forever. This skill targets those beats: shell break, lava pour, jelly wobble, sugar shards—crisp + flowing stacked for completion ceiling.

Text or one dessert image → 9:16 vertical.

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

- **Crack payoff:** shell stress → **snap**, shards, powder dust; macro sugar texture; warm dessert light.
- **Motion:** slow break or single tap; interior reveal (mousse, fruit) if user asks.
- **Audio:** crisp crack if `generate_audio` true.

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

- `Crème brûlée: knife taps shell, crack then lava pours, vertical food satisfying`
- `From this layer cake: slice motion, cream pull`
- `Food short: shell *snap* + jam burst, warm appetite light`
- `Satisfying dessert crack 9:16, shell shatter then gooey center pour`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed, vertical short) |
| Duration | 5 s (short hook mode) |
| Look | Macro, slow-mo, crystal refraction, saturated pour, minimal background |
| Audio | On (shell crack + pour ASMR) |
| Seamless loop | Off by default; when on, append loop keywords to prompt |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document and the API validity notes above; do not send unsupported fields such as `resolution`.

---

## Text → sugar crack & pour

Describe dessert type and how it’s opened—no assets required. Good for batching different foods or testing shell vs. lava vs. jelly.

Say what it is (candied hawthorn shell / lava cake / flowing pudding / crystal jelly / filled dessert) and how it breaks (single slice / spoon press / toothpick poke / squeeze burst). Build prompt from shell thickness, viscosity, color contrast, plus crack sound, pour beat, and light.

**Flow:**
1. Collect food + cut style; extract shell feel, pour color, peak beat; build prompt
2. Show this run’s parameters; wait for confirmation:
   > About to generate—confirm to start (reply **"confirm"** or list changes):
   > - model: KLING_V3_0_PRO
   > - aspect_ratio: 9:16
   > - duration: 5
   > - generate_audio: true
   > - seamless loop: off (reply "loop" to append `seamless loop, perfectly looping video, first and last frame identical`)
3. After confirmation run `node scripts/video_gen.js wait --json '…'` with `model`, `prompt`, `aspect_ratio`, `duration`, `generate_audio` matching the table; parse stdout for URLs

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Shell break + pour land in the first ~3 s; slow-mo is screenshot-friendly; ASMR synced to visuals; vertical ready to post.

> **Note:** For lava shots, name the pour color in prompt (e.g. `vivid matcha green lava`, `molten dark chocolate`)—higher saturation and contrast vs. shell strengthens the hook.

---

## Dessert image → crack / pour motion

Provide a dessert image URL; generate cut / pour motion anchored on that subject. Good for turning plating or product stills into video.

Prefer a publicly reachable **`https`** URL for the reference. Optional: motion direction (slice pour / shell shatter / jelly wobble / spoon crush). Infer shell, filling color, and shape from the image; keep look consistent with the reference.

**Flow:**
1. Collect URL + motion direction; infer food traits; build motion prompt
2. Show parameters; wait for confirmation:
   > About to generate—confirm to start (reply **"confirm"** or list changes):
   > - model: KLING_V3_0_PRO
   > - aspect_ratio: 9:16
   > - duration: 5
   > - generate_audio: true
   > - image: (your URL)
   > - seamless loop: off (reply "loop" to enable)
3. After confirmation run `node scripts/video_gen.js wait --json '…'` including `image` plus same fields as text path; parse stdout

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User image URL |

**Sample prompt:**

> Based on the provided image, animate this dessert being cut open: a sharp knife blade enters from the top in extreme close-up macro slow motion at 120fps, the outer shell or crust fractures cleanly along the cut line matching the color and texture of the original food in the image, the interior filling or lava erupts and flows outward maintaining the color palette visible in the image, warm side lighting enhances the viscosity of the flowing interior, ASMR crack and pour sound, the overall color tone and plating style matches the reference image, dark slate background

**Expected outcome:** Motion matches the dish; shell break and pour feel natural; strong before/after vs. still.

> **Note:** Prefer public **`https`** URLs; login-gated links may fail the API. If the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI. Clearer food and cleaner backgrounds improve accuracy.

---

## Prompt boosters

Drop-in phrases by food type:

**Shell shatter:** `crystalline sugar shell shatters`, `amber caramel crust fractures radially`, `tempered sugar explodes into prismatic shards`, `sugar crust collapses inward`

**Lava pour:** `molten lava erupts in viscous surge`, `liquid chocolate center oozes out slowly`, `thick custard floods the plate`, `lava flow catches backlight glowing translucent`

**Jelly wobble:** `jelly wobbles in satisfying slow motion`, `translucent cube trembles after cut`, `cross-section glistens catching blue backlight`, `jelly oscillation dampens slowly`

**Light:** `caustic light refraction through sugar crystal`, `backlit lava glowing at translucent edges`, `cold rim lighting on cut surface`, `warm amber bokeh in background`
