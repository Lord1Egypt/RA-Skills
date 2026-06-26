# shellbot-creative-studio

A headless creative production studio for AI agents. Generate images, edit photos, create videos, produce voiceover/music/SFX, and assemble polished output via Remotion — all through opinionated CLI commands with smart provider auto-routing.

Think of it as **headless Canva** that any AI agent can plug into.

## Quick start

```bash
# 1. Set at least one API key
export FREEPIK_API_KEY="your-key"    # Covers everything
export GOOGLE_API_KEY="your-key"     # Best for image generation (Nano Banana 2)

# 2. Check what's available
bash scripts/providers.sh

# 3. Generate an image
bash scripts/image.sh --prompt "Product shot of wireless earbuds on marble" --output earbuds.png

# 4. Generate a video from that image
bash scripts/video.sh --prompt "Slow orbit around earbuds" --image earbuds.png --output reveal.mp4

# 5. Or run the full pipeline
bash scripts/pipeline.sh --brief "Launch video for our new AI assistant" --dry-run
```

## What's in the box

### 13 CLI commands

| Command | What it does |
|---------|-------------|
| `image` | Generate images (Nano Banana 2 / Freepik / fal) |
| `edit` | Upscale, remove background, inpaint, outpaint, style transfer, relight |
| `video` | Text-to-video and image-to-video (Kling / fal) |
| `voice` | Text-to-speech narration (ElevenLabs) |
| `music` | Background music generation |
| `sfx` | Sound effects (whooshes, impacts, ambience) |
| `remotion init` | Bootstrap from 6 bundled Remotion templates |
| `remotion render` | Render Remotion project to MP4 |
| `plan` | Creative brief to structured storyboard |
| `pipeline` | Full end-to-end: brief to rendered video |
| `status` | Check async task status across providers |
| `providers` | Show available providers and capabilities |

### 4 providers with smart auto-routing

| Provider | Key | Best for |
|----------|-----|----------|
| **Nano Banana 2** | `GOOGLE_API_KEY` or `OPENROUTER_API_KEY` | Image generation, consistency, editing |
| **Freepik** | `FREEPIK_API_KEY` | Seedream v5 lite images, video (Kling), voice, music, SFX |
| **fal.ai** | `FAL_API_KEY` | Fast image generation, video fallback |
| **ElevenLabs** | `ELEVENLABS_API_KEY` | Direct voice, music, SFX |

You don't pick providers — the system does. Set your keys and go. Override with `--provider` when needed.

### 6 Remotion templates

| Template | Use case |
|----------|----------|
| `aida-classic-16x9` | Product marketing (AIDA framework) |
| `cinematic-product-16x9` | Premium product launches |
| `saas-metrics-16x9` | B2B SaaS, dashboard-style |
| `mobile-ugc-9x16` | Reels, TikTok, Stories (vertical) |
| `blank-16x9` | Minimal starter for custom projects |
| `explainer-16x9` | How-it-works, tutorials, walkthroughs |

### 29+ Remotion rules

Full reference library covering animations, audio, text, transitions, captions, 3D, charts, and more.

## Architecture

```
User / AI Agent
  |
  v
creative.sh (router)
  |
  +-- image.sh -----> Nano Banana 2 / Freepik / fal
  +-- edit.sh ------> Freepik / fal / Nano Banana 2
  +-- video.sh -----> Freepik Kling / fal Kling
  +-- voice.sh -----> Freepik ElevenLabs / ElevenLabs
  +-- music.sh -----> Freepik / ElevenLabs
  +-- sfx.sh -------> Freepik / ElevenLabs
  +-- plan.sh ------> Python storyboard generators
  +-- pipeline.sh --> Orchestrates all of the above
  |
  +-- remotion_init.sh ----> 6 bundled templates
  +-- remotion_render.sh --> npx remotion render
  |
  +-- lib/
  |     +-- provider_router.sh  (auto-selects provider)
  |     +-- async_poll.sh       (polls Freepik/fal tasks)
  |     +-- output.sh           (JSON stdout, colored stderr)
  |     +-- config.sh           (constants, paths)
  |     +-- task_log.sh         (JSONL task tracking)
  |
  +-- python/
        +-- brief_to_storyboard.py
        +-- brief_to_aida_plan.py
        +-- storyboard_to_remotion.py
        +-- dry_run.py
```

## The opinionated workflow

The skill is designed around a specific creative philosophy:

### 1. Images first, video second

Generate still images with Nano Banana 2 for consistency across scenes. Review and curate. Only then animate hero stills with Kling video. This gives you control over the starting frame and visual consistency.

### 2. Remotion for assembly, AI for assets

Never use AI video for things Remotion handles better (text, timing, transitions, branding). Use Kling for organic motion (product reveals, B-roll, cinematic moments). Use Remotion for everything else.

### 3. Audio layered, not mixed

Voiceover at volume 1.0 (clear, intelligible). Music at 0.15-0.25 (ducks under voice). SFX sparse and purposeful. Never let music compete with narration.

### 4. Generate many, converge to few

Generate 2-4 variations of key hero assets, pick the best, upscale it, then build the rest of the production around it.

## Output convention

Every command follows the same pattern:
- **JSON to stdout** — machine-readable, pipe into `jq`
- **Colored logs to stderr** — human status updates
- **`--dry-run`** on every command — see what would execute without API calls
- **`.creative-tasks.jsonl`** — tracks all async tasks per project

## File structure

```
shellbot-creative-studio/
+-- SKILL.md                     # Skill definition + opinionated instructions
+-- README.md                    # This file
+-- scripts/                     # All CLI commands
|   +-- creative.sh              # Router
|   +-- image.sh                 # Image generation
|   +-- edit.sh                  # Image editing (6 actions)
|   +-- video.sh                 # Video generation
|   +-- voice.sh                 # Text-to-speech
|   +-- music.sh                 # Music generation
|   +-- sfx.sh                   # Sound effects
|   +-- remotion_init.sh         # Template bootstrap
|   +-- remotion_render.sh       # Video render
|   +-- plan.sh                  # Storyboard generation
|   +-- pipeline.sh              # End-to-end pipeline
|   +-- status.sh                # Task status
|   +-- providers.sh             # Provider check
|   +-- lib/                     # Shared bash library
|   +-- python/                  # Python storyboard scripts
+-- references/                  # Documentation + Remotion rules
|   +-- command-reference.md     # Full parameter docs
|   +-- provider-matrix.md       # Provider decision tree
|   +-- creative-guidelines.md   # Quality standards
|   +-- workflow-recipes.md      # End-to-end examples
|   +-- remotion-playbook.md     # Remotion guide
|   +-- remotion-rules/          # 29+ rule files
+-- assets/
|   +-- templates/               # 6 Remotion project templates
+-- .clawhubignore               # Publish filter
+-- _meta.json                   # ClawHub registry metadata
```

## Tested with

- macOS (bash 3.2+)
- `curl`, `jq` (required)
- Node.js 18+ (for Remotion)
- Python 3.10+ (for storyboard scripts)

## License

Proprietary. Part of the ShellBot platform.
