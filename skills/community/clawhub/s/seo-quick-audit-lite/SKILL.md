---
name: seo-quick-audit-lite
description: Offline on-page SEO audit of a local HTML file — title and meta description quality, canonical, robots meta, viewport, Open Graph tags, h1 structure, image alt coverage, lang/charset. Zero network access. Use when the user asks to check a page's SEO basics from saved HTML or a template file.
---

# SEO Quick Audit (Lite)

Runs `scripts/audit.mjs` on a **local HTML file** the user supplies and reports pass/warn/fail on core on-page SEO checks. Completely offline — the script reads one file and emits JSON.

## Scope and rules

- Audit only files the user supplies. This lite version does NOT fetch URLs, robots.txt, or sitemap.xml — say so when reporting.
- Pass/fail is based on common conventions, not search-engine guarantees.
- Never modify the file. Read-only.

## 1. Run

Requires Node 18+, zero dependencies.

```bash
node <skill-dir>/scripts/audit.mjs page.html
```

JSON on stdout; exit `1` when any warn/fail is present (CI-gateable), `2` on read/usage error.

## 2. Read the report

- `summary`: pass/warn/fail/info counts.
- `checks[]`: `{id, status, detail}` for: `title`, `meta-description`, `canonical`, `robots-meta`, `viewport`, `open-graph`, `h1`, `img-alt`, `lang`, `charset`.

## 3. Fix guidance

- `title`/`meta-description` warn → rewrite to ~30-65 / 50-160 chars.
- `robots-meta: noindex` on a page meant to rank → remove the directive.
- `canonical` missing → add `<link rel="canonical">`.
- `h1` fail → exactly one descriptive h1 per page.
- `open-graph` warn → add og:title/og:description/og:image for link previews.

## Lite vs full

The full `seo-quick-audit` additionally fetches live URLs including `/robots.txt` and `/sitemap.xml` status, twitter-card check, and redirect handling.
