# Style DNA

The look in exact values. Every value here already lives in `engine/sketchy.css` (tokens) and `engine/sketchy.js` (the pencil). This page says what each value is for, so you use it on purpose and never paint a color by hand. In your own CSS, write `var(--sk-*)`, never a hex.

Two themes ship. The **day sketchbook** is the default. The **night ledger** is `<html class="sk" data-theme="night">`: chalk on night-blue paper, gold for the computed record.

## Day sketchbook

| Token | Value | Job |
|---|---|---|
| `--sk-paper` | `#c3c8d1` | cool blue-gray cartridge paper; the page, sheet backings, text halos |
| `--sk-paper-deep` / `--sk-paper-light` | `#b4bac5` / `#d6dae1` | pressed button fill / plates, hover fill |
| `--sk-shadow` | `40, 46, 72` | every shadow is blue-black at low alpha, never neutral black |
| `--sk-ink` | `#262626` | titles and the darkest text |
| `--sk-graphite` | `#4a4a4a` | every line and every word by default |
| `--sk-graphite-soft` | `#5d6068` | secondary text, the "(June)" after a heading |
| `--sk-graphite-faint` | `rgba(74,74,74,.38)` | guides, history, rubbed-out lines |
| `--sk-red` | `#d98a8a` | **red lines**: target rings, the delivered line, the gauge mark |
| `--sk-red-ink` | `#9a454b` | **red writing**: red-pen notes, `§` references, chapter labels |
| `--sk-red-frame` | `#a84f55` | **red frame**: the outline of the one main button (`.is-accent`) |
| `--sk-red-soft` | `#e7b9b5` | a pale red wash, rarely |
| `--sk-figure` | `#2f2f35` | numbers in the record (`.sk-figure`) |
| `--sk-gold` | `#b8862f` | reserved for the computed record; by day prefer `figure` |
| `--sk-cream` / `--sk-card` | `#e6e3da` / `#efece4` | cover label / postcard and slip stock |
| `--sk-stamp` / `-blue` / `-green` | `#9a454b` / `#3f5e8c` / `#3f7a5a` | rubber-stamp inks |
| `--sk-tape` / `--sk-tape-text` | `#26272c` / `#f1efe8` | black label tape for technical names |
| `--sk-cover` / `--sk-elastic` | `#5e6a7e` / `#33333c` | cloth board, elastic band |
| `--sk-door` | `#2c2e35` | the dark cover button |
| `--sk-label-ink` / `--sk-label-ink-soft` | `#3d3d42` / `#4a4a52` | writing on the cover label |
| `--sk-slip-red` / `--sk-slip-paper` / `--sk-slip-text` | `#b8392b` / `#f4efe3` / `#fff4e6` | postal red: the registered slip and the registration label |
| `--sk-btn-hover` / `--sk-btn-press` | `#d6dae1` / `#b4bac5` | button backing on hover and press |
| `--sk-btn-accent` / `--sk-btn-accent-hover` | `#c6c1c9` / `#d4cbd1` | backing of the one main button |
| `--sk-maths-ink` | `#3a3a40` | margin math text |

## Night ledger

Same token names, new values. A theme never renames a role.

| Token | Value | Job |
|---|---|---|
| `--sk-paper` | `#161c2b` | night-blue paper with fibers and grain, never flat black |
| `--sk-graphite` | `#ece6d6` | **chalk**: the hand, labels, estimates |
| `--sk-ink` | `#f6f1e4` | titles |
| `--sk-red` / `--sk-red-ink` | `#ef5f4a` / `#f28a76` | **vermilion**: targets, verdicts, money; lighter ink for text on dark |
| `--sk-gold` = `--sk-figure` | `#f0bf4f` | **gold**: the computed record and every number in it |
| `--sk-blue` | `#93a9cf` | **the benchmark**, always and only |
| `--sk-cover` / `--sk-door` | `#633537` / `#2a1416` | oxblood ledger board |
| `--sk-focus` | `#f0bf4f` | focus ring |
| `--sk-btn-hover` / `--sk-btn-press` / `--sk-btn-accent` | `#263049` / `#10151f` / `#3a2a33` | button backings on dark paper |
| `--sk-maths-ink` | `#ece6d6` | margin math in chalk; values turn gold |

Paper documents (`.sk-doc`, `.sk-slip`, `.sk-label`, `.sk-postcard`, receipts) keep their light stock at night and switch their pencils back to day ink inside: they are documents lying on a dark desk.

## Colored pencils

`--sk-blue`, `--sk-green`, `--sk-yellow`, `--sk-orange`, `--sk-violet`, `--sk-rose`, `--sk-teal`, **in that order** for data series and object colors. `Sketchy.tokens().pencils` returns them in this order. Red is not in the list: it is never a series color.

| Rule | Why |
|---|---|
| First series is blue, second green, and so on | the reader learns one mapping per deck |
| Never more than four pencils on one page | five pastels side by side read as confetti |
| Green only for checks and "done" | a green series next to a green check reads as a verdict |
| Peach (`--sk-peach`) is the lit state of a toggle | it is a state, not a series |

## Typography

Two typefaces, fixed jobs. No third.

| Role | Face and weight | Where |
|---|---|---|
| Titles, labels, buttons, notes | Caveat 600 | `h1` to `h3`, `.sk-btn`, `.sk-big`, `.sk-text` in SVG |
| Prose, subtitles, tasks | Caveat 400 | body text, `.sk-label-sub`, `.sk-corner-task` |
| Stamps, the door, the lit button | Caveat 700 | `.sk-stamp`, `.sk-door`, `aria-pressed="true"` |
| The record: numbers, dates, IDs, amounts | Courier Prime 700 | `.sk-figure`, `.sk-number`, `{ mono: true }` in the pen |
| Slip and receipt body | Courier Prime 400 | `.sk-mono` |

Caveat has a natural slant: no italics, no letter-spacing (except uppercase kickers and stamps, which the engine spaces). Inside a handwritten sentence, a value switches to `.sk-figure`: `paid back in <span class="sk-figure">28 months</span>`.

Coverage: Caveat is bundled for Latin, Latin Extended and Cyrillic; Courier Prime for Latin and Latin Extended. Greek letters and math symbols (`Σ Δ π ≈ → ✓`) and every other script fall back to a system font in a different hand ([voice.md](voice.md)).

Stage sizes on the 1920 x 1080 slide: hero 132 px, title 84, big 62, sub 40, body 34, fine 26. Layouts enlarge some (section title 150, big number 260). Pages use fluid `clamp()` sizes from 16 to 92 px. The linter flags slide text under 20 px and page text under 16 px.

## The pencil

| Mechanism | Value | Effect |
|---|---|---|
| Double stroke | `passes: 2`; the second pass at 0.8 width and 0.6 opacity | a quick hand going over its own line |
| Default line | width 1.5, opacity 0.9, round caps | graphite, not vector hairline |
| Straight lines | jittered ends, overshoot up to 3.2 px, a slight bow; long lines drift in segments of about 130 px | no ruler |
| Circles | radius wobbles on the 2nd, 3rd and 5th harmonics; the stroke overshoots its start by 3 to 10 degrees and drifts outward; the second pass retraces 20 to 55% of a turn | a circle drawn without a compass |
| Hatching (`fillStyle: 'body'`) | 38% wash, hatch at -41 deg (plus or minus 5) gap about 2.2, cross-hatch at -41 + 95 deg at 65% | a colored pencil filling a shape |
| Other fills | `hatch`, `cross`, `scribble`, `solid`, `none` | use `solid` only for tiny dots |
| Grain | SVG filter `#sk-grain` on every stroke group | graphite on paper tooth |
| Stamp ink | SVG filter `#sk-ink` on `.sk-stamp` | blotchy coverage, eaten edge |
| Boil | 4 variants of every drawing, swapped together at **10 fps** on one shared 60-step clock; 2 fps with reduced motion; off (variant 0) in `?static` and `?print` | the shimmer of hand-drawn animation; geometry is never re-randomized per frame |
| Arrows | curved (bend 0.18), two-stroke head at plus and minus 0.45 rad | a pointing hand, not a connector |
| Halo | SVG text gets a 4 px paper-colored stroke behind it; DOM text over drawings uses `.sk-glow` | labels sit on lines without boxes |

Everything is seeded: `data-seed` on the deck, `seed` in the pen, `data-sk-seed` on decorators. Same seed, same wobble in the browser, PDF, PPTX art and video.

## Line grammar

| Line | Pen options | Means |
|---|---|---|
| Solid graphite | default | the record: what happened |
| Dashed graphite | `dash: '5 5'` | the plan: forecast, estimate, target not yet met |
| Dashed red ring | `stroke: C.red, dash: '3 4'` | the target or the window |
| Faint dashed | `stroke: C['graphite-faint'], dash: '2 5'` | history: last year, the previous try |
| Solid red | `stroke: C.red, width: 1.8` | the one result that matters (delivered, the correction) |
| Smooth gold (night) | `stroke: C.gold, rough: 0, passes: 1, width: 2.2` | the computed record; smoothness is the mark of truth |
| Blue (night) | `stroke: C.blue, passes: 1` | the benchmark |
| Rubbed out | the path in `graphite-faint`, then again in `C.paper` at width + 3.5, opacity 0.28 | an abandoned attempt, kept visible |

Dashed strokes get the class `sk-plan`, so a reader of the SVG can find every plan line.

## Props

The post office is the UI kit. Each prop sits slightly rotated and slightly under-inked, so it looks pressed, not printed.

| Prop | How | Rotation | Ink |
|---|---|---|---|
| Sheet | `.sk-sheet` + `data-sk="sheet"` | arrives at -0.6 deg, rests at 0 | frame 0.95, paper backing 0.9 |
| Button | `.sk-btn` + `data-sk="button"` | 0 | frame 0.95 |
| Cover | `.sk-cover` with `data-cover`, elastic band at 86% | 0 | cloth weave |
| Label | `.sk-label` on the cover | -1.5 deg | double rule at 0.7 and 0.45 |
| Rubber stamp | `.sk-stamp` | -6 deg | 0.85 |
| Unearned stamp | `.sk-stamp.is-unearned` | -6 deg | 0.5, dashed outline |
| Postmark | `svg[data-postmark]`, `Sketchy.postmark()` | per drawing | 0.8 |
| Receipt (postage slip) | `.sk-doc.sk-receipt.sk-pinked` | 0 | day ink on card stock, pinked edges |
| Registration label | `.sk-rlabel` | -1.5 deg | postal red block |
| Cancellation waves | `Sketchy.cancelWaves()` | 0 | 0.55 |
| Postage stamp | `Sketchy.postage()` | per drawing | perforated, 1.2 px frame at 0.6 |
| Registered slip | `.sk-slip` | -3 deg | red double border |
| Tape | `.sk-tape` | -1 deg | solid black |
| Postcard | `.sk-postcard` | `--sk-tilt`, default -1.2 deg | 2 px rule at 0.35 |
| Plate | `.sk-plate` | 0 | four screws |

**Rotation and ink rule:** props sit between 0.6 and 6 degrees off square and are inked between 50 and 90%. Documents that carry columns of figures (receipts, tables, sheets) stay square so the columns read; their stamps and labels supply the tilt.

## 12 rules

1. **Paper is a material.** Seeded grain, fibers, blotches, a blue-black vignette. Never a flat fill, never a gradient you wrote.
2. **One graphite pencil does everything** by default: lines, words, outlines.
3. **One red pencil per page,** for the one thing: target, main action, correction. Lines in `red`, writing in `red-ink`, the main button frame in `red-frame`.
4. **Color is a wash under hatching** at -41 deg with a cross-hatch at +95. Shade with more hatching, never with gradients.
5. **Lines boil, slowly:** four variants at 10 fps on one clock.
6. **Circles overshoot and retrace.** Rectangles are drawn twice.
7. **Dashed is plan, solid is record.** At night, smooth gold is computed and blue is the benchmark.
8. **Handwriting for people, typewriter for the record.** Caveat 600, 400, 700; Courier Prime for every figure.
9. **Text sits on a halo,** not in a box.
10. **Numbers are filed on stationery:** slips, postmarks, stamps, labels (`business.md`).
11. **Props are pressed, not printed:** 0.6 to 6 deg, 50 to 90% ink.
12. **Motion is paper:** sheets drop 10 px with a -0.6 deg tilt, pages turn on `rotateY`, stamps slam once ([motion.md](motion.md)).

## Slop list

Each of these breaks the look. If a screenshot shows one, fix it before review.

| Slop | Why it breaks | Instead |
|---|---|---|
| Flat cream or white page fill | reads as a template, kills the paper | `class="sk"` on `html` and `body` |
| Gradients on backgrounds, text or buttons | no pencil makes a gradient | hatching, or nothing |
| A drop-shadow card around every block | a dashboard, not a sketchbook | one sheet per page; let things sit on paper |
| Emoji or icon-font icons | a different hand drew them | a sketch from the catalog (`sketches.md`) |
| Two reds, or red as decoration | the eye no longer knows where to look | one red thing per page |
| Centered body text in long paragraphs | hard to read, looks like a greeting card | left-aligned prose; center only titles and single lines |
| Stock illustration or photos inside drawn devices | breaks the single hand | draw the object, or a framed screenshot in a `<figure>` |
| Neon, saturated brand blues, glow | pastel pencils cannot do it | the pencil order above |
| Glassmorphism, blur panels | there is no glass in a sketchbook | a sheet with a paper backing |
| Third typeface, bold sans headings | breaks the two-hand rule | Caveat and Courier Prime only |
| Perfect straight connectors and flowchart boxes | software diagram, not a drawing | the pen, or a picture of the thing |
| Every element animating in on its own | busy, and not how paper moves | a sheet arrives whole |
