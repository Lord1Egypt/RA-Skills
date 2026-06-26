---
name: us-stock-analyzer
description: Three-factor stock analysis combining DCF valuation, Livermore trend trading rules, and VIX market sentiment to generate high-confidence buy signals for US equities. Use when analyzing US stocks for investment decisions, determining optimal entry points, or evaluating buy opportunities with multi-factor confirmation.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - FMP_API_KEY
      bins:
        - python3
        - pip3
    primaryEnv: FMP_API_KEY
    emoji: "📈"
    homepage: https://github.com/yourusername/us-stock-analyzer
    install:
      - kind: uv
        package: yfinance
        bins: [python3]
      - kind: uv
        package: pandas
        bins: [python3]
      - kind: uv
        package: numpy
        bins: [python3]
      - kind: uv
        package: matplotlib
        bins: [python3]
      - kind: uv
        package: pyyaml
        bins: [python3]
      - kind: uv
        package: requests
        bins: [python3]
---

# 📈 US Stock Analyzer - Three-Factor Buy Signal System

A comprehensive stock analysis system that combines **Value Investing (DCF)**, **Trend Trading (Livermore Rules)**, and **Market Sentiment (VIX)** to generate buy signals only when all three factors align.

## Quick Start

```bash
# Install dependencies
pip3 install yfinance pandas numpy matplotlib pyyaml requests

# Set API key (optional, for enhanced financial data)
export FMP_API_KEY="your_key_here"

# Run analysis
python3 scripts/decision_engine.py AAPL
```

## Three-Factor Framework

### 1️⃣ Value Factor (DCF) - 40% Weight
- **Buy Condition**: Price < Intrinsic Value × (1 - Margin of Safety)
- **Key Metrics**: Free Cash Flow, WACC, growth rates, ROE, debt levels
- **Output**: Value score 0-100, fair value estimate

### 2️⃣ Trend Factor (Livermore) - 35% Weight
- **Buy Conditions**: 
  - Break above resistance with volume confirmation (1.5x avg)
  - Sector alignment (ETF in uptrend)
  - Price > MA20 > MA60
- **Output**: Trend score 0-100, key support/resistance levels

### 3️⃣ Sentiment Factor (VIX) - 25% Weight
- **Buy Conditions**:
  - VIX < 25 (non-panic)
  - VIX percentile < 70% (not expensive)
  - Market breadth positive (SPY uptrend)
- **Output**: Sentiment score 0-100, market regime

### Final Buy Signal
```
BUY = Value ≥ 60 AND Trend ≥ 60 AND Sentiment ≥ 60 AND Composite ≥ 70
```

## Usage

### Basic Analysis
```python
from scripts.decision_engine import StockAnalyzer

analyzer = StockAnalyzer(config_path="config.yaml")
result = analyzer.analyze("TSLA")
print(result['report'])
```

### With Chart Output
```python
analyzer.plot_analysis(result['result'], save_path="tsla_analysis.png")
```

## Data Sources

| Data | Source | Required |
|------|--------|----------|
| Price/Volume | Yahoo Finance (yfinance) | Free |
| Financials | FMP API | Optional (free tier) |
| VIX | CBOE via Yahoo | Free |
| Sector ETFs | Yahoo Finance | Free |

## Configuration

Edit `config.yaml` to customize:
- DCF discount rate (default: 10%)
- Margin of safety threshold (default: 20%)
- VIX panic threshold (default: 30)
- Factor weights
- Position sizing rules

## Output

The system generates a formatted report including:
- Executive summary with composite score
- Individual factor scores with visual bars
- Buy/hold signal with confidence level
- Position sizing recommendation
- Target price and stop loss levels
- Risk assessment

## File Structure

```
us-stock-analyzer/
├── SKILL.md                 # This file
├── config.yaml             # Configuration
├── requirements.txt        # Python dependencies
├── scripts/
│   ├── data_fetcher.py    # Data retrieval
│   ├── dcf_analyzer.py    # DCF valuation
│   ├── trend_analyzer.py  # Livermore trend analysis
│   ├── sentiment_analyzer.py # VIX sentiment
│   └── decision_engine.py # Three-factor engine
├── references/
│   └── methodology.md     # Detailed methodology
└── examples/
    └── sample_report.md   # Example output
```

## Methodology

See [references/methodology.md](references/methodology.md) for:
- Detailed DCF calculation methodology
- Livermore trading rules implementation
- VIX sentiment scoring algorithm
- Position sizing formulas

## Disclaimer

This tool is for **informational purposes only** and does not constitute investment advice. Always conduct your own research and consider consulting a financial advisor before making investment decisions.

## License

MIT-0 (Public Domain)
