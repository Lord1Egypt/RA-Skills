# Slides

Read when building any deck. Every layout here is styled by the CSS block inside `engine/sketchy-deck.js`; `templates/deck.html` is a worked 12-slide example. Look and values: [style-dna.md](style-dna.md). Words: [voice.md](voice.md). Numbers: [business.md](business.md).

## The stage

Each slide is a fixed **1920 x 1080 px** stage, scaled to the window. Author in px. Slide padding is 92 px top, 120 px sides, 104 px bottom; the corner overlays sit 34 to 48 px from the edges.

```html
<html lang="en" class="sk" data-theme="day">
<body class="sk">
<main class="sk-deck" data-seed="q4-board-update" data-transition="page" data-music="sketchbook">
  <section class="sk-slide" data-layout="title" data-duration="6" data-notes="What I say here.">...</section>
</main>
<script src="engine/sketchy.js"></script>
<script src="engine/sketches.js"></script>
<script src="engine/sketchy-deck.js"></script>
<script>SketchyDeck.mount();</script>
```

`data-seed` is required (the linter warns without it): it fixes every wobble, the sky and the music. `data-sky="stars|dust|plain"` sets the specks behind the pages. `data-draw="off"` stops pictures tracing themselves in.

## The title is the point

| Topic (no) | Point (yes) |
|---|---|
| Q3 results | We delivered more, for less |
| Churn analysis | Churn halved after we cut the setup call |
| Roadmap | Two bets in Q1, one waits for data |
| Incident 4471 | A full disk took checkout down for 41 minutes |

If the title could sit on anyone's deck, rewrite it until it could only sit on this one.

## Budgets

| Item | Budget | Why |
|---|---|---|
| Body text | 40 words per slide (lint warns) | a slide is read in the time it is shown |
| Bullets | 6 at most, 3 is better | a fourth bullet usually repeats one of the first three |
| Title | 3 to 9 words, one line | the point, said once |
| Protagonist | one picture, number or chart | two protagonists split the eye |
| Red | one red thing | see style-dna rule 3 |
| Body size | 34 px on stage, never under 20 | read from the back of the room |
| Deck length | 6 to 20 slides; about one minute per slide live | a board update runs about 10, a lecture 15 to 25 |

## Layouts

| `data-layout` | Use when | The CSS expects |
|---|---|---|
| `cover` | first page; the closed sketchbook | `.sk-cover` > `.sk-cover-inner` > `.sk-label`, optional `.sk-door`, `.sk-cover-foot` |
| `title` | the one-line story of the deck | one `.sk-sheet` with `.sk-kicker`, `h1` (112 px), a line |
| `section` | chapter break | `.sk-chapter` (red), `h1` (150 px), optional line |
| `letter` | a request, a brief, a problem stated as mail | `.sk-sheet` with `.sk-letter-kicker`, `h2`, `.sk-letter-row`, `.sk-letter-hint`, `.sk-letter-actions` |
| `split` | a picture and its explanation | two children: picture (760 px column) then words; `.is-flipped` puts words first |
| `steps` | a how-to in 2 to 4 steps | `header`, `.sk-step-list` (`--cols`), `.sk-step` each with a sketch, `h3`, `p` |
| `chart` | one figure carries the slide | `.sk-corner` title, `figure.sk-chart`, `.sk-source` |
| `big-number` | one number is the news | `.sk-kicker`, `.sk-number`, `.sk-number-label`, `.sk-number-bench` |
| `compare` | plan vs record, before vs after | `header`, then two `.sk-sheet` |
| `quote` | one sentence from a real person | `blockquote`, `cite` |
| `timeline` | events in order | `header`, then one drawn `svg` |
| `ledger` | the bill: words left, a printed slip right (760 px) | `.sk-stack`, then a `.sk-doc.sk-receipt` with `data-reveal="print"` and its stamp ([business.md](business.md)) |
| `board` | decisions to take, one plate each | `.sk-corner`, `.sk-plates` (`--cols`) of `.sk-plate` |
| `end` | what was decided, signed | one `.sk-postcard` |

## Skeletons

The skeletons not shown here are in `templates/deck.html`, filled in.

```html
<section class="sk-slide" data-layout="section">
  <span class="sk-chapter">Chapter II</span><h1>What went wrong</h1>
</section>

<section class="sk-slide" data-layout="split">
  <svg data-sketch="hourglass" viewBox="0 0 140 110" style="width:700px" aria-hidden="true"></svg>
  <div class="sk-stack" style="--gap:18px"><h2>Why it took a week</h2>
    <p data-step="1"><b>1. Nobody owned it.</b> Three teams, no name on the ticket.</p></div>
</section>

<section class="sk-slide" data-layout="chart">
  <div class="sk-corner"><span class="sk-corner-title">Refunds fell after the new form</span>
    <span class="sk-corner-hint">refunds per 1,000 orders, monthly</span></div>
  <figure class="sk-chart" data-chart='{"type":"bar","title":"Refunds","unit":"per 1,000","data":[["Jul",14],["Aug",9]]}'></figure>
  <p class="sk-source">Order system export, 1 Oct 2026</p>
</section>

<section class="sk-slide" data-layout="timeline">
  <header><span class="sk-kicker">2026</span><h2>Three releases shipped, one waits</h2></header>
  <svg id="tl" data-draw viewBox="0 0 1680 360" role="img" aria-label="Releases in March, June and September; December planned"></svg>
</section>
<script>
Sketchy.onMount(function (root, C) {                 // register before SketchyDeck.mount()
  var svg = document.getElementById('tl'); if (!svg) return; svg.replaceChildren();
  Sketchy.variants(svg, function (p) {
    p.line(40, 200, 1240, 200, { width: 2.4 });                  // record: solid
    p.line(1240, 200, 1640, 200, { dash: '8 8', width: 2 });     // plan: dashed
    [[200, 'Mar'], [620, 'Jun'], [1010, 'Sep']].forEach(function (m) {
      p.dot(m[0], 200, 16); p.text(m[0], 266, m[1], { anchor: 'middle', size: 40 });
    });
    p.circle(1460, 200, 96, { stroke: C.red, dash: '4 5', width: 2.2, passes: 1 });  // the target
    p.text(1460, 124, 'Dec, planned', { anchor: 'middle', size: 38, note: true });
  }, { seed: 'tl', tokens: C });
});
</script>
```

Chart specs belong to `charts.md`; sketch names to `sketches.md`. Never draw a chart by hand when a spec can carry the data.

## Overlays on any slide

| Class | Place | Job |
|---|---|---|
| `.sk-corner` with `.sk-corner-title`, `.sk-corner-task`, `.sk-corner-hint` | top left | the HUD title pattern: point (40 px), what to look at (31 px), a hint (26 px) |
| `.sk-margin.sk-maths` | top right | margin math: right aligned, `<b>` or `.val` for values, `.sk-sect` for red `§ 2` references |
| `.sk-disclose` | bottom left | scale disclosure: "bars drawn from zero; the 2023 hub is drawn at half width" |
| `.sk-source` | bottom right | source line; the engine prints the red `§` itself, do not type it |

```html
<aside class="sk-margin sk-maths">Σ the math<br>payback = 2.1 M / 74 k = <b>28 months</b> <span class="sk-sect">§ 1</span></aside>
<p class="sk-disclose">Hub sizes drawn to scale. Trucks drawn 3x life size.</p>
<p class="sk-source">Lease offer, 12 Oct 2026; fuel invoices Jul to Sep</p>
```

## Reveals, counters, stamps

| Markup | Does | Notes |
|---|---|---|
| `data-step="1"`, `"2"` ... | hidden until the next click or key; sorted by number | going back to a slide shows all its steps |
| `data-count` on a figure | counts from 0 in 900 ms, cubic out, after 300 ms | keeps prefix, suffix, separators, decimals, `+`, `−`, `±` |
| `data-count-from`, `-delay`, `-ms` | start value, delay, duration | e.g. `data-count-from="1240600"` for a small change |
| `data-reveal="print"` on a box | its children print one by one: 95 ms apart after 180 ms | the receipt; each child is one line |
| `.sk-stamp[data-slam]` + `style="--delay:900ms"` | slams from 1.8x in 360 ms when the slide arrives | default delay 600 ms; land it after the last receipt line |
| `data-reveal="sheet"` + `--delay` | the element arrives like a sheet | for a second sheet on the same slide |
| `.sk-postcard[data-reveal]` | the postcard flies in, 420 ms | end slides |
| `svg[data-draw]` | traces itself in on first arrival | sketches and charts do this already |

Time the slam after the print: in a slip with 6 lines the last line starts at 180 + 5 x 95 = 655 ms and lands 380 ms later, at 1035 ms, so use `--delay:1100ms`.

## Notes, transitions, durations

- Speaker notes: `data-notes="..."` or a child `<aside class="sk-notes-speaker">`. They go to the presenter view (`p`) and to PPTX notes. Write what you will say, not what the slide says.
- `data-transition` on the deck or a slide: `page` (default turn), `slide`, `fade`, `none`. Leaving the cover always opens the book.
- Clicks: a `.sk-door` on a slide, or any element with `data-next`, turns to the next step or page. Nothing else on a slide reacts to clicks, so put `data-next` on the one main button.
- `data-duration` in seconds (default 6) drives `?autoplay` and video. Steps reveal evenly inside the first 60% of the duration, so a slide with 3 steps needs at least 7 s.
- Video pacing: cover 4 to 5 s, a big number 5 s, a chart 8 to 10 s, a ledger with stamps 9 s, end 6 s. `data-music-section` on a slide marks a music change (`sound.md`).
- URL modes: `?slide=3`, `?static`, `?print`, `?overview`, `?autoplay`, `?presenter`. Keys: arrows, space, Home, End, `o`, `f`, `p`, `s`.

## Storyboard patterns

Write the page list first (layout, point, picture or figure, source), then build.

**Board update.** Answer first, evidence second, ask last.

| # | Layout | Says |
|---|---|---|
| 1 | cover | the period and the audience |
| 2 | title | the answer in one line |
| 3 | big-number | the number they care about, with its benchmark |
| 4 | chart or compare | the evidence: plan vs record |
| 5 | ledger | what it costs, printed as a slip |
| 6 | board | the decisions, one plate each |
| 7 | end | what was decided, stamped |

**Pitch.** Problem as a letter, then the picture, the number, plan vs record, the ask.
`cover` → `letter` (the problem, To/Contents) → `split` (the product as a drawing) → `big-number` (the one metric) → `compare` (plan vs record so far) → `ledger` (the ask, itemized) → `end`.

**Lecture.** Hook, concept, worked example, check, recap ([education.md](education.md)).
`cover` → `quote` or `big-number` (the hook) → `split` (the concept, picture first) → `steps` (worked example) → `title` with `data-step` answers (check question) → `end` (recap postcard).

**Product launch.** `cover` → `title` (what changes for the user) → `split` (the thing, drawn) → `steps` (how to use it in three moves) → `big-number` (the measured gain, with benchmark) → `timeline` (what ships when; future dashed) → `end`.

**Incident review.** Facts before causes, failures filed, not hidden.
`title` (what broke, how long, who noticed) → `timeline` (postmarks at each event) → `split` (the cause, drawn) → `compare` (expected vs actual) → `board` (the dead letter office: every failed step with its date and one line) → `board` (fixes: keep, remove, wait) → `end`. The dead letter office page is in [business.md](business.md).
