# Template: exploded-view

**Purpose**: Generate a single premium vertical exploded-view infographic with layered component separation, technical callouts, and high material realism.

**When to use**: User needs a technical or educational product visual that explains internal structure, ingredients, or component hierarchy in one image.

**Output type**: IMAGE | **Supports analysis**: Yes | **Cost**: 1K/2K = 1 credit, 4K = 2 credits

## Assets

| Role | Min | Max | Required |
|------|-----|-----|----------|
| PRODUCT (product images) | 1 | 10 | Yes |
| LOGO (brand logo) | 0 | 1 | No |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `style` | string | `auto` | Visual style direction (see options below) |
| `customStyle` | string | — | Free-text style (only when `style=custom`) |
| `layerDensity` | string | `balanced` | Number of exploded layers: `auto`, `light`, `balanced`, `dense` |
| `backgroundMode` | string | `auto` | Background strategy (see options below) |
| `labelPlacement` | string | `balanced-callout` | Callout line and label placement |
| `aspectRatio` | string | `3:4` | Output ratio, optimized for vertical technical storytelling |
| `imageSize` | string | `2K` | Resolution: `1K`, `2K`, `4K` |
| `primaryLang` | string | `en` | Primary language code |
| `secondaryLang` | string | `none` | Secondary language code, or `none` for monolingual |

## Style Options

| Style | Visual Feel | Best For |
|-------|-------------|----------|
| `auto` | AI picks style based on product cues | Default choice |
| `premium-technical` | Controlled studio lighting, precision details | Electronics, tools, engineered products |
| `material-focus` | Texture-first macro realism | Skincare, ingredients, material-driven products |
| `lifestyle-soft` | Airy premium tone with soft depth blur | Wellness, beauty, home products |
| `studio-minimal` | Clean gradient catalog aesthetic | Modern, minimal brands |
| `morandi-editorial` | Soft muted palette, editorial premium tone | Luxury and design-forward products |
| `custom` | User-defined style text | Specific art direction |

## Background Mode

| Mode | Description | When to Use |
|------|-------------|-------------|
| `auto` | AI chooses best mode for readability + realism | Default |
| `gradient` | Multi-tone studio gradient (avoid flat single-color fill) | Modern clean visuals |
| `textured` | Subtle material/paper/stone texture backdrop | Tactile, premium tone |
| `product-matched-scene` | Scene inferred from product category/ingredients | Category storytelling with contextual cues |

Note: `scene` is accepted as a backward-compatible alias and normalized to `product-matched-scene`.

## Label Placement

| Value | Description |
|-------|-------------|
| `right-callout` | Minimalist labels on the right side |
| `left-callout` | Minimalist labels on the left side |
| `balanced-callout` | Split callouts across left and right (default) |
| `none` | No callout labels or leader lines |

## Recommended Defaults by Goal

| Goal | Suggested Options |
|------|-------------------|
| Technical education block | `{"style":"premium-technical","layerDensity":"balanced","labelPlacement":"balanced-callout"}` |
| Ingredient/material storytelling | `{"style":"material-focus","backgroundMode":"product-matched-scene","labelPlacement":"right-callout"}` |
| Clean premium hero-infographic hybrid | `{"style":"studio-minimal","backgroundMode":"gradient","labelPlacement":"none"}` |
| Mobile-first readability | `{"layerDensity":"light","labelPlacement":"none","aspectRatio":"3:4"}` |

## Examples

```bash
# Default exploded infographic (recommended starting point)
vibesku generate -t exploded-view \
  -n "Ceramic Aroma Diffuser" \
  -d "Ultrasonic diffuser with ceramic shell, BPA-free tank, and whisper-quiet operation" \
  -b "NebuHome" \
  -i diffuser-front.jpg diffuser-side.jpg

# Technical product with denser structure
vibesku generate -t exploded-view \
  -n "Smart Electric Toothbrush" \
  -d "Sonic motor, pressure sensor, magnetic charging base, IPX7 waterproof" \
  -i toothbrush.jpg \
  -o '{"style":"premium-technical","layerDensity":"dense","backgroundMode":"textured","labelPlacement":"balanced-callout","aspectRatio":"3:4"}'

# Ingredient-focused skincare visual (bilingual)
vibesku generate -t exploded-view \
  -n "Hydrating Serum" \
  -d "Niacinamide, hyaluronic acid, ceramide complex, fragrance-free" \
  -i serum.jpg \
  -o '{"style":"material-focus","backgroundMode":"product-matched-scene","labelPlacement":"right-callout","primaryLang":"zh","secondaryLang":"en"}'

# Minimal no-label version for ad use
vibesku generate -t exploded-view \
  -n "Premium Blender" \
  -i blender.jpg \
  -o '{"style":"studio-minimal","labelPlacement":"none","backgroundMode":"gradient","aspectRatio":"9:16","imageSize":"4K"}'
```

## Tips

- Start with `style=auto` unless the user provides a clear design direction.
- Use `layerDensity=light` for small screens or dense products to preserve clarity.
- Keep `labelPlacement=balanced-callout` for technical explainers; switch to `none` for cleaner ad-style outputs.
- `aspectRatio=3:4` is usually best for PDP infographics; use `9:16` for mobile-first placements.
- Use multiple product angles in `-i` when components are complex to improve fidelity.
- For bilingual labels, set both `primaryLang` and `secondaryLang`; otherwise keep `secondaryLang=none`.
