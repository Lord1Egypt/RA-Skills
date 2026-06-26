You are writing a React component for a social/marketing image.

**Read these files:**
- `.token-image/src/token.active.json` — design tokens
- `.token-image/src/viewport.tsx` — shared Viewport (import and wrap your content)
- `.token-image/src/styles.css` — stylesheet with all available CSS classes (import for typography/layout/card/grid styles)
- `<skill_base_dir>/references/components.md` — component patterns (copy what you need)
- `<skill_base_dir>/assets/<preset>/design-guide.md` — design principles (preset: {preset_name})

FORMAT: {name} — {width}px × {height}px

CONTENT BRIEF:
{content_brief}

LAYOUT: {layout_description}

CREATIVE DIRECTION: {creative_direction}

## Your Job

1. Import Viewport from "./viewport" and the stylesheet from "./styles.css"
2. Read `styles.css` — it contains all CSS classes available for this set. Use them for layout and styling.
3. Implement the layout described in the LAYOUT field using CSS classes from `styles.css`
4. Use semantic HTML (h1, h2, h3, p, ul, ol) — the stylesheet handles typography and heading spacing
5. Use inline styles only for one-off positioning or tweaks not covered by CSS classes
6. Follow the creative direction for placement, density, and visual feel

## Layout Implementation

The LAYOUT field describes the arrangement (e.g., "split — title left, 2x2 cards right" or "title above, 3-column grid below" or "hero full canvas"). Implement it using CSS classes from `styles.css`.

Common CSS classes you'll find in `styles.css`:
- `.split`, `.split-60-40`, `.split-40-60` — two-column layouts
- `.content-stack` — vertical stack with gap (title above content)
- `.content-row` — horizontal strip of items
- `.grid-2`, `.grid-3` — card grids (from base stylesheet)
- `.numbered-list`, `.numbered-item`, `.numbered-num` — numbered items
- `.card`, `.card-label`, `.card-content` — card components
- `.display`, `.metadata` — typography utilities

Check `styles.css` for the actual classes available in this set — the shared agent may have created additional ones.

If the layout description doesn't work for the content, use your judgment. Better a good layout that deviates from the description than a bad one that follows it literally.

## RULES

- Signature: `export default function Component({ tokens }: { tokens: Record<string, any> })`
- First line: `// @size {width}x{height}` — read by the render pipeline for dimensions.
- Default export required.
- Bake content from brief as constants at the top:
  ```
  const TITLE = "{exact title from brief}"
  const SUBTITLE = "{exact subtitle from brief}"
  ```
- Wrap all content in Viewport: `<Viewport tokens={tokens} variant="...">`
- Use EXACT text strings from the brief — no modifications, rewording, truncation, or additions.
- Every spacing and opacity value must come from tokens (e.g. `tokens.spacing.md`, `tokens.opacity.subtle`).
- Never import token files directly. Acceptable to hardcode: SVG path data, aspect ratio math, transform calculations.
- **No standalone decorative elements** (dots, shapes, circles, lines) unless the creative direction explicitly requests them. Background patterns applied to container divs are fine.
- **All spacing between elements is handled by flex/grid gap** — the viewport inner div, `.content-stack`, `.numbered-list`, etc. all use `gap`. Headings have `margin: 0`. Do not add `margin-top` or `margin-bottom` to headings.
- **Prefer multiple direct children inside Viewport** — headings, layout blocks, and metadata should be separate children so the viewport's built-in gap handles spacing. Do NOT wrap everything in a single `<div>` — that collapses the viewport gap to zero. If a single wrapper div is truly needed for layout reasons, it MUST replicate the viewport inner wrapper's flex behavior: `flex`, `flexDirection`, `justifyContent`, `alignItems` and etc.
- **Grid containers** (`grid-2`, `grid-3`) include `width: 100%` in the stylesheet. No need to add inline width.

Write the file directly to disk: `.token-image/src/<format>-<index>.tsx`
