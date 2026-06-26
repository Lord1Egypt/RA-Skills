# Bauhaus — Design Guide

## Key Principles
1. Strict geometry — every shape is a circle, square, or triangle. No organic forms.
2. Hard offset shadows only — `box-shadow: 4px 4px 0px 0px #121212`. Never blurred shadows.
3. Primary colors for section blocks (red #D02020, blue #1040C0, yellow #F0C020) — used sparingly for large areas, never for text.
4. Thick black borders on everything — minimum 2px, preferably 3px. Structure is visible and celebrated.
5. Outfit Black (900) uppercase for ALL display text. Aggressive scale contrast: hero text 4-5x body size.

## Stylesheet Overrides

```css
.card {
  border-radius: 0;
  border: 3px solid var(--color-border);
  box-shadow: 4px 4px 0px 0px var(--color-border);
}

h1, h2, .display {
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}
```

## Decoration Palette
- **Hard offset shadows**: `box-shadow: 4px 4px 0px 0px ${tokens.color.border}` on cards and key elements.
- **Primary color blocks**: Red, blue, yellow as `backgroundColor` for large section areas.
- **Dot grid**: `radial-gradient(circle, #ccc 1px, transparent 1px)` with `backgroundSize: "16px 16px"`.
- **Rotated stickers**: Elements rotated at -12deg or +12deg for dynamic composition.
- **Geometric shapes**: Circles, squares, triangles using `border` + `backgroundColor` with primary colors.
