# Surfaces — one palette, many media

Every recipe below consumes the token file. If a surface needs a value the tokens don't carry, add
the token in the engine — never compute it in the surface.

---

## Web / frontend / UI-UX

```bash
python3 token_engine.py --theme warm-cobalt --emit css --out build/
```

```html
<html data-theme="warm-cobalt" data-plate="day">
```

```css
body { background: var(--surface); color: var(--ink2); font-family: 'Archivo', system-ui, sans-serif; }
h1   { color: var(--ink); font-family: 'Bodoni Moda', serif; letter-spacing: -.02em; }
.rule{ border-top: 1px solid var(--rule); }
.btn { background: var(--accent); color: var(--onAccent); border-radius: 0; }
.caption { color: var(--muted); font-family: 'JetBrains Mono', monospace;
           font-size: 10.5px; letter-spacing: .16em; text-transform: uppercase; }
```

Rules that make a page read as designed rather than decorated: **three type roles** (display, body,
mono caption), **hairline rules** instead of cards, **one accent per view**, and a real type scale
(`clamp()` from 12 → 142 px). Screenshot at 1440 / 900 / 390 before saying it is done.

### Design tokens / component library

```bash
python3 token_engine.py --theme warm-cobalt --emit json --out build/
```

The JSON is the interchange format: map it to Tailwind (`theme.extend.colors`), Figma variables
(`{name, type: COLOR, value}`), or SCSS maps. Keep the *semantic* names (`accent`, `accentInk`,
`muted`) — never export `blue500`; a palette without roles cannot survive a second palette.

---

## Documents & PDF

A document theme is type scale, leading, rule weight and margins as much as colour.

```python
import json
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

t = json.load(open("build/warm-cobalt.tokens.json"))["plates"]["day"]
hex2rgb = lambda h: RGBColor.from_string(h.lstrip("#"))

doc = Document()
style = doc.styles["Normal"]
style.font.name, style.font.size = "Georgia", Pt(10.5)
style.font.color.rgb = hex2rgb(t["ink2"])
style.paragraph_format.line_spacing = 1.35

h1 = doc.styles["Heading 1"]
h1.font.name, h1.font.size = "Bodoni MT", Pt(24)
h1.font.color.rgb = hex2rgb(t["ink"])
```

For HTML→PDF (WeasyPrint / Chromium print) use the CSS emitter directly and set
`@page { margin: 28mm; background: var(--surface) }`.

**Structural rules for documents:** one display face for headings, one body face, mono only for
filenames/code/plate captions; 1px rules between sections; 28–32 mm margins; captions 8–9 pt with
`0.1em` tracking.

---

## LaTeX

```bash
python3 token_engine.py --theme warm-cobalt --emit latex --out .   # -> marble-warm-cobalt.sty
```

```latex
\documentclass[11pt]{article}
\usepackage[margin=28mm]{geometry}
\usepackage{marble-warm-cobalt}

\begin{document}
{\Huge\bfseries\color{themeBody} Title}\\[2pt]
\themeFieldRule\hfill{\footnotesize\color{themeCaption}PLATE 01}\\[6pt]
\themeHairline

\section*{A section}\color{themeBodySoft}
Body copy. \themeFieldText{a field link}, \themeRegisterText{a register mark},
\themeCode{inline code}, and \themeHairline\ between sections.
\end{document}
```

Provided macros: `\themeName`, `\themeFieldRule`, `\themeHairline`, `\themeFieldText{}`,
`\themeRegisterText{}`, `\themeCode{}`. Colour aliases: `themeBody`, `themeBodySoft`, `themeCaption`,
`themeRule`, `themePanel`, `themeField`, `themeFieldInk`, `themeRegister`.

Verify with an actual compile — `pdflatex -interaction=nonstopmode -halt-on-error sample.tex` — and
look at the PDF. Undefined colours and a package/file name mismatch are the two usual failures.

---

## VS Code

```bash
python3 token_engine.py --theme board-hivis --emit vscode --out build/
# install: ~/.vscode/extensions/<name>/package.json + the theme JSON
```

```json
{
  "name": "marble",
  "contributes": { "themes": [{ "label": "Marble Blackboard", "uiTheme": "vs-dark",
                                "path": "./themes/marble-board-hivis.json" }] },
  "engines": { "vscode": "^1.70.0" }
}
```

A complete theme means **all** of: `editor.*`, `activityBar.*`, `sideBar.*`, `list.*`, `statusBar.*`,
`titleBar.*`, `tabs.*`/`tab.*`, `panel.*`, `input.*`, `button.*`, `badge.*`, `terminal.background`,
**16 `terminal.ansi*` colours**, `tokenColors` (18 scopes: comment, string, number, keyword,
function, type, variable, escape, operator, punctuation, tag, attribute, invalid, markup.*) and
`semanticTokenColors`. Half a workbench reads as a half-finished theme.

Verify: `python -m json.tool theme.json`, then load it in the Extension Development Host (F5) and
look at a real file — code, a diff, and a terminal.

---

## Terminal / CLI

The engine's `ansi_map()` is the 16-colour set (normal + bright). Rules: keep `black` close to the
surface and `white` close to the ink; derive `cyan` as the mix of accent and secondary; make
`brightBlack` the muted token so comments stay readable.

---

## Agent / app skins (Hermes, Electron, TUI)

```bash
python3 token_engine.py --theme warm-cobalt --emit skin --out build/   # -> build/warm-cobalt.yaml
# copy to $HERMES_HOME/skins/ then:
hermes config set display.skin warm-cobalt
```

A Hermes skin needs `name`, `description`, `colors` (background, ui_accent, ui_tool, banner_title,
banner_text, ui_text, banner_dim, ui_border, ui_ok/warn/error, status_bar_*, completion_menu_*,
selection_bg), optional `branding`, and optional `customCSS` (capped at 32 KiB, scoped by
`[data-hermes-theme="<name>"]`). Apply it yourself with `hermes config set` — the watcher repaints
every surface in about a second.

For Electron/TUI hosts without skins: emit CSS variables and set them on `:root`; for a JSON-driven
host, emit the token JSON and map keys in one adapter file.

---

## Slides

Same tokens, plus a scale: title 40 pt, section 28 pt, body 18 pt, caption 10 pt. Slides are read at
distance — push the field ink into titles and headings, keep body copy in `ink2`, and never put
accent-coloured text on an accent panel (use `onAccent`).
