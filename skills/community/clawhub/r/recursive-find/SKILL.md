---
name: recursive-find
description: Find which pages on a site mention X: search a page plus every page it links to (Ctrl+F, recursive) and get back only matching pages with snippets.
---

# Recursive find (`rfind`)

Use when the question is "where on this site / in these docs / among these
listings does X appear?" One `rfind` call replaces dozens of `web_fetch` calls
and returns only hit pages with short snippets, not page bodies. Headless port
of the Recursive Find Chrome extension (github.com/grtwrn/recursive-find).

Skip it for: reading one known page (`web_fetch`), JavaScript-rendered sites or
logged-in pages (`browser`), or general web questions (`web_search`).

## Run

```sh
rfind <url> "<query>" [--depth 1] [--within /docs/] [--max-pages 100] [--mode text|word|regex] [--case] [--main] [--first] [--json]
```

(`rfind` is `scripts/rfind.mjs` in this skill, symlinked onto PATH; Node 18+, no dependencies. `rfind --help` lists every flag.)

1. Start from the most specific page you know (a docs index, a category page),
   not a site's home page. Big home pages link to hundreds of pages and burn the
   page budget before reaching the right section.
2. Narrow with `--within <path-prefix>` whenever the content lives under one
   path (e.g. `--within /docs/`). Keep the default `--depth 1`; use `--depth 2`
   only with `--within` or a small site.
3. Use `--mode word` for short words (`cat` won't match `category`), `--mode regex`
   for patterns, `--first` when one hit answers the question.
4. Add `--main` when the question is which pages *discuss* X: it searches only
   the main content (`<main>`, `role="main"`, `<article>`), so "Next topic" links,
   sidebars and menus that merely name X don't count as hits.
5. Read the summary line: if it says `hit --max-pages`, results are incomplete.
   Narrow (`--within`, a deeper start URL) before raising `--max-pages` (max 1000).
   It also flags pages over 32 MB that were only partly searched. Skipped
   non-HTML links are normal, not failures.
6. Matches show as `[[match]]` inside snippets. Cite the page URL; `web_fetch`
   it if you need more than the snippet.

## Behavior

- Same site only by default (`--any-site` to leave it); honors robots.txt
  (`--ignore-robots` only when the user asks); 4 parallel fetches; 10 s per page;
  the whole crawl stops after 120 s (`--max-seconds`), flagged in the summary.
- Text comes from server HTML only (no JS), no cookies/login. Skips PDFs,
  images and other non-HTML links.
- Exit 0 = crawl ran (even with 0 hits); 1 = start page failed; 2 = bad arguments.
