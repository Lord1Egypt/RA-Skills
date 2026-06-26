# Universal Data Analyst (通用数据分析专家)

## Introduction

An intelligent data analysis skill based on **Data Ontology**. Unlike keyword-based approaches, this skill uses LLM reasoning for every analysis, automatically identifying data types, selecting analysis methods, generating scripts, and outputting reports.

Supports both economic data (retail, subscription, finance, etc.) and non-economic data (scientific measurements, social networks, text, etc.), handling multiple formats including CSV, Excel, Parquet, JSON, and more.

---

## How to Trigger

Simply upload a data file or send any of these types of messages:

- "Help me analyze this data"
- "What patterns are in this CSV?"
- "Explore this dataset"
- "Check the data quality for me"
- Directly upload `.csv` / `.xlsx` / `.parquet` / `.json` files

---

## Core Design: Four-Layer Analysis Framework

```
Layer 1: Data Ontology
        ↓  What kind of existence is this? Entity type? Generation mechanism?
Layer 2: Problem Typology
        ↓  Descriptive / Diagnostic / Predictive / Prescriptive / Causal?
Layer 3: Methodology Mapping
        ↓  Match domain-recognized analysis frameworks
Layer 4: Validation & Output
           Data quality report + Analysis scripts + HTML/MD reports
```

Each layer invokes LLM reasoning without any hardcoded rules.

---

## Analysis Workflow (7 Steps)

| Step | Content | Description |
|------|---------|-------------|
| 1 | Data Loading | Auto-recognize formats, support multiple file types |
| 2 | Ontology Recognition | LLM judges entity type and generation mechanism |
| 3 | Quality Validation | Auto-detect missing values, outliers, duplicates, output quality score |
| 4 | Plan Generation | LLM selects analysis framework and path based on user intent |
| 5 | Script Generation | LLM generates executable Python analysis scripts |
| 6 | Execute Analysis | Run scripts, generate charts and numerical results |
| 7 | Comprehensive Report | Output HTML + Markdown dual-format reports |

### Flow Health Monitoring (NEW)

Each step has status tracking and error handling:

- **Step Dependency Check** - Automatically prevents subsequent steps when prerequisites fail
- **Clear Error Messages** - Provides explicit failure reasons and fix suggestions
- **Flow Health Report** - Outputs complete execution status and issue summary

If a step fails, you'll see:
```
⚠️ Flow Interrupted!
   Reason: Critical step 'Data Loading' failed: Encoding error

Fix Suggestions:
  1. File encoding may not be UTF-8, try manually specifying encoding parameter
  2. Common Chinese encodings: gbk, gb2312, gb18030
```

---

## Supported Data Types

### Economic Data

| Data Characteristics | Recognized As | Auto-matched Framework |
|---------------------|---------------|----------------------|
| Orders + Price + SKU | Retail Economy | Value Chain / ABC-XYZ / RFM |
| User + Subscription Cycle + Churn | Subscription Economy | LTV / Cohort / Retention Curves |
| Click / Add-to-cart / Purchase Events | Attention Economy | Funnel Analysis / AARRR |
| GMV + Platform Matching | Commission Economy | Two-sided Network Effects / Unit Economics |
| Position + Skills + Salary | Labor Market | Skill Premium / Experience Elasticity |
| OHLCV Price Data | Financial Time Series | Technical Analysis / Volatility Models |

### Non-Economic Data

| Data Type | Auto-matched Framework |
|-----------|----------------------|
| Sensors / Time Series Continuous | Time Series Decomposition, Extreme Value Analysis |
| Social / Network Relationship | Centrality Analysis, Community Detection |
| Geographic / Spatial | Spatial Autocorrelation, Hotspot Analysis |
| Text Corpus | Topic Modeling, Sentiment Analysis |
| Biomedical | Survival Analysis, Differential Expression |

---

## Supported File Formats

- **CSV / TSV** (`.csv`, `.tsv`, `.txt`) - Auto encoding detection, supports utf-8, gbk, latin1, etc.
- **Excel** (`.xlsx`, `.xls`)
- **Parquet** (`.parquet`, `.pq`)
- **JSON** (`.json`)
- **SQL Database** (via connection string)

### Encoding Fault Tolerance

CSV loading automatically tries multiple encodings:
- Auto encoding detection (if chardet library available)
- Fallback encodings: utf-8, utf-8-sig, gbk, gb2312, gb18030, latin1, etc.
- Engine fallback: Auto-switches to Python engine when C engine fails, skipping corrupted rows

---

## Output Contents

Each analysis generates:

```
session_YYYYMMDD_HHMMSS/
├── step2_ontology_prompt.txt     # Ontology recognition prompts (reusable)
├── step3_validation_report.json  # Data quality report
├── step3_cleaning_report.txt     # Data cleaning recommendations
├── step4_planning_prompt.txt     # Analysis planning prompts (reusable)
├── step5_script_prompt.txt       # Script generation prompts (reusable)
├── analysis_report.html          # Comprehensive HTML report (with charts)
├── analysis_report.md            # Markdown report
└── charts/                       # All analysis charts (PNG)
```

---

## Usage Examples

### Example 1: Analyzing E-commerce Sales Data

```
User: Help me analyze this sales data, want to know which products sell well and which customers are high-value

[Upload orders.csv]
```

Skill automatically:
1. Recognizes as "Retail Economy × Transaction/Event Data"
2. Selects RFM Customer Value Analysis + ABC Product Classification framework
3. Generates and executes analysis scripts
4. Outputs customer segmentation distribution, product sales ranking, RFM heatmap, and HTML report

---

### Example 2: Analyzing User Behavior Logs

```
User: This is our App's user behavior log, want to see the user conversion funnel

[Upload events.csv]
```

Skill automatically:
1. Recognizes as "Attention/Conversion Economy × Event Sequence Data"
2. Selects Funnel Analysis + Session Sequence Mining framework
3. Outputs conversion rates at each step, churn node analysis, user path Sankey diagram

---

### Example 3: Analyzing Meteorological Observation Data

```
User: Help me analyze this weather station observation record, understand temperature and precipitation patterns

[Upload weather.csv]
```

Skill automatically:
1. Recognizes as "Earth Science × Time Series/Trajectory Data × Instrument Measurement"
2. Selects Time Series Decomposition + Seasonality Analysis + Extreme Value Statistics framework
3. Outputs trend charts, seasonal decomposition charts, outlier reports

---

## Dependencies

```
pandas >= 1.3
numpy >= 1.21
matplotlib >= 3.4
seaborn >= 0.11
scipy >= 1.7
openpyxl >= 3.0   # Excel support
chardet >= 4.0    # Auto encoding detection (optional but recommended)
pyarrow >= 6.0    # Parquet support (optional)
sqlalchemy >= 1.4 # SQL support (optional)
```

---

## Version

**v1.1.0** · Author: Claude · License: CC BY-NC-SA 4.0

### v1.1.0 Updates (2026-03-23)

1. **Flow Health Monitoring** - Added step status tracking, dependency checks, error messages
2. **Enhanced Encoding Fault Tolerance** - Auto-try multiple encodings for CSV/TSV (utf-8, gbk, latin1, etc.)
3. **Engine Fallback** - Auto-switches to Python engine when C engine fails, skipping corrupted rows

### v1.0.0

- Initial version: Four-layer analysis framework + 7-step analysis workflow
