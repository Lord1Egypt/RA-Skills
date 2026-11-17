---
name: theme-engine
description: "Use when one palette must theme any surface."
version: 1.0.0
author: Sakib Dalal, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [theme, design-system, tokens, palette, vscode, latex, pdf, web, ui, ux, agents, frontend, contrast, accessibility]
    related_skills: [halftone-art, popular-web-designs, color-sense, latex-reports, docx, xlsx]
---

# Theme engine — one palette, every surface

A theme is not a colour picker. It is **two libraries composed into tokens, then re-expressed per
surface**: the same inks paint a web page, a PDF, a LaTeX document, a VS Code window, a terminal
and an agent's chat UI.

This skill is the whole pipeline: reference → libraries → contrast-gated tokens → surface emitters.

## When to Use

Any request of the form “make it look like X” where X is an image, a brand, a poster or a mood:

- **Web / frontend / UI-UX** — landing pages, docs sites, dashboards, component kits, design systems.
- **Documents & PDF** — reports, briefs, one-pagers, course work, invoices (Word, PDF, HTML→PDF).
- **LaTeX** — reports, papers, posters, slides (colour + type packages).
- **Editor / code** — VS Code themes, syntax palettes, terminal ANSI, diffs.
- **Agents & apps** — Hermes skins, Electron/TUI themes, any host with CSS variables or a theme JSON.
- **Brand kit / token export** — JSON, CSS, SCSS, Tailwind config, Figma variables.

**Don't use for** a one-off colour tweak on an existing theme (change the one token instead), or for
raw image generation.

## The model (learn this before touching a surface)

```
GROUNDS (stocks/surfaces)  ×  INKS (accent pairs)  →  derive()  →  tokens  →  surface emitters
```

1. **Grounds** are what the eye reads as *which* theme it is: warm paper, newsprint, bone, cool grey,
   kraft, blush, sage, graphite — and dark boards for the loud families. A ground carries the stock
   colour and its press black.
2. **Inks** come in families, and the family sets intent:
   - `riso` — muted, register-based print inks (Cobalt & Rose, Vermilion & Slate…)
   - `vivid` — high-chroma, everyday stand-out (Vivid Magenta, Electric Blue, Ultraviolet)
   - `hi-vis` — fluorescent / safety, engineered to grab attention (Hi-Vis Yellow, Laser Green)
   - `accent` — one loud colour, everything else quiet (Signal Orange)
3. **One derivation, two polarities.** Light surfaces get dark type and *darkened* inks; dark
   surfaces get cream type and *lifted* inks. Never write two derivations.
4. **Contrast is an output, not an opinion.** Every pairing is measured at build time and the build
   fails loudly under 4.5:1 (small text) / 3:1 (fills and large type).
5. **Surface emitters consume tokens — they never re-derive.** If a surface needs a value the tokens
   don't carry, add the token; do not fork the maths.

Full maths, the CLI, and the uniqueness/assignment scheme: `references/engine.md`.

## Procedure

1. **Read the reference.** Histogram it for the real inks — never eyeball. *Done when* you can name
   stock, 1–2 inks, the darkest ink, and their pixel shares.
2. **Declare the libraries** in one script (grounds × inks). Keep them declarative; derivation lives
   in one function. *Done when* `--list` shows the grid and every theme has both plates.
3. **Derive and gate.** Run the build; read the ratio table it prints. Fix nothing by hand — adjust
   an ink or accept the walk's correction. *Done when* “text pairings under AA: none”.
4. **Emit per surface.** `templates/token_engine.py --emit css|vscode|latex|json|skin`. One engine,
   one palette, many outputs. Recipes: `references/surfaces.md`.
5. **Apply and look.** Apply to the real host (skin, VS Code window, compiled PDF, browser), then
   screenshot/compile and inspect. *Done when* you have looked at the artefact, not the code.
6. **Write it back** with the generated tokens as the source of truth, and record the palette in the
   README.

## Surface routing

| surface | emitter / recipe | artefact to verify |
|---|---|---|
| Web page / landing / UI kit | CSS custom properties on `:root` | screenshot at 1440 / 900 / 390 |
| Component library / design system | token JSON → CSS + Tailwind config | component page in all states |
| Document / report (docx, PDF) | token JSON → style map (fonts, scale, colours, rules) | exported PDF, page 1 + table page |
| LaTeX (report, paper, poster) | generated `.sty` with `xcolor` definitions | `pdflatex` compiles, PDF inspected |
| VS Code | theme JSON (workbench + tokenColors + terminal ANSI) | JSON parses; theme loads |
| Terminal / CLI | ANSI 16-colour map | legible on both light and dark |
| Agent / app skin | skin YAML / CSS variables | app repaints; palette resolves |
| Slides | display + body + code styles | PDF export inspected |

Per-surface code, key names and gotchas: `references/surfaces.md`.

## Core rules that survive every surface

- **Never `#000` on `#fff`.** Warm stock `#F2EEE2`–`#FDF3E3`, ink `#12100E`–`#1D1D1D`.
- **Two text-safe variants per accent**: the raw ink is a fill; the walked ink carries small type.
- **Three type roles, no more**: display (high contrast, tight tracking), body (quiet grotesque),
  caption/mono. Body copy never in a display face.
- **Hairlines and flat fields beat cards.** 1px rules, 1.5px for structural breaks, `border-radius: 0`
  unless the host demands otherwise.
- **One accent does the pointing; everything else recedes.** If three things shout, nothing does.
- **Dark surfaces need lifted accents** — a saturated field ink is usually 2–3:1 on near-black.
- **Size display type by the longest word in the set**, or one variant will wrap.
- **Contrast, then taste.** A palette that fails AA is not a theme, it is a complaint waiting.

## Pitfalls

1. **Eyeballing hexes from a photo.** Histogram it; photographs carry JPEG drift, gradients and
   antialiased edges. Keep the flat-field colours only.
2. **Two derivations (light and dark).** They drift within a week. One function, a polarity flag.
3. **Hi-vis used as text on paper.** `#D6FF00` on stock is ~1.3:1 — a fill, or a type colour on a
   dark board only. Split fill/text tokens and let the walk decide.
4. **VS Code themes that only set `editor.*`.** An unstyled sidebar, tabs, status bar and terminal
   ANSI reads as half-finished. Emit the full workbench set.
5. **LaTeX colours defined without `xcolor`.** Load `xcolor` (with the options you need) before
   `\definecolor`, and keep `\colorlet` aliases for semantic names.
6. **Document themes that only change colour.** A document theme is type scale, leading, rule weight
   and margins as much as hue; ship those tokens too.
7. **Font weight *ranges* from Google Fonts.** `wght@0,400;0,600;0,700` returns the variable file
   (larger, and double-paints in some Chromium builds at display size). Pin the faces you use.
8. **Rotated texture overlays** need `inset: -40%` before rotation, or corners go empty.
9. **Headless screenshots can drop canvas layers** — flatten canvases to CSS backgrounds first.
10. **Deriving per-surface.** The moment a surface computes its own tints, the palette forks. Emit.

## Files

```
SKILL.md
templates/token_engine.py     grounds × inks → tokens; --emit css|vscode|latex|json|skin
references/engine.md          the maths, the CLI, uniqueness/assignment, contrast gates
references/surfaces.md        per-surface emitters: web, docs/PDF, LaTeX, VS Code, terminal, agents
references/editorial-print.md print/editorial composition grammar (dot type, specimen sheets)
```

Worked example, complete and verified: `~/Downloads/JACKAL_THEME_ENGINE` — 150-theme marble engine,
live specimen sheet, previews. Read `preview/*.png` before starting.

## Verification

- `token_engine.py --list` → the full grid; `--report` → “text pairings under AA: none”.
- `--emit vscode` → JSON parses (`python -m json.tool`), keys are real VS Code keys, terminal ANSI
  has 16 entries.
- `--emit latex` → `pdflatex` compiles a two-page sample with no undefined-colour warnings.
- `--emit css` → variables resolve; the page renders at 1440 / 900 / 390 without overflow.
- Host app: theme resolves by name, palettes match the tokens, custom CSS under the host cap.
- Look at the artefact: a screenshot, a compiled PDF, a running window. Code that “should work” is
  not verification.
