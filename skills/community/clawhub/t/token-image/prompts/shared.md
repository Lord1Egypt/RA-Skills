You are creating two shared files for a set of social/marketing images: a Viewport component and a complete stylesheet.

You are the **layout architect** for this set. You read the full content plan (all layout descriptions for every image) and create a stylesheet with every CSS class the components will need.

**Before you begin, read these files:**
- `.token-image/src/token.active.json` — design tokens
- `<skill_base_dir>/references/viewports.md` — viewport examples (pick one and customize)
- `<skill_base_dir>/references/default-styles.css` — base stylesheet (start from this)
- `<skill_base_dir>/references/components.md` — layout pattern reference (CSS + TSX pairs)
- `<skill_base_dir>/assets/<preset>/design-guide.md` — design philosophy (preset: {preset_name})

FORMAT: {name} — {width}px × {height}px

CONTENT PLAN FOR THIS SET:
{content_plan}

## FILE 1: Viewport (viewport.tsx)

1. Pick the viewport example from `viewports.md` that best matches the set's needs
2. Set alignment following the guidance in `viewports.md` — standard defaults to `alignItems: "stretch"`, hero picks from the 4 documented options
3. The inner content div must include `gap: tokens.spacing.md` — this provides consistent vertical spacing between all direct children
4. The inner content div needs padding adjacent to branding elements: `paddingTop: tokens.spacing.md` when branding sits above, `paddingBottom: tokens.spacing.md` when branding sits below. No padding on sides without branding.
5. Add branding elements if the content plan requires them (series labels, logos, decorative bars)
6. Set background pattern for hero variant based on the design guide. Apply opacity via the pattern itself — do NOT apply `opacity` to the root container
7. Adjust outer padding if needed (square formats may need more padding)

Component signature:
```tsx
export default function Viewport({ tokens, children, variant = "standard" }: { tokens: Record<string, any>; children: React.ReactNode; variant?: "standard" | "hero" })
```

First line: `// @viewport {width}x{height}`

## FILE 2: Stylesheet (styles.css)

You are the layout architect. Read the content plan above — it contains layout descriptions for every image in the set. Create CSS classes for every layout pattern the images need.

### How to build styles.css

1. **Start with `default-styles.css`** — copy it verbatim as the base. It provides typography (h1-h4, p, code, blockquote), utility classes (.display, .metadata), cards (.card, .card-label, .card-content), and grids (.grid-2, .grid-3).

2. **Add preset overrides** — from the design guide's "Stylesheet Overrides" section. Place these AFTER the default styles.

3. **Create layout classes** — read the content plan's layout descriptions and create CSS classes for each layout pattern needed. Reference `components.md` for the CSS + TSX pattern pairs. Common patterns:
   - `.split`, `.split-60-40`, `.split-40-60` — two-column layouts (if any image uses a split layout)
   - `.content-stack` — vertical stack with gap (if any image has title above content)
   - `.content-row` — horizontal strip (if any image has a row of items)
   - `.numbered-list`, `.numbered-item`, `.numbered-num` — numbered items (if any image uses numbered list)
   - Any custom classes the layouts require

4. **Add an available-classes comment at the top** — after any existing comment blocks, list all layout CSS classes you created. This tells writers what's available:
   ```css
   /* === AVAILABLE LAYOUT CLASSES ===
    * .split            — equal two-column
    * .split-60-40      — 60/40 two-column
    * .content-stack    — vertical stack with gap
    * .numbered-list    — numbered items container
    * .numbered-item    — single numbered item
    * .numbered-num     — number element
    * ================================= */
   ```

5. **All values must reference token CSS vars** (e.g., `var(--font-size-h1)`, `var(--color-surface)`). No hardcoded pixel/color values except in special cases (SVG patterns, border widths).

### Rules
- This is a CSS file — no React, no inline styles
- Every value references token CSS vars where possible
- Layout classes go AFTER the base styles and preset overrides
- Only create CSS classes that the content plan actually needs — no speculative utilities
- Headings have built-in bottom margin (h1: spacing-md, h2: spacing-md, h3: spacing-sm, h4: spacing-sm) — do not override these in layout classes

---

Write both files directly to disk:
- `.token-image/src/viewport.tsx`
- `.token-image/src/styles.css`
