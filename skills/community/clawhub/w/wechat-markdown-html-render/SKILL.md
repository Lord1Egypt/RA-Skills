---
name: wechat-markdown-html-render
description: Render Markdown to polished HTML with WeChat-friendly typography and explicit theme layering. Use when users ask to convert Markdown articles to formatted HTML, replicate or analyze wechat.bmpi.dev theme behavior, or require text theme and code-block highlighting to be independently switchable.
---

# Wechat Markdown Html Render

## Overview

Render Markdown files into standalone HTML with separate style layers: `basic-theme`, `text-theme`, `code-theme`, and `font-theme`.
Use `scripts/render-markdown-html.js` to generate deterministic output and keep code-block visuals independent from text theme.

## Workflow

1. Inspect site-mechanism notes in `references/wechat-bmpi-analysis.md` when the request mentions `wechat.bmpi.dev`.
2. Install dependencies in the skill folder:

```bash
npm install
```

3. Render Markdown, you can pick a text-theme and code-theme and font-theme according to article contents:

```bash
node scripts/render-markdown-html.js \
  --input /path/to/input.md \
  --output /path/to/output.html \
  --text-theme geek-black \
  --code-theme wechat \
  --font serif
```

4. Validate that the output includes the four style blocks and that `--text-theme` and `--code-theme` can be changed independently.

## Script Interface

- `--input`: Markdown source file path (required)
- `--output`: HTML output file path (required)
- `--text-theme`: `normal | orange-heart | geek-black | minimal-dark | gold-sea` (optional, default `gold-sea`)
- `--code-theme`: `wechat | atomOneDark | atomOneLight | monokai | github | vs2015 | xcode` (optional, default `wechat`)
- `--font`: `serif | sans` (optional, default `serif`)
- `--title`: Custom HTML title (optional)
- `--custom-css-file`: CSS file used only when `--text-theme custom` (optional)

## Notes

- The script intentionally scopes markdown typography under `#nice` and syntax highlighting under `.hljs`/`pre code` selectors so code theme remains independent.
- The output is standalone HTML and can be copied into downstream editors.

## WeChat MP editor list normalization (built into the renderer)

The script applies two post-processing rules specifically to survive the WeChat 公众号 editor's non-standard HTML ingester. These are NOT optional — they're enabled for every render — but worth knowing when reviewing output or extending the script:

1. **Flatten `<li><section>…</section></li>` for leaf items.** The MP editor drops the list marker (the `1. 2. 3.` numbers, or `•` bullets) when a `<li>` contains a block-level child like `<section>`, and also inserts an extra blank row per item from the section's vertical margins. Fix: for `<li>` that does NOT contain a nested `<ul>`/`<ol>`, the renderer unwraps the inner section and merges its typographic styles directly onto the `<li>`. Items with nested sub-lists keep the section wrapper (their sub-list layout depends on it).

2. **Zero whitespace at `<ol>`/`<ul>` boundaries and between sibling `<li>`s.** The MP editor treats whitespace text nodes between `<li>` siblings (and at the start/end of a `<ul>`/`<ol>`) as additional EMPTY list items, producing numbered/bulleted blank rows interleaved with the real ones. Newline-only stripping is NOT enough — spaces and tabs leak through and still trigger the bug. The renderer collapses all whitespace at those three positions: `<ol>` → first `<li>`, `</li>` → next `<li>`, last `</li>` → `</ol>` (and the same for `<ul>`).

Symptoms in the MP editor preview when either rule fails:
- Rule 1 broken → no `1. 2. 3.` markers, items show as plain paragraphs separated by blank rows.
- Rule 2 broken → `1. (blank) / 2. real / 3. (blank) / 4. real / …` — count of visual rows ≈ `2N + 1` for `N` real items.

If you copy text out of the MP editor and the markers are missing, that's a clipboard artifact (markers are CSS `::marker` pseudo-elements, not text nodes) — verify in the editor's visual preview, not the copied text.
