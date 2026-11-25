# Charts

Hand-drawn charts with exact numbers. Load `engine/sketchy-charts.js` after `engine/sketchy.js`, put a spec on a figure, and `Sketchy.mount()` draws it. Every chart also writes a hidden table with the exact values and puts `data-*` attributes on each mark, so screen readers, search and `scripts/lint.mjs` can read the numbers.

```html
<figure class="sk-chart"><script type="application/json">
{"type":"bar","title":"Revenue by quarter, 2026","unit":"€k","data":[["Q1",118],["Q2",131],["Q3",127],["Q4",162]]}
</script></figure>
```

`data-chart='{...}'` on the figure works too. `SketchyCharts.render(figure, spec)` draws from a script object. Charts redraw on resize and on a theme change, and the same spec at the same width always draws the same lines.

## Pick the chart from the message

Write the sentence the chart has to prove first. If the answer is one number, it is not a chart.

| The message | Type |
|---|---|
| One figure and how it moved | `bignumber` |
| Compare a few categories | `hbar` (sorted, long labels) or `bar` |
| Change over a few periods | `bar` (quarters, months) |
| A trend over many points, or against a plan | `line` |
| A total over time and what it is made of | `area` (stacked) or `stacked` |
| Two groups side by side per category | `grouped` |
| Parts of one whole, at most five | `pie`, `donut`, or `waffle` for a count of people |
| Before and after for a few items | `slope` |
| How two measures relate | `scatter` with `"trend": true` |
| Steps where people drop out | `funnel` |
| How full, against a limit | `gauge` |
| Small counts you can tick off | `tally` |
| Dates and milestones | `timeline` |
| An invoice, a bill, a cost breakdown | `ledger` |

## Spec fields

Common to every type:

| Field | Meaning |
|---|---|
| `type` | one of the types above |
| `title`, `subtitle` | the claim and its scope; the title says what the chart shows, in words |
| `unit` | `"€k"`, `"%"`, `"h"`; `""` for plain counts (a missing unit gives a console warning) |
| `data` | rows: `[["Q1", 118], ...]`, or `[{ "label": "Q1", "value": 118 }]`, or `{ "Q1": 118 }` |
| `series` | names for the value columns of each row (`["Licences", "Services"]`), or objects `{ "name", "role", "data" }` |
| `x`, `y` | axis settings: `{ "label", "unit", "min", "max" }`; `x` may also be the list of categories |
| `format` | `{ "locale": "de-DE", "decimals": 1, "currency": "EUR", "prefix", "suffix" }`, or just a locale string |
| `highlight` | one label (or index) drawn in red: the one thing to look at |
| `annotate` | `[{ "at": "Q3", "text": "launch slipped", "color": "red" }]`; for a line, `"at": { "series": "actual", "at": "Mar" }` |
| `target` | a goal: `150` or `{ "value": 150, "label": "plan" }`, drawn as a red dashed line |
| `benchmark` | a reference: `{ "value": 120, "label": "industry" }`, drawn as a blue line |
| `source` | shown under the chart after a red § mark |
| `math` | `true` writes the calculation behind the headline; or a list of lines such as `"Δ = 41.2% − 36.5% = +4.7 pts §1"` |
| `sort` | `"desc"` (default for plain categories), `"asc"`, `"none"` (default when labels carry an order: quarters, months, years, stages, answer scales) |
| `max` | top of the value axis; it can only extend the axis, never cut a bar |
| `forecastFrom` | label from which values are estimates: dashed and lighter from there |
| `height`, `fit` | height in px, or `true` to fill a figure that has a CSS height |
| `seed` | fixes the wobble; defaults to the title |

Per type:

- `line`, `area`: series `role` gives the line grammar. `actual` is solid pencil (gold ink at night), `plan`, `forecast`, `target`, `budget` are dashed, `benchmark` is blue, `old` is faint and dashed. With an actual and a plan or benchmark series, the headline prints both and the signed gap.
- `pie`, `donut`: at most five slices; the rest becomes "other" and the footnote names what is in it. `total` (or unit `%`, meaning 100) is the whole. `center`, `centerLabel` for the donut hole, `show: "value"` to print amounts instead of shares.
- `scatter`: `data` rows `[x, y, "label"]`; `trend: true` adds a least-squares line with r².
- `slope`: rows `["Starter", 6.8, 4.1]` with `series: ["before", "after"]`.
- `waffle`: shares of 100 squares, rounded so they add up exactly; the note says so when rounding happened.
- `gauge`: `max` is the full tank, `target` the red mark; rows may carry their own mark as a third value.
- `timeline`: `data` items `{ "date": "2026-11-16", "label": "Public launch", "place": "Berlin", "figure": "v1", "note": "18 learners", "done": true }`; `now` draws today in red and dashes the future. Milestones are postmarks: place on the top arc, date on the bottom arc, figure in the center.
- `funnel`: stages in order; each gap shows the conversion, the biggest drop is marked in red.
- `bignumber`: `value`, `label`, `compare: { "value", "label" }` (or `benchmark`, `target`), `good: "up"` or `"down"` to color the change.
- `ledger`: rows `{ "label", "value" }` or `{ "label", "qty", "price" }`; `tax: { "rate": 0.19, "label": "VAT" }`, `totalLabel`, `meta`, `note`, `benchmark`, `stamps: [{ "text": "Paid" }, { "text": "On time", "earned": false }]`.

## Honesty rules (the code enforces them)

- Bars and areas start at zero. A `y.min` above zero is ignored with a console warning.
- One axis. `y2`, `dualAxis` or a series with `axis: "right"` is drawn on the single axis with a warning. Show two measures as two charts, or index both to 100.
- No 3D. `3d`, `depth` and `perspective` are ignored.
- A pie adds up to its whole. Short of it, the rest is drawn as "not accounted for". Over it (answers with several choices), the chart is drawn as horizontal bars.
- A line that does not start at zero breaks its axis and prints "axis starts at …" in red.
- A ledger computes its own totals. A given `total` that disagrees is reported and the computed one is printed.
- A funnel stage larger than the one before, a tally above 120 marks and a gauge value outside its range all warn.
- Every warning also lands in `data-sk-warn` on the figure. Read the console before you ship.

Numbers follow one format: separators for thousands, one decimal under 100, whole numbers from 100, rounded to the hundred above 10,000, "1.42 million" above a million, signs as + and − (U+2212). Percentage changes of a percentage are printed in points (`+4.7 pts`). The hidden table keeps the exact values.

## Annotation patterns

- The red pencil is for the one thing: `highlight` one item, or one `target`, or one note. Three red things is no red thing.
- Notes sit in place with a curved arrow ("launch slipped two weeks", "new mobile app"), not in a legend. Keep them under six words.
- Margin math: `"math": true` adds "Σ show the math" under the chart with the calculation and red § references. Use it whenever the headline is a computed number.
- Dashed means plan, solid means what happened. Do not dash a line for decoration.
- Units go on the axis caption or on the values, once.

## Examples

A trend against a plan and a benchmark:

```json
{"type":"line","title":"Weekly active learners","unit":"",
 "series":[
  {"name":"actual","role":"actual","data":[["Aug",1190],["Sep",1260],["Oct",1340]]},
  {"name":"plan","role":"plan","data":[["Aug",1150],["Sep",1200],["Oct",1250]]},
  {"name":"cohort average","role":"benchmark","data":[["Aug",900],["Sep",930],["Oct",950]]}],
 "annotate":[{"at":{"series":"actual","at":"Aug"},"text":"new mobile app"}],
 "source":"Product analytics"}
```

One number with its comparison and the math:

```json
{"type":"bignumber","title":"Gross margin","value":41.2,"unit":"%","label":"Q3 2026",
 "compare":{"value":36.5,"label":"Q2"},"good":"up","math":true}
```

A paid invoice:

```json
{"type":"ledger","title":"Invoice No. 0042","meta":"25 Oct 2026 · due 8 Nov 2026","unit":"€",
 "data":[{"label":"Workshop day","qty":3,"price":560},{"label":"Travel","value":138.4}],
 "tax":{"rate":0.19,"label":"VAT"},"stamps":[{"text":"Paid"}]}
```

A plan with today marked:

```json
{"type":"timeline","title":"Course launch plan","now":"2026-10-25","highlight":"Public launch",
 "data":[{"date":"2026-06-02","label":"Kick-off","place":"Berlin"},
         {"date":"2026-11-16","label":"Public launch","figure":"v1"}]}
```

## Motion

`SketchyCharts.drawOn(figure)` and `Sketchy.drawOn(figure)` trace the outlines, then shade the fills, then fade in the labels. Figures count up without moving the layout, a ledger prints row by row and its stamps land one after the other. Nothing moves with `?static`, `?print` or reduced motion. While a chart draws, one boil variant is held so the lines do not flicker.

## Check before you ship

Run `node skills/sketchy/scripts/lint.mjs page.html` and read the console. `dev/charts-test.html` shows every type with realistic data, in both themes.
