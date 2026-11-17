# SEO Evaluator v2.1

> Evidence-first SEO evaluation for e-commerce pages. Separates facts from guesses, editorial from technical.

## What This Is

A structured AI agent prompt that evaluates any e-commerce page (or local HTML file) for SEO issues. Unlike conventional SEO checklists, this evaluator:

- **Labels every finding** as VERIFIED, LIKELY, EDITORIAL, UNAVAILABLE, or APPENDIX
- **Refuses to invent data** — no guessing rankings, traffic, or index status without evidence
- **Never scores** — no arbitrary 0-100 grades or letter rankings
- **No fixed rules** — no minimum word counts, keyword density targets, or H1 count limits

## Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Evidence-first** | Only report what's observable; mark speculation as LIKELY |
| **No invented benchmarks** | Don't cite "industry averages" or "recommended counts" without citation |
| **Stop on failure** | If a page blocks retrieval, stop — don't evaluate the block page |
| **Separate concerns** | Technical SEO vs editorial vs accessibility vs social preview |

## Evaluation Steps (14)

0. Access & Page Context
1. Title & Snippet Inputs
2. Headings & Page Structure
3. Content & Intent
4. Topic Coverage & Language
5. Internal Discovery
6. Images & Media
7. Crawling, Indexing & Canonical Signals
8. Rendering & JavaScript
9. Structured Data & Commerce Consistency
10. International & Duplicate Variants
11. Performance Evidence
12. Outbound, Safety, Accessibility & Social Preview
13. Comparison & Change History
14. Output

## Usage

Load `SKILL.md` into any AI agent platform that supports structured system prompts. Provide a target URL or HTML path. Optionally supply a target query, page purpose, site type, market, language, platform, or competitor URLs.

The evaluator returns a structured Markdown report with verified issues, likely concerns, editorial opportunities, and an action plan.

## Version

- **v2.1** — 2026-07-19 (frozen for research run)
- Differences from v2: removed score/grade, added 5-tier evidence labels, separated lab vs field CWV

## Category

📝 Content & SEO
