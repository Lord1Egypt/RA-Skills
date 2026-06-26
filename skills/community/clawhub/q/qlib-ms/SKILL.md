---
name: qlib
description: "Microsoft Qlib - AI-oriented Quantitative Investment Platform. Use when: (1) stock/financial data analysis, (2) quantitative trading strategy development, (3) backtesting trading strategies, (4) machine learning for finance, (5) portfolio optimization, (6) risk modeling, (7) fetching stock prices, (8) factor analysis, (9) model training for financial predictions. NOT for: general web scraping, non-financial data analysis, or when Python environment is unavailable."
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "bins": ["python"] },
      "install": [
        { "id": "pip", "kind": "pip", "package": "qlib", "label": "Install Qlib via pip" }
      ]
    }
  }
---

# Microsoft Qlib Skill

Microsoft Qlib is an AI-oriented quantitative investment platform developed by Microsoft Research.

## Features

- **Data Handling**: Professional financial data processing and management
- **Alpha Factors**: Advanced factor mining and analysis
- **Backtesting**: High-performance backtesting engine
- **Portfolio Optimization**: Risk modeling and portfolio optimization
- **Machine Learning**: ML models for financial predictions

## When to Use

This skill is perfect for:

1. **Stock/Financial Data Analysis** - Analyze historical stock data, financial indicators
2. **Quantitative Trading Strategy Development** - Build and test trading algorithms
3. **Backtesting Trading Strategies** - Validate strategies with historical data
4. **Machine Learning for Finance** - Train ML models for price prediction
5. **Portfolio Optimization** - Optimize portfolio allocation and risk management
6. **Risk Modeling** - Assess and model financial risks
7. **Fetching Stock Prices** - Retrieve real-time and historical stock data
8. **Factor Analysis** - Alpha factor mining and research
9. **Model Training** - Train predictive models for financial markets

## Installation

```bash
pip install qlib
```

## Quick Start

### Initialize Qlib

```python
import qlib
qlib.init()
```

### Fetch Stock Data

```python
from qlib.data import D

# Get stock features
df = D.features(
    instruments=["AAPL", "MSFT"],
    fields=["Close($close)", "Volume($volume)"],
    freq="day"
)
```

### Build Strategy

```python
from qlib.workflow import R
from qlib.contrib.evaluate import backtest_daily

# Create and run strategy
with R.start(experiment_name="my_strategy"):
    # Strategy implementation
    result = backtest_daily(start_time="2020-01-01", end_time="2023-12-31")
```

### Train Model

```python
from qlib.contrib.model.gbdt import LGBModel

# Initialize model
model = LGBModel()
model.fit(dataset_train)
pred = model.predict(dataset_test)
```

## Requirements

- Python 3.7+
- pip

## Resources

- **GitHub**: https://github.com/microsoft/qlib
- **Documentation**: https://qlib.readthedocs.io/
- **Official Site**: https://microsoft.github.io/qlib/

## Notes

- This skill requires Python environment with pip installed
- Qlib is maintained by Microsoft Research
- For best performance, use with sufficient memory (recommended 8GB+)
