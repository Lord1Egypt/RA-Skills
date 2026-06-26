---
name: svg-cover-generator
description: Create polished, editable SVG cover artwork for reports, articles, slide decks, social cards, ebook covers, posters, and landing-page hero images. Use when a user asks for an SVG cover, vector poster, social preview graphic, title card, thumbnail-style artwork, or branded cover image that should remain text-editable and easy to customize.
---

# SVG Cover Generator

Generate one self-contained SVG cover that is visually intentional, easy to edit, and ready to save as `.svg`.

## Quick Flow

1. Confirm the target format, dimensions, text content, and mood.
2. Read [design-rules.md](references/design-rules.md) and [layout-recipes.md](references/layout-recipes.md) before composing.
3. Pick one layout recipe that matches the brief.
4. Write a complete SVG with inline styles and no external dependencies.
5. Validate the SVG structure before finishing.

## Intake

If the user already gave a clear brief, do not over-question. Otherwise collect the minimum missing inputs:

- Title
- Optional subtitle or byline
- Intended use: report cover, social card, slide cover, poster, hero image
- Canvas size or aspect ratio
- Brand colors or visual mood
- Whether the output should feel corporate, editorial, playful, technical, minimal, or bold

Reasonable defaults:

- Use `1600x900` for general landscape covers.
- Use `1080x1350` for portrait social-style covers.
- Use `1080x1080` for square covers.
- Use a clean sans-serif fallback stack inside the SVG unless the user provided a font direction.

## Composition Rules

- Prefer bold typography and a small number of strong shapes over busy illustration.
- Keep the title as the dominant element.
- Use 2-4 colors unless the brief asks for a richer palette.
- Use gradients, grids, bands, masks, or geometric clusters to create atmosphere.
- Keep all text editable as `<text>` unless the user explicitly asks for paths.
- Avoid embedded raster images unless the user explicitly provides one and wants it included.

## Build Procedure

### 1. Choose a layout

Select a layout from [layout-recipes.md](references/layout-recipes.md) that fits the brief.

### 2. Build the SVG

Always produce:

- An `<svg>` root with `xmlns`, `width`, `height`, and `viewBox`
- A background layer
- A content layer for title and supporting text
- One visual motif layer such as lines, circles, blocks, mesh-like gradients, or abstract geometry

Keep styles inline in a `<style>` block or on elements. Do not rely on external CSS, web fonts, or remote assets.

### 3. Make the output usable

- Escape XML-sensitive characters in text.
- Keep the hierarchy readable with grouping and brief comments when helpful.
- Ensure contrast is strong enough for the title to remain legible.
- Leave comfortable margins so text does not touch the canvas edge.

## Validation

Before finishing, check:

- The file is valid XML-style SVG.
- `viewBox` matches the intended composition size.
- Required text from the brief is present.
- There are no external asset references.
- The artwork is self-contained and editable.

If the SVG is saved to a file, run:

```bash
python3 scripts/check_svg.py /path/to/file.svg
```

## Output

When the user asked for the SVG itself, return the full SVG in a fenced `svg` block.

When the user asked for a file, write the SVG to the requested path and summarize:

- dimensions
- chosen layout
- palette
- validation result

## Resources

- Use [design-rules.md](references/design-rules.md) for visual and technical rules.
- Use [layout-recipes.md](references/layout-recipes.md) for composition choices.
- Use `assets/templates/` as starting points when a blank canvas would slow things down.
- Use `scripts/check_svg.py` to catch structural mistakes before handing off the file.
