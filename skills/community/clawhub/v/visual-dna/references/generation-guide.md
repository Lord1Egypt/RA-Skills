# Generation Guide

How to use a completed Design DNA JSON to generate designs in Phase 2.

## Priority Order

1. **Colour & Typography** — define 80% of visual identity
2. **Spacing & Layout** — structural rhythm
3. **Shape & Elevation** — surface treatment
4. **Design Style qualitative fields** — mood, personality, composition
5. **Visual Effects** — special rendering layer
6. **Motion & Interaction** — enhance after static layout is solid

## Dimension 1: design_system → Code

### CSS Variables (default approach)

Generate a `:root` block with all design tokens:

```css
:root {
  --color-primary: {color.primary.hex};
  --color-secondary: {color.secondary.hex};
  --color-accent: {color.accent.hex};
  --color-bg: {surface.background};
  --color-card: {surface.card};
  --font-heading: {typography.font_families.heading};
  --font-body: {typography.font_families.body};
  --font-mono: {typography.font_families.mono};
  --radius-sm: {shape.border_radius.small};
  --radius-md: {shape.border_radius.medium};
  --radius-lg: {shape.border_radius.large};
  --shadow-low: {elevation.levels.low};
  --shadow-med: {elevation.levels.medium};
  --shadow-high: {elevation.levels.high};
  --ease: {motion.easing};
  --dur-micro: {motion.duration_scale.micro};
  --dur-normal: {motion.duration_scale.normal};
  --dur-macro: {motion.duration_scale.macro};
}
```

### Tailwind CSS (when project uses Tailwind)

```
color.primary.hex        → extend.colors.primary
typography.font_families → extend.fontFamily
spacing.scale            → extend.spacing
shape.border_radius      → extend.borderRadius
elevation.levels         → extend.boxShadow
```

### Component decisions

- `components.button_style` → button classes and hover states
- `components.card_style` → card container padding, border, shadow
- `components.navigation_pattern` → nav layout choice
- `interaction_feel.hover_behavior` → :hover/:focus states
- `motion.easing` + `duration_scale` → transition shorthand

## Dimension 2: design_style → Subjective Decisions

| DNA Field | Guides |
|-----------|--------|
| `aesthetic.mood` | Warm tones, cool precision, playful energy |
| `visual_language.whitespace_usage` | Padding/margin generosity |
| `visual_language.contrast_level` | How much elements pop vs blend |
| `composition.hierarchy_method` | Size, weight, colour, or space for emphasis |
| `composition.balance_type` | Symmetric vs dynamic asymmetry |
| `imagery.graphic_elements` | Decorative SVGs, gradients, patterns |
| `brand_voice_in_ui.tone` | Microcopy phrasing and personality |
| `interaction_feel.microinteraction_density` | How many hover/click effects |

## Dimension 3: visual_effects → Special Rendering

### Technology by performance tier

| Tier | Technologies |
|------|-------------|
| **lightweight** | CSS animations, SVG SMIL, vanilla JS |
| **medium** | Canvas 2D, GSAP, Lottie, anime.js |
| **heavy** | Three.js, custom GLSL shaders, Pixi.js, WebGL |

### Background effects
- `"none"` → skip
- `"gradient-animation"` → CSS @keyframes on linear/conic-gradient
- `"noise-field"` → Canvas 2D with Perlin/simplex noise
- `"mesh-gradient"` → SVG or canvas interpolation
- `"generative-art"` → Canvas 2D or WebGL

### Particle systems
- count < 100, no complex physics → vanilla JS + Canvas 2D
- count >= 100 or complex interaction → Pixi.js or Three.js Points
- Map `interaction` ("mouse-repel", "mouse-attract") to pointer event handlers
- Use `requestAnimationFrame`; include cleanup

### 3D elements
- Default to Three.js
- Apply lighting, camera, materials from params
- Handle resize with ResizeObserver
- CDN: `https://cdn.jsdelivr.net/npm/three@latest/build/three.module.js`

### Scroll effects
- Parallax: `transform: translateY()` × scroll offset × layer speed
- Scroll-triggered: `IntersectionObserver` with threshold array
- Scrubbed: animation progress = scroll progress

### Text effects
- `"split-letter-animate"` → split into `<span>` per char/word, stagger CSS
- `"typewriter"` → CSS `steps()` or JS interval
- `"glitch"` → layered clip-path + colour offset animation
- `"gradient-fill"` → `background-clip: text` with animated gradient

## Output Quality Checklist

Before delivering:
- [ ] Does it actually look like the reference?
- [ ] All design tokens applied (not just some)?
- [ ] Self-contained — no external dependencies that could break?
- [ ] Visual effects degrade gracefully without JS?
- [ ] `no-slop-ui` rules respected — no AI defaults slipping in?

## Pairing with no-slop-ui

Always apply `no-slop-ui` rules alongside DNA generation:
- DNA says WHAT the design IS
- `no-slop-ui` prevents AI defaults overriding it
- If DNA says `border_radius.large: 4px` — honour that, don't round everything to 20px
