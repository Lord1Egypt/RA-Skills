# ui-roi-audit

Formerly `roi-content-audit`.

Audit web pages and task-driven interfaces against source-cited conversion, usability, and ROI
criteria, then rank fixes by expected return.

## What it does

- Scores landing, home, category, product, form, and checkout pages against conversion criteria
- Scores task-driven interfaces against usability and cost-impact criteria
- Rates each gap by exposure, severity, and effort
- Estimates a conservative twelve-month ROI for the top fixes when traffic and conversion data exist
- Converts interface improvements into revenue gained or cost avoided when data exists
- Ends every report with full source references

## What it does not do

- Write or rewrite copy
- Audit SEO, brand voice, or accessibility compliance
- Promise an uplift

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Procedure, output contract, citation rules |
| `references/roi-model.md` | Formulas and estimation rules |
| `references/page-type-criteria.md` | Criteria per page type |
| `references/content-and-trust-criteria.md` | Cross-cutting content criteria |
| `references/usability-roi-module.md` | Optional usability module |
| `references/source-limitations.md` | What the sources cannot support |
| `references/report-contract.md` | Output format, citation rules, and failure handling |
| `examples/sample-audit.md` | A real audit report, as a format reference |
| `EVIDENCE.md` | What was tested and what was not |
| `ATTRIBUTION.md` | Bibliography and reuse notes |
| `INSTALL.md` | Installation for Claude Code, Claude web/chat, and Cowork |

## Example prompts

- "Run an ROI audit on this landing page. Goal: demo requests. 30k visits a month, 1.2% conversion."
- "Why doesn't this product page convert? Here is a screenshot."
- "Audit our checkout and tell me what to fix first. Include usability."
- "Audit this support workflow and estimate the ROI of reducing task time and errors."

## Sources

Built on *Web Design for ROI* (Loveday & Niehaus, 2008) and the AM+A white paper *Return on
Investment for Usable User-Interface Design* (Marcus, 2004). The skill paraphrases and cites; it
does not reproduce the sources. See `ATTRIBUTION.md`.

## Status

Version 2.0. Tested on a product page, landing page with ROI data, checkout, and a task-driven
interface. It outperformed a no-skill baseline on four of five evaluation dimensions. All 54
criterion-to-chapter mappings and the selected white-paper citations were source-verified; see
`EVIDENCE.md`.

## Author and project

- **Author:** [Monika Zapisek](https://monikazapisek.com)
- **Project:** [Symphonia Score](https://symphoniascore.com)

## License

MIT for the skill's own text and structure. The sources remain under their authors' copyright.
