# Zeyang Strategy Lab Free

**泽洋策略研究室 Free｜用自然语言描述策略，在本地完成可审计的历史回测。**

泽洋策略研究室 Free 是一个用于投资研究、策略验证和教学学习的本地历史回测 Skill。用户提供自己的历史行情 CSV，并用自然语言描述简单策略，例如：

> 回测 SPY 日线 EMA20，收盘价高于 EMA20 持仓，低于 EMA20 空仓。

系统会自动完成策略标准化、指标计算、Signal 生成、历史回测，并与 Buy & Hold 进行对比。运行完成后，入口会直接返回总收益率、交易次数、最大回撤和买入持有收益，用户不需要打开 Markdown 文件。结果可保存在本地并复核，输出包括：

- Strategy Contract
- Signals
- Validation
- Backtest
- Trade Ledger
- Markdown Summary
- Total Return
- CAGR
- Maximum Drawdown
- Exposure
- Trade Count
- Equity Curve
- Drawdown Curve
- JSON、CSV、Markdown

### Free v0.1.2 支持范围

- Single Asset、Daily、Long / Cash
- EMA、SMA、RSI
- Close vs EMA / SMA
- RSI Threshold
- Basic Commission、Basic Slippage
- Buy & Hold
- Total Return、CAGR、Maximum Drawdown、Exposure、Trade Count
- Basic Equity Chart、Basic Drawdown Chart
- User-provided local CSV

Free v0.1.2 不支持 MACD、Bollinger Bands、Cross / Crossunder、做空、杠杆、分钟数据、多标的组合、参数优化、自动抓取行情、券商连接、实盘交易或专业 Word 研究报告。

历史回测不代表未来表现。本项目仅用于研究、教育和策略验证，不构成投资建议。

---

**Zeyang Strategy Lab Free | Describe a strategy in natural language and run an auditable historical backtest locally.**

Zeyang Strategy Lab Free is a local historical backtesting Skill for investment research, strategy validation, and education. Users provide their own historical market data in CSV format and describe a simple strategy in natural language.

For example:

> Backtest SPY on daily bars using EMA20. Stay long when the close is above EMA20 and move to cash when the close is below EMA20.

The system automatically normalizes the strategy, calculates indicators, generates signals, runs the historical backtest, and compares the strategy with Buy & Hold. The final entrypoint output directly shows total return, trade count, maximum drawdown, and Buy & Hold return, so users do not need to open the Markdown file. Results can be saved and reviewed locally. Outputs include:

- Strategy Contract
- Signals
- Validation
- Backtest
- Trade Ledger
- Markdown Summary
- Total Return
- CAGR
- Maximum Drawdown
- Market Exposure
- Trade Count
- Equity Curve
- Drawdown Curve
- JSON, CSV, and Markdown artifacts

### Free v0.1.2 scope

- Single Asset, Daily, Long / Cash
- EMA, SMA, and RSI
- Close vs EMA / SMA
- RSI threshold rules
- Basic commission and slippage
- Buy & Hold comparison
- Total Return, CAGR, Maximum Drawdown, Exposure, and Trade Count
- Basic equity and drawdown charts
- User-provided local CSV data

Free v0.1.2 does not support MACD, Bollinger Bands, Cross / Crossunder rules, shorting, leverage, minute data, multi-asset portfolios, parameter optimization, automatic market-data fetching, broker connections, live trading, or professional Word research reports.

The Free edition does not automatically fetch market data, connect to brokers, or place live orders.

Historical backtests do not predict future performance. This project is for research, education, and strategy validation only and does not constitute investment advice.

## Install

Use Python 3.10 or later. The basic PNG charts require Pillow:

```text
python -m pip install Pillow
```

## Input CSV

Provide a local daily CSV. `date` and `close` are required. `open` is optional: the default `next_open` execution uses the next bar's `open` when available; when it is absent, the runtime formally falls back to the next bar's `close` and records a warning. `high`, `low`, `volume`, and one `symbol` are recommended. If `symbol` is supplied, the file must contain one asset only. Dates must be ISO-8601 compatible. See [references/data-contract.md](references/data-contract.md).

## EMA20 example

```text
python scripts/run_free_research.py --strategy "回测 TEST 日线 EMA20，收盘价高于 EMA20 持仓，低于 EMA20 空仓。" --input ./my_prices.csv
```

## RSI14 example

```text
python scripts/run_free_research.py --strategy "回测 TEST 日线 RSI14 低于 30 买入，高于 70 卖出。" --input ./my_prices.csv
```

## Output

Each run creates a local `runs/free-<run-id>/` directory containing the Strategy Contract, generated signals, validation result, backtest JSON, trade ledger, Markdown summary, and two basic charts. These files are local research artifacts and should not be committed by default.

## Research-only notice

Historical results do not predict future performance. Confirm data provenance, adjustment basis, transaction assumptions, and strategy timing before interpreting any result. This tool is for research and education only, not investment advice.

## License

Zeyang Strategy Lab Free is licensed under AGPL-3.0-only. See [LICENSE](LICENSE).

The commercial Pro edition is separately licensed and is not included in this repository.

## Contributions

For the initial public beta, issues and feedback are welcome.
Code contributions are not currently being accepted.
