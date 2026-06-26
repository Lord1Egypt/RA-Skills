---
name: seo-and-llm-rankings
description: >-
  Audits websites for traditional SEO health and AI search visibility (GEO). Generates prioritized reports with actionable fixes and ready-to-use prompts for AI coding agents. Covers Google, Bing, ChatGPT, Perplexity, Claude, Gemini, Copilot, and Google AI Overviews. Use when auditing SEO, LLM visibility, generative engine optimization, AI Overviews, or AI search optimization.
metadata:
  version: 1.1.0
---

# SEO & LLM Rankings

Audit websites for traditional SEO health and AI search visibility (GEO). Generate prioritized reports with actionable fixes and ready-to-use prompts for AI coding agents. Covers Google, Bing, ChatGPT, Perplexity, Claude, Gemini, Copilot, and Google AI Overviews.

## Before You Start

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

**Gather missing context by asking the user:**

1. **Audit mode** -- Live URL scan or local codebase scan?
2. **Site URL** (if URL mode) -- What URL should be audited?
3. **Project path** (if codebase mode) -- Where is the project? (default: current workspace)
4. **Scope** -- Full site audit or specific pages/sections?
5. **Site type** -- SaaS, e-commerce, blog, local business, portfolio, etc.
6. **Primary keywords** -- What keywords/topics matter most?
7. **Business goal** -- Traffic, leads, signups, sales, brand awareness?
8. **Known issues** -- Any specific concerns or recent traffic drops?
9. **Tech stack** -- Next.js, WordPress, Shopify, static HTML, etc.

Only ask what you don't already know. If the user gives a URL, use URL mode. If the user says "audit my project" or "scan the codebase," use codebase mode. If ambiguous, ask.

---

## Platform Detection & URL Fetching Strategy

URL mode fetches live pages via HTTP. This often fails because of WAFs (Cloudflare, etc.), corporate firewalls, bot-detection, or restricted shell environments. Before running any URL-mode fetch, detect your platform and use the most reliable method available.

**How to detect your platform:**

- **Cursor** -- You have a `WebFetch` tool and `WebSearch` tool. You may also have `@Web` mentions available. If you can call `WebFetch`, you are in Cursor.
- **Claude Code** -- You have a `WebFetch` tool natively. Similar to Cursor but runs in a terminal-based agent.
- **Codex (OpenAI)** -- You have browser tools or web-fetch MCP tools. Check your available tool list.
- **Windsurf** -- You have built-in web browsing and URL fetching capability.
- **Aider / terminal-only agents** -- No built-in web tools. You must rely on shell commands (`curl`, `python3`).
- **GitHub Copilot Workspace** -- Has web access through its own tool surface.

**URL fetching priority chain (try in order, fall back on failure):**

| Platform | Primary Fetch Method | Fallback 1 | Fallback 2 |
| --- | --- | --- | --- |
| **Cursor** | `WebFetch` tool (bypasses WAFs/firewalls) | Python script (`scripts/seo_audit.py`) | `curl` with browser UA |
| **Claude Code** | `WebFetch` tool | Python script | `curl` with browser UA |
| **Codex** | `WebFetch` / browser tools | Python script | -- |
| **Windsurf** | Built-in web browsing | Python script | `curl` with browser UA |
| **Aider / terminal** | Python script | `curl` with browser UA | -- |
| **Other** | Python script | `curl` with browser UA | -- |

**Failure detection:** Treat any of these as a fetch failure that should trigger the next fallback:
- HTTP 403, 404, 5xx status codes
- Connection timeout or connection refused
- Empty response body
- SSL/TLS errors
- `curl: command not found` (Windows without curl)

**If all methods fail**, do NOT silently skip the check. Inform the user that the URL could not be reached and suggest:
1. Trying from a different network
2. Pasting the page HTML or file content directly for analysis
3. Switching to codebase mode if they have the source locally

---

## Audit Mode Selection

This skill supports two audit modes:

| Mode              | When to Use                    | How It Works                                                                    |
| ----------------- | ------------------------------ | ------------------------------------------------------------------------------- |
| **URL mode**      | Site is live / deployed        | Fetches pages via HTTP, checks robots.txt, sitemap, llms.txt, load time         |
| **Codebase mode** | Site is local / pre-deployment | Scans project files using Glob, Read, Grep -- checks HTML, layout files, config |

**Codebase mode** is especially useful for:
- Catching SEO issues before deployment
- Projects not yet live
- When the user wants to scan source code directly
- Auditing meta tags set in framework layout/page files (Next.js, Astro, etc.)

---

## Audit Workflow

### Phase 1: Technical SEO Scan

**Choose your mode:**

#### URL Mode

Run the audit script and manual checks:

```bash
python3 scripts/seo_audit.py "https://example.com"
python3 scripts/seo_audit.py "https://example.com" --full   # detailed output
```

**Manual checks -- use the fetching strategy from "Platform Detection & URL Fetching Strategy" above.**

Follow the priority chain for your platform. Examples for each method:

**Primary: WebFetch (Cursor, Claude Code, Codex, Windsurf)**

Use `WebFetch` for each resource. This is the most reliable method -- it handles TLS, follows redirects, and bypasses most WAF/bot-detection blocks.

```
WebFetch("https://example.com")              -- main page HTML
WebFetch("https://example.com/robots.txt")   -- robots.txt
WebFetch("https://example.com/sitemap.xml")  -- sitemap
WebFetch("https://example.com/llms.txt")     -- llms.txt (AI discovery)
```

If `WebFetch` returns an error for a specific resource (403, 404, 500, or timeout), note the failure and try the next fallback for that resource. Do NOT skip the check silently.

**Fallback 1: Python script**

```bash
python3 scripts/seo_audit.py "https://example.com"
python3 scripts/seo_audit.py "https://example.com" --full
```

The script has built-in retry logic and User-Agent rotation. If the script reports a fetch failure, it will print a diagnostic message with the status code and suggested next steps.

**Fallback 2: curl with browser User-Agent**

Use a realistic browser User-Agent to avoid bot detection. Add `--retry 2` and `--max-time 30` for resilience.

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

curl -sL -A "$UA" --retry 2 --max-time 30 "https://example.com/robots.txt"
curl -sL -A "$UA" --retry 2 --max-time 30 "https://example.com/sitemap.xml"
curl -sL -A "$UA" --retry 2 --max-time 30 "https://example.com/llms.txt"
curl -sL -A "$UA" --retry 2 --max-time 30 "https://example.com"
curl -sIL -A "$UA" --retry 2 --max-time 30 "https://example.com"
```

**If all methods fail for a resource**, tell the user which resource could not be fetched, the error received, and suggest they paste the content manually or switch to codebase mode.

**PageSpeed check (optional, API-based):**

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile"
```

**What to check (both modes):**
- Title tag exists, 50-60 chars, contains primary keyword
- Meta description exists, 150-160 chars, compelling
- Single H1 per page, contains primary keyword
- Heading hierarchy: H1 > H2 > H3 (no skips)
- HTTPS enabled with valid certificate
- robots.txt exists and allows important pages
- XML sitemap exists and is accessible
- Page loads in < 3 seconds (URL mode only)
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 (URL mode only)
- Open Graph and Twitter Card tags present
- Images have alt text
- No broken internal links

#### Codebase Mode

Scan the project files directly using Glob, Read, and Grep. No live server needed.

**Step 1: Discover project structure and framework**

```
Glob: **/*.{html,jsx,tsx,astro,vue,svelte,php}
Glob: **/layout.{tsx,jsx,js,ts}
Glob: **/app/layout.{tsx,jsx}
Glob: **/_app.{tsx,jsx}
Glob: **/index.{html,tsx,jsx}
Glob: **/head.{tsx,jsx}
Glob: **/_document.{tsx,jsx}
```

**Step 2: Check meta tags in layout/page files**

For Next.js (App Router):
```
Grep: "metadata|generateMetadata|title|description" in app/layout.tsx, app/page.tsx
Grep: "openGraph|twitter|metadataBase" in app/layout.tsx
```

For Next.js (Pages Router):
```
Grep: "<Head>|<title>|meta name=.description" in pages/_app.tsx, pages/_document.tsx
```

For static HTML:
```
Grep: "<title>|<meta name=.description|<meta property=.og:" in **/*.html
```

For Astro/Vue/Svelte:
```
Grep: "<title>|<meta|defineMetadata|useHead" in **/*.{astro,vue,svelte}
```

**Step 3: Check for robots.txt and sitemap**

```
Glob: **/robots.txt
Glob: **/public/robots.txt
Glob: **/static/robots.txt
Glob: **/sitemap*.xml
Glob: **/public/sitemap*.xml
```

For Next.js dynamic generation:
```
Glob: **/app/robots.{ts,js}
Glob: **/app/sitemap.{ts,js}
```

**Step 4: Check for llms.txt**

```
Glob: **/llms.txt
Glob: **/public/llms.txt
Glob: **/static/llms.txt
```

**Step 5: Check schema markup in source**

```
Grep: "application/ld\+json|@type|schema.org|jsonLd|JsonLd" in **/*.{tsx,jsx,html,astro,vue}
```

**Step 6: Check headings structure**

```
Grep: "<h1|<h2|<h3|<H1|<H2|<H3" in page/layout files
```

For React/JSX components:
```
Grep: "className=.*h1|<h1|<H1|heading" in **/*.{tsx,jsx}
```

**Step 7: Check images for alt text**

```
Grep: "<img[^>]*(?!alt=)" in **/*.{html,tsx,jsx,astro,vue}
Grep: "<Image[^>]*(?!alt=)" in **/*.{tsx,jsx}
```

**Step 8: Check Open Graph and social tags**

```
Grep: "og:title|og:description|og:image|twitter:card|openGraph" in layout/page files
```

**Codebase mode limitations:**
- Cannot check page load time or Core Web Vitals (needs live server)
- Cannot test HTTP redirect chains or SSL
- Cannot detect runtime-only issues (client-side rendering, JS errors)
- Schema injected purely at runtime by plugins won't be visible

**Codebase mode advantages:**
- Catches issues before deployment
- Can see the actual source code and suggest exact file/line fixes
- Works offline
- Can scan all pages at once instead of one URL at a time
- Fix prompts can reference exact file paths

### Phase 2: GEO / AI Visibility Scan

**AI Crawler Access -- check robots.txt for these bots (in URL mode, fetch directly; in codebase mode, read the robots.txt file from public/ or project root):**

| Bot               | Platform   | Purpose                    |
| ----------------- | ---------- | -------------------------- |
| GPTBot            | OpenAI     | ChatGPT training/knowledge |
| ChatGPT-User      | OpenAI     | ChatGPT web browsing       |
| ClaudeBot         | Anthropic  | Claude training            |
| Claude-Web        | Anthropic  | Claude web search          |
| anthropic-ai      | Anthropic  | Claude training data       |
| PerplexityBot     | Perplexity | Real-time search answers   |
| Google-Extended   | Google     | Gemini / AI Overviews      |
| Applebot-Extended | Apple      | Apple Intelligence         |
| Bingbot           | Microsoft  | Copilot (uses Bing index)  |

**llms.txt File:**
Check if `https://example.com/llms.txt` exists. This AI discovery file (introduced 2024, widely adopted 2026) provides structured context to LLMs. Sites with llms.txt saw ~35% increase in AI visibility within 60 days. If missing, recommend creating one -- see [references/fix-prompt-templates.md](references/fix-prompt-templates.md) for a ready-to-use prompt.

**Schema Markup:**
> `web_fetch` and `curl` cannot reliably detect JS-injected schema (Yoast, RankMath, AIOSEO). Use browser tools or Google Rich Results Test for accurate detection.

Check for: FAQPage (+40% AI visibility), Article, Organization, WebPage, BreadcrumbList, SpeakableSpecification. See [references/schema-templates.md](references/schema-templates.md).

**AI Citation Scoring:**
Score the page across 5 dimensions (see [references/ai-citation-scoring.md](references/ai-citation-scoring.md)):
1. **Extractability** -- Can AI pull a useful answer?
2. **Quotability** -- Are there statements worth citing?
3. **Authority** -- Does it signal expertise?
4. **Freshness** -- Is content current?
5. **Entity Clarity** -- Can AI identify the entity?

**Veto rule:** If AI crawlers are blocked in robots.txt, AI visibility score = 0 regardless of content quality.

### Phase 3: Content Quality Assessment

**GEO Methods Check** (see [references/geo-methods.md](references/geo-methods.md)):
- Citations with sources present? (+27-40% visibility)
- Statistics with named sources? (+33-37%)
- Expert quotes with attribution? (+30-43%)
- Answer-first format? (40-60 word answer capsule after H2s)
- No keyword stuffing? (causes -9 to -10%)

**E-E-A-T Signals:**
- Author bios with credentials visible?
- About page with company information?
- Contact information accessible?
- First-hand experience demonstrated?
- Content dated and recently updated?

**Content Structure for AI Extraction:**
- Clear H2/H3 headings that match questions people ask
- Answer in first sentence after each heading
- Tables for comparisons, ordered lists for processes
- Short paragraphs (2-3 sentences)
- FAQ sections with direct answers

**AI Writing Detection:**
Check content for AI writing patterns that reduce credibility. See [references/ai-writing-detection.md](references/ai-writing-detection.md).

---

## Report Format

Generate this report after completing all three phases:

```markdown
# SEO & GEO Audit Report: [domain or project name]
**Audit mode:** URL / Codebase

## Executive Summary
- **SEO Health:** X/10
- **AI Visibility Score:** X/10
- **Critical Issues (P0):** [count]
- **Important Issues (P1):** [count]
- **Quick Wins:** [count]

## SEO Findings

| Priority | Issue   | Impact   | Fix            |
| -------- | ------- | -------- | -------------- |
| P0       | [issue] | [impact] | [specific fix] |
| P1       | [issue] | [impact] | [specific fix] |
| P2       | [issue] | [impact] | [specific fix] |

## GEO / AI Visibility Findings

### AI Citation Score: X/10

| Dimension      | Score | Assessment |
| -------------- | ----- | ---------- |
| Extractability | X/10  | [details]  |
| Quotability    | X/10  | [details]  |
| Authority      | X/10  | [details]  |
| Freshness      | X/10  | [details]  |
| Entity Clarity | X/10  | [details]  |

### AI Crawler Access

| Bot             | Status                             |
| --------------- | ---------------------------------- |
| GPTBot          | Allowed / Blocked / Not configured |
| ClaudeBot       | Allowed / Blocked / Not configured |
| PerplexityBot   | Allowed / Blocked / Not configured |
| Google-Extended | Allowed / Blocked / Not configured |
| Bingbot         | Allowed / Blocked / Not configured |

### llms.txt: Present / Missing

### Platform Readiness

| Platform             | Ready  | Key Gap |
| -------------------- | ------ | ------- |
| Google (traditional) | Yes/No | [gap]   |
| Google AI Overviews  | Yes/No | [gap]   |
| ChatGPT              | Yes/No | [gap]   |
| Perplexity           | Yes/No | [gap]   |
| Claude               | Yes/No | [gap]   |
| Copilot              | Yes/No | [gap]   |

## GEO Methods Applied

| Method                 | Present | Expected Boost |
| ---------------------- | ------- | -------------- |
| Citations with sources | Yes/No  | +27-40%        |
| Statistics with data   | Yes/No  | +33-37%        |
| Expert quotes          | Yes/No  | +30-43%        |
| Answer capsules        | Yes/No  | High           |
| FAQ schema             | Yes/No  | +40%           |
| Authoritative tone     | Yes/No  | +25%           |

## Prioritized Action Plan

### Critical (do first)
1. [action with specific instructions]

### High Impact
1. [action with specific instructions]

### Quick Wins
1. [action with specific instructions]

### Long-term
1. [action with specific instructions]
```

---

## Fix Prompt Generation

When the audit finds a small number of fixable issues, generate a ready-to-use prompt that the user can paste directly into their AI coding agent (Cursor, Claude Code, Codex, etc.).

**When to generate a fix prompt:**
- Fewer than ~10 distinct issues found
- Issues are code-level fixes (meta tags, schema, robots.txt, content structure)
- User asks for a prompt to fix things
- Codebase mode: always generate fix prompts with exact file paths and line numbers

**How to build the prompt:**

1. Read the fix prompt templates from [references/fix-prompt-templates.md](references/fix-prompt-templates.md)
2. Select the relevant template(s) based on audit findings
3. Fill in the specific issues, file paths, and current values from the audit
4. Combine into a single `.prompt.md` formatted prompt with:
   - Clear persona (SEO/GEO expert)
   - Specific task listing each issue found
   - Step-by-step fix instructions
   - Validation criteria

**Example output (URL mode):**

```markdown
---
description: "Fix SEO and AI visibility issues found in audit of example.com"
agent: "agent"
tools: ["editFiles", "codebase", "fetch"]
---

# Fix SEO & AI Visibility Issues

You are an SEO and GEO optimization expert. Fix the following issues found
during an audit of example.com.

## Issues to Fix

1. **Missing meta description** on /about page
   - Add: `<meta name="description" content="...">`
   - Must be 150-160 characters, include primary keyword

2. **AI crawlers blocked** in robots.txt
   - Add Allow rules for GPTBot, ClaudeBot, PerplexityBot

3. **No FAQPage schema** on /pricing
   - Add JSON-LD FAQPage schema with existing Q&A content

## Validation
- Run: `python3 scripts/seo_audit.py "https://example.com"`
- Verify all issues resolved
```

**Example output (codebase mode):**

```markdown
---
description: "Fix SEO issues found in codebase audit of my-project"
agent: "agent"
tools: ["editFiles", "codebase", "search"]
---

# Fix SEO & AI Visibility Issues

You are an SEO and GEO optimization expert. Fix the following issues found
during a codebase audit.

## Issues to Fix

1. **Missing meta description** in `app/layout.tsx` (line 12)
   - The `metadata` export has `title` but no `description`
   - Add: `description: "Your compelling description, 150-160 chars"`

2. **No AI crawler rules** in `public/robots.txt` (line 1)
   - Only has Googlebot rules. Add Allow rules for GPTBot, ClaudeBot,
     PerplexityBot, Google-Extended, Applebot-Extended

3. **No llms.txt** -- file missing entirely
   - Create `public/llms.txt` with company summary, contact, and services

4. **Missing OG image** in `app/layout.tsx` (line 15)
   - `openGraph` object has title and description but no `images` array
   - Add: `images: [{ url: "/og-image.png", width: 1200, height: 630 }]`

5. **No FAQPage schema** on `app/pricing/page.tsx`
   - FAQ section exists at line 85 but has no JSON-LD markup
   - Add FAQPage schema using the existing Q&A content

## Validation
- Check each file for the fixes above
- Run `npm run build` to verify no build errors
```

---

## Content Prompt Generation

When the audit identifies content gaps -- missing pages, thin content that needs rewriting, or opportunities for new pages targeting high-value queries -- generate a ready-to-use prompt that produces SEO + GEO optimized content when pasted into an AI writing/coding agent.

**When to generate a content prompt:**
- Audit reveals content gaps (missing pages for queries the site should rank for)
- Programmatic SEO opportunities identified (see table below)
- User explicitly asks for help creating new content or pages
- Thin content flagged (word count < 300) that needs a full rewrite rather than a quick fix
- Competitor analysis shows topics the site doesn't cover but should

**How to build the prompt:**

1. Read the content prompt templates from [references/content-prompt-templates.md](references/content-prompt-templates.md)
2. Select the template matching the page type:
   - **Article / Blog Post** -- informational content targeting a query
   - **Landing / Product Page** -- conversion-focused page
   - **Glossary / Definition Page** -- "What is X?" pages (great for pSEO)
   - **Comparison Page** -- "X vs Y" structured comparison
   - **FAQ / Resource Page** -- Q&A aggregation page
   - **Location / Persona Page** -- localized or audience-specific variant
3. Fill placeholders using audit findings, keyword data, and product-marketing-context (if `.agents/product-marketing-context.md` exists)
4. The template already embeds GEO optimization rules (answer capsules, citation density, quotation slots from [references/geo-methods.md](references/geo-methods.md)), anti-AI-writing constraints (from [references/ai-writing-detection.md](references/ai-writing-detection.md)), and schema markup requirements -- do not remove them
5. Output as a single `.prompt.md` formatted prompt

**Example output (article page):**

```markdown
---
description: "Create SEO + GEO optimized article: What is Retrieval-Augmented Generation?"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Create Article: What is Retrieval-Augmented Generation (RAG)?

You are a senior content strategist who specializes in search engine
optimization and generative engine optimization. You write content that
ranks on Google AND gets cited by ChatGPT, Perplexity, Claude, and
Google AI Overviews.

## Content Brief

- **Target query**: "What is RAG?" / "retrieval augmented generation explained"
- **Search intent**: informational
- **Target audience**: Software engineers evaluating RAG for production AI apps
- **Primary keyword**: retrieval augmented generation
- **Secondary keywords**: RAG architecture, RAG vs fine-tuning, RAG pipeline, vector database
- **Word count**: 2,000-2,500 words
- **Competing pages to outperform**: aws.amazon.com/what-is/retrieval-augmented-generation, cloud.google.com/...

## Pre-Writing Analysis

Before drafting:
1. Intent mapping: Engineers want to understand what RAG is, when to use it
   vs fine-tuning, and how to implement it. They need architecture details.
2. SERP shape: Competing pages use definition + architecture diagram + use
   cases format. Match this but add comparison tables and sourced benchmarks.
3. Gap analysis: Competing pages lack pricing comparisons for vector DBs,
   real latency benchmarks, and production failure modes.
4. Citation plan: Lewis et al. (2020) original paper, LlamaIndex docs,
   LangChain docs, Pinecone benchmarks, Anthropic RAG guide.

## Article Structure

H2s as questions, 40-60 word answer capsule after each H2. Include:
- 2-3 sourced statistics per section: "Claim (Source, Year)"
- At least 1 expert quote per 500 words
- Tables for all comparisons (RAG vs fine-tuning, vector DB comparison)
- FAQ section with 6 self-contained Q&A pairs

## Writing Rules

- No em dashes. No filler words. No AI-tell verbs (delve, leverage).
- Paragraphs: 2-3 sentences max.
- First 150 words must directly answer "What is RAG?"

## Schema

Include Article schema with author, datePublished, dateModified,
SpeakableSpecification. Include FAQPage schema for FAQ section.

## Validation

- [ ] Definition in first 150 words
- [ ] Answer capsule after every H2
- [ ] 2-3 sourced stats per section
- [ ] No em dashes or AI-tell words
- [ ] Article + FAQPage schema included
```

**Example output (comparison page):**

```markdown
---
description: "Create SEO + GEO optimized comparison: Notion vs Confluence"
agent: "agent"
tools: ["editFiles", "codebase", "search", "fetch"]
---

# Create Comparison Page: Notion vs Confluence

You are a product analyst with SEO and GEO expertise. You write
comparison pages that AI systems cite when users ask "Which is better?"

## Content Brief

- **Target query**: "Notion vs Confluence"
- **Search intent**: commercial investigation
- **Target audience**: Engineering/product managers choosing a team wiki
- **Primary keyword**: Notion vs Confluence
- **Secondary keywords**: Notion alternative, Confluence alternative, best wiki tool
- **Word count**: 2,000 words
- **Your product**: None (neutral comparison)

## Page Structure

- H1: "Notion vs Confluence: Which Wiki Tool Is Better for Your Team in 2026?"
- TL;DR in first 150 words with a clear verdict
- Full comparison table (pricing, features, limitations, ideal user)
- 40-60 word answer capsule after each H2
- "When to Choose Notion" and "When to Choose Confluence" sections
- Alternatives table with 3-4 options
- FAQ with 6 self-contained answers

## Writing Rules

- All pricing dated "(as of March 2026)"
- No unsupported superlatives
- No em dashes or AI-tell words
- Every claim verifiable via product docs or third-party reviews

## Schema

Include Article schema with `about` entities for both products.
Include FAQPage schema. Include SpeakableSpecification for TL;DR.

## Validation

- [ ] TL;DR with clear verdict in first 150 words
- [ ] Full comparison table
- [ ] Each product defined in 40-60 word capsule
- [ ] All pricing dated
- [ ] No em dashes or AI-tell words
- [ ] Article + FAQPage schema included
```

**Combining with programmatic SEO:** When the audit suggests scale pages (integrations, locations, personas, glossary terms), use the batch pattern in Template 3 or Template 6 from [references/content-prompt-templates.md](references/content-prompt-templates.md). Provide the list of items (terms, cities, audiences) inside the prompt so the agent generates one page per item using the same structure.

---

## Programmatic SEO Opportunities

For sites that could benefit from pages at scale, suggest opportunities from these playbooks:

| If the site has...        | Suggest...                                  |
| ------------------------- | ------------------------------------------- |
| Product with integrations | Integration pages (`/integrations/[tool]/`) |
| Multi-segment audience    | Persona pages (`/for/[audience]/`)          |
| Local presence            | Location pages (`/[service]/[city]/`)       |
| Competitor landscape      | Comparison pages (`/compare/[x]-vs-[y]/`)   |
| Industry expertise        | Glossary pages (`/glossary/[term]/`)        |
| Design/creative product   | Template pages (`/templates/[type]/`)       |

Only suggest if there's genuine search demand and the site has (or can create) unique data for each page. Use subfolders, not subdomains.

---

## Platform-Specific Optimization

For detailed ranking factors per platform, see [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

**Quick reference:**

| Platform            | Primary Index | Key Factor          | Unique Requirement    |
| ------------------- | ------------- | ------------------- | --------------------- |
| Google              | Google        | Backlinks + E-E-A-T | Core Web Vitals       |
| Google AI Overviews | Google        | E-E-A-T + Schema    | Knowledge Graph       |
| ChatGPT             | Bing-based    | Domain Authority    | Content-Answer Fit    |
| Perplexity          | Own + Google  | Semantic Relevance  | FAQ Schema, freshness |
| Claude              | Brave         | Factual Density     | Brave Search indexing |
| Copilot             | Bing          | Bing Index          | MS Ecosystem presence |

---

## Validation Tools

| Tool                     | URL                                 | Purpose                        |
| ------------------------ | ----------------------------------- | ------------------------------ |
| Google Rich Results Test | search.google.com/test/rich-results | Schema validation (renders JS) |
| Schema.org Validator     | validator.schema.org                | Schema syntax check            |
| PageSpeed Insights       | pagespeed.web.dev                   | Core Web Vitals                |
| Google Search Console    | search.google.com/search-console    | Indexing, errors, performance  |
| Bing Webmaster Tools     | bing.com/webmasters                 | Bing indexing                  |

---

## References

- [references/ai-citation-scoring.md](references/ai-citation-scoring.md) -- 5-dimension AI citation scoring framework
- [references/platform-ranking-factors.md](references/platform-ranking-factors.md) -- Per-engine ranking factors (2026)
- [references/geo-methods.md](references/geo-methods.md) -- Princeton GEO 9 methods with updated data
- [references/schema-templates.md](references/schema-templates.md) -- JSON-LD structured data templates
- [references/seo-checklist.md](references/seo-checklist.md) -- Prioritized P0/P1/P2 audit checklist
- [references/ai-writing-detection.md](references/ai-writing-detection.md) -- AI writing patterns to avoid
- [references/fix-prompt-templates.md](references/fix-prompt-templates.md) -- Fix prompt templates for AI coding agents
- [references/content-prompt-templates.md](references/content-prompt-templates.md) -- Content creation prompt templates for new pages (SEO + GEO optimized)

## Scripts

- `scripts/seo_audit.py` -- Full SEO + GEO audit (no API required). Checks meta tags, headings, robots.txt, sitemap, llms.txt, AI crawlers, schema, performance.

```bash
python3 scripts/seo_audit.py "https://example.com"          # summary
python3 scripts/seo_audit.py "https://example.com" --full    # detailed
python3 scripts/seo_audit.py "https://example.com" --ua "Custom/Agent"  # custom User-Agent
```

---

## Troubleshooting: URL Fetch Failures

URL fetching can fail for many reasons. Use this table to diagnose and recover.

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| 403 Forbidden | WAF/bot detection (Cloudflare, etc.) | Use `WebFetch` (Cursor/Claude Code) or curl with browser UA |
| 404 on known pages | URL path wrong OR CDN blocking non-browser agents | Verify URL in a browser, then try `WebFetch` |
| 429 Too Many Requests | Rate limiting | Wait and retry, or use `WebFetch` |
| 500 Server Error | Server issue or aggressive bot blocking | Retry with backoff (script does this automatically), try `WebFetch` |
| Connection timeout | Firewall blocking outbound requests | Use `WebFetch`, or ask user to paste content |
| Empty response | Bot trap returning empty body | Use `WebFetch`, verify the URL loads in a real browser |
| SSL/TLS error | Certificate issue or corporate MITM proxy | Add `--insecure` to curl (warn user), or use `WebFetch` |
| `curl: command not found` | Windows without curl or restricted env | Use Python script (`scripts/seo_audit.py`) or `WebFetch` |
| Script exits with code 2 | Connection/timeout error (no HTTP status) | Network issue; try `WebFetch` or check VPN/firewall |
| Script exits with code 1 | HTTP error (got a status code back) | Check the status code in output; likely bot detection |

**Platform-specific notes:**

- **Cursor**: Always prefer the `WebFetch` tool. It handles TLS, follows redirects, and bypasses most WAF blocks. If fetching a URL fails with `WebFetch`, do NOT silently skip the check -- inform the user with the error and suggest they paste the content or switch to codebase mode.
- **Claude Code**: Same as Cursor -- `WebFetch` is available and preferred.
- **Codex (OpenAI)**: Use available browser/web tools. Check your tool list for `WebFetch` or equivalent.
- **Windsurf**: Use built-in browsing capability. Falls back to shell commands.
- **Terminal-only agents (Aider, etc.)**: Must rely on shell commands. Use the Python script first (it has retry logic and UA rotation), then fall back to curl with a browser User-Agent.
- **GitHub Copilot Workspace**: Use platform web access tools. Fall back to Python script if unavailable.
