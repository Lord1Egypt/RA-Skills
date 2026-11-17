# News-Driven Event-Driven Stock Picking (wq-news-event-driven-stock-pick)

Receives financial news input, performs event NLP analysis via Baidu Qianfan API, links beneficiary A-share targets, and outputs event-driven stock-picking signals.

## Features

- **AI News Analysis Engine**: Integrates Baidu Qianfan LLM (default ernie-4.5-turbo-128k) to convert financial news into structured investment signals
- **Event Classification**: policy / earnings / industry / company / macro
- **Signal Strength Rating**: strong (direct beneficiary, main business >30%) / medium (indirect, supply chain) / weak (sentiment, concept correlation)
- **Beneficiary Target Linking**: stock code, name, logic, signal strength
- **Risk Factors + Signal Summary**: always annotates data source and confidence
- **Degradation Mechanism**: falls back to inline analysis with current model when Qianfan API unavailable

## Analysis Flow

```bash
# Analyze news text (recommended)
python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py -t "news content..."

# Or via stdin
echo 'news content...' | python3 ~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/scripts/news_analyzer.py
```

The script returns structured JSON (event type/summary/affected sectors/beneficiary stocks/risk/signal), formatted into a readable Markdown report.

## Event Taxonomy

| Type | Code | Example |
|------|------|---------|
| Policy | policy | RRR cut, industrial policy, new regulations |
| Earnings | earnings | Beat/miss, forecast revision |
| Industry | industry | Supply-demand change, price movement, tech breakthrough |
| Company | company | M&A, equity change, executive change |
| Macro | macro | GDP/CPI/PMI data, international trade |

See `references/event_taxonomy.md` for details.

## Web Dashboard (Event-Driven Trading Desk)

The system includes a visual web frontend, deployed at `racingai.top/event-driven` (ECS + systemd + nginx).

```
Browser (HTML+JS) → Python http.server (:5566) → news_analyzer.py → Qianfan API
```

- Frontend: event-driven trading dashboard HTML (7-layer full analysis panel)
- Backend: `server.py` pure stdlib HTTP service (ECS uses Python 3.6.8, zero external deps)
- Analysis engine: `scripts/news_analyzer.py`

See `references/web-dashboard-setup.md` for full architecture and deployment.

## Directory Structure

```
clawhub/
├── SKILL.md                        # Main skill file (analysis flow/event taxonomy/deployment/pitfalls)
├── references/
│   ├── event_taxonomy.md           # Event taxonomy details
│   └── web-dashboard-setup.md      # Web Dashboard architecture & deployment
├── scripts/
│   └── news_analyzer.py            # Qianfan API news analysis engine (env vars, no hardcoded keys)
├── templates/
│   └── output_template.md          # Analysis report output template
├── README.md                       # Chinese documentation
└── README.en.md                    # This file
```

## Security

- `scripts/news_analyzer.py` reads Qianfan API Key from environment variable (`QIANFAN_API_KEY`); **exits with an error if not set**, no built-in keys
- Server IP sanitized to `<SERVER_IP>` placeholder

## Installation

1. Place this skill directory into `~/.hermes/skills/quant-finance/wq-news-event-driven-stock-pick/`
2. Configure environment variable `QIANFAN_API_KEY`
3. Hermes Agent auto-discovers the skill; sending financial news in the "新闻流事件驱动选股" group auto-triggers analysis
