# Glassmorphism — Design Guide

## Key Principles
1. Layered depth — stack translucent surfaces at different z-depths. Every panel floats over a vibrant gradient background.
2. Frosted glass — all panels use `backdrop-filter: blur(10-20px)` with translucent white backgrounds (10-30% opacity).
3. Rounded everything — no sharp corners. All elements use `radius` tokens.
4. Text never sits directly on gradient — always has a glass panel behind it.
5. Generous gaps between panels (`lg`–`2xl`), tight padding within (`xs`–`sm`).

## Stylesheet Overrides

```css
.card {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

h1, h2 {
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.15);
}
```

## Decoration Palette
- **Gradient background**: Deep blue → electric blue → purple. Apply to Viewport root container.
- **Glass panels**: Translucent white with `backdrop-filter: blur(16px)` and subtle white border.
- **Accent glow**: Soft radial gradient or `box-shadow` around accent-colored elements.
- **Layered surfaces**: Stack 2-3 glass panels at different opacities for parallax depth.
