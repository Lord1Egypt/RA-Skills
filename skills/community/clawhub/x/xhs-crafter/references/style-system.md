# Style System

Two visual modes for social card images. Pick by editorial intent, not by topic lookup.

## Shared Rules

- Content shape decides layout. Do not pick a pretty layout first and invent content to fit it.
- Use strong hierarchy: title, hook, evidence, caption, metadata.
- Use real images as evidence or atmosphere, not decoration.
- Avoid visible clutter: no random SVG circles, oval drops, blobs, bokeh, ornamental stickers, fake diagram decorations, or decorative gradients.
- Keep all pages in a package visually related through grid, typography, palette, and recurring metadata.
- Every page should have a clear focal point.

## Mode A: Editorial Magazine x E-ink

**Good fits**: outdoor, lifestyle, reflective, humanistic, cultural, narrative — but also workplace essays, AI think-pieces, product retrospectives, anything that wants a slow magazine-feature pace.

**Visual anchors**:
- Serif or Songti-like display title plus quiet sans-serif body text
- Warm paper, deep ink, refined greys, restrained color
- Procedural paper grain + ink wash atmosphere (especially on covers, dividers, pull quotes, and sparse pages)
- Documentary photography, field-note captions, issue labels, page numbers
- Large but purposeful whitespace
- Fine rules, magazine columns, image captions, pull quotes, and editorial contrast
- Subtle paper texture is allowed; it must not lower text readability

**Use one of the 6 magazine palettes** in `theme-presets.md`. Do not improvise arbitrary warm paper colors. Five palettes are light (paper-and-ink); one — **Midnight Ink** — is dark and is used as a **rhythm tool** within a light package, not as a standalone theme.

### Editorial Identity Test

A page passes the Editorial identity test when ALL of these are true:
1. At least one atmosphere layer beyond a flat fill (paper grain / ink wash / WebGL canvas)
2. Serif display family on the title (`.h-xl`, `.h-md`, `.pullquote` use `--serif-zh`)
3. At least one of: large photo well, serif pull quote, marginalia column, or true ledger structure

A flat paper with serif title + mono pills everywhere is **Swiss-in-disguise** — switch mode.

## Mode B: Swiss International

**Good fits**: product updates, release notes, system explainers, data reports, tool tutorials, engineering walkthroughs, competitive comparisons, any content that wants a clean, structured, data-forward pace.

**Visual anchors**:
- Sans-serif everything. Light weight (200-400) on display titles. No serif font loaded.
- White or near-white paper, deep ink, single accent color
- Hairline rules (1px), no card shadows, no rounded corners beyond 4px
- KPI towers, h-bar charts, stacked ledgers, matrix grids
- One accent color only. Used for: category labels, stat numbers, pipeline dots, active states
- No decorative atmosphere. Background is flat white/grey. No grain, no wash, no WebGL.

**Use one of the 4 Swiss palettes** in `theme-presets.md`. Do not mix accent colors.

### Swiss Identity Test

A page passes the Swiss identity test when ALL of these are true:
1. Every display title ≥72px uses a typed class with weight ≤300
2. No serif font is loaded in the page
3. Only one accent color is used throughout
4. No card shadows, no decorative gradients, no rounded corners >4px
5. Dividers are hairline rules (1px), not card borders or shadow separators

A bold 90px headline is **not Swiss**. A serif pull quote on a Swiss page is **not Swiss**.

## Style ↔ Content Type Are Decoupled

The two modes are **visual stances, not content categories**. Any topic can be rendered in either mode — what changes is the page's feel and which structural devices are available (ledger / marginalia / pull quote vs matrix / KPI tower / h-bar). Pick by editorial intent ("feature story" vs "release note" / "system explainer"), not by topic lookup.

## Anti-Patterns (Both Modes)

- Nested cards (card inside card)
- Excessive rounded corners (>8px)
- Random SVG blobs, ovals, drops, circles, stickers
- Decorative gradients with no relationship to content
- `mix-blend-mode: difference` for readability
- Full-canvas uniform dark overlay on images
- `img { opacity: .6 }` — kills photo depth
- Emoji as decorative elements in layout
