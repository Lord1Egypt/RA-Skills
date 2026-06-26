---
name: quant-trader
description: Professional quantitative trading system for cryptocurrency - backtesting, paper trading, live trading, and strategy optimization
tags: [quant, trading, backtest, crypto, strategy, optimization, bitcoin, trading-bot, algorithmic-trading]
version: 0.1.0
---

# Quantitative Trading Skill

Professional quantitative trading system designed for cryptocurrency markets, featuring backtesting, paper trading, live trading, and advanced strategy optimization.

## Installation

### Step 1: Install the Skill

```bash
clawhub install quant-trader
```

### Step 2: Clone & Setup the Project

```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-quant.git ~/openclaw-quant
cd ~/openclaw-quant

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional for backtesting)
export BINANCE_API_KEY="your-key"
export BINANCE_API_SECRET="your-secret"
```

### Step 3: Verify Installation

```bash
cd ~/openclaw-quant
python -m openclaw_quant --help
```

---

## Core Features

- **Backtesting Engine**: Test strategies on historical data with realistic simulation
- **Paper Trading**: Real-time simulation with live market data
- **Live Trading**: Automated trading on real exchanges (Binance, OKX, etc.)
- **Strategy Optimization**: Parameter optimization using Bayesian methods
- **Technical Indicators**: 50+ built-in indicators (MA, RSI, MACD, Bollinger, etc.)
- **Risk Management**: Position sizing, stop-loss, take-profit
- **Performance Analytics**: Sharpe ratio, max drawdown, win rate, profit factor
- **Multi-Exchange Support**: Via ccxt library (100+ exchanges)

---

## When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `backtest`, `trading strategy`, `quant`, `cryptocurrency trading`, `optimize strategy`
- Requests like: "test this trading strategy", "backtest MA cross", "paper trade bitcoin"
- Strategy descriptions: "buy when RSI < 30, sell when RSI > 70"
- Performance questions: "what's the sharpe ratio", "calculate max drawdown"

**TRIGGER EXAMPLES**:
- "Backtest a moving average crossover strategy on Bitcoin"
- "Optimize RSI parameters for the last 6 months"
- "Start paper trading with my momentum strategy"
- "What's the win rate of this strategy?"

**DO NOT USE** when:
- Only portfolio tracking (use portfolio-tracker skill)
- Only price alerts (use price-alert skill)
- General crypto news or information

---

## Quick Start Examples

### Example 1: Simple Moving Average Strategy

```python
from openclaw_quant import Strategy, Backtest

class MAStrategy(Strategy):
    # Parameters (can be optimized)
    fast_period = 10
    slow_period = 30

    def init(self):
        # Vectorized indicator calculation
        self.fast_ma = self.I(SMA, self.data.Close, self.fast_period)
        self.slow_ma = self.I(SMA, self.data.Close, self.slow_period)

    def next(self):
        # Event-driven logic
        if self.fast_ma[-1] > self.slow_ma[-1]:
            if not self.position:
                self.buy()
        else:
            if self.position:
                self.sell()

# Backtest
bt = Backtest(MAStrategy, data, cash=10000, commission=0.001)
result = bt.run()
print(result)
result.plot()
```

### Example 2: RSI Mean Reversion

```python
class RSIStrategy(Strategy):
    rsi_period = 14
    oversold = 30
    overbought = 70

    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)

    def next(self):
        if self.rsi[-1] < self.oversold:
            if not self.position:
                self.buy()
        elif self.rsi[-1] > self.overbought:
            if self.position:
                self.sell()

bt = Backtest(RSIStrategy, data, cash=10000)
result = bt.run()
```

### Example 3: Parameter Optimization

```python
# Optimize parameters automatically
result = bt.optimize(
    fast_period=range(5, 20, 2),
    slow_period=range(20, 60, 5),
    maximize='sharpe_ratio'  # or 'total_return', 'profit_factor'
)

print(f"Best parameters: {result.best_params}")
print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
```

### Example 4: Paper Trading

```python
from openclaw_quant import LiveTrading

# Paper trading with real-time data
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=True  # Simulation mode
)

live.run()
```

### Example 5: Live Trading

```python
# Real trading (use with caution!)
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=False,  # Real mode
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_API_SECRET')
)

live.run()
```

---

## Agent Usage Guide

### Command-Line Interface

```bash
# Backtest a strategy
openclaw-quant backtest --strategy ma_cross --symbol BTCUSDT --days 365

# Optimize parameters
openclaw-quant optimize --strategy rsi --symbol ETHUSDT --metric sharpe_ratio

# Paper trading
openclaw-quant paper --strategy ma_cross --symbol BTCUSDT

# Live trading
openclaw-quant live --strategy ma_cross --symbol BTCUSDT --confirm

# View results
openclaw-quant results --backtest-id abc123
```

### Natural Language (via OpenClaw Agent)

Agent can understand requests like:

- "Backtest a moving average crossover on Bitcoin for the last year"
- "Optimize RSI parameters to maximize Sharpe ratio"
- "Start paper trading with 10k USDT using my momentum strategy"
- "Show me the performance metrics of the last backtest"
- "What's the max drawdown of my live trading account?"

---

## Performance Metrics

The system calculates comprehensive performance metrics:

| Metric | Description |
|--------|-------------|
| **Total Return** | Overall profit/loss percentage |
| **Annualized Return** | Return extrapolated to one year |
| **Sharpe Ratio** | Risk-adjusted return (higher is better) |
| **Sortino Ratio** | Downside risk-adjusted return |
| **Max Drawdown** | Largest peak-to-trough decline |
| **Win Rate** | Percentage of profitable trades |
| **Profit Factor** | Gross profit / Gross loss |
| **Calmar Ratio** | Return / Max drawdown |
| **Average Win/Loss** | Mean profit/loss per trade |
| **Expectancy** | Expected value per trade |

---

## Built-in Strategies

The system includes several ready-to-use strategies:

1. **MA Cross**: Moving average crossover
2. **RSI Mean Reversion**: Buy oversold, sell overbought
3. **MACD Momentum**: MACD line and signal crossover
4. **Bollinger Bounce**: Trade Bollinger band touches
5. **Breakout**: Support/resistance breakouts
6. **Grid Trading**: Buy low, sell high in range
7. **DCA (Dollar Cost Average)**: Regular accumulation
8. **Mean Reversion**: Statistical arbitrage

---

## Technical Indicators

50+ indicators available via `self.I()` method:

**Trend Indicators:**
- SMA, EMA, WMA, DEMA, TEMA
- MACD, ADX, Aroon, Supertrend

**Momentum Indicators:**
- RSI, Stochastic, CCI, Williams %R
- ROC (Rate of Change), Momentum

**Volatility Indicators:**
- Bollinger Bands, ATR, Keltner Channels
- Standard Deviation, Historical Volatility

**Volume Indicators:**
- OBV, Volume SMA, MFI, VWAP
- Accumulation/Distribution, CMF

---

## Risk Management

Built-in risk management features:

```python
class MyStrategy(Strategy):
    def init(self):
        # Set risk parameters
        self.risk_per_trade = 0.02  # 2% of capital
        self.stop_loss = 0.05       # 5% stop loss
        self.take_profit = 0.10     # 10% take profit

        self.ma = self.I(SMA, self.data.Close, 20)

    def next(self):
        if self.ma[-1] > self.data.Close[-1]:
            if not self.position:
                # Calculate position size based on risk
                size = self.calculate_position_size(
                    risk=self.risk_per_trade,
                    stop_loss=self.stop_loss
                )
                self.buy(size=size)
                self.set_stop_loss(self.stop_loss)
                self.set_take_profit(self.take_profit)
```

---

## Data Sources

Supports multiple data sources:

1. **Exchange APIs**: Binance, OKX, Bybit, etc. (via ccxt)
2. **CSV Files**: Load historical data from files
3. **Database**: PostgreSQL, SQLite for caching
4. **Real-time WebSocket**: Live market data

```python
# Example: Load data from Binance
from openclaw_quant import DataFetcher

fetcher = DataFetcher('binance')
data = fetcher.fetch_candles(
    symbol='BTC/USDT',
    timeframe='1h',
    since='2023-01-01',
    limit=1000
)
```

---

## Configuration

Example configuration file (`config.yaml`):

```yaml
backtest:
  initial_capital: 10000
  commission: 0.001  # 0.1%
  slippage: 0.0005   # 0.05%

strategy:
  name: ma_cross
  parameters:
    fast_period: 10
    slow_period: 30

exchange:
  name: binance
  testnet: false

risk:
  max_position_size: 0.1  # 10% of capital
  max_drawdown: 0.2       # Stop if 20% drawdown
  daily_loss_limit: 0.05  # Stop if 5% daily loss

notification:
  telegram:
    enabled: true
    bot_token: "your-token"
    chat_id: "your-chat-id"
```

---

## Project Structure

```
openclaw-quant/
├── src/
│   ├── openclaw_quant/
│   │   ├── __init__.py
│   │   ├── strategy.py         # Strategy base class
│   │   ├── backtest.py         # Backtest engine
│   │   ├── live.py             # Live trading engine
│   │   ├── broker.py           # Order execution
│   │   ├── data.py             # Data fetching
│   │   ├── indicators.py       # Technical indicators
│   │   ├── optimizer.py        # Parameter optimization
│   │   ├── metrics.py          # Performance metrics
│   │   └── risk.py             # Risk management
│   └── strategies/
│       ├── ma_cross.py
│       ├── rsi.py
│       └── ...
├── examples/
│   ├── backtest_example.py
│   ├── optimization_example.py
│   └── paper_trading_example.py
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

---

## Requirements

```
Python >= 3.9
pandas >= 2.0.0
numpy >= 1.24.0
ccxt >= 4.0.0
optuna >= 3.0.0
matplotlib >= 3.7.0
pydantic >= 2.0.0
```

---

## Troubleshooting

### Issue 1: API Connection Error

**Error**: `ccxt.NetworkError` or connection timeout

**Solution**:
```bash
# Check internet connection
# Verify API keys are correct
# Use testnet for testing:
exchange = ccxt.binance({'enableRateLimit': True, 'options': {'defaultType': 'future', 'testnet': True}})
```

### Issue 2: Insufficient Data

**Error**: Not enough candles for strategy

**Solution**:
```python
# Increase warmup period
bt = Backtest(strategy, data, warmup=100)  # Skip first 100 candles

# Or fetch more historical data
data = fetcher.fetch_candles(symbol='BTC/USDT', limit=5000)
```

### Issue 3: Optimization Takes Too Long

**Solution**:
```python
# Reduce search space
result = bt.optimize(
    fast_period=range(5, 20, 5),  # Larger step
    slow_period=range(20, 60, 10),
    max_tries=50  # Limit iterations
)
```

---

## Safety Guidelines

### Backtesting
- Always test on historical data first
- Use realistic commission and slippage
- Beware of overfitting
- Walk-forward validation recommended

### Paper Trading
- Test for at least 1-2 weeks
- Monitor slippage and fills
- Check strategy behavior in different market conditions

### Live Trading
- Start with small capital
- Set strict risk limits
- Monitor continuously for first week
- Have emergency stop mechanism
- Never risk more than you can afford to lose

---

## Performance Tips

1. **Vectorization**: Use `self.I()` for indicators (computed once)
2. **Data Caching**: Cache historical data to avoid repeated API calls
3. **Optimization**: Use Bayesian optimization, not grid search
4. **Parallel Backtesting**: Test multiple symbols simultaneously
5. **WebSocket**: Use WebSocket for real-time data (faster than REST)

---

## Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-quant
- **Quick Start**: `~/openclaw-quant/QUICKSTART.md`
- **API Reference**: `~/openclaw-quant/docs/API.md`
- **Strategy Guide**: `~/openclaw-quant/docs/STRATEGIES.md`
- **Full README**: `~/openclaw-quant/README.md`

---

## Roadmap

### Version 0.1.0 (Current)
- Basic backtesting engine
- Simple strategies (MA, RSI)
- Binance support

### Version 0.2.0
- Paper trading
- Parameter optimization
- More indicators

### Version 0.3.0
- Live trading
- Multi-exchange support
- Advanced risk management

### Version 1.0.0
- Production-ready
- Web dashboard
- Strategy marketplace

---

## Cost

- **Development**: Free and open source (MIT License)
- **Data**: Free (using exchange APIs)
- **Trading Fees**: Varies by exchange (typically 0.1%)
- **API Costs**: Free tier available on most exchanges

---

## License

MIT License - Free for personal and commercial use

---

## Support

- **Issues**: https://github.com/ZhenRobotics/openclaw-quant/issues
- **Discussions**: https://github.com/ZhenRobotics/openclaw-quant/discussions
- **ClawHub**: https://clawhub.ai/ZhenStaff/openclaw-quant

---

## Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- Check if project is installed before use
- Warn about risks in live trading mode
- Validate strategy parameters
- Show clear performance metrics
- Explain optimization results

**DON'T**:
- Execute live trades without explicit confirmation
- Recommend specific trading strategies
- Guarantee profits or returns
- Ignore risk warnings
- Make financial advice

---

**Status**: Under Development (Alpha)

**Author**: @ZhenStaff

**Last Updated**: 2026-03-05
