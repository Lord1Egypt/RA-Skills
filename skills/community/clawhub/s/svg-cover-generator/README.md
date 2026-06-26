# SVG Cover Generator

Create polished, editable SVG cover artwork for reports, articles, slide decks, social cards, posters, ebook covers, and hero images.

This repository contains a Codex skill plus reusable SVG templates and validation tooling.

## What It Includes

- `SKILL.md`: The skill instructions Codex uses to generate SVG covers
- `references/design-rules.md`: Visual and technical design rules
- `references/layout-recipes.md`: Layout patterns for different cover styles
- `scripts/check_svg.py`: Structural validation for generated SVG files
- `assets/templates/`: Starter SVG templates for landscape and square formats

## Typical Use Cases

- Report cover
- Slide deck title page
- Social preview card
- Poster-style title artwork
- Game or app cover graphic
- Landing-page hero image

## Design Goals

- Self-contained SVG output
- Editable text layers
- Strong visual hierarchy
- Minimal external dependencies
- Fast customization for new titles and themes

## Example Prompt

Ask Codex for something like:

```text
Create an SVG cover for a technical AI report called "Agent Patterns".
Use a 1600x900 canvas, make it dark, modern, and structured.
```

Or:

```text
Generate a retro arcade-style SVG game cover for "坦克大战".
Make it bold, energetic, and readable as a thumbnail.
```

## Validate An SVG

```bash
python3 scripts/check_svg.py path/to/cover.svg
```

## Templates

Starter files live in:

- `assets/templates/landscape-cover.svg`
- `assets/templates/square-cover.svg`

Use them as a base when you want a faster first draft instead of composing from scratch.

## Repository Role

This repo is both:

- a usable Codex skill installed under `~/.codex/skills/svg-cover-generator`
- a standalone GitHub repository for iterating on the prompts, templates, and validator
