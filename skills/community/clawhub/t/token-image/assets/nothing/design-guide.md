# Nothing — Design Guide

## Key Principles
1. Monochromatic hierarchy: `textDisplay` → `text` → `textSecondary`. Gray scale carries all hierarchy. Never introduce new gray values.
2. Accent red is an **interrupt only** — one red element per image max. Never decorative, never part of the typographic hierarchy.
3. Max 2 fonts, 3 sizes, 2 weights per image. Numbers always use mono.
4. One moment of surprise per image — an unexpected placement, an oversized glyph, a deliberate void.
5. Confidence through emptiness. White (black) space is part of the design. Never use even spacing across the whole image.

## Stylesheet Overrides

```css
/* Nothing uses the default styles as-is — no overrides needed */
```

## Decoration Palette
- **Dot-grid**: `radial-gradient(circle, ${tokens.color.border} 1px, transparent 1px)` with `backgroundSize: "16px 16px"`. Use `tokens.opacity.subtle`.
- **Geometric shapes**: Circles, rectangles, lines using `border` + `tokens.color.border`. Keep shapes simple.
- **Surface cards**: `tokens.color.surface` background + `tokens.opacity.subtle` for layered depth.
