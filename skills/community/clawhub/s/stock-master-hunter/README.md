# StockMasterHunter — Primary Wave & 100-Bagger Hunter

> World-first AI Skill fusing Elliott Wave Theory, volume-price dynamics, trend-cycle analysis, and 100-bagger fundamental screening. Powered by 2,359 IMA knowledge base articles.

[![Version](https://img.shields.io/badge/version-2.1.0-blue)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-WorkBuddy%20%7C%20OpenClaw%20%7C%20Claude%20Code%20%7C%20GitHub%20Copilot-orange)]()

---

## What Is StockMasterHunter?

A deployable AI Skill (System Prompt) that transforms any LLM Agent into a professional stock investment analyst, combining:

| Module | Knowledge Base | Capability |
|--------|---------------|------------|
| **Elliott Wave Theory** | Frost & Prechter, Constance Brown, 2 伍朝辉 works | Wave counting + 3 Iron Rules + Fibonacci projection |
| **Volume-Price Dynamics** | O'Dea Principle, 黑马王子 量柱擒涨停, 刘炟鑫 均线主升浪 | Breakout detection + fakeout filtering |
| **SQGLP Genetic Screening** | Christopher Mayer 365x100-bagger empirical, Jesse Stine 146x system | 100-bagger identification framework |
| **Backtesting Engine** | 373 stock KB articles | Retrospective wave validation + signal accuracy |
| **IMA Knowledge Base** | 2,359 articles across 6 KBs | Persistent domain knowledge + sync protocol |
| **Real-Time Data** | weStock / AkShare / East Money | Multi-source market data pipeline |
| **Value Investing** | Li Lu, Buffett, PAG Shan Weijian, DBS | Fundamental conviction complement |

## Knowledge Base Foundation

```
股票知识库 (373) ──── 短线起涨点/中线斐波那契/量价/波浪/百倍股
z-library (971) ──── 全球投资视野/深度思考
香港上市招股书 (643) ─ 公司商业模式/IPO估值/行业TAM
巴菲特研究 (106) ──── 巴菲特股东大会/交易复盘
价值投资大师 (83) ─── 芒格/巴菲特体系
麦肯锡100年 (183) ─── 战略咨询框架
═════════════════════════════
总计: 2,359 篇专业内容支撑
```

## Quick Start

### Deploy as System Prompt

```python
system_prompt = open("SKILL.md").read()
response = client.chat.completions.create(
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Analyze 603256 HongHe Technology"}
    ]
)
```

### Install in WorkBuddy

```bash
cp -r stock-master-hunter ~/.workbuddy/skills/
```

### Install in OpenClaw / ClawHub / Claude Code

Upload the directory to your skills directory and reference in agent configuration.

## Project Structure

```
stock-master-hunter/
├── SKILL.md                          # Main skill prompt (433 lines)
├── README.md                         # This file
├── references/
│   ├── wave-theory.md                # Elliott Wave complete reference
│   ├── volume-price.md               # Volume-price dynamics + O'Dea
│   ├── hundred-bagger.md             # SQGLP framework + genetic scoring
│   ├── ima-integration.md            # IMA knowledge base API guide
│   └── ima-learned.md                # IMA-absorbed frameworks (v2.1)
├── examples/
│   ├── example-603256.md             # HongHe Tech 40x retrospective
│   └── example-hk2513.md             # ZhiPu 100x deep dive
└── LICENSE                           # MIT
```

## Function Calling Contracts

For advanced deployment, wire up these three functions:

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `get_stock_finance(stock_code)` | Stock code | Market cap, PE, ROE, growth | SQGLP genetic screening |
| `get_kline_data(stock_code, period)` | Code + period | OHLCV + MA + MACD | Wave + volume verification |
| `calculate_fibonacci(low, high)` | Low, high prices | Retracement + extension levels | Target price calculation |

## Analysis Workflow (4-Phase)

```
User Input
    │
    ▼
[1] 🔍 Genetic Screening — SQGLP score (1-10)
    │
    ▼
[2] 📈 Wave Positioning — 8-wave cycle + 3 Iron Rules
    │
    ▼
[3] ⚖️ Volume-Price Check — Breakout + MACD + Fakeout
    │
    ▼
[4] 🎯 Entry/Exit Guidance — Trigger + Target + Stop-Loss
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-06-28 | HK IPO prospectus KB (643 items) absorbed; industry cross-reference |
| 2.0.0 | 2026-06-28 | Full stock KB (373) + z-library (971) absorption; 伍朝辉/刘炟鑫/Constance Brown/Mayer/Stine frameworks |
| 1.1.0 | 2026-06-28 | IMA value investing integration; Li Lu/Buffett/PAG/DBS frameworks |
| 1.0.0 | 2026-06-28 | Initial release: 4-phase analysis, SQGLP, backtesting |

## Author

**王东杰 (Wang Dongjie)**
- Title: 资深复合型战略财务专家 | 上市公司资本运作操盘手
- Role: CFO 首席财务官
- Email: Wdj_@163.com
- Phone: 13952453499

## License

MIT — Free for personal, educational, and commercial use.

---

*"The stock market is a device for transferring money from the impatient to the patient." — Warren Buffett*
*"The greatest investment returns come from identifying societies undergoing structural transformation." — Li Lu*
