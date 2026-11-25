---
name: sketchy
description: "Creates hand-drawn pencil-sketchbook slides, charts, explainers, lessons, business reports, one-pagers, decision boards, postcards and short videos with generative music, as self-contained HTML that exports to PDF, PPTX and MP4. Use when someone wants a presentation, deck, slides, pitch, lesson, tutorial, explainer, chart, data story, report, one-pager, social card or explainer video in a hand-drawn, sketch, sketchnote, whiteboard, notebook or Excalidraw-like style, or names sketchy. Not for production web apps, dashboards with live data, or photo-real design."
license: MIT
metadata:
  version: "0.1.0"
  author: "OthmanAdi"
  homepage: "https://github.com/OthmanAdi/sketchy"
---

# sketchy

Looks sketchy. The numbers are real.

sketchy turns what someone needs to say into pages from a pencil sketchbook: graphite on cool blue-gray paper, one red pencil for the thing that matters, colored-pencil hatching, handwriting for people and typewriter figures for the record. Lines boil gently like hand-drawn animation, pages turn like paper, stamps slam, and the sound (off until the viewer turns it on) is generated in the browser. Every output is one HTML file that opens offline and exports to PDF, PPTX and MP4.

The enemy is the default deck: gradient title, three bullets, stock icon, chart nobody reads. A sketchbook is a thinking medium. It explains, it shows the working, and it is honest about what was estimated and what was measured.

## What it makes

| Ask | Template | Typical length | Exports |
|---|---|---|---|
| Slides, pitch, board update, lecture | `templates/deck.html` | 6 to 20 slides | HTML, PDF, PPTX, MP4 |
| Lesson, tutorial, how it works | `templates/explainer.html` | one long page, or a deck | HTML, PDF |
| Report, one-pager, memo, plan vs actual | `templates/report.html` | 1 to 3 printed pages | HTML, PDF |
| Chart, data story | `templates/chart.html` | one figure or a sheet of them | HTML, PNG, PDF |
| Decisions to take (keep or remove, go or no-go) | `templates/board.html` | 3 to 30 plates | HTML |
| Social card, thank-you, certificate | `templates/postcard.html` | 1200 x 800 or 1080 x 1350 | HTML, PNG |
| Explainer video, launch clip, recap | a deck in video mode | 20 s to 3 min | MP4 with music |

## Verbs

People say these, or the plain-language version of them. Each maps to the workflow below.

| Verb | Means |
|---|---|
| `sketchy deck <topic>` | build a slide deck |
| `sketchy explain <topic>` | build a lesson or explainer |
| `sketchy report <data or doc>` | build a report or one-pager |
| `sketchy chart <data>` | draw one chart or a sheet of charts |
| `sketchy board <items>` | build a decision board |
| `sketchy postcard <message>` | build a card |
| `sketchy video <deck or topic>` | render a deck to MP4 with music |
| `sketchy audit <file>` | lint and review an existing sketchy file, report only |
| `sketchy theme <name>` | make a theme from a brand color or a reference |

## The rules

Each rule is here because the opposite looks generated, misleads, or breaks.

1. **Paper is a material, not a fill.** Use `class="sk"` on `<html>` and `<body>` so the engine lays its seeded grain, fibers, vignette and sky. Never paint a flat cream or white page, never add a gradient background.
2. **One graphite pencil, one red pencil.** Graphite draws and writes everything. Red marks the single thing to look at on a page: the target, the main action, the correction. Colored pencils (blue, green, yellow, orange, violet, rose, teal, in that order) are for data series and objects. Never use red for decoration.
3. **Dashed means plan, solid means record.** Forecasts, targets, estimates, hints and goals not yet met are dashed or drawn as outline stamps. What happened is a solid line. In the night theme the computed result is smooth gold ink and the benchmark is always blue.
4. **Handwriting for people, typewriter for the record.** Caveat for titles, sentences, labels and buttons. Courier Prime (`.sk-figure`, `{ mono: true }`) for every number, date, ID and amount. No third typeface.
5. **Numbers are honest.** Use only figures the user gave or that you can cite. If a number is missing, write `—` with a note, or change the slide. Every result gets its benchmark and its owner where one exists, units always, bars from zero, distortions printed ("drawn 6x life size"), sources on the page with a red `§`.
6. **One idea per page.** At most 40 words of body text on a slide and at most 6 bullets; prefer a picture, a number or a chart to a bullet. The slide title states the point, not the topic ("We delivered more, for less", not "Q3 results").
7. **Draw the thing itself.** Use the sketch catalog (`references/sketches.md`) for objects. No emoji as icons, no stock photos, no clip art, no arrows chained into a flowchart when a picture of the object would do.
8. **Motion is paper.** Sheets arrive with a 10 px drop and a -0.6 degree tilt, pages turn on `rotateY`, stamps slam once, receipts print line by line, numbers count up, lines boil at 10 fps. No fly-ins, no bounces, no zooms. Reduced motion is respected by the engine; do not override it.
9. **Deadpan voice.** Short sentences and imperatives. A dry joke may sit next to a real number, never inside it. Stamps and states in capitals (DELIVERED, OVERDUE). See `references/voice.md`.
10. **Self-contained output.** The final file runs from `file://` with no network. Build it with `scripts/build.mjs`. Fonts are bundled (SIL OFL).
11. **Sound is opt-in.** The viewer turns it on. Music is generative from the deck's seed, so the video soundtrack is the same piece every time.
12. **Look before you say done.** Lint, screenshot, open the screenshots, fix, and only then report. A render log is not a review.

## Workflow

### 0. Find what already exists
Look for the user's own material first, in this order: `./.sketchy/themes/` and `./.sketchy/templates/` in the project, then `~/.sketchy/themes/` and `~/.sketchy/templates/`, then this skill's `themes/` and `templates/`. Use brand colors, fonts or a previous sketchy file if the user has them. Read `references/themes-and-templates.md` when you use or make one.

### 1. Brief
Settle these, from the request and the material, before drawing: audience; the one sentence they must remember; what they must decide or do afterwards; which numbers exist and where they come from; language; output (live deck, PDF, PPTX, video); length or duration. Ask once, briefly, only for what changes the result and cannot be inferred. Otherwise state your assumptions and go.

### 2. Deal a style
Run `node scripts/deal.mjs --brief "<one line>"`. It deals paper and theme, cover color, the two leading pencils, a motif and the opening page, and it avoids the user's recent draws so decks do not converge. If the user wants to choose, describe three dealt directions in three or four lines each (feel, opening page, paper and pencils, the signature move), recommend one, and wait. If they said "just do it", take the deal and say which one you took.

### 3. Storyboard in text
Write the page list before any HTML: page number, layout, the point in one line, the picture or chart, the figures with their source. Use the patterns in `references/slides.md` (decks), `references/education.md` (lessons) and `references/business.md` (reports, plan vs actual, bills, verdicts). Check the storyboard against rule 6 and rule 5 now; it is cheaper than after drawing.

### 4. Build
Run `node scripts/new.mjs <deck|explainer|report|chart|board|postcard> <out-folder> [--theme <name>] [--title "..."]`. It copies the template and the engine into `<out-folder>` so the file previews from disk. Fill the `<!-- slot:... -->` parts. Use only engine classes and tokens (`references/components.md`); no raw colors in your CSS, only `var(--sk-*)`. Charts are specs, not drawings: `references/charts.md`. Sketches are names: `references/sketches.md`. Sound and music: `references/sound.md`.

### 5. Check by looking
```bash
node scripts/build.mjs <file.html>            # one self-contained file in <folder>/out/
node scripts/lint.mjs <out/file.html>         # overflow, collisions, tiny type, contrast, words per slide, placeholders, network
node scripts/shoot.mjs <out/file.html>        # every slide or page at 1920x1080 and 390x844, plus contact-sheet.png
```
Fix every lint error. Open `contact-sheet.png`, then every screenshot, and look for: text crossing lines, labels colliding, a page with two protagonists, red used twice, empty or crowded pages, numbers without units or source, anything that reads as a template. Fix, re-shoot only what changed, stop when it is right. When a subagent with image reading is available, hand the screenshots (not your code) to a fresh one with `references/review.md`; it scores 1 to 10 on six axes and lists fixes. Aim for 8 or more on every axis.

### 6. Subtract
One last pass per page: remove repeated words, decorative lines that explain nothing, a second accent, a bullet that repeats the title. Keep names, figures, states and the main action.

### 7. Export and deliver
```bash
node scripts/export-pdf.mjs <out/file.html>
node scripts/export-pptx.mjs <out/file.html> --mode faithful    # or editable; see references/export.md
node scripts/render-video.mjs <out/file.html> --fps 30          # MP4 with generated music; needs FFmpeg
```
Report in the format under Output below.

## Output

Every run ends with the files on disk and a short report in the user's language:

```text
Made: 10-slide board update for the directors (Q3, Northwind)
Style: day sketchbook, slate cover, blue and green pencils, postal motif (dealt)
Files:
  ./sketchy/q3-update/q3-update.html        working file, previews from disk
  ./sketchy/q3-update/out/q3-update.html    one self-contained file, 610 KB
  ./sketchy/q3-update/out/q3-update.pdf     10 pages, 1920x1080
Checks: lint 0 errors, 1 warning (slide 8: 46 words, kept on purpose: it is the bill)
        screenshots read: all 10 slides and the 390 px view
Review: fresh reviewer 8/9/8/9/8/9 (Point/Hierarchy/Craft/Honesty/Voice/Restraint), 3 fixes applied
Not done: PPTX (not asked), video (FFmpeg missing; `node scripts/doctor.mjs` prints the install line)
Numbers: all from Q3_figures.xlsx, sheet "Board"; none estimated
```

## Example

Request: *"Explain to my class of 14-year-olds why we have seasons. 6 slides, they are visual learners."*

1. Brief: audience 14-year-olds; the one sentence "Seasons come from the tilt, not the distance"; afterwards they can draw the tilted Earth in four positions; numbers: tilt 23.4 degrees, distance varies about 3 percent (cited).
2. Deal: `graph` paper, `moss` cover, yellow and blue pencils, margin-maths motif, opening on a big question.
3. Storyboard: cover; big question "Is summer when we are closest to the Sun?"; misconception crossed out; split page with the tilted Earth sketch and three numbered steps; math margin with the 3 percent; recap postcard.
4. Build with `new.mjs deck ./seasons --theme graph`, then lint, shoot, look, fix two labels that touched a line, export PDF.

## Files

| Path | What it is |
|---|---|
| `engine/sketchy.css` | tokens (day and night), paper, type, sheets, buttons, cover, stamps, slips, tape, postcards, gauges, motion |
| `engine/sketchy.js` | the pencil: seeded geometry, pen API, boil, decorators (`data-sk`), postal objects, paper, `Sketchy.mount()` |
| `engine/sketches.js` | the sketch catalog, more than 100 small drawings of things |
| `engine/sketchy-charts.js` | hand-drawn charts with honest data (`<figure class="sk-chart">`) |
| `engine/sketchy-deck.js` | the slide runtime: stage, page turn, steps, counters, overview, notes, print and video modes |
| `engine/sketchy-sound.js` | procedural sound effects and generative music |
| `themes/` | token files; `_starter.css` is the one to copy for a brand |
| `templates/` | starting files per artifact, with slots |
| `scripts/` | `new`, `deal`, `build`, `lint`, `shoot`, `export-pdf`, `export-pptx`, `render-video`, `doctor` |

## When to read which reference

| Reference | Read when |
|---|---|
| `references/style-dna.md` | always once per session: the look in exact values |
| `references/slides.md` | building any deck: layouts, storyboard patterns, page budget |
| `references/education.md` | a lesson, tutorial, how-it-works, or anything for learners |
| `references/business.md` | numbers, money, plans, results, decisions: the stationery that files them |
| `references/charts.md` | any chart or figure |
| `references/components.md` | the classes and attributes you can use in HTML |
| `references/sketches.md` | choosing pictures |
| `references/motion.md` | anything that moves, reveals or counts |
| `references/voice.md` | writing any word on a page |
| `references/sound.md` | sound effects, music, video soundtrack |
| `references/export.md` | PDF, PPTX, PNG and MP4, and their limits |
| `references/themes-and-templates.md` | brand colors, the user's own themes and templates |
| `references/review.md` | the fresh-eyes review and its rubric |

## Setup

The engine needs nothing; any browser opens the files. The scripts need Node 18+ and Playwright 1.63.0 with Chromium; video needs FFmpeg. Run `node scripts/doctor.mjs` first when anything fails: it prints the exact install line for the platform.

## Limits

- The bundled Caveat covers Latin and Cyrillic. Arabic, Hebrew, Greek, CJK and math symbols (Σ, Δ, π, ≈) fall back to a system font; check the screenshots and say so.
- PPTX cannot carry the handwriting font or the boil. `faithful` mode bakes each slide as a picture with real notes and hidden text; `editable` mode uses real text boxes in a safe font over the drawn art.
- No live data, no photographs, no 3D. Screenshots of real products may be placed in a `<figure>` with a hairline frame, never inside a drawn device.
