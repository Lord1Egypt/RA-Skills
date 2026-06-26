---
name: stock-review
description: A-share market automated review and analysis system, generating daily market insights with Gemini AI, supporting publishing to Hugo blog and WeChat Official Account
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/donvink/stock-review
    requires:
      anyBins:
        - python3
        - python
---

# 🚀 Stock Review

👉 **[Live Demo Blog](https://donvink.github.io/stock-review/)**

### GitHub: 👉 **[https://github.com/Donvink/stock-review](https://github.com/Donvink/stock-review)**

## Language

**Match user's language**: Respond in the same language the user uses. If the user writes in Chinese, respond in Chinese. If the user writes in English, respond in English.

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `{baseDir}`, then use `{baseDir}/scripts/<name>.py`. Ensure Python 3.10+ is installed and dependencies are configured.

| Script | Purpose |
|------|------|
| `scripts/fetch_data.py` | Fetch A-share market data (indices, stocks, sectors, etc.) |
| `scripts/analyze.py` | Gemini AI analysis of market data |
| `scripts/post_to_hugo.py` | Publish to Hugo blog |
| `scripts/post_to_wechat.py` | Publish to WeChat Official Account |
| `scripts/main.py` | Main execution script, coordinates the entire workflow |

## Configuration Preferences

1. Check if config.yaml exists: `{baseDir}/stock-review/config.yaml`

2. Check if .env file exists and is configured with `GEMINI_API_KEY`, `WECHAT_APP_ID`, `WECHAT_APP_SECRET`: `{baseDir}/stock-review/.env`


**config.yaml supports**: Default publishing platforms | Whether to skip AI analysis by default | Default data backtracking days | Default request delay | Default retry count | API key configuration
**.env supports**: API key configuration

**Minimum supported keys** (case-insensitive, accepts `1/0` or `true/false`):

| Key | Default | Description |
|-----|---------|------|
| `date` | `null` | Date in YYYYMMDD format |
| `force_refresh` | `false` | Whether to force refresh already fetched data |
| `skip_ai_analysis` | `false` | Whether to skip AI analysis |
| `platforms` | `["hugo"]` | Default publishing platforms (['hugo']/['wechat']/['hugo', 'wechat']) |
| `data_dir` | `null` | Directory for data storage |
| `max_retries` | `3` | Default retry count |
| `request_delay` | `0.5` | Default request delay (seconds) |
| `backtrack_days` | `0` | Default data backtracking days |
| `type` | `gemini` | Model type |
| `model_name` | `gemini-2.5-flash` | Model name |


**Recommended config.yaml example**:

```yml
# default configuration for stock review skill
review:
  markets:                          # can include "shanghai", "shenzhen", "hongkong"
    - "shanghai"
    - "shenzhen"
    - "hongkong"
  default_period: "daily"           # can be "daily", "weekly", "monthly"
  date: null                        # can be specific date "YYYYMMDD" like "20260101" or null for today
  force_refresh: false              # whether to force refresh data even if cached data is available
  skip_ai_analysis: false           # whether to skip AI analysis and just return raw data
  platforms: ["hugo"]               # platforms to publish the report, e.g. ['hugo', 'wechat'] or ['hugo'] or ['wechat']

paths:
  data_dir: null                    # directory to store fetched data and cache, null means current project directory

parameters:
  max_retries: 3
  request_delay: 0.5
  backtrack_days: 0
  
models:
  type: "gemini"
  model_name: "gemini-2.5-flash"
```

**.env example**:

```md
# Gemini API Key
GEMINI_API_KEY="your_gemini_api_key"

# WeChat Official Account Configuration
WECHAT_APP_ID="your_wechat_app_id"
WECHAT_APP_SECRET="your_wechat_app_secret"
```

### How to Get a Gemini API Key:
1. Visit the official portal: Go to https://aistudio.google.com/ and log in with your Google account.

2. Create an API Key: Click "Get API key" in the left sidebar, click "Create API key in new project", and copy the generated string (please save it securely—you won't be able to see the full key again after closing the window).

3. Important Notes:
**Free Tier**: Provides free quota but with request frequency limits (RPM/RPD).
**Data Privacy**: Free tier data may be used for model improvement. For commercially sensitive data, consider enabling the paid mode.

### How to Get WeChat Official Account Credentials:

1. Visit https://developers.weixin.qq.com/platform/
2. Navigate: My Business → Official Account → Development Keys
3. Add a development key, copy the AppID and AppSecret
4. **Add the IP address of your machine to the whitelist**


## Environment Check

Before first use, install the dependencies.

```bash
pip install -r {baseDir}/requirements.txt
```

Check items: Python version | Dependencies | API keys | Network connection | Directory permissions

**If any check fails**, provide fix guidance:

| Check Item | Fix Method |
|-------|----------|
| Python version | Install Python 3.10+: `brew install python@3.10` (macOS) or `apt install python3.10` (Linux) |
| Dependencies | Run `pip install -r {baseDir}/requirements.txt` |
| Gemini API key | Configure in .env or via environment variables |
| WeChat Official Account credentials | Configure in .env or via environment variables |
| Network connection | Check network proxy settings |
| Directory permissions | Ensure data/ and content/posts/ directories are writable |

## Workflow Overview

Copy this checklist and check items as you progress:

```
Review Analysis Progress:
- [ ] Step 0: Load preferences (config.yaml, .env), determine execution parameters
- [ ] Step 1: Fetch market data
- [ ] Step 2: Run AI analysis (optional)
- [ ] Step 3: Generate report
- [ ] Step 4: Publish to platforms
- [ ] Step 5: Report complete
```

### Step 0: Load Preferences

Check and load config.yaml settings (see Configuration Preferences section above), parse and store default values for subsequent steps.

### Step 1: Fetch Market Data

Fetch the following data for the specified date:

| Data Type | Source | File |
|----------|------|------|
| Index data | stock_zh_index_spot_sina | `data/{date}/index_{date}.csv` |
| Limit-up pool | stock_zt_pool_em | `data/{date}/zt_pool_{date}.csv` |
| Limit-down pool | stock_zt_pool_dtgc_em | `data/{date}/dt_pool_{date}.csv` |
| Failed limit-up pool | stock_zt_pool_zbgc_em | `data/{date}/zb_pool_{date}.csv` |
| Full market data | stock_zh_a_spot_em | `data/{date}/A_stock_{date}.csv` |
| Top 20 by turnover | Calculated | `data/{date}/top_amount_stocks_{date}.csv` |
| Concept sectors | stock_board_concept_name_em | `data/{date}/concept_summary_{date}.csv` |
| Top traders list | stock_lhb_detail_daily_sina | `data/{date}/lhb_{date}.csv` |
| Watchlist | Calculated | `data/{date}/watchlist*_{date}.csv` |

**Retry Mechanism**:
- Default 3 retries
- 0.5 second request interval
- Automatic fallback to alternative interfaces on failure

### Step 2: Run AI Analysis

**CRITICAL**: Run AI analysis only if:
- `--skip-ai` is not set
- `GEMINI_API_KEY` is configured (via config.yaml or environment variables)

**AI Analysis Prompt**:

```python
prompt = f"""
Role Setting: You are a seasoned A-share strategy analyst with 20 years of experience...

Task Description: Conduct a multi-dimensional review based on the [daily review data]:
1. 🚩 Market Sentiment Diagnosis
2. 💰 Core Themes and Capital Flow
3. 🪜 Consecutive Limit-up Gradient and Space Game
4. ⚡ Key Stocks with Abnormal Movements Analysis
5. 🧭 Next Trading Day Strategy Recommendations

📊 Daily Review Data:
{market_summary}
"""
```

**Output**: `data/{date}/ai_analysis_{date}.md`

### Step 3: Generate Reports

**Market Summary Report**:
- File: `data/{date}/market_summary_{date}.md`
- Format: Markdown
- Content: Tabular summary of all data

**AI Analysis Report** (if run):
- File: `data/{date}/ai_analysis_{date}.md`
- Format: Markdown
- Content: In-depth analysis generated by Gemini

### Step 4: Publish to Platforms

**Hugo Blog Publishing**:

```bash
python3 {baseDir}/scripts/post_to_hugo.py --market-summary <file> --ai-analysis <file> --date <date>
```

**Output**: `content/posts/stock-analysis-{YYYY-MM-DD}.md`

**WeChat Official Account Publishing** (requires API credentials):

```bash
python3 {baseDir}/scripts/post_to_wechat.py --market-summary-file <file> --ai-analysis-file <file> --date <date> --cover-file <file> --title <title>
```

**WeChat Official Account API Request Rules**:
- Endpoint: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN`
- `article_type`: `news`
- Requires `thumb_media_id` (cover image)
- Comment settings: `need_open_comment=1`, `only_fans_can_comment=0`

### Step 5: Completion Report

**Success Report**:

```
✅ A-share Review Analysis Complete!

Date: 2026-03-04
Data: data/20260304/ (12 files)
AI Analysis: ✓ Generated (Gemini 2.0 Flash)

Published Platforms:
→ Hugo Blog: content/posts/stock-analysis-2026-03-04.md
→ WeChat Official Account: Draft ID: abc123def456

Market Snapshot:
• Shanghai Composite: 3350.52 (+1.02%)
• Turnover: 1.95 trillion
• Advance/Decline: 2857 / 2058
• Limit-up/Limit-down: 78 / 3

View Blog: https://donvink.github.io/stock-review/
```

**Error Report**:

```
❌ Review Analysis Failed

Error: Unable to fetch limit-up pool data
Suggestions: 
1. Check network connection
2. Try --force parameter to force refresh
3. Use --date to specify another date
```

## Detailed Feature Description

### Data Fetching Module

| Function | Purpose | Retry | Cache |
|------|------|------|------|
| `stock_summary()` | Fetch index data | ✓ | ✓ |
| `stock_zt_dt_pool()` | Fetch limit-up/down data | ✓ | ✓ |
| `fetch_all_stock_data()` | Fetch full market data | ✓ (3 times) | ✓ |
| `get_top_amount_stocks()` | Fetch top 20 by turnover | ✓ | ✓ |
| `get_concept_summary()` | Fetch concept sectors | ✓ | ✓ |
| `get_lhb_data()` | Fetch top traders list | ✓ | ✓ |

### AI Analysis Module

**Model**: `gemini-2.5-flash`

**Analysis Dimensions**:
1. **Market Sentiment Diagnosis** - Advance/decline ratio, limit-up/down comparison, turnover
2. **Core Theme Tracking** - Capital flow, hot sectors
3. **Consecutive Limit-up Gradient Analysis** - Space board height, limit-up structure
4. **Abnormal Movement Stock Analysis** - High turnover, top traders list
5. **Next Day Strategy Recommendations** - Data-based trading suggestions

### Publishing Module

| Platform | Method | Requirements | Output |
|------|------|------|------|
| Hugo Blog | File write | None | Markdown file |
| WeChat Official Account | API | AppID/Secret | Draft ID |

## Feature Comparison

| Feature | Data Fetching | AI Analysis | Hugo Publishing | WeChat Publishing |
|------|----------|--------|----------|----------|
| Auto-fetch latest date | ✓ | - | - | - |
| Data caching | ✓ | - | - | - |
| Retry mechanism | ✓ | - | - | - |
| Multi-source backup | ✓ | - | - | - |
| Format values (hundreds millions/ten thousands) | ✓ | - | - | - |
| Filter ST stocks | ✓ | - | - | - |
| Watchlist construction | ✓ | - | - | - |
| Market sentiment diagnosis | - | ✓ | - | - |
| Limit-up gradient analysis | - | ✓ | - | - |
| Strategy recommendations | - | ✓ | - | - |
| Markdown format | - | ✓ | ✓ | ✓ |
| Timezone handling | - | - | ✓ | - |
| Hugo frontmatter | - | - | ✓ | - |
| WeChat HTML conversion | - | - | - | ✓ |
| Comment settings | - | - | - | ✓ |

## Prerequisites

**Required**:
- Python 3.10+
- Dependencies: `pip install -r requirements.txt`
- Gemini API key (for AI analysis)

**Optional**:
- WeChat Official Account AppID and AppSecret (for WeChat publishing)
- Hugo blog environment (for blog publishing)

**Configuration Locations** (priority order):
1. CLI parameters
2. config.yaml, .env (project-level/user-level)
3. Environment variables
4. Default values

## Troubleshooting

| Issue | Solution |
|------|----------|
| Unable to fetch data | Check network, specify another date |
| Gemini API error | Check if API key is valid, quota is sufficient |
| Limit-up pool data empty | Possibly non-trading day, try backtracking to another date |
| WeChat publishing failed | Check AppID/Secret, **confirm IP is whitelisted** |
| Chinese character encoding issues | Ensure file encoding is UTF-8 |
| Data format error | Check CSV files, ensure code column isn't converted to numbers |
| Timeout error | Increase `request_delay` or `max_retries` |
| Insufficient memory | Reduce data volume or process in batches |

## Extension Support

Customize via config.yaml. See the **Configuration Preferences** section for supported options.

## Related References

| Topic | Reference |
|------|------|
| AkShare Documentation | https://akshare.akfamily.xyz/index.html |
| Gemini API | https://aistudio.google.com/ |
| WeChat Official Account API | https://developers.weixin.qq.com/platform |
| Hugo Documentation | https://gohugo.io/ |

## Version History

| Version | Date | Changes |
|------|------|------|
| 1.0.0 | 2026-03-11 | Initial version |
