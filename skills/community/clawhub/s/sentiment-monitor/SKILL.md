---
name: sentiment-monitor
version: "0.3.1"
license: MIT
description: >
  Public opinion monitoring and structured report generation.
  Collects publicly available web information about celebrities, TV shows, or brands,
  performs sentiment analysis, and generates responsive HTML reports.
  Trigger keywords: sentiment, public opinion, reputation, monitoring report.
  Examples: "monitor reputation of X", "public opinion analysis for X".
---

# Public Opinion Monitoring & Report Generation

This skill provides a structured methodology for monitoring and analyzing public sentiment about public-facing entities (celebrities, entertainment products, brands) using publicly available web information.

## Purpose & Scope

- **Input**: A target entity name and optional time range
- **Output**: A self-contained HTML report with sentiment analysis, event timeline, and actionable recommendations
- **Data sources**: Public web pages, news articles, social media (public content only)
- **Output format**: HTML file with embedded CSS (no external dependencies)

## Prerequisites

This skill requires the AI assistant platform to provide the following built-in tools:

| Tool | Role | Required |
|------|------|----------|
| WebSearch | Retrieve public web information | Yes |
| WebFetch | Read detailed web page content | Yes |
| Write | Save the generated HTML report | Yes |
| preview_url | Display the HTML report preview | Optional |
| deliver_attachments | Deliver the report file to the user | Optional |

> **Note**: If the platform does not provide WebSearch or WebFetch, this skill cannot function.
> In that case, inform the user that the required web access tools are not available.

This skill has **zero external dependencies**. It does not install packages, execute scripts, access system files, or communicate with external servers.

## Privacy & Data Policy

- All data comes from **publicly accessible web sources** only
- No private data, personal information, or non-public content is accessed
- Aggregate statistics (e.g., view counts, play counts) are only collected when explicitly displayed on public pages
- Missing data is labeled as "Data Unavailable" in reports — **no data is fabricated or estimated**
- Reports are saved to the user's local workspace; no data leaves the local environment

## Data Availability Caveats

> **Important context for agents**:
>
> The skill instructs gathering platform metrics (social media trending, view counts, engagement data).
> In practice, most specific numerical metrics (e.g., exact view counts, follower numbers) are only accessible
> through platform-specific APIs and are typically **not available** via public web search or page fetching.
>
> The agent should:
> - Only report metrics that are **explicitly visible** in the web search results or fetched page content
> - Never estimate, extrapolate, or fabricate numerical data
> - Use qualitative descriptions (e.g., "high activity", "significant engagement") when exact numbers are unavailable
> - Label any unavailable data as "Data Unavailable"

## Trigger Conditions

This skill activates when user requests include keywords related to:
- Public opinion, sentiment, reputation monitoring
- Celebrity or brand image analysis
- Media coverage or buzz tracking

## Supported Monitoring Targets

- **Entertainment figures**: Actors, musicians, influencers
- **Media products**: TV series, films, variety shows
- **Brands and products**: Consumer brands, product launches

## Workflow

### Phase 1: Parameter Identification

Extract from the user request:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Target | User-specified | Name of the entity to monitor |
| Time range | Last 30 days | Customizable by user |
| Output format | HTML | Only HTML format is supported |
| Focus areas | All dimensions | Fan data, reputation events, platform activity, risk alerts |

### Phase 2: Public Information Gathering

The AI assistant gathers information from publicly accessible web sources across these dimensions:

**Basic data** (3-5 searches recommended):
- Recent news coverage
- Trending topics and hot searches
- Public reviews and discussions
- Fan community activity
- Cross-platform discussion volume

**Event identification**:
- Positive events: product releases, awards, charity work
- Negative events: controversies, criticism, backlash
- For each event: timestamp, platform, sentiment direction

> **Important**: Only data obtainable through public web searches should be used.
> If specific numerical data is unavailable, the report should indicate "Data Unavailable".

### Phase 3: Analysis

**3.1 Sentiment Classification**
Categorize the overall public opinion into:
- Positive proportion (favorable coverage, support, enthusiasm)
- Neutral proportion (objective reporting, general discussion)
- Negative proportion (criticism, controversy, backlash)

**3.2 Event Timeline**
Organize major events chronologically (minimum 5 events), including:
- Event name and description
- Timestamp
- Sentiment direction (positive / neutral / negative)
- Impact level (high / medium / low)

**3.3 Risk Assessment**
Identify current or potential reputation risks:
- Active negative sentiment trends
- Sensitive topics that may escalate
- Competitive disadvantages

### Phase 4: Report Generation

Generate a complete, self-contained HTML report using the template structure below.
The template is provided inline — no external file dependencies are required.

**File naming**: `{target_name}{days}day_sentiment_report_{YYYYMMDD}.html`

**Report sections**:

1. **Header** — Title, monitoring period, generation date
2. **KPI Overview** — Overall sentiment score (0-100), positive/neutral/negative ratios, event count, active platforms
3. **Sentiment Distribution** — Visual bar chart and trend description
4. **Event Timeline** — Chronological list with sentiment and impact tags
5. **Platform Performance** — Cross-platform activity comparison
6. **Risk Assessment Matrix** — Current risks with severity and recommendations
7. **Operational Recommendations** — Short-term (1-2 weeks), mid-term (1 month), long-term (3+ months)
8. **Disclaimer** — Data source clarification

### Phase 5: Delivery

1. Save the HTML report using the Write tool
2. Display the report preview using preview_url (if available)
3. Deliver the file using deliver_attachments (if available)
4. If tools are unavailable, provide the file path for manual access

## Guidelines

- All data must originate from public web sources — fabrication is strictly prohibited
- Unavailable data must be clearly marked as "Data Unavailable"
- Time ranges are calculated automatically based on the current date
- Sentiment analysis should be evidence-based, avoiding subjective assumptions
- Reports should maintain objectivity, presenting multiple viewpoints for controversial events
- Sensitive political content should be avoided in reports

## Report Template

Use the following HTML structure as the report template. All CSS is embedded inline — no external stylesheets, fonts, or scripts are required. Replace `{PLACEHOLDER}` tokens with actual data.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #f5f7fa; color: #1a1a2e; line-height: 1.6; padding: 20px;
        }
        .report {
            max-width: 900px; margin: 0 auto; background: #fff;
            border-radius: 12px; box-shadow: 0 2px 20px rgba(0,0,0,0.08); overflow: hidden;
        }
        .report-header {
            background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff;
            padding: 40px 30px; text-align: center;
        }
        .report-header h1 { font-size: 28px; margin-bottom: 12px; }
        .report-header .meta { font-size: 14px; opacity: 0.8; }
        .report-header .meta span { margin: 0 12px; }
        .kpi-section { padding: 30px; }
        .kpi-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px; margin-bottom: 24px;
        }
        .kpi-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px;
            padding: 20px; text-align: center; border-left: 4px solid #0f3460;
        }
        .kpi-card .value { font-size: 32px; font-weight: 700; color: #0f3460; }
        .kpi-card .label { font-size: 13px; color: #666; margin-top: 6px; }
        .kpi-card.positive { border-left-color: #27ae60; }
        .kpi-card.positive .value { color: #27ae60; }
        .kpi-card.negative { border-left-color: #e74c3c; }
        .kpi-card.negative .value { color: #e74c3c; }
        .kpi-card.neutral { border-left-color: #f39c12; }
        .kpi-card.neutral .value { color: #f39c12; }
        .section { padding: 0 30px 30px; }
        .section-title {
            font-size: 20px; font-weight: 600; color: #1a1a2e; margin-bottom: 20px;
            padding-bottom: 10px; border-bottom: 2px solid #e9ecef;
            display: flex; align-items: center; gap: 10px;
        }
        .section-title .icon { font-size: 22px; }
        .sentiment-bar {
            display: flex; height: 36px; border-radius: 8px; overflow: hidden; margin-bottom: 16px;
        }
        .sentiment-bar .positive { background: #27ae60; }
        .sentiment-bar .neutral { background: #f39c12; }
        .sentiment-bar .negative { background: #e74c3c; }
        .sentiment-legend { display: flex; gap: 24px; font-size: 14px; color: #555; }
        .sentiment-legend span { display: flex; align-items: center; gap: 6px; }
        .sentiment-legend .dot {
            width: 12px; height: 12px; border-radius: 50%; display: inline-block;
        }
        .timeline { position: relative; padding-left: 30px; }
        .timeline::before {
            content: ''; position: absolute; left: 8px; top: 0; bottom: 0;
            width: 2px; background: #e0e0e0;
        }
        .timeline-item { position: relative; margin-bottom: 24px; }
        .timeline-item::before {
            content: ''; position: absolute; left: -26px; top: 6px;
            width: 12px; height: 12px; border-radius: 50%;
            background: #0f3460; border: 2px solid #fff; box-shadow: 0 0 0 2px #0f3460;
        }
        .timeline-item.positive::before { background: #27ae60; box-shadow: 0 0 0 2px #27ae60; }
        .timeline-item.negative::before { background: #e74c3c; box-shadow: 0 0 0 2px #e74c3c; }
        .timeline-item .date { font-size: 13px; color: #999; margin-bottom: 4px; }
        .timeline-item .title { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
        .timeline-item .desc { font-size: 14px; color: #555; }
        .timeline-item .tag {
            display: inline-block; font-size: 12px; padding: 2px 8px;
            border-radius: 4px; margin-top: 6px; color: #fff;
        }
        .tag.positive { background: #27ae60; }
        .tag.neutral { background: #f39c12; }
        .tag.negative { background: #e74c3c; }
        .tag.impact-high { background: #8e44ad; }
        .tag.impact-mid { background: #2980b9; }
        .tag.impact-low { background: #95a5a6; }
        .risk-table { width: 100%; border-collapse: collapse; font-size: 14px; }
        .risk-table th {
            background: #1a1a2e; color: #fff; padding: 12px 16px; text-align: left;
        }
        .risk-table td { padding: 12px 16px; border-bottom: 1px solid #eee; }
        .risk-table tr:hover { background: #f8f9fa; }
        .risk-badge {
            display: inline-block; padding: 2px 10px; border-radius: 12px;
            font-size: 12px; font-weight: 600; color: #fff;
        }
        .risk-badge.high { background: #e74c3c; }
        .risk-badge.mid { background: #f39c12; }
        .risk-badge.low { background: #27ae60; }
        .advice-block { margin-bottom: 20px; }
        .advice-block h4 {
            font-size: 16px; color: #0f3460; margin-bottom: 10px;
            padding-left: 12px; border-left: 3px solid #0f3460;
        }
        .advice-block ul { list-style: none; padding: 0; }
        .advice-block ul li {
            padding: 8px 0 8px 20px; position: relative; font-size: 14px; color: #444;
        }
        .advice-block ul li::before {
            content: '>'; position: absolute; left: 0; color: #0f3460; font-weight: 700;
        }
        .disclaimer {
            background: #f8f9fa; padding: 20px 30px; font-size: 12px;
            color: #999; border-top: 1px solid #eee;
        }
        @media (max-width: 600px) {
            body { padding: 10px; }
            .report-header { padding: 24px 20px; }
            .report-header h1 { font-size: 22px; }
            .kpi-grid { grid-template-columns: repeat(2, 1fr); }
            .section, .kpi-section { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="report">
        <div class="report-header">
            <h1>{TITLE}</h1>
            <div class="meta">
                <span>{PERIOD}</span>
                <span>{DATE}</span>
            </div>
        </div>
        <div class="kpi-section">
            <div class="kpi-grid">
                <div class="kpi-card positive">
                    <div class="value">{POSITIVE}%</div>
                    <div class="label">Positive</div>
                </div>
                <div class="kpi-card neutral">
                    <div class="value">{NEUTRAL}%</div>
                    <div class="label">Neutral</div>
                </div>
                <div class="kpi-card negative">
                    <div class="value">{NEGATIVE}%</div>
                    <div class="label">Negative</div>
                </div>
                <div class="kpi-card">
                    <div class="value">{HOT_COUNT}</div>
                    <div class="label">Key Events</div>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="section-title"><span class="icon">&#128202;</span> Sentiment Distribution</div>
            <div class="sentiment-bar">
                <div class="positive" style="width: {POSITIVE_NUM}%"></div>
                <div class="neutral" style="width: {NEUTRAL_NUM}%"></div>
                <div class="negative" style="width: {NEGATIVE_NUM}%"></div>
            </div>
            <div class="sentiment-legend">
                <span><span class="dot" style="background:#27ae60"></span> Positive {POSITIVE}%</span>
                <span><span class="dot" style="background:#f39c12"></span> Neutral {NEUTRAL}%</span>
                <span><span class="dot" style="background:#e74c3c"></span> Negative {NEGATIVE}%</span>
            </div>
            <p style="margin-top:16px; color:#555; font-size:14px;">{TREND_SUMMARY}</p>
        </div>
        <div class="section">
            <div class="section-title"><span class="icon">&#128197;</span> Key Events Timeline</div>
            <div class="timeline">
                <div class="timeline-item {EVENT_CLASS}">
                    <div class="date">{EVENT_DATE}</div>
                    <div class="title">{EVENT_TITLE}</div>
                    <div class="desc">{EVENT_DESC}</div>
                    <span class="tag {EVENT_CLASS}">{EVENT_SENTIMENT}</span>
                    <span class="tag impact-{EVENT_IMPACT}">{EVENT_IMPACT_LABEL}</span>
                </div>
            </div>
        </div>
        <div class="section">
            <div class="section-title"><span class="icon">&#128240;</span> Platform Performance</div>
        </div>
        <div class="section">
            <div class="section-title"><span class="icon">&#9888;</span> Risk Assessment</div>
            <table class="risk-table">
                <thead><tr><th>Risk</th><th>Level</th><th>Recommendation</th></tr></thead>
                <tbody>
                    <tr><td>{RISK_DESC}</td><td><span class="risk-badge {RISK_LEVEL}">{RISK_LEVEL_LABEL}</span></td><td>{RISK_SUGGESTION}</td></tr>
                </tbody>
            </table>
        </div>
        <div class="section">
            <div class="section-title"><span class="icon">&#128161;</span> Recommendations</div>
            <div class="advice-block">
                <h4>Short-term (1-2 weeks)</h4>
                <ul><li>{ADVICE_SHORT_1}</li><li>{ADVICE_SHORT_2}</li></ul>
            </div>
            <div class="advice-block">
                <h4>Mid-term (1 month)</h4>
                <ul><li>{ADVICE_MID_1}</li><li>{ADVICE_MID_2}</li></ul>
            </div>
            <div class="advice-block">
                <h4>Long-term (3+ months)</h4>
                <ul><li>{ADVICE_LONG_1}</li><li>{ADVICE_LONG_2}</li></ul>
            </div>
        </div>
        <div class="disclaimer">
            <p>This report is based on publicly available web information and is for reference only.</p>
            <p>Report generated by AI; does not represent any official position.</p>
        </div>
    </div>
</body>
</html>
```
