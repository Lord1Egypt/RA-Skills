---
name: shellbot-creative-studio
version: 1.0.2
description: Headless creative production studio for AI agents. Generate images,
  edit photos, create videos, produce voiceover/music/SFX, and assemble polished
  output via Remotion. Supports Freepik, fal.ai, Nano Banana 2 (Gemini),
  OpenRouter, and ElevenLabs. Use when building product videos, social ads,
  explainers, marketing assets, or any visual/audio content pipeline.
allowed-tools: Bash(curl *api.freepik.com*), Bash(curl **.freepik.com*), Bash(curl *queue.fal.run*),
  Bash(curl *api.fal.ai*), Bash(curl *fal.run*), Bash(curl *api.elevenlabs.io*),
  Bash(curl *generativelanguage.googleapis.com*), Bash(curl *openrouter.ai*),
  Bash(jq *), Bash(mkdir *), Bash(infsh *), Bash(node *), Bash(npx *), Bash(npm
  *), Bash(ffmpeg *), Bash(python3 scripts/*), Bash(bash scripts/*), Read, Write
argument-hint: <command> [--param value]
metadata:
  openclaw:
    emoji: 🎬
    primaryEnv: FREEPIK_API_KEY
    providerEnv:
      - FREEPIK_API_KEY
      - FAL_API_KEY
      - GOOGLE_API_KEY
      - OPENROUTER_API_KEY
      - ELEVENLABS_API_KEY
    requires:
      env:
        - FREEPIK_API_KEY
      anyBins:
        - curl
        - jq
    homepage: https://getshell.ai
    tags:
      - creative
      - image
      - video
      - audio
      - remotion
      - production
---

# shellbot-creative-studio

Headless creative production studio for AI agents. One skill to generate images, edit photos, create videos, produce audio, and assemble everything into polished video output via Remotion.

**Philosophy:** Opinionated defaults, narrow overrides. Just works with whatever API keys you have.

## Commands

| Command | Description | Example |
| --------- | ------------- | --------- |
| `image` | Generate images (T2I, reference-guided) | `image --prompt "product shot" --style photo` |
| `edit` | Edit images (upscale, remove-bg, inpaint, outpaint, style-transfer, relight) | `edit --input img.png --action upscale` |
| `video` | Generate video clips (T2V, I2V) | `video --prompt "cinematic intro" --duration 5` |
| `voice` | Text-to-speech narration | `voice --text "Welcome to..." --output vo.mp3` |
| `music` | Background music generation | `music --prompt "upbeat cinematic" --duration 30` |
| `sfx` | Sound effects generation | `sfx --prompt "whoosh transition" --duration 2` |
| `remotion init` | Bootstrap Remotion project from template | `remotion init --template cinematic-product-16x9` |
| `remotion render` | Render Remotion project to MP4 | `remotion render --project ./my-video` |
| `plan` | Creative brief to storyboard JSON | `plan --brief "Launch video for..." --framework aida` |
| `pipeline` | End-to-end production (plan to render) | `pipeline --brief "..." --template aida-classic-16x9` |
| `status` | Check async task status | `status --task-id abc123 --provider freepik` |
| `providers` | Show available providers | `providers` |

Read `references/command-reference.md` for full parameter docs.

## Arguments

- **Command:** `$0` — one of the commands above
- **All args:** `$ARGUMENTS` — forwarded to the command script

## Authentication

Set one or more of these environment variables:

| Variable | Provider | Capabilities | Setup |
| ---------- | ---------- | ------------- | ------- |
| `FREEPIK_API_KEY` | Freepik | image, edit, video, voice, music, sfx | https://www.freepik.com/api/keys |
| `FAL_API_KEY` | fal.ai (+ Nano Banana 2 via fal) | image, edit, video | https://fal.ai/dashboard/keys |
| `GOOGLE_API_KEY` | Nano Banana 2 (via Google) | image, edit | https://aistudio.google.com/apikey |
| `OPENROUTER_API_KEY` | OpenRouter (Nano Banana 2 + many image models) | image | https://openrouter.ai/keys |
| `ELEVENLABS_API_KEY` | ElevenLabs | voice, music, sfx | https://elevenlabs.io/app/settings/api-keys |

Nano Banana 2 auto-detects the best available backend: `GOOGLE_API_KEY` (preferred) > `FAL_API_KEY` (fal-ai/nano-banana-2) > `OPENROUTER_API_KEY` > `infsh` CLI. OpenRouter also works as a standalone image provider with access to many models — see https://openrouter.ai/collections/image-models

At minimum, set `FREEPIK_API_KEY` (covers all capabilities). Run `providers` to check what's available.

## Provider auto-routing

Each command auto-selects the best provider based on available API keys. Override with `--provider`.

| Task | Priority 1 | Priority 2 | Priority 3 |
| ------ | ----------- | ----------- | ----------- |
| image | Nano Banana 2 (`GOOGLE_API_KEY` / `FAL_API_KEY` / `OPENROUTER_API_KEY`) | Freepik Seedream v5 lite | fal Flux-2 / OpenRouter |
| edit | Freepik (precision upscale) | fal (creative upscale) | Nano Banana 2 (iterative) |
| video | Freepik Kling v3 (quality) | fal Kling v2 (fallback) | — |
| voice | Freepik ElevenLabs | ElevenLabs direct | — |
| music | Freepik music gen | ElevenLabs | — |
| sfx | Freepik SFX | ElevenLabs | — |

Read `references/provider-matrix.md` for the full model selection decision tree.

---

## Opinionated creative workflow

This is how to think about when to use each tool. Follow this decision framework.

### When to use Nano Banana 2 (Gemini) for images

Nano Banana 2 is the **default for image generation** because:

- Best multi-image consistency (same character, same product across scenes)
- Instruction-based editing with up to 14 reference images
- Native Google Search grounding for real-world accuracy
- Fast and cheap (~$0.067/1K image on Flash, ~$0.134 on Pro)

**Use Nano Banana 2 (`gemini-3.1-flash-image-preview`) when:**

- Ideating scene visuals (fast iteration, batch 4 variants)
- Building a visual kit (hero, alt angle, detail, background — same style)
- Editing existing images with text instructions
- Combining multiple reference images into a new composition

**Use Nano Banana Pro (`gemini-3-pro-image-preview`) when:**

- Maximum quality needed for hero shots
- Complex compositions with precise text rendering
- Final delivery assets (not just concepting)

**Switch to Freepik Seedream v5 lite when:**

- Fast, high-quality generation with Freepik (default Freepik model)
- You want Freepik's rendering quality without specifying a model
- Commercial-ready output

**Other Freepik models (use `--model`):**

- `seedream-v4-5` — typography-heavy posters and ad creatives
- `mystic` — ultra-photoreal product photography (slower, higher cost)
- `flux-2-klein` — sub-second generation for rapid concepting

### When to use Kling (video) vs Remotion

This is the most important decision. **Never use AI video for what Remotion does better.**

**Use Kling (`video` command) for:**

- Hero moments: product reveals, cinematic openings, emotional beats (3-8s clips)
- Organic motion that's hard to code: water, fire, fabric, hair, camera orbits
- Image-to-video: animate a still into a living scene
- Transition inserts: short clips between Remotion scenes

**Use Remotion for:**

- Text animations, captions, kinetic typography
- Precise timing synced to voiceover
- Brand overlays, logos, consistent color grading
- Data visualizations, metric counters, charts
- Scene transitions (cuts, wipes, dissolves — deterministic)
- Final assembly: compositing Kling clips + stills + audio + text

**The ideal workflow:**

1. Generate scene stills with Nano Banana 2 (consistency across scenes)
2. Animate 2-3 hero stills with Kling (cinematic motion)
3. Generate voiceover + music
4. Assemble everything in Remotion (timing, text, transitions, audio mix)

### When to use the `pipeline` command vs manual steps

**Use `pipeline`** for standard product marketing or explainer videos where you trust the defaults. It runs the full plan-to-render sequence automatically.

**Use manual steps** when:

- You need to review/cherry-pick assets between steps
- The creative direction requires unusual choices
- You want to iterate on individual scenes
- You're composing a complex multi-format campaign (16:9 + 9:16 + stills)

---

Read `references/prompt-cookbook.md` for proven prompt patterns for every command — product photography, SaaS UI, transparent assets, video reveals, audio recipes, and full end-to-end examples.

---

## Command behavior

### `$0 = image`

Generate images with smart provider selection.

```bash
bash scripts/image.sh --prompt "Studio product shot of wireless earbuds, soft lighting" \
  --style photo --size 16:9 --resolution 2k --output hero.png
```

Force a specific provider or model:
```bash
bash scripts/image.sh --prompt "..." --provider freepik --model seedream-v4-5
bash scripts/image.sh --prompt "..." --provider nano-banana-2 --count 4
bash scripts/image.sh --prompt "..." --provider nano-banana-2 --model pro  # Nano Banana Pro
```

**Nano Banana 2 models:**
- `gemini-3.1-flash-image-preview` (default) — fast, cheap, great consistency
- `pro` or `gemini-3-pro-image-preview` — highest quality, 2x cost

### `$0 = edit`

Edit images with 6 actions: `upscale`, `remove-bg`, `inpaint`, `outpaint`, `style-transfer`, `relight`.

```bash
bash scripts/edit.sh --input hero.png --action upscale --scale 4 --output hero-4k.png
bash scripts/edit.sh --input photo.jpg --action remove-bg --output photo-nobg.png
bash scripts/edit.sh --input scene.png --action outpaint --left 512 --right 512 --prompt "extend the landscape"
```

### `$0 = video`

Generate video clips. Supports text-to-video and image-to-video.

**Opinionated approach:** Always generate a still first with `image`, review it, then animate with `video --image`. This gives you control over the starting frame.

```bash
bash scripts/video.sh --prompt "Product floating in space, rotating slowly" \
  --duration 5 --aspect 16:9 --output hero-clip.mp4

bash scripts/video.sh --prompt "Camera orbits around the product" \
  --image hero.png --duration 5 --output orbit-clip.mp4
```

### `$0 = voice`

Generate voiceover narration.

```bash
bash scripts/voice.sh --text "Welcome to the future of productivity." \
  --voice 21m00Tcm4TlvDq8ikWAM --output vo-intro.mp3
```

### `$0 = music`

Generate background music.

```bash
bash scripts/music.sh --prompt "cinematic ambient, subtle and professional" \
  --duration 45 --output music.mp3
```

### `$0 = sfx`

Generate sound effects.

```bash
bash scripts/sfx.sh --prompt "soft whoosh transition" --duration 1.5 --output whoosh.mp3
```

### `$0 = remotion init`

Bootstrap a Remotion project from bundled templates.

```bash
bash scripts/remotion_init.sh --template cinematic-product-16x9 --name MyProduct --output ./my-video
bash scripts/remotion_init.sh --list  # Show available templates
```

**Templates:** `aida-classic-16x9`, `cinematic-product-16x9`, `saas-metrics-16x9`, `mobile-ugc-9x16`, `blank-16x9`, `explainer-16x9`

All templates use Remotion 4.0.419 (pinned), React 18, TypeScript. Each includes `npm run start` (studio), `npm run render`, and `npm run verify`.

### `$0 = remotion render`

Render a Remotion project to MP4.

```bash
bash scripts/remotion_render.sh --project ./my-video --output final.mp4 --codec h264 --crf 18
```

### `$0 = plan`

Convert a creative brief into a structured storyboard.

```bash
bash scripts/plan.sh --brief "Launch video for FitPulse, a fitness app for busy professionals" \
  --framework aida --duration 45 --output storyboard.json
```

For AIDA framework, provide structured brief JSON:
```bash
bash scripts/plan.sh --brief-file brief.json --framework aida --output plan.json
```

Required AIDA fields: `product_name`, `audience`, `problem`, `solution`, `use_cases` (array), `cta`, `incentive`

### `$0 = pipeline`

Run the full production pipeline: brief to rendered video.

```bash
bash scripts/pipeline.sh \
  --brief "Launch video for a new AI writing assistant targeting content creators" \
  --template cinematic-product-16x9 \
  --output-dir ./creative-output \
  --duration 45

# Dry run to preview the plan:
bash scripts/pipeline.sh --brief "..." --dry-run

# Stop before render for review:
bash scripts/pipeline.sh --brief "..." --skip-render
```

**Pipeline steps:** plan > generate images > upscale heroes > generate video clips > voiceover > music > Remotion assembly > render

### `$0 = providers`

Check which providers are available.

```bash
bash scripts/providers.sh
```

### `$0 = status`

Check async task status.

```bash
bash scripts/status.sh --task-id abc123 --provider freepik
bash scripts/status.sh --all  # Show all tracked tasks
```

## Output convention

- **JSON to stdout** — machine-readable, pipe-friendly
- **Colored logs to stderr** — human-readable status updates
- All commands support `--dry-run` to preview without API calls
- Async tasks are tracked in `.creative-tasks.jsonl` per output directory

## Remotion principles

- Remotion is the source of truth for timing, layout, animation, and render
- External tools (Freepik, ElevenLabs, Kling) generate ancillary assets only
- Transitions: 8-18 frames, purposeful (not decorative)
- Load fonts explicitly with `@remotion/google-fonts`
- Always run `npm run verify` before `npm run render`
- Load reference rules from `references/remotion-rules/` as needed

Read `references/remotion-playbook.md` for detailed Remotion implementation guidance.

## Local resources

### Scripts (CLI commands)

- `scripts/creative.sh` — Main router (dispatches to sub-commands)
- `scripts/image.sh` — Image generation
- `scripts/edit.sh` — Image editing (6 actions)
- `scripts/video.sh` — Video generation
- `scripts/voice.sh` — Text-to-speech
- `scripts/music.sh` — Music generation
- `scripts/sfx.sh` — Sound effects
- `scripts/remotion_init.sh` — Remotion project bootstrap
- `scripts/remotion_render.sh` — Remotion render
- `scripts/plan.sh` — Brief to storyboard
- `scripts/pipeline.sh` — End-to-end pipeline
- `scripts/status.sh` — Task status checker
- `scripts/providers.sh` — Provider availability

### References

- `references/command-reference.md` — Full parameter docs for every command
- `references/provider-matrix.md` — Provider/model decision tree
- `references/creative-guidelines.md` — Quality standards
- `references/workflow-recipes.md` — End-to-end recipe examples
- `references/remotion-playbook.md` — Remotion implementation guide
- `references/freepik-ancillary-assets.md` — Asset generation recipes
- `references/template-showcase.md` — Template selector guide
- `references/remotion-rules-index.md` — Index of 29+ Remotion rule files
- `references/remotion-rules/` — Detailed Remotion rules (animations, audio, text, transitions, etc.)

### Templates (Remotion projects)

- `assets/templates/aida-classic-16x9/` — AIDA product marketing
- `assets/templates/cinematic-product-16x9/` — Dramatic product launch
- `assets/templates/saas-metrics-16x9/` — B2B dashboard metrics
- `assets/templates/mobile-ugc-9x16/` — Vertical social (Reels/TikTok)
- `assets/templates/blank-16x9/` — Minimal starter
- `assets/templates/explainer-16x9/` — 5-scene how-it-works
