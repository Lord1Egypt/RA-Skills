---
name: research-cog
description: "AI deep research powered by CellCog. Market research, competitive analysis, investment research, academic research, due diligence, literature reviews with citations, financial analysis, crypto research, news intelligence. Multi-source synthesis across hundreds of sources. #1 on DeepResearch Bench (Apr 2026)."
author: CellCog
homepage: https://cellcog.ai
metadata:
  openclaw:
    emoji: "🔬"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
dependencies: [cellcog]
---
# Research Cog - Deep Research Powered by CellCog

**#1 on DeepResearch Bench (Apr 2026).** Your AI research analyst for comprehensive, citation-backed research on any topic.

Leaderboard: https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## What You Can Research

### Competitive Analysis

Analyze companies against their competitors with structured insights:

- **Company vs. Competitors**: "Compare Stripe vs Square vs Adyen - market positioning, pricing, features, strengths/weaknesses"
- **SWOT Analysis**: "Create a SWOT analysis for Shopify in the e-commerce platform market"
- **Market Positioning**: "How does Notion position itself against Confluence, Coda, and Obsidian?"
- **Feature Comparison**: "Compare the AI capabilities of Salesforce, HubSpot, and Zoho CRM"

### Market Research

Understand markets, industries, and trends:

- **Industry Analysis**: "Analyze the electric vehicle market in Europe - size, growth, key players, trends"
- **Market Sizing**: "What's the TAM/SAM/SOM for AI-powered customer service tools in North America?"
- **Trend Analysis**: "What are the emerging trends in sustainable packaging for 2026?"
- **Customer Segments**: "Identify and profile the key customer segments for premium pet food"
- **Regulatory Landscape**: "Research FDA regulations for AI-powered medical devices"

### Stock & Investment Analysis

Financial research with data and analysis:

- **Company Fundamentals**: "Analyze NVIDIA's financials - revenue growth, margins, competitive moat"
- **Investment Thesis**: "Build an investment thesis for Microsoft's AI strategy"
- **Sector Analysis**: "Compare semiconductor stocks - NVDA, AMD, INTC, TSM"
- **Risk Assessment**: "What are the key risks for Tesla investors in 2026?"
- **Earnings Analysis**: "Summarize Apple's Q4 2025 earnings and forward guidance"

### Academic & Technical Research

Deep dives with proper citations:

- **Literature Review**: "Research the current state of quantum error correction techniques"
- **Technology Deep Dive**: "Explain transformer architectures and their evolution from attention mechanisms"
- **Scientific Topics**: "What's the latest research on CRISPR gene editing for cancer treatment?"
- **Historical Analysis**: "Research the history and impact of the Bretton Woods system"

### Due Diligence

Comprehensive research for decision-making:

- **Startup Due Diligence**: "Research [Company Name] - founding team, funding, product, market, competitors"
- **Vendor Evaluation**: "Compare AWS, GCP, and Azure for enterprise AI/ML workloads"
- **Partnership Analysis**: "Research potential risks and benefits of partnering with [Company]"

---

## Research Output Formats

CellCog can deliver research in multiple formats:

| Format | Best For |
|--------|----------|
| **Interactive HTML Report** | Explorable dashboards with charts, expandable sections |
| **PDF Report** | Shareable, printable professional documents |
| **Markdown** | Integration into your docs/wikis |
| **Plain Response** | Quick answers in chat |

Specify your preferred format in the prompt:
- "Create an interactive HTML report on..."
- "Generate a PDF research report analyzing..."
- "Give me a markdown summary of..."

---

## Chat Mode for Research

| Scenario | Recommended Mode |
|----------|------------------|
| Trivial lookups, basic facts | `"agent"` |
| Deep research, competitive analysis, market research, investment analysis | `"agent team"` |
| Cutting-edge academic research, high-stakes due diligence, institutional-grade analysis | `"agent team max"` |

**Use `"agent team"` for most research** (the default). Agent team mode enables multi-source research, cross-referencing, citation verification, and deeper analysis with multiple reasoning passes.

**Use `"agent"` only for trivial lookups** like "What's Apple's stock ticker?"

**Use `"agent team max"` for cutting-edge academic research and high-stakes due diligence** — when the research directly informs costly decisions (investment thesis, M&A, regulatory compliance, PhD-level analysis). All settings maxed for the deepest reasoning. The quality gain is incremental but meaningful when accuracy is critical. Requires ≥2,000 credits.

---

## Research Quality Features

### Citations (On Request)

**Citations are NOT automatic.** CellCog focuses on delivering accurate, well-researched content by default.

If you need citations:
- **Explicitly request them**: "Include citations for all factual claims with source URLs"
- **Specify format**: "Provide citations as footnotes" or "Include a references section at the end"
- **Indicate placement**: "Citations inline" vs "Citations in appendix"

Without explicit citation requests, CellCog prioritizes delivering accurate information efficiently.

### Data Accuracy
CellCog cross-references multiple sources for financial and statistical data, ensuring accuracy even without explicit citations.

### Structured Analysis
Complex research is organized with clear sections, executive summaries, and actionable insights.

### Visual Elements
Research reports can include:
- Charts and graphs
- Comparison tables
- Timeline visualizations
- Market maps

---

## Example Research Prompts

**Quick competitive intel:**
> "Compare Figma vs Sketch vs Adobe XD for enterprise UI design teams. Focus on collaboration features, pricing, and Figma's position after the Adobe acquisition failed."

**Deep market research:**
> "Create a comprehensive market research report on the AI coding assistant market. Include market size, growth projections, key players (GitHub Copilot, Cursor, Codeium, etc.), pricing models, and enterprise adoption trends. Deliver as an interactive HTML report."

**Investment analysis:**
> "Build an investment analysis for Palantir (PLTR). Cover business model, government vs commercial revenue mix, AI product strategy, valuation metrics, and key risks. Include relevant charts."

**Academic deep dive:**
> "Research the current state of nuclear fusion energy. Cover recent breakthroughs (NIF, ITER, private companies like Commonwealth Fusion), technical challenges remaining, timeline to commercial viability, and investment landscape."

---

## Tips for Better Research

1. **Be specific**: "AI market" is vague. "Enterprise AI automation market in healthcare" is better.

2. **Specify timeframe**: "Recent" is ambiguous. "2025-2026" or "last 6 months" is clearer.

3. **Define scope**: "Compare everything about X and Y" leads to bloat. "Compare X and Y on pricing, features, and market positioning" is focused.

4. **Request structure**: "Include executive summary, key findings, and recommendations" helps organize output.

5. **Mention output format**: "Deliver as PDF" or "Create interactive HTML dashboard" gets you the right format.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
