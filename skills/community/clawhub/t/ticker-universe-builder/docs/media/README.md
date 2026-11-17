# README illustration

The dark [desktop image](universe-report.jpg) is designed for **880 px display width**,
using two columns, 17 px ticker labels and 16 px descriptions. The
[mobile image](universe-report-mobile.jpg) uses a **390 px single-column** design with
16 px ticker labels and 15 px descriptions. These are design targets, not fixed
GitHub README dimensions. Increasing export resolution alone does not enlarge text
when a wide image is scaled down.

Both images show **12 tickers across four US Medium theme excerpts**, with an
original short description beside **every ticker**. Each theme shows three selected
rows and discloses its full display-group count. The four excerpts cover compute/AI
hardware, megacap platforms, cybersecurity and power technology. Full reasoning remains in
the [generated Markdown](../../examples/us-medium/output/us-medium-2026-10-08.en.md).
Ticker identities, merged group counts and reasons were checked against that report
and its JSON. Featured themes are an editorial choice, not a live popularity ranking.

Source: [US Medium example](../../examples/us-medium/), version `803482441ee9`:
294 company tickers, 44 references, 51 company themes and 338 exported symbols.
Facts: 2026-10-08; historical price cutoff: 2026-10-06; captured: 2026-10-09.
[Editable HTML](universe-report.html) renders both layouts from the same presentation.
It is a README illustration, not an additional CLI output or product dashboard.

## Embed from the root README

Use repository-relative paths and descriptive alt text. The mobile source is selected
below a 600 px viewport; the desktop fallback is capped at 880 px. Link to the full
Markdown underneath so the image is not the only route to its information.

```html
<picture>
  <source media="(max-width: 600px)" srcset="docs/media/universe-report-mobile.jpg">
  <img src="docs/media/universe-report.jpg" width="880" alt="US Medium universe: 294 company tickers and 44 references, with four theme excerpts and descriptions for all 12 displayed tickers.">
</picture>
```

```markdown
[View the full universe and reasoning](examples/us-medium/output/us-medium-2026-10-08.en.md)
```

References: [GitHub image and relative-path documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images)
and [Primer Markdown image width rules](https://github.com/primer/css/blob/main/src/markdown/images.scss).
Local browser checks cover 900, 720 and 390 px viewport widths; no GitHub publication
or live README rendering is claimed. The TradingView still remains removed; its GIF
will be recorded by the user.
