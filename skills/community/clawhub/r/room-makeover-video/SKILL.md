---
name: room-makeover-video
version: 1.0.1
description: "Generate vertical home makeover shorts (WeryAI): rental cream aesthetic, balcony café corner, themed kids’ rooms, strong before/after. Use when you need room makeover reels, soft-furnishing glow-up clips, or users ask for lights-on reveal and split before/after. SEO: room makeover video; room transformation video generation."

tags: [makeover, home, aesthetics, healing, life-inspo, short-video]

metadata: { "openclaw": { "emoji": "🏠", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Room makeover & refresh video generation

Three pillars:

- **Before/after:** worn or plain “before” vs. elevated “after” in one clip
- **Process:** staging, mood lighting, DIY decor—compressed on a rhythmic timeline
- **Anthropomorphic cast:** bunny / hamster / cat doing the work—more emotion and completion

One line: character + space + style → clip. Fits home / aesthetics / makeover feeds.

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

- **Space arc:** before clutter or dull → paint/furniture/light **after**; wide establish → detail passes.
- **Light:** warm interior practicals; window rake optional; **cozy or luxury** tone per user.
- **Payoff:** readable layout transformation, not random decor jump cuts.

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

- `Shabby rental turned cream aesthetic by a hamster—rug, string lights, warm lights full on at end`
- `From this messy balcony: motion into a coffee corner`
- `Kids’ room: paint + star ceiling, big contrast but cozy`
- `Room makeover timelapse 9:16, cozy lighting reveal at end`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed, vertical short) |
| Duration | 10 s (`duration: 10`, room for full process) |
| Audio | Off |
| Look | Medium or wide, natural + warm accent light; before cooler/darker, after warmer/brighter; time-lapse compression |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document and the API validity notes above; do not send unsupported fields such as `resolution`.

---

## Anthropomorphic room makeover

Animals “finish” a tired space overnight—the classic arc: enter messy room → busy montage → lights on, new room.

**User provides:**
- Character (bunny / hamster / cat / bear / custom)
- Space (rental bedroom / balcony / study / kids’ room / small shop / living nook)
- Target style (cream / cyberpunk / café corner / Nordic minimal / forest fairy / retro Hong Kong)

**Flow:**
1. Collect character, space, style—ask if any are missing
2. Build prompt in three beats: before dull & cluttered → character staging → lights-on reveal
3. If params unspecified, show defaults and wait for confirmation.
**Show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Field | This run | Notes |
   > |-------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best tier default; fast: text `VEO_3_1_FAST`, image `CHATBOT_VEO_3_1_FAST` (`duration` fixed 8); good → `KLING_V3_0_STA`; or specify a model name |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 only; if you switch model, check that row’s `aspect_ratios` etc. |
   > | `duration` | `10s` | KLING family: 5 / 10 / 15; VEO fast: duration 8 only |
   > | `generate_audio` | `false` | Auto-generate audio or not |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `seamless loop` | off | Reply "loop" to add seamless loop |
   >
   > Reply **"confirm"** to start, or list what to change.
4. After confirmation, in the terminal from the skill package root:

   ```sh
   node scripts/video_gen.js wait --json '{"model":"(confirmed model)","prompt":"(full English prompt)","aspect_ratio":"9:16","duration":10,"generate_audio":false}'
   ```

   `aspect_ratio`, `duration`, `generate_audio`, `model` must match the table; add `resolution` only if supported. Parse `videos` from stdout.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | false |

**Sample prompt (bunny, rental, cream):**
> A small white bunny with oversized ears begins transforming a dull, cluttered rental apartment bedroom, medium wide shot shows peeling walls and mismatched cheap furniture, the bunny hangs linen curtains, places cream-colored cushions, adds dried pampas grass in a ceramic vase, time-lapse with warm evening light slowly shifting, final reveal: the same room now glows in a soft cream-beige aesthetic with warm Edison bulb string lights overhead, low-angle medium shot shows the complete transformation, diffused golden light, cozy hygge atmosphere, paint texture walls, before-after contrast dramatic

**Sample prompt (hamster, study, cyber):**
> A tiny hamster in overalls transforms a bare study corner into a cyberpunk workspace, medium shot follows the hamster mounting LED strip lights in cyan and purple, placing holographic desk accessories, hanging circuit board art prints, time-lapse compression of the assembly process, dramatic before-after cut: sterile white room transitions to neon-lit cyberpunk den, wide establishing shot captures the full room with light reflections on all surfaces, dark dramatic void background outside window, Dutch angle for final reveal, high contrast neon against deep shadow

**Sample prompt (cat, old balcony → café):**
> A gray cat with white gloves methodically converts a neglected dusty balcony into a cozy café corner, overhead wide shot starts with cracked tiles and dead plants, cat places small round table with mosaic top, installs string fairy lights along the railing, arranges potted herbs in terracotta planters, golden hour time-lapse as the sun sets, final reveal at dusk: the balcony warmly lit with fairy lights, espresso machine on the table, trailing ivy across the wall, warm amber light, wide-to-close dolly movement revealing the full transformation

**Expected outcome:** Strong before/after; clear rhythm peak at lights-on; color temp cold→warm for emotional arc—fits home / lifestyle accounts.

---

## Space-only before/after (no character)

More “real” makeover: camera on the room only—good when the result itself is the star.

**User provides:**
- Before state (worn / cluttered / mixed style / dated finish)
- After target (specific style + key pieces)
- Focus (lighting change / staging / layout / detail macro)

**Flow:**
1. Collect before/after descriptions
2. Build prompt stressing light shift, palette change, macro beats on key decor
3. After confirmation, from the skill package root:

   ```sh
   node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(full English prompt)","aspect_ratio":"9:16","duration":10,"generate_audio":false}'
   ```

   Fields match the table; parse stdout for URLs.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | false |

**Sample prompt (low-budget rental glow-up):**
> Wide establishing shot of a low-budget rental room transformation, left half of the frame shows original water-stained walls, plastic furniture, fluorescent lighting, the right half reveals the same space after makeover with white paint, thrifted wooden shelf, warm LED strip lights, fabric headboard, time-lapse renovation progress fills the center, final wide shot shows the complete after: cozy Scandinavian-minimalist aesthetic on zero budget, warm 3000K ambient lighting, slight aerial perspective

---

## Usage tips

**Style precision:** Cream → `cream-beige aesthetic, warm Edison bulb`; cyber → `neon cyan and purple, dark dramatic void`; café corner → `mosaic table, terracotta, fairy lights, trailing ivy`. More specific style tokens reduce drift.

**Time span:** Add `time-lapse compression` and `golden hour light slowly shifting` so 10 s reads like “one night” of work.

**Reveal peak:** Use `before-after contrast dramatic` or `reveal moment` so the model knows there’s a single dramatic turn—usually lights-on.
