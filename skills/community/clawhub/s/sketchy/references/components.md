# Components

Every class, attribute and call the engine offers, with one line on its job and a minimal snippet. If it is not on this page, it does not exist: compose from these, use `var(--sk-*)` tokens in any local style, and do not invent engine classes. Values and colors: [style-dna.md](style-dna.md). Motion timings: [motion.md](motion.md).

## Page setup

```html
<!doctype html>
<html lang="en" class="sk" data-theme="day">          <!-- data-theme="night" for the night ledger -->
<head><meta charset="utf-8"><title>Q3 for the board</title>
<link rel="stylesheet" href="engine/sketchy.css">
<link rel="stylesheet" href="themes/brand.css"></head>   <!-- optional token file -->
<body class="sk">
  ...content...
<script src="engine/sketchy.js"></script>
<script src="engine/sketches.js"></script>               <!-- optional: pictures -->
<script src="engine/sketchy-charts.js"></script>         <!-- optional: charts -->
<script src="engine/sketchy-sound.js"></script>          <!-- optional: sound -->
<script src="engine/sketchy-deck.js"></script>           <!-- decks only -->
<script>SketchyDeck.mount();</script>                    <!-- pages: Sketchy.mount(); -->
</body></html>
```

| Attribute / class | Job |
|---|---|
| `html.sk`, `body.sk` | paper, grain, vignette, base type; required on both |
| `.sk-page` | the same paper on a container instead of `body` |
| `data-theme="day\|night"` on `html` | picks the token set; changing it redraws everything |
| `data-paper="day\|night"` on `html` | paper texture override (defaults to the theme) |
| `data-sk-boil` on `html` | set by the engine (0 to 3, or `off`); never write it |
| `html.sk-static` | set by `?static` and `?print`: no animation, boil off |

## Type

| Class | Job | Snippet |
|---|---|---|
| `h1` to `h3`, `.sk-h1` to `.sk-h3` | Caveat 600 titles | `<h2>Where it went</h2>` |
| `.sk-big` | a big handwritten line (600) | `<p class="sk-big">Three wins</p>` |
| `.sk-line` | a slightly larger body line | `<p class="sk-line">One sentence.</p>` |
| `.sk-kicker` | small uppercase label above a title, on slides and pages | `<span class="sk-kicker">Q3 · July to September</span>` |
| `.sk-small`, `.sk-fine` | smaller print in full graphite | `<p class="sk-fine">As of 3 Oct.</p>` |
| `.sk-hand`, `.sk-mono` | force Caveat or Courier Prime | `<td class="sk-mono">` |
| `.sk-figure` | a number in the record: Courier 700, tabular, ink by day, gold by night | `<span class="sk-figure">€2.26</span>` |
| `.sk-note` | red-pen note in HTML | `<span class="sk-note">the old one</span>` |
| `.sk-sect` | red `§` reference | `<span class="sk-sect">§ 2</span>` |
| `.sk-red`, `.sk-soft` | red ink text, soft graphite text | `<tr class="sk-red">` |
| `.sk-glow` | paper halo for DOM text over a drawing | `<p class="sk-glow">` |
| `.sk-sr` | visually hidden, read by screen readers | `<span class="sk-sr">Revenue table</span>` |

## Surfaces

| Class | Job | Snippet |
|---|---|---|
| `.sk-sheet` + `data-sk="sheet"` | a pencil-framed sheet with paper backing and a soft shadow | `<div class="sk-sheet" data-sk="sheet">...</div>` |
| `.sk-callout` | a small note box, max 32 characters wide; first `b` is its title | `<div class="sk-callout" data-sk="frame"><b>Why</b>It is cheaper.</div>` |
| `.sk-toast` | a short dashed-border message | `<div class="sk-toast">Saved.</div>` |
| `.sk-veil` | full-screen veil behind a modal sheet | `<div class="sk-veil"></div>` |
| `.sk-plate` | a decision plate with four screws (boards) | `<div class="sk-plate sk-stack">...</div>` |
| `.sk-doc` | a light paper document on card stock; day ink inside, even at night | `<div class="sk-doc">...</div>` |
| `.sk-pinked` | zigzag (pinked) top and bottom edges, for slips and receipts | `<div class="sk-doc sk-pinked">` |

## Decorators (`data-sk`)

Any element with `data-sk` gets a pencil overlay sized to it, redrawn on resize, theme change and state change.

| Value | Draws | Default pencil |
|---|---|---|
| `sheet` | frame with paper backing | graphite |
| `frame` | frame, no backing (add `data-sk-backing` for one) | graphite |
| `button` | button frame with backing; lit hatching when pressed | graphite, red frame with `.is-accent` |
| `box` | plain double-stroke rectangle | graphite |
| `underline` | one hand line under the element | red |
| `circle` | an ellipse around the element (overshoots) | red |
| `strike` | a line through the element | red |
| `highlight` | yellow hatching behind the text | yellow |
| `bracket` | a left square bracket | graphite |

| Attribute | Job |
|---|---|
| `data-sk-color="blue"` | any token name (`red`, `green`, `graphite-soft`...) or a CSS color |
| `data-sk-seed="hud-next"` | fixes the wobble (defaults to the text) |
| `data-sk-width="2"` | stroke width |
| `data-sk-backing` | paper backing on `frame` |

`<span data-sk="circle">97.1%</span>`, `<span data-sk="highlight">the window</span>`, `<span data-sk="strike">30%</span>`.

## Buttons

| Markup | Job |
|---|---|
| `<button class="sk-btn" data-sk="button">Next page</button>` | a pencil button, Caveat 600 25 px (34 px on a slide) |
| `.is-accent` | the one main action: red frame |
| `aria-pressed="true"` or `.is-on` | lit toggle: peach hatching, bold label |
| `disabled` or `.is-locked` | 45% and not clickable |
| `.is-ready` | pulses gently to say "now"; dashed red outline with reduced motion |
| `<button class="sk-door" type="button">Begin</button>` | the dark cover button with a `›`; on a slide it turns to the next page (on a page, use an `<a class="sk-door">` link) |
| `data-next` on any element in a deck | clicking it turns to the next page or step |
| `<button class="sk-close" aria-label="Close">×</button>` | close cross for a sheet, top right |

## Cover and label

```html
<div class="sk-cover" data-cover="slate">       <!-- slate, oxblood, moss, ochre, ink; .no-band hides the elastic -->
  <div class="sk-cover-inner">
    <div class="sk-label"><span class="sk-label-title">Field Notes</span>
      <span class="sk-label-sub">Q4 plan · for the leadership team</span></div>
    <button class="sk-door" type="button">Begin</button>
  </div>
  <div class="sk-cover-foot">Prepared by finance, 25 Oct 2026.</div>   <!-- its <small> line is 15 px: pages only -->
</div>
```

## Postal objects in HTML

| Markup | Job |
|---|---|
| `<span class="sk-stamp">Delivered</span>` | rubber stamp, red ink, -6 deg, capitals |
| `.is-green`, `.is-blue`, `.is-big` | done ink, informational ink, page-verdict size |
| `.is-unearned` | a goal not yet earned: dashed outline at 50% |
| `.is-slam` | slams once on load (pages); in decks use `data-slam` |
| `<div class="sk-doc sk-receipt sk-pinked">` with `.sk-receipt-brand`, `.sk-receipt-row` (`.is-total`, `.is-bench`) | the postage slip: Courier rows, automatic dotted leaders; add `data-reveal="print"` to print it |
| `<span class="sk-rlabel"><b>R</b><span>No. 0007<small>Report</small></span></span>` | registration label: the document's number; larger on slides; inside a grid (sheet, `.sk-stack`) wrap it in `.sk-row` so it does not stretch |
| `<table class="sk-table">` with `.is-better`, `.is-worse` cells | ruled plan vs record table: first column handwritten, figures right aligned |
| `<svg data-postmark="TOP\|BOTTOM" data-postmark-center="P.O." data-cancel viewBox="0 0 160 110">` | standalone postmark; `data-cancel` adds wavy cancellation lines |
| `<div class="sk-slip">` with `.sk-slip-head` (+ `.sk-r`), `.sk-slip-title`, `.sk-slip-action` | the registered notice: a red-bordered card at -3 deg |
| `<span class="sk-tape">CACHE_TTL</span>` | black label tape for technical names, IDs, flags |
| `<div class="sk-postcard" style="--sk-tilt:-1.2deg">` + two children | postcard: picture or message left, stamp and address right; `.is-in` flies it in |
| `<div class="sk-gauge" style="--value:.62; --mark:.18"></div>` | hatched gauge filled to `--value`, red mark at `--mark` |
| `<aside class="sk-maths">` with `<b>` or `.val`, `.sk-sect` | margin math, right aligned; values gold at night |

```html
<div class="sk-doc sk-receipt sk-pinked" data-reveal="print">
  <div class="sk-receipt-brand">Postage slip</div>
  <div class="sk-receipt-row"><span>Lease</span><span>1,650,000</span></div>
  <div class="sk-receipt-row is-total"><span>IN ALL, €</span><span>2,100,000</span></div>
  <div class="sk-receipt-row is-bench"><span>2023 hub</span><span>2,640,000</span></div>
</div>
<div class="sk-slip">
  <div class="sk-slip-head"><span class="sk-r">R</span>No. 0042 · Notice</div>
  <div class="sk-slip-title">Your invoice is overdue.</div>
  <div>Paid by 31 Oct, nothing else happens.</div>
  <div class="sk-slip-action">Pay now</div>
</div>
```

## Drawing

| Markup / call | Job |
|---|---|
| `<svg data-sketch="truck" viewBox="0 0 140 110" aria-hidden="true"></svg>` | a picture from the catalog (`sketches.md`); `data-seed` varies it |
| `<svg class="sk-specks" data-specks="seed" data-specks-count="150" viewBox="0 0 1600 1000" aria-hidden="true">` | a sky of colored-pencil specks behind a page |
| `<figure class="sk-chart" data-chart='{...}'>` | a chart from a spec (`charts.md`) |
| `Sketchy.pen(svg, { seed, width, rough, passes })` | the pen: `line rect frame circle ellipse poly polyline curve path arrow text dot group into` |
| `Sketchy.variants(svg, (p, v, C) => {...}, { seed, tokens })` | draw four boil variants; labels drawn once on top |
| `Sketchy.postmark(p, cx, cy, r, top, bottom, { center, color })` | circular date stamp, red ink by default |
| `Sketchy.cancelWaves(p, x, y, w, { lines })` | wavy cancellation lines |
| `Sketchy.postage(p, x, y, w, h, { value, label, tint, inner })` | perforated postage stamp; `inner(p, box)` draws its picture |
| `Sketchy.onMount((root, C) => {...})` | run your drawing on every mount; clear the SVG first |
| `Sketchy.register(name, (p, C, parts) => {...})` | add a sketch to the catalog |
| `Sketchy.tokens()` | current colors: `paper`, `graphite`, `red`, `red-ink`, `gold`, `pencils` ... |
| `Sketchy.drawOn(root, { stagger, duration, delay })` | trace strokes in (returns a promise) |

Pen style options: `stroke, width, passes, rough, opacity, fill, fillStyle ('body' default, 'hatch', 'cross', 'scribble', 'solid', 'none'), gap, angle, fillOpacity, dash, grain`. Text options: `anchor, size, color, weight, mono, note, rotate, opacity, halo`.

## Layout helpers

| Class | Job | Snippet |
|---|---|---|
| `.sk-stack` | vertical grid; gap from `--gap` (14 px) | `<div class="sk-stack" style="--gap:18px">` |
| `.sk-row` | wrapping row; gap from `--gap` (12 px) | `<div class="sk-row">` |
| `.sk-center` | centered grid | `<div class="sk-center">` |
| `.sk-split` | two columns, 1 : 1.3, stacks under 720 px | `<div class="sk-split">` |
| `.sk-noprint` | hidden in print and PDF | `<nav class="sk-noprint">` |
| `.sk-in` | sheet entrance on a page | `<div class="sk-sheet sk-in" data-sk="sheet">` |
| `.sk-out-page`, `.sk-out-back` | page turn away, forward or back (pages) | added by your script |

## Deck

| Markup | Job |
|---|---|
| `main.sk-deck` | the deck; `data-seed` (required), `data-transition`, `data-duration`, `data-music`, `data-sky="stars\|dust\|plain"`, `data-draw="off"` |
| `section.sk-slide` | one 1920 x 1080 slide; `data-layout`, `data-duration`, `data-transition`, `data-notes`, `data-music-section` |
| `aside.sk-notes-speaker` | speaker notes as a child element |
| `data-step="1"` | reveal on the next click, in number order |
| `data-count`, `data-count-from`, `data-count-delay`, `data-count-ms` | count a figure up |
| `data-reveal="print"` | children print like receipt lines |
| `data-reveal="sheet"` + `--delay` | arrive like a sheet |
| `.sk-stamp[data-slam]` + `--delay` | slam when the slide arrives (default 600 ms) |
| `.sk-postcard[data-reveal]` + `--delay` | postcard flies in (default 200 ms) |
| `svg[data-draw]` | trace your own drawing in on first visit |
| `data-next` | a click on this element turns the page (`.sk-door` on a slide does it too) |

On pages (no deck), `[data-reveal]`, `[data-count]`, `svg[data-sketch][data-draw]` and `.sk-chart[data-draw]` play once, the first time a quarter of them scrolls into view.

| Layout helper | Job |
|---|---|
| `.sk-corner` > `.sk-corner-title`, `.sk-corner-task`, `.sk-corner-hint` | top-left HUD title |
| `.sk-margin` | top-right box; pair with `.sk-maths` |
| `.sk-disclose`, `.sk-source` | bottom-left distortion note, bottom-right source with red `§` |
| `.sk-chapter` | red chapter label on `section` slides |
| `.sk-step-list` (`--cols`) > `.sk-step` | numbered steps; each `h3` is numbered by the CSS |
| `.sk-number`, `.sk-number-label`, `.sk-number-bench` | big-number parts |
| `.sk-plates` (`--cols`) | grid of plates on `board` |
| `.sk-letter-kicker`, `.sk-letter-row`, `.sk-letter-hint`, `.sk-letter-actions` | parts of the `letter` sheet |
| `.is-flipped` on a `split` slide | words column first, picture column second |

JavaScript: `SketchyDeck.mount()`, `.ready`, `.count`, `.index`, `.go(i)`, `.next()`, `.prev()`, `.on('change', fn)` (same as `'slide'`; also `'step'`, `'ready'`, `'end'`), `.timeline()`, `.seek(s)`. The same events reach `document` as `sk:slide`, `sk:step`, `sk:ready`, `sk:end`.

## Lint and sound hooks

| Attribute | Job |
|---|---|
| `data-lint-ignore` | an overlap or a stroke over text is intended |
| `data-lint-small-ok` | small type is intended (labels, legal lines) |
| `data-lint-contrast-ok` | low contrast is intended (a faint plan label) |
| `data-sk-sound-toggle` | a button that turns sound on and off (`sound.md`) |
