---
name: draw
description: Build a URL, get an SVG chart — pie, bar, line, radar, gauge, sankey, QR, any ECharts chart, from x-cmd.com/draw. No install, no key, no stored data. Embed as [![chart]](/draw/explore) — click to explore/edit. The URL is the data — humans see the story, agents get exact numbers. No vision tokens.
version: 1.0.1
metadata:
  openclaw:
    emoji: 📊
    homepage: https://x-cmd.com/draw
---

# draw — charts as URLs

`https://x-cmd.com/draw?type=pie&labels=TS,Py,Go&values=4821,2312,980&title=Stars` — open it and you get an SVG chart. No install, no key, no state: **the URL is the data**, so links are self-describing, shareable, and cacheable forever. Always build URLs on **`https://x-cmd.com/draw`**.

Rendering is **stateless**: every chart is derived from the URL alone — no database, no server-side data retention (edge caches hold finished responses briefly, like any CDN).

## The embed pattern — READMEs, issues, PRs, blogs & chat

[![Stars by language](https://x-cmd.com/draw?type=pie&labels=TS,Py,Go,Rust&values=4821,2312,980,645&title=Stars%20by%20language)](https://x-cmd.com/draw/explore?type=pie&labels=TS,Py,Go,Rust&values=4821,2312,980,645&title=Stars%20by%20language)

```markdown
[![chart](https://x-cmd.com/draw?...)](https://x-cmd.com/draw/explore?...)
```

Concrete moments it wins:

- **README** — put the language mix or downloads trend right under your badges; visitors see the picture, click, and poke at the real numbers.
- **Issue** — attach the latency spread of that bug instead of a table of numbers; the maintainer hovers, spots the outlier, edits the data to test a theory, and pastes the new URL back into the thread.
- **PR description** — before/after benchmarks side by side; a reviewer notices a typo'd value, fixes it in explore, and re-posts the corrected chart — no re-run asked for.
- **Blog post** — a chart in the article stays interactive: readers question a number, click, and re-cut the data their own way instead of taking your word for it.
- **Chatroom** — drop the link in Discord/Slack: the preview renders the chart, and instead of pasting numbers back and forth, teammates click, tweak, and return a new chart URL.
- **Reports & notes** — anywhere Markdown renders.

The image is the rendered SVG; the link opens the **explore webapp** — hover the data, tweak params, edit the values, copy the new URL. `/draw/explore` takes the exact same params as `/draw`; the ECharts layer explores at `/draw/explore/echarts?d=<urlencoded option>`. Works in GitHub-flavored Markdown and plain HTML.

## Agents read the URL, not the pixels

A draw embed costs an agent **zero vision tokens**. The data is in the URL itself, and every rendered SVG carries a `<metadata>` block with the full dataset — so an agent that meets a chart in an issue or PR parses the link and knows the chart *exactly*: type, labels, values, style, version. No image reading, no OCR guessing, no pixel-counting — and no hallucinated numbers, because the values are plain text, not something to squint at.

## Pick a chart by data shape

| Data shape | type | Copy-paste example |
|---|---|---|
| Part of a whole | `pie` | `type=pie&labels=TS,Py,Go&values=4821,2312,980` |
| Compare categories | `bar` | `type=bar&labels=Mon,Tue&values=120,180` |
| Compare, multiple series | `bar` | `type=bar&labels=Mon,Tue&series=a:12,18&series=b:9,10` |
| Ranking / long labels | `hbar` | `type=hbar&labels=TS,Py,Go&values=4821,2312,980` |
| Trend over time | `line` / `area` | `type=line&labels=Jan,Feb,Mar&values=3,7,5` |
| Multi-dimension score | `radar` | `type=radar&t=evil&labels=speed,eco,dx&series=a:8,9,7&series=b:6,7,8` |
| Single KPI / progress | `gauge` | `type=gauge&title=Pass rate&value=87&max=100` |
| Two numeric variables | `scatter` | `type=scatter&x=1,2,3&y=4,5,6` |
| Bars + line together | `combo` | `type=combo&labels=Mon,Tue&series=dl:120,180&line=growth:5,8` |
| Flow / funnel | `sankey` | `type=sankey&labels=Ads,Web,Buy&links=Ads>Buy:30;Web>Buy:20` |
| QR code | `qr` | `type=qr&d=https://x-cmd.com/draw` |

## Shared parameters

- `title=` chart title · `unit=` value unit
- `t=<family>` style family (see below) · `scheme=light|dark|auto` (auto follows the viewer's system)
- `w=` / `h=` size in px (200–1600 / 140–1200; defaults per style)
- `num=all|peak|none` value labels (default per style; ignored by radar/gauge/sankey/qr)
- `v=N` pin a render version (1-day cache); omit for latest (short cache)

Per-type limits worth knowing: pie ≤100 slices (>9 auto-merge into *Other*), bar ≤30 groups × 6 series, line/area ≤60 points, scatter ≤200 points, radar 3–12 axes, sankey ≤24 nodes.

## Style families (`t=`)

Each type has defaults; `t=` swaps the look. Highlights: pie `evil` `market-mono` `revenue`; hbar `xcmd-issue` (butterfly open-vs-closed) `rank`; line `evil-glow` (glow) `opendata` (end labels); area `star` (hand-drawn) `pixel`; gauge `gradient`; sankey `pipeline`. Full table: <https://x-cmd.com/draw> demo page.

## Anything else: the ECharts layer

For charts the core does not cover (heatmap, boxplot, candlestick, sunburst, funnel, graph, native gauge, …) send a whole ECharts option, urlencoded, in `?d=`:

```
https://x-cmd.com/draw/echarts?d=%7B%22xAxis%22%3A%7B%22type%22%3A%22category%22%2C%22data%22%3A%5B%22A%22%2C%22B%22%5D%7D%2C%22yAxis%22%3A%7B%22type%22%3A%22value%22%7D%2C%22series%22%3A%5B%7B%22type%22%3A%22bar%22%2C%22data%22%3A%5B1%2C2%5D%7D%5D%7D
```

Minimal options work (cartesian series get axes auto-injected); the shared `w/h/t/scheme/v` params apply; the option may not exceed 16,000 chars. Charts come back in the same house style — palette, fonts, light/dark — because style tokens are injected as defaults your option can override.

## Errors

Invalid params return 4xx **plain text with a corrective example** — read the message, fix the URL, retry. Values must be ≥0 (scatter may be negative); text never overlaps (labels that do not fit are dropped as a layer).

## Offline / no-network fallback

The same params render locally, no network:

```sh
npx @x-cmd/draw --type pie --labels A,B --values 3,2 --out pie.svg
npx @x-cmd/draw echarts '{"series":[{"type":"bar","data":[1,2,3]}]}'   # ECharts layer: inline JSON | file | stdin
npx @x-cmd/draw --type pie --labels A,B --values 3,2 --out pie.png    # PNG raster via the CLI
```

Library: `import { draw } from '@x-cmd/draw'` (npm) or `jsr:@x-cmd/draw` (Deno) — same params, same output, synchronous.

---
Source & self-hosting: <https://github.com/x-cmd/draw> · Apache-2.0. Docs: <https://x-cmd.com/draw>.
