# Prompt Cookbook

Proven prompt patterns for each command. Copy-paste and adapt.

## Image generation

### Product photography
```bash
bash scripts/image.sh --prompt "Studio product shot of [PRODUCT], soft directional lighting, \
  white cyclorama background, shallow depth of field, 85mm lens look" --resolution 2k
```

### SaaS dashboard UI
```bash
bash scripts/image.sh --prompt "Clean SaaS analytics dashboard, dark mode, \
  data visualization with blue and purple accent colors, glassmorphism cards, \
  no text placeholders, professional UI design" --size 16:9
```

### Lifestyle context shot
```bash
bash scripts/image.sh --prompt "Professional woman using [PRODUCT] at a modern coworking space, \
  natural window light, candid moment, editorial photography style" --style photo
```

### Isometric illustration
```bash
bash scripts/image.sh --prompt "Isometric 3D render of [SCENE], miniature style, \
  warm indirect lighting, pastel color palette, clean white background" --resolution 2k
```

### Icon / asset with transparency (green screen trick)
```bash
bash scripts/image.sh --prompt "[OBJECT] centered on a solid bright green background (#00FF00), \
  no shadows, no gradients, flat green, product photography lighting"
# Then remove the green:
bash scripts/edit.sh --input result.png --action remove-bg --output clean.png
```

### Multiple variations for selection
```bash
bash scripts/image.sh --prompt "Abstract geometric pattern, tech vibes, dark blue and cyan" \
  --count 4 --provider nano-banana-2
```

### Hero with Nano Banana Pro (maximum quality)
```bash
bash scripts/image.sh --prompt "Luxury tech product floating in volumetric light, \
  photorealistic, dramatic studio lighting, 8K detail" --provider nano-banana-2 --model pro
```

### Consistent visual kit (same style across scenes)
```bash
# Generate all scenes in one batch session with Nano Banana 2
# The model maintains consistency when prompted with shared style cues
bash scripts/image.sh --prompt "Scene 1: [DESCRIPTION], flat illustration style, \
  blue and orange palette, thick outlines" --provider nano-banana-2 --output scene-1.png
bash scripts/image.sh --prompt "Scene 2: [DESCRIPTION], flat illustration style, \
  blue and orange palette, thick outlines" --provider nano-banana-2 --output scene-2.png
bash scripts/image.sh --prompt "Scene 3: [DESCRIPTION], flat illustration style, \
  blue and orange palette, thick outlines" --provider nano-banana-2 --output scene-3.png
```

## Image editing

### Upscale for final delivery
```bash
bash scripts/edit.sh --input hero.png --action upscale --scale 4 --output hero-4k.png
```

### Remove background for Remotion compositing
```bash
bash scripts/edit.sh --input product.jpg --action remove-bg --output product-nobg.png
```

### Extend canvas for wider scene
```bash
bash scripts/edit.sh --input scene.png --action outpaint \
  --left 512 --right 512 --prompt "continue the landscape naturally"
```

### Style transfer from a reference
```bash
bash scripts/edit.sh --input photo.jpg --action style-transfer \
  --reference artistic-ref.jpg --output stylized.png
```

### Inpaint a region
```bash
bash scripts/edit.sh --input scene.png --action inpaint \
  --mask mask.png --prompt "a red sports car parked here" --output modified.png
```

### Relight a scene
```bash
bash scripts/edit.sh --input portrait.jpg --action relight \
  --prompt "warm golden hour sunset lighting from the left" --output relit.png
```

## Video generation

### Hero product reveal (the gold standard workflow)
```bash
# Step 1: Generate still with Nano Banana 2
bash scripts/image.sh --prompt "Sleek wireless headphones on dark reflective surface, \
  dramatic rim lighting" --output product-still.png
# Step 2: Animate with Kling
bash scripts/video.sh --prompt "Slow camera orbit around the headphones, \
  subtle light reflections shift, cinematic" --image product-still.png --duration 5 --output reveal.mp4
```

### Cinematic B-roll
```bash
bash scripts/video.sh --prompt "Aerial view of a modern city at golden hour, \
  smooth drone movement, cinematic color grading" --duration 5 --aspect 16:9
```

### Organic texture for Remotion backgrounds
```bash
bash scripts/video.sh --prompt "Abstract flowing liquid gold, dark background, \
  smooth continuous motion" --duration 10 --output texture-bg.mp4
```

### App demo animation
```bash
bash scripts/image.sh --prompt "Mobile app showing chat interface, clean UI" --size 9:16 --output app-screen.png
bash scripts/video.sh --prompt "Finger scrolls through the chat messages, \
  smooth natural motion" --image app-screen.png --duration 5 --aspect 9:16 --output app-demo.mp4
```

## Audio

### Professional voiceover
```bash
bash scripts/voice.sh --text "Introducing FlowPilot — the AI co-pilot that keeps your team in sync." \
  --voice 21m00Tcm4TlvDq8ikWAM --speed 0.95 --output vo-intro.mp3
```

### Background music (ducks under voiceover)
```bash
bash scripts/music.sh --prompt "Subtle ambient electronic, minimal beats, \
  corporate technology feel, not distracting" --duration 45 --output bg-music.mp3
```

### Transition whoosh
```bash
bash scripts/sfx.sh --prompt "Smooth cinematic whoosh, medium speed" --duration 1 --output whoosh.mp3
```

### UI click sound
```bash
bash scripts/sfx.sh --prompt "Soft digital click, subtle, modern UI interaction" \
  --duration 0.5 --output click.mp3
```

### Ambient loop
```bash
bash scripts/sfx.sh --prompt "Calm office ambience, soft keyboard typing, \
  distant conversation" --duration 15 --loop --output office-ambience.mp3
```

## Full pipeline

### Product launch (automated)
```bash
bash scripts/pipeline.sh \
  --brief "Launch video for FlowPilot, an AI productivity assistant for remote teams. \
  Target audience: engineering managers. Problem: scattered updates across tools. \
  CTA: Start free trial." \
  --template cinematic-product-16x9 --duration 45 --output-dir ./flowpilot-launch
```

### Dry run first (always recommended)
```bash
bash scripts/pipeline.sh --brief "..." --dry-run
```

### Stop before render for manual review
```bash
bash scripts/pipeline.sh --brief "..." --skip-render
# Review assets in creative-output/, then:
bash scripts/remotion_render.sh --project ./creative-output/remotion-project --output final.mp4
```
