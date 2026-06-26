# Retro-Futurism — Design Guide

## Key Principles
1. Neon glow is the signature — display text glows with `text-shadow` using cyan or pink. Every headline should feel like a neon sign.
2. Dark and moody — deep purple backgrounds, neon-lit panels. No pastels, no muted tones.
3. Angular and geometric — no rounded corners, no organic shapes. Think Tron grid lines and HUD displays.
4. Dense clusters with voids between — tight groupings of info, generous section gaps, like a control panel.
5. Hot pink is the interrupt — cyan is the default glow, pink breaks through for emphasis.

## Stylesheet Overrides

```css
.card {
  border-radius: 0;
  border: 1px solid var(--color-border);
  background: rgba(139, 92, 246, 0.08);
}

h1, h2, .display {
  text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF;
}

.metadata {
  text-shadow: 0 0 5px currentColor;
}
```

## Decoration Palette
- **Neon glow**: `text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF` on display text.
- **CRT scanlines**: `backgroundImage: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px)`.
- **Grid lines**: `border: 1px solid ${tokens.color.border}` creating visible grid structure.
- **Hot pink accent**: `tokens.color.accent` for CTAs, underlines, and interrupt elements.
