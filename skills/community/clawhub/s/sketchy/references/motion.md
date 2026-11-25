# Motion

Read for anything that moves, reveals or counts. Motion is paper: sheets drop and settle, pages turn, stamps slam once, receipts print, numbers count, lines boil. Nothing flies, bounces, zooms or spins. Every value below is what the engine already does; use the class or attribute, do not rebuild the motion.

## The vocabulary

| Motion | Trigger | Duration | Curve | Movement |
|---|---|---|---|---|
| Sheet in | `.sk-in`, `[data-reveal="sheet"]` in decks | 260 ms | `--sk-ease` `cubic-bezier(.2,.8,.2,1)` | from 10 px down, -0.6 deg, transparent; arrives whole |
| Page reveal (no deck) | `[data-reveal]`, `[data-count]`, `svg[data-sketch][data-draw]`, `.sk-chart[data-draw]` | 420 ms, once, when a quarter is in view | `--sk-ease` | the sheet-in motion; print, count and trace as below |
| Slide arrives (deck) | page or cover transition | 360 ms after 140 ms | `--sk-ease` | the sheet-in motion for the whole page |
| Page over | deck `page` transition, `.sk-out-page` | 650 ms | `--sk-ease-page` `cubic-bezier(.37,0,.63,1)` | `rotateY` to -120 deg around the left edge, opaque until 70%; perspective 1400 px |
| Page back | going back, `.sk-out-back` | 650 ms | `--sk-ease-page` | `rotateY` to +120 deg around the right edge |
| Cover open | leaving a `cover` slide forward | 800 ms | `--sk-ease-cover` `cubic-bezier(.3,.6,.2,1)` | `rotateY` to -165 deg |
| Slide (alt.) | `data-transition="slide"` | in 520 ms, out 360 ms | `--sk-ease` / `--sk-ease-page` | 60 px with a 0.6 deg tilt; out 40 px |
| Fade (alt.) | `data-transition="fade"` | in 420 ms, out 260 ms | ease-out / ease-in | opacity only |
| Stamp slam | `.sk-stamp.is-slam`, `.sk-stamp[data-slam]` | 360 ms, deck delay 600 ms (`--delay`) | `--sk-ease-slam` `cubic-bezier(.3,.6,.3,1.25)` | from 1.8x, to 0.94x at 70%, settles at 1x; stays at -6 deg |
| Postcard in | `.sk-postcard.is-in`, `.sk-postcard[data-reveal]` | 420 ms, deck delay 200 ms | `--sk-ease-card` `cubic-bezier(.2,.9,.25,1.05)` | from 40 px down, +4 deg, 0.94x, to its `--sk-tilt` |
| Receipt lines | `[data-reveal="print"] > *` | 380 ms each, 95 ms apart, after 180 ms | `--sk-ease` | each line from 5 px down |
| Counter | `[data-count]` | 900 ms after 300 ms | cubic out, `1 − (1 − p)³` | 0 (or `data-count-from`) to the value, in the page's number format (`<html lang>`) |
| Step reveal | `[data-step]` on click | 260 ms | `--sk-ease` | like a small sheet: 10 px, -0.6 deg |
| Draw-on | `svg[data-sketch]`, `.sk-chart svg`, `svg[data-draw]`, first visit only | 520 ms per stroke, 10 ms apart, from 220 ms, +120 ms per SVG | `cubic-bezier(.35,.1,.25,1)` | strokes trace via dash offset; hatching fades in after |
| Boil | always | 10 fps, 2 fps reduced | stepped | 4 variants on one shared 60-step clock (6 s loop) |
| Ready pulse | `.sk-btn.is-ready` | 900 ms, infinite | `cubic-bezier(.45,0,.55,1)` | 1.045x at the middle |
| Edge bump | next at the last slide, back at the first | 260 ms | `--sk-ease` | 12 px toward the edge and back |
| Veil | `.sk-veil` | 180 ms | ease-out | opacity |
| Press | `.sk-btn:active` | instant | none | label and frame 1 px down and right |
| Hover fill | `.sk-btn:hover` | 120 ms | ease-out | backing lightens |
| Door | `.sk-door` | 90 ms | linear | hover 1 px up, press 2 px down, hard shadow shrinks |

The one signature curve is `cubic-bezier(.2,.8,.2,1)`: fast out, soft landing. Overshoot exists only on stamps (1.25) and postcards (1.05), because those are small objects thrown onto paper.

## The three base motions

Every artifact needs these three, and usually nothing more.

| Motion | What it is here | How |
|---|---|---|
| Feedback on the main action | the press that answers a click; in a deck, the page that turns on "next" | `.sk-btn` with `data-sk="button"`; `.is-accent` for the one main action; `data-next` or a `.sk-door` makes it turn the page; the deck bumps at the ends by itself |
| One state change that shows where things go | something arrives where it belongs: the stamp lands on the slip it judges, the step appears in its place, the page turns in the reading direction | `data-slam` timed after the last receipt line; `data-step`; never reorder steps against the DOM |
| One first entrance | the page or sheet arrives once, drawings trace once | first visit only (the deck remembers visited slides); on explainer pages `data-reveal` plays once as each block scrolls in |

Before adding any other motion, say which of feedback, guidance or continuity it serves. If none, leave it out.

## Choreography of one slide

```
0 ms      old page turns away (650 ms)
140 ms    new page arrives (360 ms)
180 ms    receipt line 1 prints; one more every 95 ms
220 ms    drawings start tracing (+120 ms per drawing)
300 ms    counters start (900 ms)
600 ms    default stamp slam; set --delay after the last receipt line
on click  data-step elements, in number order
```

The reader's eye goes to what moves. Let only the protagonist move after the page has landed.

## What not to animate

| Do not | Why | Instead |
|---|---|---|
| Animate each element in on its own | busy, and paper does not do it | the sheet arrives whole; steps are clicks |
| Fly-ins, bounces, zooms, spins, parallax | not how paper moves | sheet-in, page turn |
| Scroll-linked motion, parallax, reveals that replay | the reader waits for text | the engine's one reveal per block, the first time it scrolls in; mark only the blocks that matter |
| Type text letter by letter | slow and theatrical | receipt lines print whole |
| Grow chart bars or morph shapes | it lies about the data mid-flight | the pencil traces the drawing |
| Loop anything but the boil and the ready pulse | attention leaks | still pages |
| Count numbers that are not the result | only the headline earns a count | static `.sk-figure` |
| Move or scale the paper and sky | the paper is the table | the sky stays fixed while pages turn |
| Hover lifts over 2 px, glows, color shifts | a web app, not a sketchbook | the engine's button states |

## Reduced motion

The engine reads `prefers-reduced-motion: reduce` and changes itself. Never override it, and never put information only in an animation.

| Motion | With reduced motion |
|---|---|
| Boil | slows to 2 fps |
| Page turns, cover, slide transitions | become a cross-fade (in 420 ms, out 260 ms or 200 ms) |
| Sheet in, every `[data-reveal]`, postcards | none; the element is just there, on pages without waiting for scroll |
| Receipt print, stamp slam | none; final state at once |
| Counters | show the final value at once |
| Draw-on | skipped; drawings are complete |
| Ready pulse | replaced by a dashed red outline |
| Edge bump | off |
| Steps | still wait for the click, then appear at once with no transition |

Check by emulating reduced motion in the browser, or rely on `shoot.mjs`, which runs with reduced motion on.

## How video sees motion

`scripts/render-video.mjs` steps the deck frame by frame on a virtual clock (`export.md`).

| Fact | Consequence for authors |
|---|---|
| The engine uses CSS animations and transitions on purpose: they appear in `document.getAnimations()`, so the renderer pauses and seeks each one to the frame time | your own CSS animations also render correctly |
| `SketchyDeck.timeline()` lists each slide's start, duration and step times; `SketchyDeck.seek(seconds)` jumps there | set `data-duration` on every slide that needs more than 6 s |
| Steps reveal at `start + (k + 1) x duration x 0.6 / (steps + 1)` | all steps are out by 60% of the slide's time; leave the rest for reading |
| Counters and the boil read the page clock (`requestAnimationFrame`, `performance.now`) | the renderer drives that clock; never time motion with `setTimeout`, `Date.now()` or `Math.random()` |
| `?video` turns on autoplay and hides the controls and cursor | do not put needed content in the HUD |

A slide is long enough when its last motion (stamp delay plus 360 ms) is done with at least 2 s of stillness left to read it.
