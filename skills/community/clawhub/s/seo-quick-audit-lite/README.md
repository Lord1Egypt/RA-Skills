# seo-quick-audit-lite

Offline on-page SEO audit of a local HTML file — title, meta description, canonical, robots meta, viewport, Open Graph, h1, image alt, lang/charset. Zero dependencies, zero network. Node 18+.

## Install

```bash
npx skills add NenadZivotic/lite-agent-skills --skill seo-quick-audit-lite
```

Or clone and point your agent at `seo-quick-audit-lite/SKILL.md`.

## Run

```bash
node scripts/audit.js page.html
```

JSON report on stdout; exit `1` on warn/fail (CI-gateable).

## Full version

The full `seo-quick-audit` skill ($12) audits **live URLs** — fetches the page plus `/robots.txt` and `/sitemap.xml`, checks twitter-card meta, follows redirects. Ask for it by slug.
