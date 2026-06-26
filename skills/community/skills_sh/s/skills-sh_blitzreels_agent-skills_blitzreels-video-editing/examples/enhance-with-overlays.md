# Example: Enhance with Overlays

Add graphics, code blocks, and backgrounds to an existing project.

## 1. Check Current State

```bash
bash scripts/editor.sh context proj_abc123 timeline
# → See existing clips, timing, and layers
```

## 2. Add Opening Text Overlay

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/content-items '{
  "kind": "overlay",
  "text": "5 Tips for Better Code",
  "start_seconds": 0,
  "duration_seconds": 3,
  "layer_index": 1
}'
```

## 3. Add Code Snippet (Motion Code)

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/motion-code '{
  "code": "const greet = (name: string) => {\n  return `Hello, ${name}!`;\n};",
  "language": "typescript",
  "theme": "github-dark",
  "font": "JetBrains Mono",
  "position": "center",
  "showWindowChrome": true,
  "windowTitle": "greeting.ts",
  "showLineNumbers": true,
  "startSeconds": 5,
  "durationSeconds": 8,
  "transition": "typewriter"
}'
```

## 4. Add Lower-Third Label

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/content-items '{
  "kind": "overlay",
  "text": "Jane Smith — Senior Developer",
  "start_seconds": 2,
  "duration_seconds": 5,
  "layer_index": 1
}'
```

## 5. Add Cinematic Background

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/backgrounds '{
  "style_keyword": "film",
  "span_full_video": true
}'
```

Or use a custom gradient:

```bash
bash scripts/blitzreels.sh POST /projects/proj_abc123/backgrounds '{
  "color": "#0a1628",
  "gradient_enabled": true,
  "vignette_intensity": 0.3,
  "film_grain_style": "subtle",
  "span_full_video": true
}'
```

## 6. Export

```bash
bash scripts/editor.sh export proj_abc123 --resolution 1080p
```
