# Workflow Recipes

## 1) Product marketing video (45s)

1. Build storyboard:
```bash
python3 scripts/creative_brief_to_storyboard.py \
  --brief "Launch campaign for AI sales assistant" \
  --format product-marketing --duration 45 --out storyboard.json
```
2. Generate hero assets with Freepik Mystic or Nano Banana 2.
3. Create 2-4 hero motion clips with Kling.
4. Generate voiceover + music with Freepik audio endpoints.
5. Build Remotion manifest:
```bash
python3 scripts/remotion_manifest_from_storyboard.py \
  --storyboard storyboard.json --fps 30 \
  --voiceover-url "https://.../voice.mp3" \
  --music-url "https://.../music.mp3" \
  --out creative-output/manifests/remotion.json
```
6. Render final in Remotion.

## 2) Explainer video with reusable visual kit

1. Plan with `--format explainer`.
2. Generate a reusable image pack (hero, alternate angle, detail, background).
3. Edit all selected assets to match the same color palette.
4. Use Remotion text/caption overlays for step-by-step explanation.

## 3) Image edit + upscale chain

1. Start with Nano Banana 2 instruction edits.
2. Move selected outputs to Freepik upscaler (`image-upscaler-precision-v2`).
3. Export high-res stills for ads, thumbnails, and scene inserts.

## 4) Hybrid AI motion + Remotion composition

1. Create scene stills via Nano Banana 2 or Freepik.
2. Animate selected stills with Freepik Kling or fal image-to-video model.
3. Composite generated clips in Remotion with deterministic transitions, captions, and brand elements.
4. Mix voiceover + music and render final delivery versions (16:9 and 9:16).
