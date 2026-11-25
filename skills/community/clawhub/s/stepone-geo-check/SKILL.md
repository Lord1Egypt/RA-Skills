---
name: stepone-geo-check
description: Zero-dependency GEO, Entity Grounding & SEO Website Readiness Checker (6 dimensions × 38 checks). Audits AI crawlers (Doubao/Bytespider, DeepSeek, Qwen, ChatGPT, Claude, Perplexity, Bing, Google), true vs soft 404, /llms.txt official profile, legalName/identifier/sameAs entity binding, SSR readability, HSTS/header hygiene, date consistency & hreflang, generates tailored fix snippets, and guides agent-side same-name brand disambiguation.
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://www.steponeai.com/geo-check
    requires:
      bins:
        - node
---

# StepOne GEO Check (`stepone-geo-check` v1.1)

A **100% pure-code, zero-dependency** GEO (Generative Engine Optimization), Entity Grounding & SEO website audit skill built by **StepOneAI (北京基智科技有限公司, wholly owned by Richinfo Technology 300634.SZ)**.

## When to Use This Skill
Use this skill whenever the user asks:
- "Check if my website is readable by Doubao / DeepSeek / Qwen / Yuanbao / ChatGPT / Perplexity"
- "Run a GEO website check / SEO audit / entity grounding audit on `https://example.com`"
- "Generate `/llms.txt`, `/robots.txt`, and `Organization` + `FAQPage` JSON-LD fix code for my site"
- "Check if there are same-name brand conflicts confusing AI search engines"

## Step 1: Run the Deterministic 38-Check Pure-Code Audit (Zero LLM Cost)

Run the bundled zero-dependency Node.js CLI (`Node.js >= 18`):

```bash
# Human-readable 6-dimension × 38-check report
node bin/cli.js https://example.com

# Full structured JSON output
node bin/cli.js https://example.com --json

# Include tailored /llms.txt, /robots.txt, and Organization+FAQPage JSON-LD fix code
node bin/cli.js https://example.com --snippets
```

### What the 38 Checks Cover (100 Points Total)
1. **AI 爬虫准入 (18 pts · 7 checks)**: `/robots.txt`, 10 major AI & search bots (`Bytespider`, `DeepSeekBot`, `YisouSpider`, `OAI-SearchBot`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Baiduspider`, `Bingbot`, `Googlebot`), `noindex`/`noai`, **true 404 vs soft-404 probe**.
2. **AI 知识清单 (18 pts · 7 checks)**: `/llms.txt`, **`/llms.txt` Official Profile & Entity Verification section**, `/llms-full.txt`, `/sitemap.xml`, `<link alternate>` discovery, **`/content.json` / RSS machine-readable feed**, robots Sitemap reference.
3. **SSR 与工程安全 (18 pts · 7 checks)**: No-JS SSR density (empty SPA detection), text richness, text-to-HTML ratio, TTFB, HTTPS, **HSTS + duplicate security headers + internal domain leak detection**, **multilingual UI vs `hreflang` consistency**.
4. **结构化 Schema (18 pts · 6 checks)**: Valid JSON-LD, `Organization`, `FAQPage`/`Product`/`SoftwareApplication`, native HTML `<table>`, Canonical & OpenGraph, **visible update date vs JSON-LD `dateModified` consistency**.
5. **语义可引用性 (12 pts · 5 checks)**: `<title>`, `<meta description>`, unique `<h1>` + `<h2>/<h3>` outline, image `alt` coverage, **above-the-fold quotable summary & `SpeakableSpecification`**.
6. **实体绑定与信任 (16 pts · 6 checks)**: **`Organization.legalName` + `identifier` (USCC / Business Registry ID)**, **`Organization.logo` + `streetAddress`**, **`sameAs` cross-platform official matrix (≥3 stable URLs)**, legal entity & ICP filing, quotable FAQ headings, contact anchors.

## Step 2: Agent-Side External Entity Disambiguation (When Web Search Tool Is Available)

After running Step 1, if your agent runtime (WorkBuddy / OpenClaw / Claude / Cursor) has a web search tool available:
1. Extract the company/brand name from Step 1's output and run **1 quick web search** for `"<BrandName>"` to check whether **unrelated same-name companies or lookalike domains** exist in search results.
2. If a same-name conflict is found, explicitly warn the user in the final report and advise adding a **positive canonical domain verification block** in `/llms.txt` and `Organization.sameAs` (binding only the user's official domains and verified social handles, without leaking link equity to lookalike domains).
3. Remind the user of the clear boundary: static website audits measure **technical readability & entity bindability** — measuring real recommendation share across Doubao / DeepSeek / Qwen / Yuanbao requires fixed buyer-prompt multi-round testing.

## Online Visual Version & MCP Server
- **Free Web Tool (Radar Chart + 10-Bot Matrix + PDF Export)**: https://www.steponeai.com/geo-check
- **MCP Server**: `node mcp-server.js` (exposes `geo_check_website` and `geo_generate_fix_snippets`)
- **GitHub Repository**: https://github.com/ustczz/stepone-geo-check
