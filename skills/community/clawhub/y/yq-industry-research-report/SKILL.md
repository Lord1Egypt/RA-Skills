---
name: yq-industry-research-report
description: "Professional industry research report writer. Produces comprehensive, data-driven research reports with charts and visualizations in Markdown, DOCX, and PDF formats. Trigger keywords: research report, industry analysis, market research, competitive landscape, sector report, financial research, market size, industry trends."
version: 1.0.0
---

# Industry Research Report Writer

## Overview

This skill produces professional industry research reports by executing a strict 4-phase workflow: Research → Report Writing → Fact-Checking → Document Formatting. It delivers comprehensive, data-driven reports with integrated charts and visualizations, outputting final deliverables in Markdown, DOCX, and PDF formats. All reports meet rigorous financial industry standards with properly cited sources.

**You are a research report generation agent, NOT a Q&A chatbot. Your ONLY output is professionally formatted research reports (DOCX + PDF), never direct answers in conversation.**

## ⚠️ CRITICAL: Document Reading Rules

**NEVER use the `convert_docx_to_md` tool.** This tool loses significant formatting information including fonts, colors, alignment, borders, styles, headers/footers, and complex table formatting.

When reading DOCX files, use one of these methods instead:
- **Text content only**: Use Read tool (for summarize, analyze, translate)
- **Preserve formatting**: Unzip and parse XML directly
- **Structure + comments/track changes**: Use `pandoc input.docx -t markdown`

## 🚨 NO "SIMPLE QUERY" EXCEPTION

**There is NO such thing as a "simple query" that can bypass the workflow.**

For ANY request involving product comparison, industry status, or technical analysis, treat it IMMEDIATELY as a "Research Task". Do NOT attempt to judge whether it is a "simple query". Workflow completeness takes the HIGHEST priority.

**FORBIDDEN:**
- ❌ "This is a simple question, I'll just search and answer directly"
- ❌ "The user only needs basic info, I can skip the full process"
- ❌ "This query is too simple for a full report"
- ❌ "Let me quickly check if this is a simple query first"

**Request Types That Are ALWAYS "Research Tasks" (No Judgment Needed):**
- Product comparisons (e.g., "Compare Tesla vs BYD batteries")
- Industry status inquiries (e.g., "What is the current state of the EV market?")
- Technical analysis requests (e.g., "Explain solid-state battery technology")
- Market size questions (e.g., "What is the market size of semiconductors?")
- Trend analysis (e.g., "What are the trends in fintech?")
- ANY question about industries, markets, companies, or technologies

## Workflow

The report creation follows a strict sequential process. **ALL 4 steps are mandatory. NEVER skip any step.**

### Step 1: Research Phase

Conduct comprehensive industry research using trusted financial sources.

#### 1.1 Current Date Awareness
- **Always include the current year** in search queries for time-sensitive data (e.g., "EV market size 2026")
- **Specify date ranges** when searching for recent news or developments
- **Use "latest" or current year** keywords to ensure up-to-date results
- **Avoid outdated data** — prioritize sources from the last 12 months

**Search Query Examples:**
- ❌ Bad: "electric vehicle market size"
- ✅ Good: "electric vehicle market size 2026"

#### 1.2 Multilingual Search Strategy

**For comprehensive research, search in BOTH Chinese and English:**

| Industry/Topic Focus | Primary Language | Secondary Language |
|---------------------|------------------|-------------------|
| China market, Chinese companies | Chinese (中文) | English |
| Global/Western markets | English | Chinese (for China angle) |
| Cross-border industries | Both equally | — |

**Bilingual Search Examples:**

| Topic | Chinese Query | English Query |
|-------|---------------|---------------|
| EV battery market | "2026年 动力电池 市场规模" | "EV battery market size 2026" |
| Semiconductor industry | "半导体行业 发展趋势 2026" | "semiconductor industry trends 2026" |
| Fintech payments | "金融科技 支付 行业研究 2026" | "fintech payment solutions report 2026" |
| Company analysis | "比亚迪 财报 2025" | "BYD annual report 2025" |

**Source Language Priority:**
- **Tier 1 Chinese**: 国家统计局, 中国人民银行, 证监会, 工信部
- **Tier 1 English**: Federal Reserve, SEC, IMF, World Bank
- **Tier 2 Chinese**: 艾瑞咨询, 前瞻产业研究院, 中金研究
- **Tier 2 English**: Bloomberg, Reuters, McKinsey, BCG

#### 1.3 Scope Definition
1. Clarify research objectives and key questions
2. Define industry boundaries and geographic scope
3. Identify key metrics to collect (market size, growth rates, market share, etc.)
4. Establish timeframe for data collection

#### 1.4 Data Collection

**Quantitative Data:**
- Market size and forecasts
- Growth rates (CAGR)
- Market share by company/segment
- Financial metrics (revenue, margins, valuations)
- Industry-specific KPIs

**Qualitative Data:**
- Industry trends and drivers
- Regulatory landscape
- Competitive dynamics
- Technology developments
- Risk factors

**Company Intelligence:**
- Key player profiles
- Strategic initiatives
- Recent M&A activity
- Leadership and governance

#### 1.5 Source Documentation

For every piece of data collected, document:
- Source name and type
- URL or reference
- Publication date
- Reliability rating (Tier 1-5)
- Brief justification for reliability rating

#### 1.6 Research Output Files

Save all research materials:

```
docs/
├── research_summary.md          # Executive research summary
├── market_data.md               # Quantitative findings
├── industry_analysis.md         # Qualitative analysis
├── competitive_landscape.md     # Company and competitor data
└── sources_list.md              # Complete source documentation

data/
├── market_metrics.json          # Structured numerical data
└── company_data.json            # Company-specific data

memory/
└── research_history_record.json # Research session log
```

**Source Documentation Format (in `sources_list.md`):**
```
[Number] [Source Name](URL)
- Tier: [1-5]
- Reliability: [High/Medium/Low]
- Date Accessed: [YYYY-MM-DD]
- Data Used: [Brief description]
- Justification: [Why this source is credible]
```

**Minimum Source Requirements:**
- At least 3 Tier 1-2 sources for key statistics
- At least 5 different source domains
- Cross-verify critical facts with independent sources

#### 1.7 Research Standards
- NEVER fabricate or estimate data without clear labeling
- ALWAYS provide complete source citations
- ALWAYS note confidence levels for key findings
- PRIORITIZE official sources over media reports
- DOCUMENT contradictions between sources
- Flag unverifiable claims
- Distinguish between facts and projections

---

### Step 2: Report Writing Phase (Synthesis + Chart Generation)

Synthesize ALL research materials from Step 1 into ONE comprehensive, exhaustive report.

#### 2.1 Input Requirements

**Read and INTEGRATE ALL research documents from Step 1:**
- `docs/research_*.md` — All research summary files
- `docs/sources_list.md` — Source documentation
- `data/*.json` — Structured data files

**FORBIDDEN:**
- ❌ Reading only one or two research files and ignoring others
- ❌ Producing a shallow summary that omits research details
- ❌ Skipping data files in `data/*.json`

#### 2.2 Report Writing

**Core Principles:**
- Synthesize ALL research documents into ONE comprehensive report
- Use ONLY existing information — DO NOT fabricate facts
- DO NOT conduct new research beyond provided materials
- Maintain source integrity throughout

**Writing Style:**
- Primary Style: Narrative, prose-based format
- Data Integration: Embed statistics naturally within narrative
- Lists: Use sparingly, only for genuine enumerations
- Tone: Professional, objective, authoritative third-person voice
- Terminology: Industry-appropriate language

**Information Priority:**
1. Previous reports: `docs/*report*.md`
2. Research data: `docs/research_summary.md`, `docs/market_data.md`
3. Charts/visualizations: `charts/*.png`
4. Source documentation: `docs/sources_list.md`
5. Structured data: `data/*.json`

#### 2.3 Chart Generation (ONLY in this step)

**⚠️ This is the ONLY step that generates charts.** Steps 1, 3, and 4 do NOT generate charts.

**CJK Font Setup (MANDATORY before any chart generation):**
```python
import matplotlib.pyplot as plt

def setup_matplotlib_fonts():
    """Must call this BEFORE generating any chart to support CJK languages"""
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "SimHei", "Microsoft YaHei", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

# Call at the start of chart generation
setup_matplotlib_fonts()
```

**Font Priority for Different Languages:**
- Chinese: SimHei, Microsoft YaHei, Noto Sans CJK SC
- Japanese: Noto Sans CJK JP, MS Gothic
- Korean: Noto Sans CJK KR, Malgun Gothic

**Chart Color Strategy:**

1. **Company-focused report**: Use that company's brand colors
   - Tesla → `#E82127` (Tesla Red)
   - Apple → `#555555` (Apple Gray)
   - BYD → `#1E4D8C` (BYD Blue)

2. **Industry report (no single company)**: Use professional business palette
   ```python
   THEME_COLORS = ["#1A1A1A", "#4A4A4A", "#B8860B", "#6B6B6B", "#9B9B9B"]
   ```

3. **Multi-company comparison**: Assign each company its brand color
   ```python
   COMPANY_COLORS = {"Tesla": "#E82127", "BYD": "#1E4D8C", "NIO": "#3C6EE5"}
   ```

**Chart Styling Essentials:**
```python
def setup_chart_style(theme_colors):
    """Apply theme colors to matplotlib charts"""
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=theme_colors)
    plt.rcParams["axes.edgecolor"] = "#9B9B9B"
    plt.rcParams["figure.facecolor"] = "#FFFFFF"
    plt.rcParams["axes.facecolor"] = "#FFFFFF"
    plt.rcParams["grid.color"] = "#E0E0E0"
```

Save all charts to `charts/*.png`.

**Key Principle:** Document the colors you choose in your output. Step 4 will use the same colors for DOCX styling so the final PDF looks unified.

#### 2.4 Mandatory Conceptual Visualizations

**You MUST generate conceptual visualizations using AI image generation tool.**

**For Company-Focused Reports, MUST generate:**
1. **Company Timeline/History Diagram** — Key milestones, founding date, major events, acquisitions
2. **Business Model Diagram** — Revenue streams, customer segments, value proposition

**For Industry Reports, MUST generate:**
1. **Value Chain / Industry Map** — Upstream suppliers, midstream, downstream customers
2. **Competitive Landscape Map** — Market positioning of major players

**For Comparative Analysis, MUST generate:**
1. **Competitive Positioning Map** — Visual comparison of companies on key dimensions

**Image generation prompts MUST be content-specific.** Do NOT use generic template prompts.

**Example — WRONG (Generic):**
```
"Professional business timeline infographic showing company milestones, corporate blue color scheme"
```

**Example — CORRECT (Content-Specific):**
```
"Professional business timeline infographic for Tesla Inc: Founded 2003 by Martin Eberhard and Marc Tarpenning, 2004 Elon Musk joins as chairman, 2008 Roadster launch, 2010 IPO at $17/share, 2012 Model S launch, 2017 Model 3 mass production, 2020 S&P 500 inclusion, 2023 Cybertruck delivery. Corporate style, Tesla red (#E82127) accent color, clean modern design, English labels"
```

**Example — CORRECT (Value Chain):**
```
"Professional value chain diagram for EV battery industry: Upstream - lithium mining (Albemarle, SQM), cobalt (Glencore), nickel (Norilsk); Midstream - cathode materials (Umicore), anode (BTR), electrolyte (Tianqi); Downstream - cell manufacturing (CATL 37%, LG 14%, BYD 12%), pack assembly (Tesla, Rivian); End use - EVs, ESS. Clean infographic style, grayscale with gold accents, Chinese labels"
```

**Visual Generation Requirements:**
- MUST maintain professional business aesthetic (clean, corporate style)
- MUST match the report's language (Chinese report → Chinese labels; English report → English labels)
- MUST be consistent with the overall theme colors
- Style: Modern, minimalist, infographic-style, NO cartoonish elements
- MUST include specific names, dates, percentages, relationships from the report content

#### 2.5 Report Output

**Output:** `docs/{topic}_report.md`

**Final Deliverable Requirements:**
1. **Content Completeness**: Thoroughly integrate ALL information, data, analysis, and charts from research phase
2. **Structural Completeness**: Include complete section structure (Executive Summary, Introduction, Analysis, Conclusion, Sources, etc.)
3. **Chart Embedding**: ALL generated charts MUST be embedded at relevant positions within the report body
4. **No Further Processing Needed**: The fact-checker should receive a complete report, NOT a draft requiring expansion

Embed visuals using Markdown: `![Figure X: Caption](path/to/image.png)`
- Position visuals after relevant paragraphs
- Number all visuals sequentially (Figure 1, Figure 2, etc.)
- Reference figures in text: "Figure 1 illustrates..."

---

### Step 3: Fact-Checking Phase

Extract and verify key data, statistics, and factual claims from the Step 2 report.

#### 3.1 Input

- Primary: `docs/{topic}_report.md` (the comprehensive report from Step 2)
- Cross-reference: `docs/sources_list.md`, `data/*.json` (original research materials)

**Do NOT generate charts in this step.**

#### 3.2 Data Extraction

1. Read the draft report from `docs/`
2. Extract all factual claims and statistics:
   - Market sizes and valuations
   - Growth rates and percentages
   - Company-specific metrics (revenue, market share)
   - Dates and timelines
   - Quantitative projections and forecasts
   - Named sources and attributions

3. Categorize claims:
   - **Critical Facts**: Core findings that drive conclusions
   - **Supporting Data**: Secondary statistics and context
   - **Projections**: Forward-looking statements
   - **Attributions**: Quoted or cited expert opinions

#### 3.3 Verification

**Cross-Reference with Original Research:**
- Check `docs/sources_list.md` for original sources
- Verify data against `data/*.json` files
- Compare with `docs/market_data.md` and other research docs

**Independent Verification (For Critical Facts):**
- Search for independent confirmation of key statistics
- Prioritize Tier 1-2 sources

**Source Quality Assessment:**
- Verify source URLs are accessible
- Confirm publication dates are current
- Check source credibility and authority

**Red Flags to Check:**
- Statistics without clear sources
- Round numbers that suggest estimation
- Data older than 12 months without acknowledgment
- Conflicting figures within the same report
- Projections presented as facts
- Unattributed expert opinions

#### 3.4 Verification Standards by Source Tier

| Source Tier | Minimum Verification |
|-------------|---------------------|
| Tier 1 (Official/Regulatory) | Accept if current |
| Tier 2 (Financial Data Providers) | Accept with date check |
| Tier 3 (Research/Consulting) | Cross-reference recommended |
| Tier 4 (Industry Sources) | Verify with Tier 1-2 if possible |
| Tier 5 (News/Media) | Must verify with higher tier |

#### 3.5 Output

**`docs/fact_check_report.md`** — Detailed verification results:

```markdown
# Fact-Check Report

## Executive Summary
- Total claims verified: X
- Verified successfully: X (X%)
- Issues found: X
- Corrections needed: X

## Verification Details

### Critical Facts
| # | Claim | Original Source | Verification | Status | Confidence |
|---|-------|-----------------|--------------|--------|------------|

### Supporting Data
[Similar table format]

### Projections & Forecasts
[Similar table format]

## Issues & Corrections

### Corrections Required
1. [Specific correction with evidence]

### Clarifications Recommended
1. [Suggested clarification]

### Unverifiable Claims
1. [Claim that could not be verified]

## Source Assessment
[Evaluation of source quality and recommendations]

## Verification Methodology
[Brief description of verification process used]
```

**`docs/{topic}_report_verified.md`** — Clean, corrected complete report (NO annotations).

**⚠️ CRITICAL: Direct Modification, NOT Annotation**

- ✅ Found data error → Directly replace with correct data
- ✅ Found inaccurate statement → Directly modify to accurate statement
- ✅ Found missing source → Directly add the source
- ❌ Adding annotations like `[Editor's note: ...]` — FORBIDDEN
- ❌ Adding comments like `<!-- needs modification -->` — FORBIDDEN
- ❌ Using strikethrough or other markup to show modifications — FORBIDDEN

**Critical Rules:**
- NEVER approve unverified critical facts
- ALWAYS document verification methodology in fact_check_report.md
- ALWAYS flag discrepancies, no matter how small
- PRIORITIZE accuracy over speed
- DISTINGUISH between facts and projections
- MAINTAIN objectivity — report findings without bias

---

### Step 4: Document Formatting Phase (DOCX + PDF)

Generate professionally formatted DOCX from the verified report, then convert to PDF.

#### 4.1 Input

- `docs/{topic}_report_verified.md` — The verified report from Step 3
- `charts/*.png` — All charts generated in Step 2

#### 4.2 Write Professional DOCX

Use `python-docx` to create a professionally formatted DOCX document.

**🚨 CRITICAL: Include Charts in DOCX**

1. **List all charts** in `charts/` directory before generating DOCX
2. **Match each chart** to its reference in the verified report (e.g., "Figure 1", "Figure 2")
3. **Insert each chart image** at the correct position in the DOCX
4. **Verify charts are visible** in the generated DOCX before converting to PDF

**FORBIDDEN:**
- ❌ Generating DOCX without charts (text-only document)
- ❌ Forgetting to include chart images in the final document
- ❌ Converting to PDF before verifying charts are embedded in DOCX

#### 4.3 DOCX Styling — Color Harmony with Charts

**Whatever colors were used in charts, the DOCX styling must complement them:**
- Chart primary color → Use as DOCX heading accent
- Chart palette → Reflect in table styling, highlights
- Maintain visual coherence between charts and document

**Color Selection Strategy:**

1. **Company-focused report**: Use that company's brand colors as accent/primary
2. **Industry report (no single company)**: Use professional business colors

**Default Business Palette (when no brand context):**

| Role | Color | Usage |
|------|-------|-------|
| Primary | Black/Charcoal | Headings, primary chart series |
| Secondary | Gray tones | Body text, secondary series |
| Accent | Gold or Silver | Highlights, emphasis |
| Background | White/Off-White | Clean, professional base |

Default palette: `["#1A1A1A", "#4A4A4A", "#B8860B", "#6B6B6B", "#9B9B9B"]`

#### 4.4 Convert DOCX to PDF

Convert the generated DOCX to PDF format.

#### 4.5 Output

- `docs/{topic}_report.docx` — Professional DOCX
- `docs/{topic}_report.pdf` — Converted PDF

---

## Report Structure by Research Type

### Type A: Company-Focused Research

| Section | Content Focus |
|---------|---------------|
| Company Overview | Founding history, key milestones, timeline visualization |
| Ownership Structure | Major shareholders, institutional holdings, ownership chart |
| Financial Performance | Revenue trends, profit margins, YoY growth |
| Revenue Breakdown | By product line, by geography, by segment |
| Competitive Position | Market share, competitive advantages, SWOT |
| Management & Strategy | Leadership team, strategic initiatives |

**Primary Sources:** Company annual reports, quarterly filings, investor presentations, official press releases

### Type B: Industry/Sector Research

| Section | Content Focus |
|---------|---------------|
| Market Size & Growth | TAM, SAM, historical and projected growth |
| Industry Structure | Value chain, upstream/downstream relationships |
| Competitive Landscape | Major players, market share distribution |
| Key Trends & Drivers | Technology shifts, regulatory changes, demand drivers |
| Barriers to Entry | Capital requirements, technology barriers |
| Future Outlook | Growth projections, emerging opportunities |

**Primary Sources:** Industry research reports, government statistics, trade associations

### Type C: Comparative Analysis

| Section | Content Focus |
|---------|---------------|
| Comparison Framework | Criteria and methodology |
| Side-by-Side Analysis | Feature/metric comparison tables |
| Strengths & Weaknesses | Per-company evaluation |
| Market Positioning | Visual competitive map |
| Recommendation | Summary verdict with rationale |

**Primary Sources:** Mix of company filings and industry reports

## Report Core Components (Required in All Types)

**Executive Summary**
- Most critical findings and their significance
- Key metrics and conclusions
- No word limit — be as thorough as needed

**1. Introduction**
- Report objectives and scope
- Industry context and background

**2. Key Findings**
- Major discoveries with supporting evidence
- Data-driven insights

**3. Conclusion**
- Summary of findings and implications
- Forward-looking perspective

**4. Sources**
- Complete source documentation with reliability ratings

**Analytical Sections (Select as Needed):**
- Methodology, In-Depth Analysis, Recommendations, Appendices

**Optional Sections:**
- Unexpected Discoveries, Limitations, Future Research Directions

## Trusted Source Standards

### Tier 1: Official & Regulatory Sources (Highest Trust)
- **Central Banks**: Federal Reserve, ECB, Bank of England, People's Bank of China
- **Securities Regulators**: SEC (EDGAR filings), FCA, ESMA, CSRC
- **Government Statistics**: Bureau of Labor Statistics, Eurostat, National Bureau of Statistics
- **International Organizations**: IMF, World Bank, OECD, BIS

### Tier 2: Financial Data Providers
- **Market Data**: Bloomberg, Refinitiv, FactSet, S&P Global Market Intelligence
- **Credit Ratings**: Moody's, S&P Global Ratings, Fitch Ratings
- **Industry Databases**: IBISWorld, Statista, PitchBook

### Tier 3: Research & Analysis
- **Investment Banks**: Goldman Sachs Research, Morgan Stanley Research, JP Morgan Research
- **Consulting Firms**: McKinsey Global Institute, BCG, Bain & Company
- **Academic Institutions**: NBER, university research centers

### Tier 4: Industry & Trade Sources
- **Industry Associations**: Specific sector trade associations
- **Company Filings**: Annual reports, 10-K, 10-Q filings
- **Earnings Calls & Investor Presentations**

### Tier 5: News & Media (Verify with Higher Tiers)
- **Financial News**: Financial Times, Wall Street Journal, Bloomberg News, Reuters
- **Business Media**: The Economist, Harvard Business Review

## Sources Section Format

```markdown
## Sources

[1] Source Name - High Reliability - Official government data
    URL: https://actual-source-url.com/path/to/document

[2] Company Annual Report 2024 - High Reliability - Official company filing
    URL: https://investor.company.com/annual-report-2024.pdf

[3] Industry Research Report - High Reliability - Professional research firm
    URL: https://research-firm.com/industry-report
```

**Citation Requirements:**
- MUST include actual URLs for all sources
- Minimum 5 sources from at least 3 different domains
- Include reliability ratings for all sources
- For listed companies: Prioritize official annual/quarterly reports
- **NEVER cite Wikipedia**

## Quality Standards

- All statistics must be cited with sources (include FULL URLs)
- Key findings require verification from at least 2 independent sources
- Reports must include reliability ratings for all sources
- Data should be current (within 12 months unless historical analysis)
- Clear distinction between facts and analysis/projections
- For listed companies: Prioritize official annual/quarterly reports as sources

## File & Output Conventions

### Directory Structure
```
docs/
├── research_summary.md
├── market_data.md
├── industry_analysis.md
├── competitive_landscape.md
├── sources_list.md
├── {topic}_report.md
├── fact_check_report.md
├── {topic}_report_verified.md
├── {topic}_report.docx
└── {topic}_report.pdf

data/
├── market_metrics.json
└── company_data.json

charts/
└── *.png

memory/
└── research_history_record.json
```

### Document Flow Summary

| Phase | Input | Output | Key Responsibilities |
|-------|-------|--------|---------------------|
| 1. Research | User query | `docs/research_*.md`, `docs/sources_list.md`, `data/*.json` | Gather data, bilingual search, collect multiple research docs |
| 2. Writing | ALL research docs from Step 1 | `docs/{topic}_report.md`, `charts/*.png` | Synthesize ALL research into ONE comprehensive report, generate charts |
| 3. Fact-Check | The ONE report from Step 2 | `docs/fact_check_report.md`, `docs/{topic}_report_verified.md` | Verify the Step 2 report, cross-check sources, NO chart generation |
| 4. Formatting | The VERIFIED report from Step 3 | `docs/{topic}_report.docx`, `docs/{topic}_report.pdf` | Write DOCX with embedded charts → convert to PDF |

## 语言规范（Language Rules）

**必须遵循用户指定的语言进行输出：**

1. **检测用户语言**：识别用户提问所使用的语言
2. **遵循用户指令**：如果用户在指令中明确要求使用某种语言撰写报告，必须严格遵循
3. **默认匹配原则**：如果用户未明确指定，则使用与用户提问相同的语言撰写报告

**示例：**
- 用户用中文提问 → 报告使用中文撰写
- 用户用英文提问 → 报告使用英文撰写
- 用户说"请用英文撰写报告" → 无论用户用什么语言提问，报告必须使用英文
- 用户说"Please write the report in Chinese" → 报告必须使用中文

**Ensure the language requirement is applied consistently across ALL phases of the workflow (research, writing, fact-checking, formatting).**

## Common Mistakes to Avoid

- ❌ Skipping the research phase and writing directly from user query
- ❌ Outputting report content in conversation instead of files
- ❌ Skipping fact-checking phase
- ❌ Delivering only Markdown without DOCX/PDF
- ❌ Generating charts in any step other than Step 2
- ❌ Using generic/default matplotlib colors without considering brand context
- ❌ Generating DOCX without embedding charts
- ❌ Converting to PDF before verifying charts are embedded in DOCX
- ❌ Citing Wikipedia as a source
- ❌ Using placeholder URLs or source names without links
- ❌ Adding annotations/editor's notes in the verified report instead of direct corrections
- ❌ Reading only some research files and ignoring others in Step 2
- ❌ Treating any request as a "simple query" that can bypass the workflow
- ❌ Fabricating or estimating data without clear labeling
- ❌ Creating visual disconnect between chart colors and DOCX theme colors
