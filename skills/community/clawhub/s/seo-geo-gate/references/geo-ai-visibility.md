# GEO — Generative Engine Optimization (AI / LLM visibility)

GEO = being found, cited, and **recommended** by AI assistants (ChatGPT, Claude, Perplexity, Gemini, AI Overviews). Classic SEO gets you into Google's index; GEO gets you into the model's answer. The two share a foundation (crawlable, structured, fast) but GEO adds three things: **let the AI crawlers in**, **give them an AI-readable map (`llms.txt`)**, and **describe your entity in schema (`knowsAbout`)**.

> Strategic stance: if your business depends on AI discovery, you *want* AI crawlers. The common reflex of blocking GPTBot/CCBot to "protect content" directly removes you from the systems that recommend products. Decide deliberately.

---

## 1. robots.txt — explicitly allow the AI crawlers
Default `User-agent: *` rules don't reliably cover AI bots, and some managed robots presets **block them by default**. Allow them explicitly. Exact user-agents that matter (2026):

| Operator | Crawl/Train | Search | User-initiated fetch |
|---|---|---|---|
| OpenAI | `GPTBot` | `OAI-SearchBot` | `ChatGPT-User` |
| Anthropic | `ClaudeBot` | `Claude-SearchBot` | `Claude-User` |
| Perplexity | — | `PerplexityBot` | `Perplexity-User` |
| Google AI | `Google-Extended` (training control token) | (Googlebot for AI Overviews) | — |
| Common Crawl | `CCBot` (feeds many open models) | — | — |
| Others | `Bytespider`, `Amazonbot`, `Applebot-Extended` | | |

Template (production):
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/admin/

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: https://www.example.com/sitemap.xml
```
`audit-live.mjs` reports which of these are allowed vs blocked.

**Pitfalls (learned in prod):**
- Some platforms (e.g. Cloudflare "AI Crawl Control / Managed robots.txt") **inject their own robots rules ahead of your origin's**, silently `Disallow:` the AI bots, and override what your app serves. This is a zone/dashboard toggle your code can't see. **Verify robots policy on the real production origin**, not a staging domain (staging often shows the injected version). Never enable a managed "block AI" preset on the domain you want AI traffic to.
- Staging/dev should be `Disallow: /` (don't index pre-prod). Branch robots by environment.

## 2. `llms.txt` — an AI-readable site map
A Markdown file at `/llms.txt`: a curated, sectioned index of your authoritative pages so an LLM can orient without crawling everything. Order sections by importance; exclude noise (legal, pure lead-capture forms).

```
# Example

> One-paragraph description of what the company/site is and does.

## Start here
- [Home](https://www.example.com/): what we do in one line
- [Product](https://www.example.com/product/): the core offering

## Concepts & definitions
- [Glossary term](https://www.example.com/glossary/term/): short gloss

## Research & resources
- [Whitepaper](https://www.example.com/whitepapers/x/): what it covers
- [Blog post](https://www.example.com/blog/y/): what it covers

## Industry guides
- [Guide](https://www.example.com/industries/z/): who it's for
```
Generate it from your route table (same source as the sitemap) so it never drifts. `audit-live.mjs` checks `/llms.txt` exists and is non-empty.

## 3. Entity schema — `knowsAbout`
See `structured-data.md`. The `Organization.knowsAbout` array is the most direct lever on "what does the model think this brand is about" — list 6–10 specific topics you want to be recommended for.

## 4. IndexNow — push freshness on deploy
IndexNow tells Bing/Yandex (and via Bing, Copilot) about new/changed URLs instantly instead of waiting for a crawl. One-time: host a key file at `/{key}.txt`. On each deploy, POST changed URLs:
```
POST https://api.indexnow.org/indexnow
Content-Type: application/json; charset=utf-8
{ "host": "www.example.com", "key": "<key>",
  "keyLocation": "https://www.example.com/<key>.txt",
  "urlList": ["https://www.example.com/page/", ...] }
```
200/202 = accepted. Wire it into the deploy pipeline (reference: `indexnow-ping.mjs`, run post-deploy with all routes).

## 5. Content shape for AI extraction
Beyond infra, LLMs preferentially quote content that is:
- **Direct and factual** — lead with the answer, then elaborate (inverted pyramid). LLMs extract the first clear statement.
- **Well-structured** — real headings, lists, tables, definitions. A glossary/FAQ page is highly quotable.
- **Self-contained** — each page answers one question fully; don't require reading three pages to get the point.
- **Entity-explicit** — name the product/brand/category in text, not just images, so retrieval and attribution work.

## What "good GEO" looks like (the reference site prod, verified)
robots allows GPTBot/OAI-SearchBot/ChatGPT-User/ClaudeBot/Claude-User/Claude-SearchBot/PerplexityBot/Perplexity-User/Google-Extended/GoogleOther · declares Sitemap · `/llms.txt` present · homepage `@graph` ships Organization+WebSite+FAQPage+Service+Product+SoftwareApplication · HSTS + `Vary: User-Agent` headers. Run `audit-live.mjs <origin>` and aim for the same.
