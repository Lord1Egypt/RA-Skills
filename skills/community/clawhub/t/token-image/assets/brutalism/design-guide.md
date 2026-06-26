# Brutalism — Design Guide

## Key Principles
1. Visible structure — thick black borders (2-4px) define every section. If something is a grid, show the grid lines.
2. No softness — zero border-radius, no shadows, no gradients, no blur, no opacity fades. Sharp geometry only.
3. Asymmetric and tense — elements can break boundaries, bleed past container edges, overlap. One moment of tension per image.
4. Red is structural, not decorative — use as full blocks, thick underlines, or single-word highlights. Never as background wash.
5. Contrast through scale — pair oversized hero text with tiny metadata for maximum impact.

## Stylesheet Overrides

```css
.card {
  border-radius: 0;
  border: 3px solid var(--color-border);
  background: transparent;
}

.grid-2, .grid-3 {
  gap: var(--spacing-sm);
}

.metadata {
  font-weight: var(--font-weight-bold);
}
```

## Decoration Palette
- **Thick borders**: `border: 3px solid ${tokens.color.border}` on containers, sections, cards.
- **Grid lines**: Visible structural lines using border or background-image patterns.
- **Diagonal cuts**: Rotated elements at max 15° for tension.
- **Red blocks**: `tokens.color.accent` as full background blocks or thick underlines.
