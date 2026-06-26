<p align="center">
  <a href="README.md">中文</a> | <a href="readme-en.md">English</a>
</p>

# TikTok Hotspot Monitor Skill

TikTok hotspot monitoring Skill. Crawls TikTok video metadata via Apify Actor or Playwright local browser, performs offline trend analysis, and generates static HTML reports.

Source repository: https://github.com/TanDongTaotao/tiktok-hotspot-monitor

This Skill ships with a **US women's fashion keyword set** as a default example. You can customize it with any keywords, hashtags, creators, or music sources to monitor any domain you care about.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Agent Skill                        │
│  ┌─────────┐   ┌──────────┐   ┌──────────────────┐  │
│  │  Crawl   │──▶│ Analyze  │──▶│  HTML Report     │  │
│  │ Apify /  │   │ heat +   │   │  dark theme      │  │
│  │  MCP     │   │ coverage │   │                  │  │
│  └─────────┘   └──────────┘   └──────────────────┘  │
│        │              │                │             │
│        ▼              ▼                ▼             │
│  snapshot.jsonl  analysis.json    report.html        │
└─────────────────────────────────────────────────────┘
```

## 10-Layer Structure

This Skill follows the mature Agent Skill framework:

| Layer | Description | Location |
|-------|-------------|----------|
| 1. Scope | What it does / doesn't | `skill.md §1` |
| 2. Input Schema | Config, CLI, env formats | `skill.md §2` |
| 3. Output Schema | JSONL, JSON, HTML contracts | `skill.md §3` |
| 4. Tools | Script call rules & prohibitions | `skill.md §4` |
| 5. State Machine | Crawl→Analyze→Report flow | `skill.md §5` |
| 6. Error Recovery | Per-failure recovery steps | `skill.md §6` |
| 7. Planning | Task decomposition & decisions | `skill.md §7` |
| 8. Guardrails | Cost, time, rate, security limits | `skill.md §8` |
| 9. Evaluation | Success/failure thresholds | `skill.md §9` |
| 10. Composability | File contracts for chaining | `skill.md §10` |

## Quick Start

### Apify Mode (Primary)

```bash
# 1. Install dependencies
pip install apify-client

# 2. Set Apify API Token
echo "APIFY_TOKEN=your_token_here" > .env

# 3. Crawl (10 sources × window weights)
python scripts/crawl_tiktok_hotspots.py --once

# 4. Analyze
python scripts/analyze_tiktok_hotspots.py

# 5. Generate report
python scripts/render_tiktok_hotspot_report.py
```

### Local Crawl (Playwright MCP Backup)

When no Apify token is available or for small-scale testing:

```bash
# 1. Install dependencies
pip install playwright
playwright install chromium

# 2. Save TikTok session (manual QR login required)
python scripts/tiktok_login_save_session.py

# 3. Switch config provider type to "tiktok_mcp"
# Edit config/tiktok_hotspot_sources.json

# 4. Local crawl (~12 items per keyword, TikTok web limit)
python scripts/crawl_tiktok_hotspots.py --once --max-sources 2
```

**MCP limitations:**
- ~12 items per keyword (TikTok web page cap)
- Only supports `keyword` and `hashtag` source types
- Requires pre-saved TikTok login session
- No window weight allocation
- Best for small validation; use Apify for > 200 records

## File Structure

```
skills/tiktok-hotspot-monitor/
├── skill.md               # Agent instructions (10 layers)
├── README.md              # Chinese documentation
├── readme-en.md           # English documentation (this file)
├── metadata.json          # Machine-readable metadata
├── LICENSE                # MIT license
├── requirements.txt       # Python dependencies
├── examples/
│   ├── report.html                    # Sample report
│   ├── report_preview.png             # Preview screenshot
│   ├── report_top.png                 # Top section screenshot
│   ├── report_mid.png                 # Middle section screenshot
│   └── report_bottom.png              # Bottom section screenshot
├── scripts/
│   ├── crawl_tiktok_hotspots.py          # Main crawler
│   ├── analyze_tiktok_hotspots.py        # Offline analyzer
│   ├── render_tiktok_hotspot_report.py   # HTML report generator
│   ├── tiktok_search_mcp_adapter.py      # Playwright adapter
│   └── tiktok_login_save_session.py      # Session setup
└── config/
    ├── tiktok_hotspot_sources.json       # Main config
    ├── _tiktok_hotspot_apify_500_config.json  # 500-record validation config
    └── .env.example                      # Env template
```

## Report Preview

![Report Overview](examples/report_top.png)
![Signal Analysis](examples/report_mid.png)
![Long-term Terms & Rankings](examples/report_bottom.png)

Full sample report: [examples/report.html](examples/report.html)

## Output Directory

All outputs go under the project `data/` directory:

```
data/tiktok_hotspots/
  snapshots/tiktok_hotspots_<ts>.jsonl    # Raw records
  logs/tiktok_hotspots_<ts>.jsonl         # Run logs + round summary
data/tiktok_hotspot_analysis/
  tiktok_hotspot_analysis_<ts>.json       # Analysis results
  tiktok_hotspot_report_<ts>.html         # Dark-themed report
```

## Integration

Other agents consume outputs via file paths:

```python
import json
report = json.load(open("data/tiktok_hotspot_analysis/latest_analysis.json"))
top_signals = report["top_videos"][:5]
```

## Version History

- 1.0.0: Initial release. Apify Actor crawling (5-window Most-liked-first strategy), Playwright MCP local validation, offline analysis (heat score / coverage score / novelty detection), static HTML report generation.

## License

MIT License. See [LICENSE](LICENSE) for details.
