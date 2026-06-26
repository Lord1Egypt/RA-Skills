---
name: rednote-images
description: Generate RedNote image series with structured style and layout choices and bundled generation tooling. Use when the user asks to create RedNote image cards, RedNote cover cards, or social infographic series.
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "📱", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# RedNote Image Series (`rednote-images`)

## Reference Images (Important)

If you use reference images (image-to-image / series reference / consistency refs):

- Reference images must be public URLs.
- **HTTPS is strongly recommended.**
- `http://` may work but is insecure and can be blocked by some networks.
- Local file paths and `data:` URLs are not supported by the WeryAI gateway.

Generate RedNote image cards, RedNote cover cards, and social infographic series with a stable card-by-card workflow.

This RedNote image skill turns a RedNote image-series request into a more stable set of card prompts and generates the resulting sequence. Use it to create RedNote image cards, RedNote cover cards, or a social infographic series from one topic.

**Dependencies:** `scripts/scaffold.ts`, `scripts/build-prompts.ts`, `scripts/build-batch.ts`, the bundled runtime under `scripts/vendor/`, `IMAGE_GEN_API_KEY`, and Node.js + npm. No other skills are required.

## Authentication and first-time setup

Before the first real generation run:

1. Create a WeryAI account.
2. Open the API key page at `https://www.weryai.com/api/keys`.
3. Create a new API key and copy the secret value.
4. Add it to the required environment variable `IMAGE_GEN_API_KEY`, or let the setup flow persist it under `.image-skills/rednote-images/.env`.
5. Make sure the WeryAI account has available balance or credits before paid generation.

### OpenClaw-friendly setup

- This skill already declares `IMAGE_GEN_API_KEY` in `metadata.openclaw.requires.env` and `primaryEnv`.
- After installation, if the installer or runtime asks for required environment variables, paste the key into `IMAGE_GEN_API_KEY`.
- If you are configuring the runtime manually, export it before running commands:

```sh
export IMAGE_GEN_API_KEY="your_api_key_here"
```

### Quick verification

Use one safe check before the first paid run:

```sh
cd {baseDir} && npm run doctor -- --project . --workflow rednote
cd {baseDir} && npm run ensure-ready -- --project . --workflow rednote --dry-run
cd {baseDir} && npm run generate -- --prompt "RedNote layout smoke test" --image ./out/rednote-smoke.png --ar 1:1 --dry-run
```

- `doctor` is read-only and confirms whether the key and local tooling are ready.
- `ensure-ready --dry-run` confirms the guided setup path without changing the workspace.
- `generate --dry-run` prints the final request body without calling WeryAI or consuming credits.

Script:

- `scripts/scaffold.ts`
- `scripts/build-prompts.ts`
- `scripts/build-batch.ts`

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Secret handling**: Treat `IMAGE_GEN_API_KEY` as a runtime secret. Do not commit it into the repository or paste it into generated prompt/output files.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/rednote-images/` (project) and/or `~/.image-skills/rednote-images/` (home).

## Example Prompts

- `Create 5 RedNote image cards that summarize this product comparison`
- `Make a RedNote cover card plus 4 follow-up cards for this skincare topic`
- `Turn this outline into a social infographic series for RedNote`

## Use Cases

- RedNote card series
- social knowledge-card sequences
- product recommendation cards, summary cards, and comparison cards
- content that should be split into 1 to 10 connected images

Not a good fit for:

- a single article cover image
- a multi-page knowledge comic
- a very dense single infographic

## Core Dimensions

Choose the two core dimensions first, then split the series:

1. `style`
2. `layout`

See:

- [references/dimensions.md](references/dimensions.md)
- [references/outline-template.md](references/outline-template.md)
- [references/presets.md](references/presets.md)

## Commands

| Script | Purpose |
| --- | --- |
| `scripts/scaffold.ts` | Initialize `outline.md` and per-card prompt files |
| `scripts/build-prompts.ts` | Regenerate prompts from `outline.md` |
| `scripts/build-batch.ts` | Generate `batch.json` from card prompts |
| `npm run generate` | Generate card images |
| `scripts/vendor/compression-runtime/scripts/main.ts` | Compress output for delivery |

## Workflow

### Step 1: Understand the Content

Extract:

- the main topic
- the target audience
- the ideal number of cards, usually 3 to 7
- the 1 to 3 most important points for each card
- the user's language, especially if cards contain on-canvas text

### Step 2: Choose `style` and `layout`

Default priorities:

- `style`: `notion`
- `layout`: `balanced`

Recommended rules:

- knowledge summaries and practical explainers -> `notion`, `chalkboard`, or `minimal`
- emotional or recommendation-driven sharing -> `warm`, `cute`, or `fresh`
- strong opinions, warnings, or contrast -> `bold` or `retro`
- poster-like and strong visual impact -> `editorial`

If the user explicitly specifies style, density, or series feel, follow that preference.

### Step 3: Map to the Bundled Runtime

The bundled image runtime currently exposes one structured style argument, `--style`, so:

- map `style` to `--style`
- write `layout` into the prompt body
- create one prompt per card
- prefer batch generation for the whole series

Recommended mapping:

| rednote style | runtime `--style` |
| --- | --- |
| `cute` | `anime` |
| `fresh` | `flat-illustration` |
| `warm` | `watercolor` |
| `bold` | `poster` |
| `minimal` | `editorial` |
| `retro` | `poster` |
| `notion` | `flat-illustration` |
| `chalkboard` | `chalk` |
| `editorial` | `editorial` |

### Step 4: Scaffold `outline.md` and Prompt Files

Initialize the working directory:

```bash
${BUN_X} {baseDir}/scripts/scaffold.ts \
  --output-dir rednote-images/topic-slug \
  --theme "Topic or thesis" \
  --style notion \
  --layout balanced \
  --lang zh \
  --cards 5
```

This creates:

- `outline.md`
- `prompts/01-cover.md`
- `prompts/02-content.md`
- ...

Then refine `outline.md` and the generated prompts as needed.

### Step 5: Refine `outline.md`, Then Build Prompts

Generate prompt files from the outline:

```bash
${BUN_X} {baseDir}/scripts/build-prompts.ts \
  --outline rednote-images/topic-slug/outline.md \
  --output-dir rednote-images/topic-slug/prompts
```

Then generate cards in order:

- `01-cover`
- `02-content`
- `03-content`
- ...

Use [references/prompt-template.md](references/prompt-template.md) for each card prompt.

Requirements:

- each card should carry one main information focus
- state the `layout` explicitly in that card's prompt
- state the target language if the image includes text
- default RedNote aspect suggestions are `3:4` or `1:1`
- for multi-card sets, prefer a shared series reference image first, then reuse it across all cards

### Step 6: Generate the Shared Series Reference First

Before building the final card batch, generate the canonical series reference image:

```bash
cd {baseDir} && npm run generate -- \
  --promptfiles rednote-images/topic-slug/references/series-reference.md \
  --style flat-illustration \
  --image rednote-images/topic-slug/references/series-reference.png \
  --ar 3:4 \
  -m "$M"
```

This step is the default for multi-card sets. Do not skip it when consistency matters.

### Step 7: Build `batch.json` and Run Generation

Build a batch file from the prompt directory:

```bash
${BUN_X} {baseDir}/scripts/build-batch.ts \
  --prompts rednote-images/topic-slug/prompts \
  --output rednote-images/topic-slug/batch.json \
  --images-dir rednote-images/topic-slug \
  --model "$M"
```

Then run the bundled image generator:

On first use in a new project, run `cd {baseDir} && npm run ensure-ready -- --project <your-project> --workflow rednote` before generation. This reads the doctor report and auto-runs `bootstrap` if local script dependencies are still missing. If the report shows a missing `IMAGE_GEN_API_KEY` and the user approves, run `cd {baseDir} && npm run setup -- --project <your-project> --workflow rednote --persist-api-key` when the key is already in env, or persist it to `.image-skills/rednote-images/.env` on the user's behalf, then continue without leaving this workflow.

When this skill is first connected, tell the user that the default generation model is **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`). Also tell them it can be switched later whenever another model fits the task better.

```bash
cd {baseDir} && npm run generate -- --batchfile rednote-images/topic-slug/batch.json --json
```

If only one cover card is needed, a single direct call is fine:

```bash
cd {baseDir} && npm run generate -- \
  --promptfiles prompts/01-cover.md \
  --style flat-illustration \
  --image rednote-images/topic-slug/01-cover.png \
  --ar 3:4 \
  -m "$M"
```

If the user has not chosen a model yet, follow this skill's model-selection rules first.

Consistency strategy for multi-card sets:

1. create one canonical `references/series-reference.png` first
2. treat that image as the source of truth for palette, recurring subject, typography feel, and layout rhythm
3. reuse the same shared reference for every card task
4. keep card-specific continuity anchors plus previous/next-card context in every prompt
5. if the shared reference image is missing, do not proceed to final batch generation yet

## Output Convention

Suggested output directory:

```text
rednote-images/<topic-slug>/
```

Suggested minimum files:

- `outline.md`
- `batch.json`
- `prompts/01-cover.md`
- `prompts/02-content.md`
- `01-cover.png`
- `02-content.png`

## Re-run Behavior

- `scaffold.ts` on an existing directory overwrites `outline.md` and the starter prompt files for the requested card count.
- `build-prompts.ts` overwrites prompt files in `prompts/` from the current `outline.md`.
- `build-batch.ts` overwrites `batch.json`.
- Re-running the base generator with `--batchfile` re-generates every listed card; keep good cards by removing their tasks from `batch.json` first.
- Re-running the shared reference step overwrites `references/series-reference.png`.

## Definition of Done

- `outline.md` and per-card prompt files exist in the output directory.
- All cards are generated and shown to the user in order.
- Card count, style, layout, and model are stated in the delivery summary.
- A compressed webp set is produced for delivery.

## Iteration

When the user wants changes after seeing the generated cards:

- **Style mismatch** ("change the style") → change `style` / `--style` for all cards, rebuild batch, re-generate. Ask if all cards or specific ones.
- **Color/tone issues** ("too cold", "colors are dull") → adjust `palette` and `mood` in prompt body. Only re-generate affected cards.
- **Content split wrong** ("card 3 has too much content") → revise `outline.md` to redistribute content, rebuild prompts and batch for affected cards.
- **Want more/fewer cards** → adjust card count in `outline.md`, re-scaffold and rebuild.
- **Single card redo** → re-generate only that card by running the bundled generator with `--promptfiles` for the specific prompt.

When re-generating a subset, keep the existing good images and only replace the ones that need changes.

## Delivery

When the card series is ready:

1. **Show each card image directly** in order (cover → content → summary). Do not just list file paths.
2. Briefly state: card count, style, aspect ratio.
3. Ask if any cards need changes or if the user wants to proceed.
4. **Auto-compress**: once confirmed, run the bundled compression runtime on the output directory to produce webp versions for social upload.

```bash
${BUN_X} {baseDir}/scripts/vendor/compression-runtime/scripts/main.ts rednote-images/topic-slug/ -r -f webp -q 80
```

For series with many cards, show the first 2-3 immediately as they complete, then batch-show the rest.

Internal checklist (for agent): card count, `style / layout`, model, batch execution, target language, compression done.
