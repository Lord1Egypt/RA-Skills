---
name: seo-audit
description: "Audit and optimize any website's SEO + GEO (AI/LLM visibility) + Core Web Vitals, then fix what's broken. Runs a portable, zero-dependency hard-gate audit over a build output directory (Astro/Next/Hugo/Jekyll/plain HTML) and a live-URL crawl/GEO audit (robots.txt AI-crawler policy, sitemap, llms.txt, on-page JSON-LD, canonical, security headers). Includes a battle-tested LCP playbook (7.5s → 1.5s mobile on the reference site): render-blocking CSS, critical-CSS split, font preload discipline, third-party JS deferral. Use when asked to: check/improve a site's SEO, raise a Lighthouse/PageSpeed score, fix slow LCP / Core Web Vitals, make a site discoverable by AI agents (ChatGPT/Claude/Perplexity/Gemini), add structured data, set up robots/sitemap/llms.txt, or review a site before launch. Distilled from the reference site's production build-time SEO gates."
compatibility: Claude Code, Claude Desktop, Cursor
keywords:
  - seo-audit
  - seo
  - geo
  - ai-visibility
  - llms.txt
  - structured-data
  - json-ld
  - robots.txt
  - sitemap
  - canonical
  - lighthouse
  - pagespeed
  - core-web-vitals
  - lcp
  - render-blocking
  - critical-css
  - font-loading
  - LCP优化
  - 性能优化
  - open-graph
  - schema.org
  - technical-seo
  - generative-engine-optimization
  - ai-crawler
  - indexnow
  - hard-gates
  - SEO体检
  - SEO优化
  - 网站SEO
  - AI可见性
  - 结构化数据
  - 站点审计
  - 上线前检查
  - 搜索引擎优化
  - GEO优化
  - 爬虫策略
metadata:
  author: zeze
  source: a production site's build-time audit gates + worker SEO layer
  openclaw:
    homepage: "https://github.com/Cosmofang/seo-audit"
    author: "zeze"
    runtime:
      node: ">=18"
    permissions:
      - "Reads files under the build-output directory you point it at (audit-seo.mjs)"
      - "Makes outbound HTTPS requests to the live URL you provide (audit-live.mjs)"
      - "Writes nothing — reports are printed to stdout / saved only where you redirect them"
---

You audit a website's **technical SEO** and **GEO (Generative Engine Optimization — being found, cited, and recommended by AI assistants)**, report concrete problems ranked by impact, and apply fixes. This is an *actionable harness*, not just advice: two zero-dependency Node scripts do the measuring, the reference files tell you exactly what to fix and why.

The rules here are distilled from a production site whose build **fails** if any gate is violated — that discipline is why it scores high. Treat the gates as hard constraints, not suggestions.

## When to use
- "Check/improve my site's SEO", "raise my PageSpeed/Lighthouse SEO score", "review before launch"
- "Make my site visible to AI / ChatGPT / Claude / Perplexity", "add llms.txt", "fix robots for AI crawlers"
- "Add structured data / JSON-LD / schema", "set up sitemap / canonical / Open Graph"
- "My LCP is slow / fix Core Web Vitals / PageSpeed says my site takes 7 s to load"

## What you have
- `scripts/audit-seo.mjs` — **on-disk auditor.** Runs the 12 hard-gate checks over a directory of built HTML + its local CSS/JS/images. Framework-agnostic. Node ≥18, no install.
- `scripts/audit-live.mjs` — **live-URL auditor.** Checks the things only visible on a deployed origin: robots.txt policy (incl. per-AI-bot allow/deny), sitemap.xml, llms.txt, homepage JSON-LD (@graph-aware), canonical, HSTS / Vary / Cache-Control.
- `references/hard-gates.md` — the 12 gates: exact thresholds, the general rule, and the Astro+Cloudflare reference implementation.
- `references/structured-data.md` — copy-paste JSON-LD recipes (Organization, WebSite, Breadcrumb, Article, Product, FAQ) using the nested `@graph` pattern.
- `references/geo-ai-visibility.md` — the GEO layer: robots AI-crawler allowlist (exact user-agents), `llms.txt` format, AI-oriented schema, IndexNow.
- `references/lcp-playbook.md` — **Core Web Vitals deep-dive**: the measured levers that took the reference site from 7.5 s → ~1.5 s mobile LCP (render-blocking CSS, critical-CSS split, font discipline, deferring non-LCP DOM, third-party JS, CLS guardrails, CI lock-in). Use when the problem is *speed*, not markup.

## Workflow

### 1. Locate the build output (don't audit source — audit the shipped HTML)
SEO lives in the *rendered* HTML. Find the build dir: Astro `dist/`, Next `out/` (or `.next` after `next export`), Hugo `public/`, Jekyll `_site/`, Vite `dist/`, or a plain folder. If it doesn't exist yet, run the project's build first. Confirm with the user if ambiguous.

### 2. Run the on-disk audit
```bash
node scripts/audit-seo.mjs --dir <build-dir>
# options: --strict (warns→errors, CI mode) · --json · --max-page-kb 500 · --max-img-kb 500
```
Read the output: `✗` = ERROR (genuinely hurts ranking / breaks crawlers / Core Web Vitals — fix these first), `⚠` = WARN (best-practice miss). The heuristic score is a rough dial, not a Lighthouse number.

### 3. Run the live audit (if deployed)
```bash
node scripts/audit-live.mjs https://www.example.com
```
This is where GEO shows up: which AI crawlers are allowed/blocked, whether `llms.txt` exists, what JSON-LD `@type`s the homepage actually ships.

### 4. Report and fix
- Group findings by severity; fix ERRORs first, then high-value WARNs.
- For each fix, open `references/` for the exact target value and the reference implementation, then edit the source (templates/layout/config) — **not** the built HTML (it's regenerated).
- Re-run the audit to confirm green. For CI, wire `audit-seo.mjs --strict` into the build so regressions fail the pipeline.

## The 12 hard gates (cheat-sheet — full detail in references/hard-gates.md)
1. **Exactly one `<h1>`** per page.
2. **Viewport meta** `width=device-width, initial-scale=1`.
3. **Semantic landmarks** — `<main>` + `<nav>` + `<footer>` present.
4. **`<title>`** present (≈10–60 chars) + **meta description** present (≈50–160 chars). *Length is a soft warn — longer is a valid deliberate GEO choice.*
5. **Canonical** — absolute-URL `<link rel="canonical">`, host matches the deploy origin (build-time, never runtime).
6. **Open Graph** — `og:title` + `og:image`.
7. **Images** — every `<img>` has `width`+`height`+`alt`; non-hero `loading="lazy"`; hero `fetchpriority="high"`; each file ≤500 KB (WebP/AVIF).
8. **No inline executable `<script>`** (allow only `application/ld+json`/`json`/`importmap`) and **no `on*=` handlers** → strict CSP `script-src 'self'`.
9. **No external resource refs** (fonts/img/css/js) — self-host for CSP + speed.
10. **Page weight** — HTML + same-page CSS + JS ≤500 KB (images budgeted separately).
11. **Structured data** — JSON-LD present; site-wide Organization + WebSite.
12. **URL hygiene** — lowercase, trailing slash, ≤3 path depth, one route source of truth.

GEO layer (references/geo-ai-visibility.md): robots.txt explicitly **allows** the major AI crawlers, ship **`llms.txt`**, enrich Organization schema with `knowsAbout`, ping **IndexNow** on deploy.

**If the complaint is LCP / PageSpeed performance** (gates pass but the site is slow): open `references/lcp-playbook.md`. Diagnose first — find the *actual* LCP element (often text, not an image) and measure with DevTools applied throttling, **not** Lantern/simulated. Then work the levers in impact order: render-blocking CSS → critical-CSS split → font preload discipline → defer non-LCP viewport DOM → eager hero image → third-party JS on idle/interaction → IntersectionObserver-deferred init. Keep CLS at 0 by reserving space for everything you defer, and lock wins in with a Lighthouse CI gate + per-page JS byte budget.

## Notes
- 404/50x pages are exempt from canonical/description/OG/JSON-LD (they're noindex by design) — the auditor already skips them.
- The auditor uses conservative regex extraction, not a full DOM — it's for audit *signals*. A clean run is strong evidence, not a formal guarantee.
- Don't relax a threshold to make the audit pass. Fix the page.

---

## Purpose & Capability

seo-audit is an **actionable SEO + GEO auditing harness**. Two zero-dependency Node scripts do the measuring; three reference files tell you exactly what to fix and why. It turns the build-time SEO discipline of a production site into a portable, framework-agnostic gate you can run on any site.

| Capability | Description |
|------------|-------------|
| On-disk hard-gate audit | `audit-seo.mjs` runs 12 hard gates (h1, viewport, landmarks, title/desc, canonical, OG, images, CSP-safe scripts, no external refs, page weight, JSON-LD, URL hygiene) over any built static dir |
| Live-URL GEO audit | `audit-live.mjs` checks robots.txt AI-crawler policy, sitemap.xml, llms.txt, homepage JSON-LD (`@graph`-aware), canonical, HSTS/Vary/Cache-Control |
| Fix references | `references/` gives exact thresholds, copy-paste JSON-LD recipes, and the AI-crawler allowlist + llms.txt format |
| LCP playbook | `references/lcp-playbook.md` — measured Core Web Vitals levers (7.5 s → 1.5 s mobile LCP on the reference site) with diagnosis method, impact ranking, CLS guardrails, and CI lock-in |
| CI integration | `audit-seo.mjs --strict` turns warnings into errors so regressions fail the build |

**Does NOT:**
- Audit source files — it audits *rendered/built* HTML (run your build first)
- Modify your site — it reports; you (or the agent) apply fixes to source templates
- Replace Lighthouse — its score is a heuristic dial for audit signals, not an official number
- Send your URL or content anywhere except the live origin you explicitly pass to `audit-live.mjs`

## Instruction Scope

**In scope (will handle):**
- "Check / improve my site's SEO", "raise my Lighthouse/PageSpeed SEO score", "review before launch"
- "Make my site visible to AI / ChatGPT / Claude / Perplexity", "add llms.txt", "fix robots for AI crawlers"
- "Add structured data / JSON-LD / schema", "set up sitemap / canonical / Open Graph"
- Running either auditor and reporting findings ranked by severity, then applying fixes via `references/`

**Out of scope (won't handle):**
- Off-page SEO, backlinks, keyword-ranking tracking, or paid-search work
- Content writing / copywriting beyond meta title & description guidance
- Auditing a directory that hasn't been built yet (build first, then point the auditor at the output)

**Behavior on missing input:**
- `audit-seo.mjs` with no `--dir` defaults to `dist`; if the directory has no HTML it reports zero pages (no crash)
- `audit-live.mjs` with no URL prints usage and exits with code 2

## Credentials

**No credentials required.** This skill uses no API keys, tokens, or accounts.

| Action | Credential | Network |
|--------|-----------|---------|
| `audit-seo.mjs --dir <dir>` | None | None — local filesystem read only |
| `audit-live.mjs <url>` | None | Outbound HTTPS to the URL you pass (and its robots.txt/sitemap/llms.txt) |

No hardcoded secrets exist anywhere in the scripts.

## Persistence & Privilege

**Writes:** nothing by default. Both scripts print reports to stdout; `--json` still prints to stdout. Output is persisted only where you redirect it (e.g. `> report.json`).

**Does NOT write:**
- No files inside your project, the skill directory, or your home directory
- No shell-config or credential files
- No cron jobs or background processes

**Privilege:** runs as the current user, no sudo or elevated permission. Requires only Node ≥18 (global `fetch`).

**Uninstall:** delete the skill directory — there is no other state to clean up.

## Install Mechanism

### Standard install (clawHub)

```bash
clawhub install seo-audit
```

### Manual install

```bash
cp -r /path/to/seo-audit ~/.claude/skills/seo-audit/
```

### Verify install

```bash
node scripts/audit-seo.mjs --help 2>/dev/null || node scripts/audit-seo.mjs --dir . --json | head
node scripts/audit-live.mjs            # should print usage and exit 2
```

Both scripts are zero-dependency (Node ≥18). No `npm install` step is needed.

---

*Version: 1.1.0 · Created: 2026-06-09 · Updated: 2026-06-10 · Changes: see [CHANGELOG.md](CHANGELOG.md)*
