---
name: shellbot-creative
version: 1.0.0
description: Opinionated creative production system for image/video generation, image editing, motion scenes, voiceovers, music, and Remotion assembly. Combines Freepik, fal.ai, Nano Banana 2 (Gemini 3.1 Flash Image Preview), and Remotion workflows for explainers, product marketing videos, social ads, and reusable asset pipelines. Use when users ask to create or edit visual assets, generate clips, produce narration/music, or deliver a polished final video from a brief.
allowed-tools: Bash(curl *api.freepik.com*), Bash(curl *queue.fal.run*), Bash(curl *api.fal.ai*), Bash(curl *fal.run*), Bash(jq *), Bash(mkdir *), Bash(infsh *), Bash(node *), Bash(npx *), Bash(npm *), Bash(ffmpeg *), Bash(python3 scripts/*), Read, Write
argument-hint: "<command> [provider_or_model] [--param value]"
metadata: {"openclaw":{"emoji":"🎬","primaryEnv":"FREEPIK_API_KEY","providerEnv":["FREEPIK_API_KEY","FAL_KEY","INFERENCE_API_KEY"],"homepage":"https://docs.openclaw.ai/tools/skills"}}
---

# shellbot-creative

Create high-end creative outputs by chaining providers intentionally:

1. Generate reusable assets (Nano Banana 2 / Freepik / fal)
2. Generate scene motion (Freepik Kling / fal video models)
3. Add voice and music (Freepik ElevenLabs voiceover + music or fal equivalents)
4. Assemble and polish in Remotion

Use this skill as a production orchestrator, not as isolated single calls.

## Arguments

- **Command:** `$0` (`plan` | `asset` | `edit` | `video` | `voice` | `music` | `remotion` | `pipeline` | `status` | `sample`)
- **Arg 1:** `$1` (provider, model, or workflow type)
- **Arg 2+:** `$2`, `$3`, etc.
- **All args:** `$ARGUMENTS`

## Authentication and provider checks

Support any of these providers:

- `FREEPIK_API_KEY` for Freepik API
- `FAL_KEY` for fal.ai API
- `INFERENCE_API_KEY` (or `infsh login`) for Nano Banana 2 via inference.sh

Before any generation call:

```bash
[ -n "$FREEPIK_API_KEY" ] && echo "Freepik ready"
[ -n "$FAL_KEY" ] && echo "fal ready"
command -v infsh >/dev/null && echo "infsh available"
```

If a requested provider is not authenticated, route to another available provider and clearly explain the fallback.

## Provider routing (opinionated defaults)

- **Asset ideation / strong multi-image consistency:** Nano Banana 2
- **Photoreal product hero, posters, typography, upscale/edit suite:** Freepik
- **Fast model exploration or niche fal endpoint needs:** fal.ai
- **Final timeline composition, transitions, captions, audio mix:** Remotion

Read `references/provider-matrix.md` for exact model choices.

## Command behavior

### `$0 = plan`

Turn a user brief into a production storyboard and shot list.

```bash
python3 scripts/creative_brief_to_storyboard.py \
  --brief "Launch video for a new fitness app aimed at busy professionals" \
  --format product-marketing \
  --duration 45 \
  --aspect-ratio 16:9 \
  --out storyboard.json
```

Then create a provider/model routing recommendation:

```bash
python3 scripts/creative_provider_router.py \
  --goal full-video \
  --priority quality \
  --needs-consistency true \
  --needs-typography true
```

### `$0 = asset`

Generate still assets for scenes.

- **Nano Banana 2 default (consistency + editing):**
```bash
infsh app run google/gemini-3-1-flash-image-preview --input '{
  "prompt": "Premium SaaS dashboard on a laptop, soft studio light",
  "aspect_ratio": "16:9",
  "num_images": 4,
  "resolution": "2K"
}'
```

- **Freepik high-fidelity product image (Mystic):**
```bash
curl -s -X POST "https://api.freepik.com/v1/ai/mystic" \
  -H "x-freepik-api-key: $FREEPIK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Studio product shot of matte black earbuds on reflective surface","resolution":"2k","styling":{"style":"photo"}}'
```

- **fal fast concepting (Flux):**
```bash
curl -s -X POST "https://queue.fal.run/fal-ai/flux-2" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Cyberpunk storefront, rainy night","image_size":"landscape_16_9"}'
```

### `$0 = edit`

Perform image editing/upscaling/background work before animation.

- Prefer Freepik edit endpoints for deterministic production flows.
- Prefer Nano Banana 2 when iterative instruction-based edits are needed with multiple references.
- Use Freepik upscalers for final delivery quality.

See `references/workflow-recipes.md` for edit chains.

### `$0 = video`

Generate motion scenes from prompts or keyframes.

- Freepik default for premium multi-shot video: `kling-v3-omni-pro`
- fal default when Freepik key is unavailable: `fal-ai/kling-video/v2/image-to-video`

Always save scene outputs in a structured project folder:

```bash
mkdir -p ./creative-output/{assets,scenes,audio,final,manifests}
```

### `$0 = voice`

Generate narration.

- Default: Freepik ElevenLabs voiceover endpoint
- Fallback: fal text-to-speech model if user requests fal-only flow

Use concise script-first narration lines generated from storyboard scenes.

### `$0 = music`

Generate background music and keep loudness headroom for voiceover.

- Default: Freepik `music-generation`
- Target: deliver 10-240s cue matching storyboard duration

### `$0 = remotion`

Assemble final video with composited assets, generated clips, captions, and audio mix.

```bash
npx create-video@latest creative-video
cd creative-video
```

Generate a Remotion manifest from the storyboard:

```bash
python3 ../scripts/remotion_manifest_from_storyboard.py \
  --storyboard ../storyboard.json \
  --fps 30 \
  --voiceover-url "https://example.com/voice.mp3" \
  --music-url "https://example.com/music.mp3" \
  --out ./src/creative-manifest.json
```

Then implement composition using `assets/remotion/ProductMarketingTemplate.tsx` as a baseline.

### `$0 = pipeline`

Run end-to-end sequence:

1. `plan` from brief
2. `asset` generation per scene
3. `edit` and upscale selected assets
4. `video` generation for hero scenes
5. `voice` + `music`
6. `remotion` assembly + render

If the user asks for a product marketing or explainer video, this is the default command path.

### `$0 = status`

Check async task status for Freepik/fal requests and report:

- current state
- queue position if available
- failed-step diagnosis
- next action

### `$0 = sample`

Load ready-to-run workflows from `references/samples.md`.

## Quality bar for "outstanding" creative output

Always enforce:

- Clear narrative arc: hook -> value -> proof -> CTA
- Visual consistency across scenes (same product, palette, style)
- Voice/music balance (voice intelligibility first)
- Captions and on-screen text optimized for mobile safe zones
- Brand-safe outputs and explicit user approval before final render

## Production workflow policy

- Prefer 16:9 for explainers and product demos unless user asks otherwise
- Prefer 9:16 for shorts/reels/tiktok style cuts
- Generate 2-4 variations of key hero scenes, then converge
- Keep source assets reusable (clean backgrounds, layered variants when possible)
- For revisions, edit prompts/scene timing first before regenerating everything

## Local resources included in this skill

- `scripts/creative_brief_to_storyboard.py` - brief -> timed scene plan
- `scripts/creative_provider_router.py` - requirement -> provider/model route
- `scripts/remotion_manifest_from_storyboard.py` - storyboard -> Remotion-ready manifest
- `scripts/run_full_dry_run.py` - full local dry run that outputs storyboard, routes, manifest, and runnable API plan
- `scripts/package_skill.sh` - build a distributable `.tar.gz` of the skill
- `scripts/install_skill.sh` - install the skill folder into an OpenClaw skills directory
- `references/creative-guidelines.md` - durable standards for creative quality
- `references/provider-matrix.md` - provider/model decision matrix
- `references/workflow-recipes.md` - end-to-end recipes for common outcomes
- `references/samples.md` - concrete command samples
- `references/remotion-playbook.md` - Remotion-specific finishing guidance
- `assets/remotion/ProductMarketingTemplate.tsx` - starter Remotion composition
- `assets/remotion/Root.tsx` - composition registration sample

## References

- OpenClaw skills format and frontmatter: https://docs.openclaw.ai/tools/skills
- OpenClaw slash command behavior (`$0`, `$1`, `$ARGUMENTS`): https://docs.openclaw.ai/tools/slash-commands
- OpenClaw metadata config (`metadata.openclaw`): https://docs.openclaw.ai/tools/skills-config
- OpenClaw creating skills guide: https://docs.openclaw.ai/tools/creating-skills
