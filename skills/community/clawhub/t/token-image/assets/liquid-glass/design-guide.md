# Liquid Glass — Design Guide

## Key Principles
1. Everything feels like liquid crystal — morphing shapes, translucent panels, iridescent accents.
2. Backdrop blur on every surface — `backdrop-filter: blur(20px) saturate(1.5)` with translucent backgrounds.
3. Iridescent gradients for accent elements — rainbow spectrum (max 5 colors) creates premium shimmer.
4. Morphing border-radius — containers use asymmetric radii like `30% 70% 70% 30% / 30% 30% 70% 70%`.
5. Chromatic aberration on key text — offset RGB channels create a holographic effect.

## Stylesheet Overrides
Applied AFTER default-styles.css. Add these rules to the set's styles.css:

```css
.card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px) saturate(1.5);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

h1, h2, .display {
  text-shadow: -1px 0 #FF006E, 1px 0 #00DDFF;
  letter-spacing: 0.02em;
}
```

## Decoration Palette
- **Iridescent gradient**: `linear-gradient(135deg, #FF006E, #8B00FF, #00DDFF, #00FF88, #FFD700)` for accent elements.
- **Glass surface**: `backdrop-filter: blur(20px) saturate(1.5)` + `background: tokens.color.surface` + subtle white border.
- **Chromatic aberration**: `textShadow: '-1px 0 #FF006E, 1px 0 #00DDFF'` on display text.
- **Morphing border-radius**: `borderRadius: '30% 70% 70% 30% / 30% 30% 70% 70%'` on container elements.
