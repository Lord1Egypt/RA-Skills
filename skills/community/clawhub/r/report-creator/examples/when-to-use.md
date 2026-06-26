# When To Use

Use `kai-report-creator` when the user needs a single-file HTML report, business summary, research document, or KPI dashboard.

- `/report --plan "AI 行业趋势报告"` — create a `.report.md` outline before rendering.
- `/report --generate report-ai.report.md` — render approved IR into HTML.
- `/report --from notes.md` — turn source notes into a report.
- `/report --from https://example.com/research` — summarize a source page into report structure when browsing/source extraction is available.
- `/report --review report.html` — run the one-pass report review checklist on an existing HTML report.
- `/report --themes` — preview built-in report themes.
- `/report --export-image im` — export the generated HTML as an IM-friendly long image after HTML generation.
