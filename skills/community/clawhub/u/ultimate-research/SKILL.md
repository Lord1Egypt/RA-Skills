---
name: ultimate-research
description: Orchestrate broad or multi-domain research by routing every query through a mandatory core of memory, self-improvement, brainstorming, research, web scraping, and market research, then add only the specialist skills that materially improve the answer. Use when the user wants a researched recommendation, strategy, competitive analysis, market or SEO guidance, a current digest, or any ambiguous query that needs one clarifying question or a structured synthesis.
---

# Ultimate Research

## Operating model

Turn one vague or broad question into one high-confidence answer.

## Rules

- Ask **one** clarifying question when the query is too vague to route well.
- Always use the mandatory core: `web-scraper`, `self-improvement`, `supermemory`, `brainstorming`, `zo-research-topic`, and `market-research`.
- Add only the specialist skills that materially improve the answer.
- Prefer the smallest useful set of extra skills. Do not run everything beyond the mandatory core.
- Never invent facts. If evidence is missing, say so.
- For research-heavy answers, include citations and source links.
- Return a structured answer in this exact order:
  1. Question breakdown
  2. Skills used
  3. Evidence
  4. Recommendation
  5. Next steps

## Routing sequence

1. **Scope the question**
   - Identify the actual decision, not just the topic.
   - If vague, ask one clarifying question and stop.

2. **Load context**
   - Use `supermemory` for prior decisions, preferences, projects, and recurring context.
   - Use `self-improvement` as a quick sanity and quality layer on every query.
   - Use `brainstorming` to narrow the angle, compare approaches, and define success criteria.
   - Use `zo-research-topic` for general deep research and synthesis.

3. **Ground the answer**
   - Use `web-scraper` for current web pages, extraction, verification, and quotes.
   - Use `market-research` for market sizing, industry data, demand signals, and quantitative context.

4. **Add specialist skills only when they help**
   - Market and growth: `marketing-ideas`, `marketing-psychology`, `pricing-strategy`, `free-tool-strategy`, `launch-strategy`, `competitor-alternatives`.
   - Search and growth: `seo-audit`, `programmatic-seo`, `analytics-tracking`, `zo-daily-news-digest`.

5. **Synthesize once**
   - Merge the outputs into one answer.
   - Resolve conflicts explicitly.
   - Prefer concrete conclusions over open-ended notes.

6. **Quality check**
   - Remove redundancy.
   - Keep only the best evidence.
   - Flag uncertainty.

## Specialist skill map

- `market-research`: industry size, BLS/FRED/Census, market demand, NAICS, TAM-style questions.
- `seo-audit`: rankings, indexation, crawlability, technical SEO, on-page SEO, organic traffic issues.
- `marketing-psychology`: persuasion, behaviour, decision-making, cognitive bias, framing, pricing psychology.
- `marketing-ideas`: growth ideas, acquisition channels, campaign ideas, promotional strategy.
- `pricing-strategy`: tiers, packaging, value metrics, willingness to pay, freemium, monetisation.
- `free-tool-strategy`: lead-gen tools, calculators, generators, engineering-as-marketing, SEO tool ideas.
- `launch-strategy`: launches, beta, early access, Product Hunt, announcements, rollout planning.
- `zo-daily-news-digest`: recurring current-news monitoring or digest-style news summaries.
- `competitor-alternatives`: alternative pages, versus pages, comparison pages, competitive positioning.
- `analytics-tracking`: GA4, GTM, events, attribution, conversion tracking, measurement plans.
- `programmatic-seo`: template-driven SEO at scale, directory pages, location pages, comparison pages.

## Use the helper script

Use `scripts/ultimate_research.py` when you want a fast deterministic routing draft for a query. It produces a structured plan with recommended skills and an answer outline.

## Output standard

Default to concise, structured answers. Expand only when the evidence or decision complexity justifies it.