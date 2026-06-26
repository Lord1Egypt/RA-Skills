# Product Demo Templates

Ready-to-use prompt templates for product showcase videos. Adapt the bracketed fields to your specific product.

## Hero Shot (4-8s)
Classic product reveal with premium studio feel.

```
Use case: product demo
Primary request: close-up of [PRODUCT] on [SURFACE: marble pedestal / wooden table / glass shelf]
Scene/background: dark studio cyclorama, subtle haze
Subject: [PRODUCT DESCRIPTION: matte black wireless speaker with fabric texture]
Action: slow [15-30]-degree orbit over [4-8] seconds
Camera: 85mm, shallow depth of field, steady dolly
Lighting/mood: soft key light, gentle rim, premium studio feel
Color palette: [3-5 COLORS: charcoal, slate, warm amber accents]
Constraints: no logos, no text, no people
Avoid: harsh bloom; oversharpening; clutter
```

### CLI command:
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Close-up of a matte black wireless speaker on a marble pedestal" \
  --use-case "product demo" \
  --scene "dark studio cyclorama, subtle haze" \
  --camera "85mm, shallow depth of field, slow 20-degree orbit" \
  --lighting "soft key, gentle rim, premium studio feel" \
  --palette "charcoal, slate, warm amber" \
  --constraints "no logos, no text" \
  --seconds 8
```

## Feature Highlight (8-12s)
Show a specific product feature in action.

```
Use case: product feature demo
Primary request: [PRODUCT] demonstrating [FEATURE: wireless charging / auto-adjust / water resistance]
Scene/background: clean workspace, natural light, minimal props
Subject: [PRODUCT] centered on [SURFACE]
Action: beat 1 (0-4s) product at rest, subtle light play; beat 2 (4-8s) [FEATURE ACTIVATION: lid opens / light turns on / water splashes]; beat 3 (8-12s) hold on result
Camera: 50mm, gentle push-in transitioning to locked-off
Lighting/mood: bright, modern, confident
Color palette: [BRAND COLORS], white background
Constraints: single product in frame; feature clearly visible; no people
Avoid: motion blur on feature activation; cluttered background
```

## 360 Product Spin (8-16s)
Full rotation product view.

```
Use case: product showcase
Primary request: full 360-degree rotation of [PRODUCT]
Scene/background: seamless white or gradient backdrop
Subject: [PRODUCT] centered on turntable
Action: smooth continuous rotation, one full turn over [8-16] seconds
Camera: locked-off, eye-level, 85mm, shallow depth of field
Lighting/mood: soft even studio lighting, subtle shadows
Color palette: [PRODUCT COLORS] against white/neutral
Constraints: perfectly centered; consistent lighting throughout rotation; no text
Avoid: wobble; speed variation; shadow changes
```

## Unboxing Sequence (12-20s)
Premium unboxing experience.

```
Use case: product unboxing
Primary request: premium unboxing of [PRODUCT] from [PACKAGING: matte box / eco kraft / magnetic case]
Scene/background: clean surface, warm ambient light
Subject: product packaging transitioning to revealed product
Action: beat 1 (0-4s) box slides into frame; beat 2 (4-8s) lid lifts smoothly; beat 3 (8-12s) product revealed with soft glow; beat 4 (12-16s) product placed on surface
Camera: top-down shifting to 45-degree angle, gentle motion
Lighting/mood: warm, aspirational, premium
Color palette: [BRAND COLORS], neutral backdrop
Constraints: smooth transitions; no visible hands; product pristine
Avoid: fast motion; harsh shadows; cluttered surface
```

## Macro Detail (4-8s)
Extreme close-up highlighting material quality.

```
Use case: product detail
Primary request: macro shot of [DETAIL: brushed aluminum / leather grain / glass surface] on [PRODUCT]
Scene/background: out-of-focus neutral backdrop, soft bokeh
Subject: [SPECIFIC DETAIL AREA] surface texture and finish
Action: slow push-in over [4-8] seconds, subtle light play across surface
Camera: 100mm macro, shallow depth of field, locked tripod
Lighting/mood: directional key, subtle speculars revealing texture
Color palette: [MATERIAL COLORS], soft highlights
Constraints: sharp focus on texture; no text; no logos
Avoid: flicker; unstable reflections; excessive noise
```

## Usage Notes
- Start with 4-8s clips for iteration, then extend successful takes
- Use `sora-2` for rapid iteration, `sora-2-pro` for final hero shots
- Input reference images help lock first-frame composition — use product photos
- For product lines, create character references for mascots/brand elements
- Download assets promptly — URLs expire after ~1 hour
