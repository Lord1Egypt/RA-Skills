# Aurora UI — Design Guide

## Key Principles
1. Always gradient atmosphere — never flat solid backgrounds. Flowing mesh gradients (blue→purple→pink→teal) cover every surface.
2. Content floats on translucent surface cards — nothing sits directly on the gradient.
3. Gradient direction should feel natural, like light — top-to-bottom or diagonal, never random.
4. Multiple gradient layers at different opacities for depth. Max 4 gradient colors.
5. Soft and luminous — no hard edges, no sharp corners, no static layouts.

## Stylesheet Overrides

```css
.card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

h1, h2 {
  background: linear-gradient(135deg, #ffffff, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## Decoration Palette
- **Mesh gradient background**: `conic-gradient(from 180deg, #0080FF, #8B00FF, #FF1493, #20B2AA, #0080FF)` on Viewport root.
- **Iridescent shimmer**: Gradient text on display elements using `background-clip: text`.
- **Soft glow**: `text-shadow: 0 0 20px rgba(167, 139, 250, 0.3)` on key text elements.
- **Translucent cards**: Surface background at 6% opacity + `backdrop-filter: blur(12px)`.
