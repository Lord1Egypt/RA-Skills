# Terminal — Design Guide

## Key Principles
1. JetBrains Mono for everything — display, body, and labels. Single monospace family. No sans-serif or serif.
2. Green-on-black is the ONLY color scheme — amber for warnings/accents only. No other colors.
3. Dense and precise — tight line height, minimal padding, maximum information density. Like a terminal buffer.
4. Every screen starts with a prompt prefix: `$`, `>`, or `~/path`. Content lives in bordered terminal windows.
5. Zero border-radius — all corners sharp. No shadows, no gradients, no soft elements.

## Stylesheet Overrides
Applied AFTER default-styles.css. Add these rules to the set's styles.css:

```css
h1, h2, h3, h4, p, .display, .metadata {
  font-family: var(--font-family-mono);
}

.card {
  border-radius: 0;
  border: 1px solid var(--color-accent);
  background: transparent;
}

.metadata {
  color: var(--color-text-secondary);
  opacity: 0.7;
}
```

## Decoration Palette
- **Terminal windows**: ASCII borders using `┌`, `─`, `│`, `└` characters in pre/code blocks.
- **Scanline overlay**: `backgroundImage: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)` at low opacity.
- **Prompt prefix**: `$` or `>` as a decorative element before titles or commands.
- **Progress bars**: Text-based `[#####-----] 50%` in code blocks.
- **Blinking cursor**: CSS animation on a key element (text-decoration: underline blink).
