# Business: numbers filed on stationery

Read for anything with numbers, money, plans, results or decisions. Every real number is filed on a piece of stationery, and each kind of stationery has one job. Layouts: [slides.md](slides.md). Classes: [components.md](components.md). All figures on this page are examples; never carry one into a real artifact.

## Which stationery for which number

| Stationery | Job | Business use | Build from |
|---|---|---|---|
| Postage slip | settle the account after the event | invoice, budget, plan vs actual | `.sk-doc.sk-receipt.sk-pinked` with `data-reveal="print"`, on a `ledger` slide |
| Signed headline figure | the one number of the slip | variance, saving, overrun | `.sk-figure` + `data-count` |
| Postmark | timestamp an event where it happened | milestone, launch, incident event | `svg[data-postmark]`; `Sketchy.postmark()` inside your own drawing |
| Rubber stamp | a categorical verdict | ON BUDGET, OVERDUE, APPROVED | `.sk-stamp`, `.is-green`, `.is-blue` |
| Outline stamp | a goal not yet earned | KPI not met yet | `.sk-stamp.is-unearned` |
| Envelope | the brief before the work | project brief, scope | `letter` slide |
| Registration label | the document's identity | report ID, ticket number | `.sk-rlabel` |
| Postage stamp | an allowance | budget, plan tier | `Sketchy.postage()` |
| Certificate | close the program | annual summary | `title` slide: stamps, slam, three facts |
| Dead letter office | failures kept on the record | incident log, lost deals | `board` slide of plates |
| Navigator's table | side-by-side audit | plan vs actual table | `.sk-table` with `.is-better`, `.is-worse` |
| Postcard | shareable summary | social card, thank-you | `.sk-postcard` (`end` slide or `templates/postcard.html`) |

## The postage slip

Words left, slip right. The brand line names the slip, the rows print one by one, the total follows a solid rule, the benchmark sits under it in soft graphite, the verdict stamp lands last. The slip is a `.sk-doc`: light paper with day ink, even in the night ledger.

```html
<section class="sk-slide" data-layout="ledger" data-duration="9">
  <div class="sk-stack" style="--gap:16px">
    <h2>Q3 came in under plan</h2>
    <div class="sk-figure" style="font-size:96px" data-count>−€184,000</div>
    <p class="sk-line">Nobody has asked for it back.</p>
  </div>
  <div class="sk-stack" style="--gap:18px">
    <div class="sk-doc sk-receipt sk-pinked" data-reveal="print">
      <div class="sk-receipt-brand">Postage slip · € thousands</div>
      <div class="sk-receipt-row"><span>Salaries</span><span>1,410</span></div>
      <div class="sk-receipt-row"><span>Cloud</span><span>212</span></div>
      <div class="sk-receipt-row"><span>Other</span><span>160</span></div>
      <div class="sk-receipt-row is-total"><span>IN ALL</span><span>1,782</span></div>
      <div class="sk-receipt-row is-bench"><span>June plan</span><span>1,966</span></div>
    </div>
    <span class="sk-stamp is-green" data-slam style="--delay:1000ms">Under plan</span>   <!-- outside the receipt, so it does not print as a line -->
  </div>
  <p class="sk-source">Ledger close, 3 Oct 2026</p>
</section>
```

| Row rule | Why |
|---|---|
| One `.sk-receipt-row` per line: label `<span>`, value `<span>`; the dotted leader fills itself | values line up on the right edge without padding |
| Currency and scale once, in the brand line or the total label (`IN ALL, €`) | eight euro signs are noise; the linter also counts each digit group as a word, so `1,410,000` costs three of the 40 |
| `.is-total` after the items: solid rule, bold | the sum is the record |
| `.is-bench` under the total, in soft graphite | the comparison is always on the slip |
| The stamp sits next to the receipt, not inside it | inside, it would print as a line and then slam |
| Split rows by owner when two parties caused the cost | attribute every cost |
| The joke line goes in Caveat next to the slip, never inside a row | the record stays clean |

The headline figure is signed and counts up (900 ms) as the slip prints. A deck uses one slip per page; a report may stack two.

## Postmarks for milestones

A postmark marks an event where it happened. The standalone one needs no script:

```html
<svg data-postmark="LAUNCHED · BERLIN|25 OCT 2026" data-postmark-center="v2.0" data-cancel data-draw
     viewBox="0 0 160 110" style="width:320px" role="img" aria-label="Postmark: launched in Berlin, 25 Oct 2026"></svg>
```

`data-postmark` is the top arc and the bottom arc, split by `|`: the event and place, then the date, both uppercase. `data-postmark-center` is a version, an amount or `P.O.`. `data-cancel` adds wavy cancellation lines on the left. It prints in red ink, so it is the one red mark of its page.

On a timeline or a chart, draw postmarks inside your own drawing so they sit beside the event: `Sketchy.postmark(p, x, y, r, 'SHIPPED · V1.4', '3 JUN 2026', { color: C.graphite })` within `Sketchy.variants()` (see the timeline in [slides.md](slides.md)). Routine milestones go in graphite; red ink is for the one that matters. Never place a postmark on top of the line.

## Rubber stamps: earned and not yet

```html
<span class="sk-stamp">On budget</span>                                   <!-- earned verdict, red ink -->
<span class="sk-stamp is-green">Shipped</span>                            <!-- done -->
<span class="sk-stamp is-blue">Waiting</span>                             <!-- parked, informational -->
<span class="sk-stamp is-unearned">On time</span>                        <!-- not yet earned: dashed, 50% -->
<span class="sk-stamp is-big" data-slam style="--delay:900ms">Approved</span>  <!-- the page verdict -->
```

Write stamp words in sentence case; the CSS sets capitals. One to three words. One slammed stamp per page; the rest sit still. When a goal is met, drop `is-unearned` and pick its ink.

## The envelope as brief

```html
<section class="sk-slide" data-layout="letter">
  <div class="sk-sheet" data-sk="sheet">
    <div class="sk-row"><span class="sk-rlabel"><b>R</b><span>No. 0042<small>Brief</small></span></span></div>
    <h2>for the platform team</h2>
    <p class="sk-letter-row"><b>To:</b> four engineers, one product manager.</p>
    <p class="sk-letter-row"><b>Contents:</b> checkout errors under 0.5% by 31 Jan.</p>
    <p class="sk-letter-row"><b>Precedent:</b> search, 11 weeks, 2025.</p>
    <p class="sk-letter-hint">Budget 12 engineer-weeks; benchmark 0.6%.</p>
    <div class="sk-row" style="justify-content:center; --gap:16px">
      <span class="sk-stamp is-unearned">On time</span>
      <span class="sk-stamp is-unearned">On budget</span></div>
    <div class="sk-letter-actions"><span class="sk-btn is-accent" data-sk="button">Start</span></div>
  </div>
</section>
```

The registration label (ID), To (who), Contents (the goal, measurable), Precedent (what was done before), the rules and the benchmark in the hint, the goals as unearned stamps, one main action. At the end of the project, repeat the page with the earned stamps inked.

## Registration label, certificate, dead letter office

**Registration label** (document ID): `<span class="sk-rlabel"><b>R</b><span>No. 0007<small>Report</small></span></span>`. It scales up on slides by itself. Put it once, top left of a brief, a report or a slip. Inside a sheet or a `.sk-stack` (both grids), wrap it in `<div class="sk-row">`, or it stretches to the full width. Its red block is postal red (`--sk-slip-red`), so keep the other marks on that page graphite.

**Certificate** (annual summary): a `title` slide. Kicker with the ledger number, the year in one line, a row of quarter stamps (earned inked, missed with `.is-unearned`), three facts in `.sk-figure`, then one big slammed stamp such as `Year closed`. It reads best in the night ledger, where every figure turns gold.

**Dead letter office** (incident log, lost deals): a `board` slide, one plate per failure. Each plate: the ID on tape, a stamp chip, one line with the date, the amount and the reason. Never leave a failure off this page to make the quarter look better.

```html
<div class="sk-plate sk-stack"><span class="sk-tape">DEAL_0417</span>
  <span class="sk-stamp is-blue">Returned</span>
  <p><span class="sk-figure">€84,000</span> · lost 2 Sep · a cheaper quote, by 9%</p></div>
```

## Navigator's table: plan vs actual

```html
<div class="sk-sheet" data-sk="sheet">
  <table class="sk-table">
    <tr><th>Item</th><th>Plan</th><th>Record</th><th>Gap</th></tr>
    <tr><td>Orders</td><td>1,100,000</td><td>1,240,600</td><td class="is-better">+140,600</td></tr>
    <tr><td>Cost per order</td><td>€2.41</td><td>€2.26</td><td class="is-better">−€0.15</td></tr>
    <tr><td>On time</td><td>95.0%</td><td>97.1%</td><td>+2.1 pts</td></tr>
    <tr><td>Hub opening</td><td>1 Mar</td><td>12 Apr</td><td class="is-worse">+42 days</td></tr>
  </table>
</div>
```

Columns: the item, the plan, the record, the signed gap. The first column is handwritten, the rest are Courier and right aligned. Mark gap cells only: `.is-better` in green ink, `.is-worse` in red ink. Red is still the one thing, so mark only the worse gap that needs a decision; other gaps keep their sign and stay graphite.

## Storytelling rules

1. **Always a benchmark.** Every result sits next to the plan, last year, a competitor or the industry figure the user gave. A number alone is not news.
2. **Attribute every cost.** Split it by who caused it; name owners on rows and plates.
3. **Convert units into something you can picture.** "2.4 TB a day" becomes "a full laptop drive every five hours"; check the conversion and show it in the margin math.
4. **Annotate in place, not in a legend.** Label the line where it ends, the bar where it stands.
5. **Print the distortions** with `.sk-disclose`: truncated axes, enlarged objects ("drawn 6x life size"), log scales. Bars start at zero.
6. **Failures are filed, not hidden.** They go to the dead letter office with a date and a reason.
7. **Plan is dashed, record is solid** on every chart and drawing.
8. **The joke goes next to the number, never inside it.**
9. **Reveal like a receipt:** lines print, the total counts up, the stamp lands, then the buttons.

## Number formatting

| Quantity | Rule | Example |
|---|---|---|
| Thousands | separate from 1,000 up (German: see voice.md) | 1,240,600 |
| Under 100 | one decimal | 43.4, 97.1% |
| Large, in prose | round and say "million" | 1.24 million parcels |
| Signs | `+` gain, `−` loss (U+2212, never a hyphen), `±` no change within rounding | +18.4%, −6.2%, ±0.0 |
| Change of a percentage | in points | +2.1 pts |
| Dates | day, short month, year; uppercase on stamps and postmarks | 25 Oct 2026, 25 OCT 2026 |
| Ranges | words, not a dash | Jul to Sep, 3 to 5 days |
| Estimates | dashed in drawings, "est." or "about" in text | about 1,200 (est.) |
| Units | always; a space before units, none before % | 41 min, 2.3 GB, 97.1% |

`data-count` keeps prefix, suffix, separators, decimals and signs, and always writes the true minus sign. It reads `<html lang>`: in comma locales (de, fr and others) `97,1 %` and `1.240.600` count correctly. Type U+2212 in static text too.

## Honesty

- Use only figures the user gave or that you can cite. Put the citation in `.sk-source`.
- A missing figure is written `—` with a fine-print note naming who will supply it and when, or the slide changes. Never a plausible guess.
- The linter fails on `TODO`, `TBD`, `xxx`, `lorem` and `[insert`. Do not ship them, and do not dodge the linter with other filler.
- Mark estimates as estimates (dashed, "est."), state rounding ("rounded to the nearest €1,000"), and keep units on every number.
- When a template's example figures remain anywhere, the artifact is not finished.
