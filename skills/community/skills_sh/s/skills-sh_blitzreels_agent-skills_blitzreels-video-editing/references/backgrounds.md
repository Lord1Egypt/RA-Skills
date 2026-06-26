# Backgrounds (Fill Layers) Reference

BlitzReels exposes background "fill layers" via the **Backgrounds** endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/projects/{projectId}/backgrounds` | List background fill layers |
| POST | `/projects/{projectId}/backgrounds` | Add background fill layer |

Notes:
- The public API uses `/backgrounds` (not `/fill-layers`).
- There is no public "list presets" endpoint. Prefer `style_keyword` or explicit settings.

## Add A Background (Common Patterns)

### 1) Solid Color (Full Video)

```bash
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/backgrounds" '{
  "color": "#0b0f19",
  "opacity": 1,
  "span_full_video": true
}'
```

### 2) Style Keyword (Full Video)

```bash
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/backgrounds" '{
  "style_keyword": "moody",
  "span_full_video": true,
  "opacity": 1
}'
```

### 3) Pattern + Grain + Vignette

```bash
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/backgrounds" '{
  "color": "#0b0f19",
  "pattern": "scanlines",
  "film_grain_style": "vhs",
  "vignette_intensity": 0.4,
  "opacity": 0.9,
  "span_full_video": true
}'
```

## Request Fields (OpenAPI)

Fields supported by `POST /projects/{projectId}/backgrounds`:

- `preset_id` (string) Optional. If you already know a preset id.
- `style_keyword` (string) Optional. One of:
  - `dark` `light` `minimal` `neutral` `professional` `moody` `creative` `warm` `dramatic` `magical` `film` `noir` `hollywood` `epic` `tech` `retro` `graphic` `modern` `vhs` `vintage` `neon` `vignette` `grain` `dreamy`
- `span_full_video` (boolean) Optional. Default: false.
- `start_seconds` (number) Optional. Default: 0.
- `duration_seconds` (number) Optional.
- `layer_index` (integer 0..10) Optional.
- `name` (string) Optional.
- `color` (string) Optional. Example: `#000000`.
- `gradient_enabled` (boolean) Optional.
- `pattern` (string) Optional. One of:
  - `none` `dots` `grid` `lines` `diagonal` `scanlines` `noise`
- `film_grain_style` (string) Optional. One of:
  - `none` `subtle` `moderate` `heavy` `16mm` `35mm` `super8` `vhs`
- `vignette_intensity` (number 0..1) Optional.
- `opacity` (number 0..1) Optional.

