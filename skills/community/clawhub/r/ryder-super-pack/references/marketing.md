# Marketing (OpenClaw Optimized)

This reference defines the high-performance marketing frameworks and workflows for AI agents operating within the OpenClaw environment, merging Perplexity's research depth with OpenClaw's execution capabilities.

## 1. Content Creation & SEO (The Execution Engine)

OpenClaw agents should use `web_search` and `web_fetch` to build data-driven content.

### SEO Workflow (OpenClaw Style)
1. **Keyword Research**: Use `web_search` to find high-volume, low-difficulty keywords.
2. **Competitor Audit**: Use `web_fetch` on top 3 SERP results to analyze structure and gaps.
3. **Brief Generation**: Create a `content-brief.md` in the workspace.
4. **Drafting**: Use the templates below to generate high-quality drafts.
5. **Optimization**: Run a check against the "Semantic Terms" identified in step 2.

### Blog Post Templates
- **How-To**: Focus on actionable steps. Use `exec` to verify technical steps if applicable.
- **Listicle**: Curate the "best of" using real-time web data.
- **Thought Leadership**: Use `web_search` to find "conventional wisdom" and then generate a contrarian take.

---

## 2. Campaign Planning & Demand Gen

### The "Always-On" Agent Workflow
- **Monitoring**: Use `heartbeat` to check campaign performance or social mentions.
- **Adjustment**: If `web_fetch` of analytics shows a dip, the agent should proactively suggest a budget reallocation or creative refresh.
- **Launch Checklist**: Use `PLAN.md` to track launch tasks across channels.

---

## 3. Analytics & Performance (Data-Driven Decisions)

### Tool-Integrated Analytics
- **Data Ingestion**: Use `read` to ingest CSV exports of marketing data.
- **Analysis**: Use `exec` with Python scripts to run cohort analysis or MMM (Marketing Mix Modeling).
- **Reporting**: Automatically generate a `MARKETING_REPORT.md` and deliver it via the active channel (Telegram/Discord).

---

## 4. Competitive Intelligence & PMM

### Real-Time Battlecards
1. **Trigger**: User mentions a competitor.
2. **Action**: Agent runs `web_search` for "[Competitor] vs [Our Product]" and `web_fetch` on their pricing page.
3. **Output**: Generate a temporary `BATTLECARD.md` for immediate tactical use.

---

## 5. App Store Optimization (ASO)

### Mobile Growth Workflow
- **Keyword Evaluation**: Use `web_search` to find trending app terms.
- **Review Mining**: Use `web_fetch` on app store web views to extract and summarize user sentiment/pain points for copy optimization.

---

## 6. Prompt Engineering for Marketing (OpenClaw Specific)

### Role-Based Dispatches
- **The Copywriter**: Use `subagent spawn` with a "Senior Direct Response Copywriter" persona for high-conversion ads.
- **The Strategist**: Use the main session for high-level campaign architecture and budget decisions.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
