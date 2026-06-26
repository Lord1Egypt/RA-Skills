# Resource Position Analysis / 资源位转化数据波动分析

A Cursor agent skill for analyzing conversion funnel data of frontend resource positions (banners, cards, popups, etc.).

## What it does

Decomposes data fluctuations in the **Exposure → Click → Business Conversion** funnel using the **Sequential Substitution Method** (连环替代法), quantifying how much each factor (exposure volume, click-through rate, conversion rate) contributes to the overall data change.

### Key Features

- **Factor Decomposition** — Breaks down `Conversion = Exposure × CTR × CVR` to attribute fluctuations to individual factors with contribution percentages
- **Multiple Comparison Modes** — Day-over-day, week-over-week, or custom date range comparison
- **Multi-Position Cross Analysis** — Analyze and compare multiple resource positions side by side
- **Smart Findings** — Auto-detects anomalies like "exposure up but conversion flat" (traffic quality issue)
- **Actionable Recommendations** — Maps root causes to operational strategies (creative refresh, landing page optimization, traffic tuning)

### Output

Generates a structured Markdown report with:

1. Data overview table (current vs previous period)
2. Factor contribution breakdown per resource position
3. Cross-position comparison matrix
4. Key findings
5. Prioritized recommendations

## Data Format

Provide an Excel file (`.xlsx`) with these columns (supports Chinese column names):

| Column | Chinese Alias | Description |
|--------|--------------|-------------|
| date | 日期 | Date |
| resource_position | 资源位 | Position identifier |
| exposure_uv | 曝光UV | Unique exposure users |
| click_uv | 点击UV | Unique click users |
| conversion_count | 转化量 | Business conversions |

## Usage

```bash
# Day-over-day
python3 scripts/analyze.py data.xlsx --mode dod --date 2026-03-25

# Week-over-week
python3 scripts/analyze.py data.xlsx --mode wow --date 2026-03-25

# Custom range
python3 scripts/analyze.py data.xlsx --mode custom \
  --base-start 2026-03-18 --base-end 2026-03-24 \
  --compare-start 2026-03-11 --compare-end 2026-03-17
```

## Requirements

- Python 3.8+
- pandas, openpyxl (auto-installed on first run if missing)

## Install

```bash
npx clawhub install resource-position-analysis
```

## License

MIT
