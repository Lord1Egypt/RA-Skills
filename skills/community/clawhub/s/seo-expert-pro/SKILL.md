---
name: seo-expert-pro
description: "Enable SEO superpowers for OpenClaw. Get a massive boost in knowledge about technical SEO, content SEO, site structure, and measurement."
metadata:
  version: "1.3.1"
  openclaw:
    skillKey: seo-expert-pro
    homepage: "https://developers.google.com/search/docs"
    requires:
      anyBins:
        - curl
---

Instructions in this file are plain Markdown (no hidden or encoded content).

**Bundle version:** 1.3.1

# SEO Expert: User Guide

## What this skill is

This skill equips your OpenClaw agent with **structured guidance** for **search engine optimization**: technical foundations, on-page content, information architecture, performance signals relevant to crawl and indexation, and **measurement** (without guaranteeing rankings).

**References:** German **Google Search Central** excerpts under `{baseDir}/references/` — **fundamentals** (`01_seo_grundlagen.md`), **crawling & indexing** (`02_crawling_indexierung.md`), **ranking & appearance** (`03_ranking_darstellung.md` hub + `03.1`–`03.7`), **monitoring & troubleshooting** (`04_monitoring_fehlerbehebung.md`), **web-specific guides** (`05_webspezifische_leitfaeden.md` hub + `05.1`–`05.8`). Index: **`{baseDir}/references/OVERVIEW.md`**.

**Not exhaustive:** SEO platforms, algorithms, and guidelines change continuously. Prefer **primary sources** (e.g. Google Search Central, Bing Webmaster, your stack’s documentation) when behavior, limits, or compliance matter.

The AI may use **`curl`** for HTTP checks (status, headers, robots) when your gateway policy allows. Broader tools follow your host configuration; optional OpenClaw policy notes can be added under `{baseDir}/references/` as the skill grows.

## No companion plugin (v1.1)

There is **no** bundled OpenClaw plugin in v1 — only this skill and tools your host already allows.

## Installation (typical)

1. Install the skill (ClawHub or `skills/seo-expert-pro` on the gateway host).
2. Allow **`curl`** (and optionally browser or fetch tools) per your `openclaw.json` / sandbox policy.
3. Restart the gateway after skill or policy changes if needed.

Details: `{baseDir}/README.md`, `{baseDir}/references/OVERVIEW.md`.

## What you can expect from the AI

- **Structured audits and checklists** grounded in documented SEO practice — not black-hat or platform-terms-violating tactics.
- **No secrets in chat** — API keys for Search Console or third-party tools belong in env only (see `{baseDir}/references/AUTH.md` when present).
- **Honest limits:** nobody can ethically promise rankings; the skill focuses on **discoverability, quality, and measurement hygiene**.

## Required setup (eligibility)

Per **`metadata.openclaw.requires`**:

1. **`curl`** available on the gateway for optional HTTP diagnostics.

Optional: target site URL or API credentials — document env names in `.env.example` and future `AUTH.md` when you add tool integrations.

## When the agent should use this skill

Use for **SEO-related** work: crawling/indexing, metadata, structured data, site structure, redirects, Core Web Vitals context, analytics/search-console style workflows, content quality for search — and for **clarifying** what is vs is not in scope.

Load **`{baseDir}/references/OVERVIEW.md`** first, then the **smallest** matching reference (`01_…`, `02_…`, `04_…`, `03` hub / `03.n_…` parts, or `05` hub / `05.n_…` parts).

## Rules for the assistant (summary)

1. **Cite primary guidelines** where possible; flag uncertainty when platforms differ or update silently.
2. **Never** promise rankings, “instant” results, or tactics that violate search engine or legal terms.
3. **Never** echo tokens or API keys; reference env **names** only.
4. Prefer **measurable** recommendations (what to check, how to verify) over vague advice.

**Where work runs:** on the **OpenClaw gateway** and in conversation — not inside Google/Bing systems unless the user connects official tools separately.
