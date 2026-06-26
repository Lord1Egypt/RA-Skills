# Presentation Design Notes

This reference constrains `slidev-ppt-generator` to produce output that looks like a real, professionally designed presentation — not a text document with slide breaks.

## The #1 Rule

**If a slide has no background, no layout, and no visual structure, it is not a presentation slide — it is a text document.** Every slide must have intentional visual design.

## Goals

- Each slide conveys exactly one main conclusion
- Text should be concise and precise; no explanatory paragraphs
- Use backgrounds, grids, whitespace, and hierarchy to organize information
- Prioritize speakability over flashiness
- Content must never overflow beyond the screen edges

## Visual Hierarchy Rules

### Slide Types and Their Visual Treatment

| Slide Type | Must Have | Layout | Background |
|------------|-----------|--------|------------|
| Cover | Title, subtitle, author | `cover` | Unsplash photo (required) |
| Section divider | Chapter title | `section` or `cover` | Gradient or photo (required) |
| Content | One main point | `default`, `two-cols`, `image-right` | Optional |
| Data/Stats | Key number | `fact` | Optional gradient |
| Quote | Attribution | `quote` | Optional |
| Architecture | Components + flow | `default` with card grid | Optional |
| Closing | Thank you + contact | `cover` | Photo (required) |

### Background Image Strategy

- Pick 3-5 Unsplash photos that match the topic before writing any slides
- Use the same photo on cover and closing for visual bookending
- Section dividers can share a gradient or use a different photo from the set
- Content pages are OK without backgrounds — but never more than 3 consecutive plain pages
- For dark-background slides, add `class: text-white` to the frontmatter

### Color and Contrast

- Light theme (`colorSchema: light`): dark text on white/light backgrounds. Use `bg-gray-100`, `bg-blue-50` for card backgrounds.
- Dark theme (`colorSchema: dark`): light text on dark backgrounds. Use `bg-white/10`, `bg-gray-800` for card backgrounds.
- On photo backgrounds, the `cover` layout auto-adds a dark overlay. For other layouts on photos, manually add `class: text-white`.

## Core Rules

### 1. One Idea Per Slide

- Each slide has one central proposition
- If a slide covers "definition + architecture + value", split it
- Titles should read like conclusions: "Four layers make AI actually execute" not "System Overview"

### 2. Control Text Density

- Keep body text to ~2-3 short sentences or 3-5 bullet points per slide
- Each card in a grid: max 2-3 lines
- No more than 6 primary blocks per slide
- Lists over 5 items: split across pages or use a grid

### 3. Layout Variety

**Never use the same layout for more than 3 consecutive slides.** Alternate between:

- `default` (standard content)
- `two-cols` (comparison, code + explanation)
- `image-right` (text + visual, apple-basic theme)
- `fact` (big number or statement)
- `quote` (testimony or principle)
- `section` (chapter break)
- `statement` (big idea, minimal text)

A good 10-slide deck might use: cover → default → two-cols → section → fact → default → image-right → default → statement → cover(closing)

### 4. Whitespace First

- Reserve 8-10% safe margin on all sides
- Consistent spacing between cards (use `gap-4` or `gap-6`)
- Important content needs breathing room
- Never pad text to "fill the screen"

### 5. Card Grids Over Bullet Lists

When you have 3-6 items to present (features, components, benefits), use a card grid instead of bullets:

```html
<div class="grid grid-cols-2 gap-6 mt-8">
<div class="p-6 bg-gray-100 rounded-lg">
  <h3 class="font-bold mb-2">Title</h3>
  <p class="text-sm opacity-75">Description</p>
</div>
<!-- repeat -->
</div>
```

This immediately makes the slide look designed rather than drafted.

### 6. Architecture Without Mermaid

Mermaid does not render in PDF/PPTX export. For architecture diagrams, use:

**Option A: Component grid** — 3-column grid with colored cards showing Input → Core → Output

**Option B: Flow with arrows** — Styled divs with `→` characters between them

**Option C: ASCII in code block** — For very technical audiences only

### 7. Overflow Control

- Title over two lines: rewrite shorter, don't shrink font
- Two-column layouts: both columns roughly equal height
- Footnotes must not push content off screen
- Closing slides: don't combine big title + cards + footnotes + tagline

## Slidev-Specific Tips

- UnoCSS/Tailwind classes work directly in HTML: `class="grid grid-cols-2 gap-4 mt-8"`
- Use `<div class="abs-br m-6 text-sm opacity-50">` for bottom-right attribution
- Use `<br>` for spacing in `fact` layouts between numbers
- `v-click` works in preview but is flattened in PDF export — don't rely on it for content structure

## Post-Generation Checklist

1. Does cover have a background image? (must be yes)
2. Does closing page have a background? (must be yes)
3. Any plain-white section dividers? (fix: add gradient)
4. More than 3 consecutive bullet-list pages? (fix: insert visual layout)
5. Any Mermaid diagrams when targeting PDF? (fix: replace with card grid)
6. Any slide with more than 6 blocks? (fix: split)
7. Is there at least one fact/quote/statement page? (should be yes)
8. Do all Unsplash URLs use `?w=1920` suffix? (must be yes)

## Output Style

- Stable, professional, speakable
- Restrained but visually distinctive
- Looks like an experienced designer made it, not auto-generated
- Every slide has intentional layout choices, not just dumped text
