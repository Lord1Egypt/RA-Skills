# Claymorphism — Design Guide

## Key Principles
1. Double shadows create depth — inner shadow + outer shadow on every card. Elements feel pressable, tactile.
2. Rounded everything — minimum 16px border-radius. No sharp corners anywhere.
3. Thick borders (3-4px) on interactive elements. Pastel colors only — no dark or moody tones.
4. Nunito Black (900) for headings only — never use Nunito for body text (too decorative at small sizes).
5. Playful asymmetry — slightly rotated elements, varied sizes, cards on cards for layered depth.

## Stylesheet Overrides
Applied AFTER default-styles.css. Add these rules to the set's styles.css:

```css
.card {
  border-radius: var(--radius-lg);
  border: 3px solid var(--color-border);
  box-shadow: inset -2px -2px 8px rgba(0,0,0,0.1), 4px 4px 8px rgba(0,0,0,0.15);
}

h1, h2, .display {
  font-weight: 900;
}
```

## Decoration Palette
- **Double shadows**: `box-shadow: inset -2px -2px 8px rgba(0,0,0,0.1), 4px 4px 8px rgba(0,0,0,0.15)` on cards.
- **Thick borders**: `border: 3px solid ${tokens.color.border}` on interactive elements.
- **Soft bounce**: `transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1)` for hover/press effects.
- **Pastel backgrounds**: Use `tokens.color.surface` for card backgrounds, `tokens.color.bg` for the viewport.
