# PTRADE Strategy Generator Skill

> OpenClaw Skill — Generate ready-to-use quantitative trading strategies for the Guojin PTRADE platform.

---

## English

### Overview

This OpenClaw skill generates Python strategy code for the **Guojin PTRADE quantitative trading platform** (国金 PTRADE). It provides strategy templates, API references, and code generation based on your knowledge base documents stored in IMA.

### Features

- **Strategy Templates**: Moving Average (MA), Financial Factor, Intraday Trading
- **Full API Reference**: Market data, trading functions, financial factors
- **Code Generation**: Generate complete strategies from templates in seconds
- **Knowledge Base Integration**: Reads documents from IMA `个人知识库 -> 国金量化`

### Installation

```bash
skillhub install ptrade-strategy
```

### Usage

Trigger keywords: `PTRADE`, `量化策略`, `量化交易`, `生成策略`

Example:
> "帮我生成一个双均线策略"
> "Generate a financial factor stock selection strategy"

### Included Templates

| File | Description |
|------|-------------|
| `templates/dual_ma_strategy.py` | Dual Moving Average (Golden/Death Cross) |
| `templates/factor_strategy.py` | Financial Factor Stock Selection |
| `templates/ma_strategy.py` | Basic MA Strategy |

### Strategy Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SECURITY` | `000001.XSHG` | Trading symbol (Code.Exchange) |
| `SHORT_WIN` | `5` | Short MA period |
| `LONG_WIN` | `20` | Long MA period |
| `PERIOD` | `1d` | K-line period: `1d` daily, `60m`, `5m` |
| `STOP_LOSS_PCT` | `5%` | Stop loss threshold |
| `TAKE_PROFIT_PCT` | `15%` | Take profit threshold |

### PTRADE API Reference

```python
# Market data
security.get_bars(n, end_date, fields, count, period)
security.get_financial_data(start_date, end_date, count, fields)
security.get_index_stocks(index_code)  # e.g. "000300.XSHG"
security.get_positions()
security.get_account_info()

# Trading
trade.open_long(security, volume, price, price_type)
trade.close_long(security, volume, price, price_type)
# price_type: "market" (open price), "latest" (requires live data)

# Supported: numpy, pandas, scipy, sklearn, statsmodels
```

### How to Run in PTRADE

1. Open PTRADE -> 策略研究 -> 新建策略
2. Paste the generated code -> Save
3. Backtest: Set date range and initial capital
4. Optimize: Adjust SHORT_WIN / LONG_WIN
5. Live: Enable auto-execution

---

## 中文说明

本 Skill 为**国金 PTRADE 量化交易平台**生成可运行的 Python 策略代码。

### 核心功能

- **策略模板**：双均线、财务因子选股、日内交易
- **API 参考**：行情获取、下单函数、财务数据
- **代码生成**：从模板快速生成完整策略
- **知识库集成**：读取 IMA「个人知识库 -> 国金量化」中的官方文档

### 使用方式

触发关键词：`PTRADE`、`量化策略`、`量化交易`、`生成策略`

### PTRADE 使用步骤

1. 打开 PTRADE -> 策略研究 -> 新建策略
2. 粘贴代码 -> 保存（Ctrl+S）
3. **回测**：设置时间范围和初始资金
4. **参数优化**：调整均线周期等参数
5. **实盘运行**：订阅策略，开启自动下单

### 注意事项

- `volume` 必须为 100 的整数倍（1手=100股）
- 回测撮合默认以**开盘价**成交，需订阅实时行情才能用最新价
- 支持库：`numpy` `pandas` `scipy` `sklearn` `statsmodels`

---

## Repository Structure

```
ptrade-strategy/
├── SKILL.md                    # Main skill file
├── kb_ref.md                   # Knowledge base document index
└── templates/
    ├── dual_ma_strategy.py     # Dual MA strategy (recommended)
    ├── ma_strategy.py           # Basic MA strategy
    └── factor_strategy.py       # Financial factor strategy
```

---

## License

MIT
