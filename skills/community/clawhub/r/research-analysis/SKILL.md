---
name: research-analysis
version: 1.0.0
description: "McKinsey-style business research and analysis skill. This skill should be used when the user needs consulting-grade insights, quantitative data modeling, competitor deep-dive analysis, user persona research, industry trend reports, or structured business problem-solving. Triggers on requests like analyze this market, compare competitors, build a user persona, estimate market size, write a research report, do a SWOT analysis, or any business research task requiring structured frameworks and data-driven conclusions."
author: nannl22
tags: ["business", "analysis", "research", "consulting", "competitor", "user-research", "data-modeling", "market-research"]
permissions: []
agent_created: true
---

# Research Analysis

## Overview

This skill provides McKinsey-style consulting analysis capabilities, including structured
thinking frameworks, quantitative modeling methods, competitor analysis templates, user
research methodologies, and tool integration guides. It transforms complex business
problems into conclusion-first, data-supported, actionable recommendations.

## Core Principles

All analysis must follow three rules:

1. **Conclusion first** - Lead with the answer, then support with data (pyramid principle)
2. **Data supported** - Every claim backed by evidence with cited sources
3. **Actionable** - End with specific, prioritized recommendations with timelines

## Analysis Workflow

### Step 1: Problem Definition

Clarify the core question before diving into analysis:

- Restate the user's question in SCQA format (Situation, Complication, Question, Answer)
- Identify the decision-maker and what decision they need to make
- Define the scope: what is in-scope vs. out-of-scope
- Determine the output format: executive summary, full report, presentation, or comparison table

### Step 2: Framework Selection

Load `references/analysis-frameworks.md` and select the appropriate framework(s):

| Problem Type | Recommended Framework |
|-------------|----------------------|
| Strategy formulation | SWOT + Porter's Five Forces |
| Market entry | 3C + TAM/SAM/SOM |
| Marketing optimization | 4P + Customer Journey |
| Business model design | Business Model Canvas |
| Problem decomposition | MECE + Issue Tree |
| Hypothesis testing | Hypothesis-Driven Analysis |
| Revenue growth | GMV decomposition / Funnel analysis |
| User needs | Kano Model |

Multiple frameworks can be combined for complex problems.

### Step 3: Data Collection and Analysis

Based on the analysis type, load the relevant reference files:

- **Competitor analysis** -> Load `references/competitor-analysis.md`
  - Use the 6-dimension framework (product, business model, market, company, operations, reputation)
  - Query enterprise data via Tianyancha MCP (see `references/tool-usage.md`)
  - Query app market data via Qimai (see `references/tool-usage.md`)

- **User research** -> Load `references/user-research.md`
  - Select research method based on goal (qualitative vs. quantitative)
  - Build user personas using the 3-dimension framework (demographic, behavioral, psychological)
  - Map user journeys with emotion curves and opportunity points
  - Segment users using RFM or lifecycle models

- **Quantitative modeling** -> Load `references/data-modeling.md`
  - Build metric systems (North Star metric -> core metrics -> process metrics)
  - Estimate market size using TAM/SAM/SOM or Fermi estimation
  - Calculate unit economics (LTV, CAC, payback period)
  - Analyze funnels, cohorts, and ROI
  - Perform sensitivity analysis on key variables

### Step 4: Data Visualization

Load `references/tool-usage.md` (VisActor section) and generate charts:

| Data relationship | Chart type | Tool |
|------------------|-----------|------|
| Trend over time | Line/area chart | VChart |
| Comparison | Bar chart | VChart |
| Composition | Pie/donut chart | VChart |
| Correlation | Scatter/bubble chart | VChart |
| Funnel conversion | Funnel chart | VChart |
| Retention analysis | Heatmap | VTable |
| Multi-dimensional | Radar chart | VChart |

Chart rules:
- Title states the conclusion, not the data description
- Annotate data source and date below each chart
- Use professional color palette; Chinese stock convention: red = up, green = down
- Generate as standalone HTML with VisActor CDN for browser rendering

### Step 5: Report Generation

Structure the final output as:

```
1. Executive Summary (3-5 key findings + top 3 recommendations)
2. Background & Methodology
3. Analysis (framework-driven, data-supported)
4. Key Findings (with visualizations)
5. Action Recommendations (prioritized table: P0/P1/P2 with timeline)
6. Data Sources & Limitations
```

## Tool Integration

### Tianyancha (Enterprise Data)

When enterprise information is needed (competitor background, financing, shareholders, IP, risk):

1. Check if `tyc-mcp` connector is connected (connector name: `tyc-mcp Tianyancha`)
2. If connected: call `mcp__tyc-mcp__*` tools to query enterprise data
3. If not connected: inform user to enable it in Connector Management, or use WebSearch
   to search Tianyancha public pages as fallback

### Qimai (App Market Data)

When app market data is needed (downloads, rankings, reviews, ASO):

1. Use WebSearch to find Qimai data pages for the target app
2. Use WebFetch to extract data from public Qimai pages
3. Alternatively, accept user-provided Qimai export files (Excel/CSV)

### VisActor (Charts)

Generate standalone HTML files with VisActor CDN for data visualization:

- VChart CDN: `https://unpkg.com/@visactor/vchart/build/index.min.js`
- VTable CDN: `https://unpkg.com/@visactor/vtable/build/index.min.js`
- Full code templates available in `references/tool-usage.md`

## Information Quality Standards

1. **Multi-source verification**: Key data points verified by at least 2 independent sources
2. **Source attribution**: Every data point annotated with source and date
3. **Fact vs. opinion**: Objective data separated from analyst opinions
4. **Timeliness**: Prioritize data from the last 6 months
5. **Confidence labeling**: Mark data confidence as high/medium/low

## Common Data Sources

| Data type | Recommended sources |
|-----------|-------------------|
| Industry reports | iResearch, QuestMobile, Aurora Mobile, IDC |
| Enterprise financing | Tianyancha, IT Juzi, Crunchbase |
| App market data | Qimai, SensorTower, App Annie |
| E-commerce data | Stardust, Mojing Market Intelligence |
| Macroeconomics | NBS, World Bank, IMF |
| Public company financials | CNINFO, Wind, East Money |
| Social media data | Newrank, WeIndex, Weibo Data Center |

## Bundled Resources

| File | Purpose |
|------|---------|
| `references/analysis-frameworks.md` | 10 consulting frameworks: MECE, SCQA, Pyramid, SWOT, Porter's Five Forces, 3C, 4P, BMC, Hypothesis-Driven, Kano |
| `references/competitor-analysis.md` | Competitor analysis methodology: 6-dimension framework, selection strategy, comparison templates, SWOT deep-dive, report template |
| `references/user-research.md` | User research methods: persona building, journey mapping, need discovery, RFM segmentation, lifecycle staging, report template |
| `references/data-modeling.md` | Quantitative modeling: metric systems, TAM/SAM/SOM, unit economics, funnel analysis, cohort retention, ROI, forecasting |
| `references/tool-usage.md` | Tool integration guides: Tianyancha MCP, Qimai data, VisActor chart templates, web search strategies, data source directory |

## Changelog

### v1.0.0
- Initial release
- 10 consulting frameworks (MECE, SCQA, Pyramid, SWOT, Porter's Five Forces, 3C, 4P, BMC, Hypothesis-Driven, Kano)
- 6-dimension competitor analysis methodology
- User research toolkit (personas, journey maps, RFM, lifecycle)
- Quantitative modeling (TAM/SAM/SOM, unit economics, funnel, cohort, ROI)
- Tool integration guides (Tianyancha, Qimai, VisActor)
