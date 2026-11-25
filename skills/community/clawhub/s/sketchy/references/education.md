# Teaching on paper

Read when the reader is a learner: a lesson, tutorial, how-it-works, onboarding, a lecture deck. A sketchbook is a thinking medium; use it to show the working, not to decorate a script. Layouts: [slides.md](slides.md). Words: [voice.md](voice.md).

## The rules

| Rule | How | Why |
|---|---|---|
| One concept per page | one slide, or one sheet on an explainer page, per idea | a learner can hold one new thing at a time |
| Picture first, then words | the drawing takes the 760 px column of a `split`; the words come second | the picture is what they remember; the words label it |
| Show the working | worked examples with numbered steps, revealed one by one | the steps are the lesson, the answer is not |
| Mark it like a teacher | red-pen notes on the drawing: "pull here", "now!", "not this one" | the red pen points; it never decorates |
| Put the formula in the margin | `.sk-maths` beside the picture, with `§` references | the math is there for those who want it, out of the way for those who do not |
| Check, then move on | a question page after every two or three concepts | it shows the teacher what landed |
| Cross out the wrong idea | the `strike` decorator, then the right idea next to it | misconceptions do not leave unless named |
| Draw analogies as objects | a bucket, a scale, a ladder, from the sketch catalog | an object carries the idea home |
| Recap as a postcard | the `end` layout, three lines, signed | short enough to photograph |

## Worked example with steps

One picture, the steps beside it, each step revealed on click. Red notes sit on the drawing, in lowercase, at 28 px or larger.

```html
<section class="sk-slide" data-layout="split" data-notes="Do the first step on the board before revealing it.">
  <svg id="pct" data-draw viewBox="0 0 700 520" role="img" aria-label="A bar growing from 80 to 92"></svg>
  <div class="sk-stack" style="--gap:22px">
    <h2>Percent change: 80 to 92</h2>
    <p data-step="1"><b>1. Subtract.</b> new minus old: 92 − 80 = <span class="sk-figure">12</span></p>
    <p data-step="2"><b>2. Divide by the old one.</b> 12 / 80 = <span class="sk-figure">0.15</span></p>
    <p data-step="3"><b>3. Times 100.</b> <span class="sk-figure">+15%</span></p>
  </div>
</section>
<script>
Sketchy.onMount(function (root, C) {
  var svg = document.getElementById('pct'); if (!svg) return; svg.replaceChildren();
  Sketchy.variants(svg, function (p) {
    p.rect(80, 260, 400, 90, { fill: C.blue });                 // old: 80
    p.rect(80, 380, 460, 90, { fill: C.green });                // new: 92 (scale 5 px per unit)
    p.line(480, 240, 480, 490, { dash: '5 5' });
    p.text(510, 230, 'the extra 12', { note: true, size: 30 });
    p.arrow(560, 238, 520, 400, { stroke: C.red, width: 1.6 });
    p.text(90, 240, '80', { size: 34, mono: true }); p.text(90, 500, '92', { size: 34, mono: true });
  }, { seed: 'pct', tokens: C });
});
</script>
```

Register `onMount` hooks before `SketchyDeck.mount()` (or before `Sketchy.mount()` on a page). The hook clears its SVG first because the engine mounts again after fonts load and when the theme changes.

Red-pen notes: `.sk-note` in HTML, `{ note: true }` in the pen. They are terse, lowercase, and point at one place: "pull here", "now!", "carry the 1", "divide by THIS". One red note per page.

## Show the math in the margin

The margin carries the formula and its value; the page carries the picture.

```html
<aside class="sk-margin sk-maths">Σ the math<br>
  change = (new − old) / old<br>
  = (92 − 80) / 80 = <b>0.15</b> <span class="sk-sect">§ 3</span></aside>
```

On a slide `.sk-margin` pins it top right. On an explainer page, put an `aside.sk-maths` beside the paragraph. At most three lines; the `§ 3` points to a notes page at the end where the full derivation lives. Values are bold; at night they turn gold Courier automatically.

## Check your understanding

A question, then the answers one click at a time. Put the wrong answers first so the room commits before it sees the right one.

```html
<section class="sk-slide" data-layout="title">
  <div class="sk-sheet" data-sk="sheet">
    <span class="sk-kicker">Check</span>
    <h1>A price goes from 50 to 40. What changed?</h1>
    <p class="sk-line" data-step="1"><span data-sk="strike">−10%</span> <span class="sk-note">careful</span></p>
    <p class="sk-line" data-step="2"><span class="sk-figure">−20%</span>: 10 / 50, the old one</p>
  </div>
</section>
```

On an explainer page, hide the answer in `<details class="sk-sheet" data-sk="sheet"><summary>Show the answer</summary>...</details>`; the frame redraws when it opens.

## Misconception pages

Name the wrong idea, strike it in red, then show the right one on its own sheet. Use `compare`: left sheet is the myth, right sheet (revealed with `data-step`) is the fix.

```html
<section class="sk-slide" data-layout="compare">
  <header><span class="sk-kicker">A common mistake</span><h2>You cannot average two rates</h2></header>
  <div class="sk-sheet" data-sk="sheet"><h3>What people do</h3>
    <p><span data-sk="strike">(10% + 50%) / 2 = 30%</span></p></div>
  <div class="sk-sheet" data-sk="sheet" data-step="1"><h3>What is true</h3>
    <p>10 of 100 plus 5 of 10 is 15 of 110 = <span class="sk-figure">13.6%</span></p></div>
</section>
```

`data-sk="strike"` draws in red by default; the linter knows a decorator may cross its own text.

## Analogies as objects

| Idea | Object to draw (catalog name, see `sketches.md`) |
|---|---|
| a trade-off | `scale-balance` |
| a deadline, a time budget | `hourglass` |
| growth that compounds | `growth-plant` |
| a staged career or maturity model | `ladder-up` |
| connecting two systems | `bridge` |
| a decision point | `crossroads` or `signpost` |
| savings, reserves | `piggy-bank` |

Draw the object, label its parts in place with the pen, and say the mapping once in a sentence. Do not draw both the object and a flowchart of the same idea.

## The how-to page

Pictures left, numbered steps right. On an explainer page each step is one `.sk-split` row (it stacks under 720 px wide). In a deck, use `steps` (one picture per step) or `split` (one picture, steps beside it).

```html
<section class="sk-sheet" data-sk="sheet">
  <span class="sk-kicker">How to</span>
  <h2>File an expense claim in three steps</h2>
  <ol class="sk-stack" style="--gap:28px; padding:0; list-style:none">
    <li class="sk-split"><svg data-sketch="receipt" viewBox="0 0 140 110" style="max-width:240px" aria-hidden="true"></svg>
      <div><h3>1. Photograph the receipt</h3><p>The whole slip, flat, with the total readable.</p></div></li>
    <li class="sk-split"><svg data-sketch="invoice-stamp" viewBox="0 0 140 110" style="max-width:240px" aria-hidden="true"></svg>
      <div><h3>2. Attach it to the claim</h3><p>One receipt per line. <span class="sk-note">not a PDF of ten</span></p></div></li>
    <li class="sk-split"><svg data-sketch="coin-stack" viewBox="0 0 140 110" style="max-width:240px" aria-hidden="true"></svg>
      <div><h3>3. Submit by the 25th</h3><p>Paid with the next salary run.</p></div></li>
  </ol>
</section>
```

## Pacing

| Block | 45 minutes | 90 minutes |
|---|---|---|
| Hook (a question, a number, a picture) | 3 min, 1 page | 5 min, 1 page |
| Concepts, one per page | 3 concepts, 12 min | 5 concepts, 25 min |
| Worked example with steps | 1 example, 8 min | 2 examples, 15 min |
| Check pages | 2 checks, 5 min | 4 checks, 10 min |
| Practice (learners work, page stays up) | 12 min | 25 min, with a break at 45 |
| Recap postcard and next step | 5 min | 10 min |
| Pages in total | 10 to 14 | 18 to 25 |

Rule of thumb: one new concept every 4 to 5 minutes, a check after every second concept, and nothing new in the last 5 minutes.

## Accessibility

| Topic | Rule |
|---|---|
| Size | stage body 34 px, never under 20; explainer pages 19 to 22 px, never under 16. Labels inside drawings at least 28 px on stage. |
| Contrast | graphite on day paper is about 5.3:1, ink about 9:1. Red ink and `graphite-soft` are about 3.8:1: large text only (28 px and up). Fine print (`.sk-fine`, `.sk-small`) is full graphite, and `.sk-source` and `.sk-disclose` are 26 px on slides; still, put what a learner needs in body text, not in fine print. Night chalk on night paper passes easily. |
| Color | never the only signal: label series in place, add a word or a stamp next to red and green |
| Motion | the engine honors reduced motion (boil 2 fps, no page turns, counters show the final value). Never put information only in an animation. |
| Pictures | decorative sketches get `aria-hidden="true"`; a drawing that teaches gets `role="img"` and an `aria-label` that says what it shows |
| Language | set `lang` on `<html>`; for German and Arabic see [voice.md](voice.md). The handwriting covers Latin and Cyrillic; Greek letters, math symbols and other scripts fall back to a system font, so check the screenshots. |
| Reading order | steps reveal in `data-step` order; keep the DOM order the same as the reading order |
