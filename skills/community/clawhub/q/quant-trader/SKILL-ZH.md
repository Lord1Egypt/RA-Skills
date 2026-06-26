---
name: quant-trader
description: 专业的加密货币量化交易系统 - 回测、模拟盘、实盘交易和策略优化
tags: [量化交易, 回测, 加密货币, 策略, 优化, 比特币, 交易机器人, 算法交易]
version: 0.1.0
---

# 量化交易 Skill

专为加密货币市场设计的专业量化交易系统，支持回测、模拟盘、实盘交易和高级策略优化。

## 安装

### 步骤 1: 安装 Skill

```bash
clawhub install quant-trader
```

### 步骤 2: 克隆并设置项目

```bash
# 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-quant.git ~/openclaw-quant
cd ~/openclaw-quant

# 安装依赖
pip install -r requirements.txt

# 设置 API 密钥（回测可选）
export BINANCE_API_KEY="your-key"
export BINANCE_API_SECRET="your-secret"
```

### 步骤 3: 验证安装

```bash
cd ~/openclaw-quant
python -m openclaw_quant --help
```

---

## 核心功能

- **回测引擎**: 在历史数据上测试策略，提供真实的模拟环境
- **模拟盘交易**: 使用实时行情进行零风险模拟交易
- **实盘交易**: 连接真实交易所（币安、OKX等）自动交易
- **策略优化**: 使用贝叶斯方法自动优化参数
- **技术指标**: 内置 50+ 指标（均线、RSI、MACD、布林带等）
- **风险管理**: 仓位管理、止损、止盈
- **绩效分析**: 夏普比率、最大回撤、胜率、盈亏比
- **多交易所支持**: 通过 ccxt 库支持 100+ 交易所

---

## 使用场景

**自动触发** 当用户消息包含：

- 关键词: `回测`, `交易策略`, `量化`, `加密货币交易`, `策略优化`
- 请求如: "测试这个交易策略", "回测均线交叉", "模拟比特币交易"
- 策略描述: "RSI 低于 30 买入，高于 70 卖出"
- 绩效问题: "夏普比率是多少", "计算最大回撤"

**触发示例**:
- "回测比特币的均线交叉策略"
- "优化过去6个月的 RSI 参数"
- "用我的动量策略开始模拟交易"
- "这个策略的胜率是多少？"

**不使用** 当：
- 只是组合跟踪（使用 portfolio-tracker skill）
- 只是价格提醒（使用 price-alert skill）
- 一般的加密货币新闻或信息

---

## 快速开始示例

### 示例 1: 简单移动均线策略

```python
from openclaw_quant import Strategy, Backtest

class MAStrategy(Strategy):
    # 参数（可优化）
    fast_period = 10
    slow_period = 30

    def init(self):
        # 向量化指标计算
        self.fast_ma = self.I(SMA, self.data.Close, self.fast_period)
        self.slow_ma = self.I(SMA, self.data.Close, self.slow_period)

    def next(self):
        # 事件驱动逻辑
        if self.fast_ma[-1] > self.slow_ma[-1]:
            if not self.position:
                self.buy()
        else:
            if self.position:
                self.sell()

# 回测
bt = Backtest(MAStrategy, data, cash=10000, commission=0.001)
result = bt.run()
print(result)
result.plot()
```

### 示例 2: RSI 均值回归

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

### 示例 3: 参数优化

```python
# 自动优化参数
result = bt.optimize(
    fast_period=range(5, 20, 2),
    slow_period=range(20, 60, 5),
    maximize='sharpe_ratio'  # 或 'total_return', 'profit_factor'
)

print(f"最佳参数: {result.best_params}")
print(f"夏普比率: {result.sharpe_ratio:.2f}")
```

### 示例 4: 模拟盘交易

```python
from openclaw_quant import LiveTrading

# 使用实时数据进行模拟交易
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=True  # 模拟模式
)

live.run()
```

### 示例 5: 实盘交易

```python
# 真实交易（谨慎使用！）
live = LiveTrading(
    strategy=MAStrategy,
    exchange='binance',
    symbol='BTC/USDT',
    paper=False,  # 实盘模式
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_API_SECRET')
)

live.run()
```

---

## Agent 使用指南

### 命令行界面

```bash
# 回测策略
openclaw-quant backtest --strategy ma_cross --symbol BTCUSDT --days 365

# 优化参数
openclaw-quant optimize --strategy rsi --symbol ETHUSDT --metric sharpe_ratio

# 模拟交易
openclaw-quant paper --strategy ma_cross --symbol BTCUSDT

# 实盘交易
openclaw-quant live --strategy ma_cross --symbol BTCUSDT --confirm

# 查看结果
openclaw-quant results --backtest-id abc123
```

### 自然语言（通过 OpenClaw Agent）

Agent 可以理解如下请求：

- "回测比特币过去一年的均线交叉策略"
- "优化 RSI 参数以最大化夏普比率"
- "用 10000 USDT 和我的动量策略开始模拟交易"
- "显示上次回测的性能指标"
- "我的实盘账户最大回撤是多少？"

---

## 性能指标

系统计算全面的性能指标：

| 指标 | 描述 |
|------|------|
| **总收益** | 整体盈亏百分比 |
| **年化收益** | 推算到一年的收益率 |
| **夏普比率** | 风险调整后收益（越高越好）|
| **索提诺比率** | 下行风险调整后收益 |
| **最大回撤** | 最大的峰谷跌幅 |
| **胜率** | 盈利交易的百分比 |
| **盈亏比** | 总盈利 / 总亏损 |
| **卡玛比率** | 收益 / 最大回撤 |
| **平均盈亏** | 每笔交易的平均盈亏 |
| **期望值** | 每笔交易的期望收益 |

---

## 内置策略

系统包含多个开箱即用的策略：

1. **MA Cross**: 移动均线交叉
2. **RSI Mean Reversion**: 超卖买入，超买卖出
3. **MACD Momentum**: MACD 线和信号线交叉
4. **Bollinger Bounce**: 布林带触碰交易
5. **Breakout**: 支撑阻力突破
6. **Grid Trading**: 网格交易
7. **DCA**: 定投策略
8. **Mean Reversion**: 统计套利

---

## 技术指标

通过 `self.I()` 方法提供 50+ 指标：

**趋势指标：**
- SMA, EMA, WMA, DEMA, TEMA
- MACD, ADX, Aroon, Supertrend

**动量指标：**
- RSI, KDJ, CCI, Williams %R
- ROC（变化率）, Momentum

**波动率指标：**
- 布林带, ATR, 肯特纳通道
- 标准差, 历史波动率

**成交量指标：**
- OBV, 成交量均线, MFI, VWAP
- 累积/派发, CMF

---

## 风险管理

内置风险管理功能：

```python
class MyStrategy(Strategy):
    def init(self):
        # 设置风险参数
        self.risk_per_trade = 0.02  # 每笔交易 2% 风险
        self.stop_loss = 0.05       # 5% 止损
        self.take_profit = 0.10     # 10% 止盈

        self.ma = self.I(SMA, self.data.Close, 20)

    def next(self):
        if self.ma[-1] > self.data.Close[-1]:
            if not self.position:
                # 根据风险计算仓位大小
                size = self.calculate_position_size(
                    risk=self.risk_per_trade,
                    stop_loss=self.stop_loss
                )
                self.buy(size=size)
                self.set_stop_loss(self.stop_loss)
                self.set_take_profit(self.take_profit)
```

---

## 数据源

支持多种数据源：

1. **交易所 API**: 币安、OKX、Bybit 等（通过 ccxt）
2. **CSV 文件**: 从文件加载历史数据
3. **数据库**: PostgreSQL、SQLite 缓存
4. **实时 WebSocket**: 实时市场数据

```python
# 示例：从币安加载数据
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

## 配置

示例配置文件（`config.yaml`）：

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
  max_position_size: 0.1  # 资金的 10%
  max_drawdown: 0.2       # 20% 回撤停止
  daily_loss_limit: 0.05  # 5% 日亏损限制

notification:
  telegram:
    enabled: true
    bot_token: "your-token"
    chat_id: "your-chat-id"
```

---

## 项目结构

```
openclaw-quant/
├── src/
│   ├── openclaw_quant/
│   │   ├── __init__.py
│   │   ├── strategy.py         # 策略基类
│   │   ├── backtest.py         # 回测引擎
│   │   ├── live.py             # 实盘引擎
│   │   ├── broker.py           # 订单执行
│   │   ├── data.py             # 数据获取
│   │   ├── indicators.py       # 技术指标
│   │   ├── optimizer.py        # 参数优化
│   │   ├── metrics.py          # 性能指标
│   │   └── risk.py             # 风险管理
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

## 依赖要求

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

## 故障排查

### 问题 1: API 连接错误

**错误**: `ccxt.NetworkError` 或连接超时

**解决方案**:
```bash
# 检查网络连接
# 验证 API 密钥正确
# 使用测试网进行测试:
exchange = ccxt.binance({'enableRateLimit': True, 'options': {'defaultType': 'future', 'testnet': True}})
```

### 问题 2: 数据不足

**错误**: 策略的 K 线数据不够

**解决方案**:
```python
# 增加预热期
bt = Backtest(strategy, data, warmup=100)  # 跳过前 100 根 K 线

# 或获取更多历史数据
data = fetcher.fetch_candles(symbol='BTC/USDT', limit=5000)
```

### 问题 3: 优化时间太长

**解决方案**:
```python
# 减少搜索空间
result = bt.optimize(
    fast_period=range(5, 20, 5),  # 更大的步长
    slow_period=range(20, 60, 10),
    max_tries=50  # 限制迭代次数
)
```

---

## 安全指南

### 回测
- 始终先在历史数据上测试
- 使用真实的手续费和滑点
- 警惕过拟合
- 建议使用步进验证

### 模拟盘
- 至少测试 1-2 周
- 监控滑点和成交
- 检查策略在不同市场条件下的表现

### 实盘交易
- 从小资金开始
- 设置严格的风险限制
- 第一周持续监控
- 有紧急停止机制
- 永远不要冒超出承受能力的风险

---

## 性能优化建议

1. **向量化**: 使用 `self.I()` 计算指标（只计算一次）
2. **数据缓存**: 缓存历史数据避免重复 API 调用
3. **优化算法**: 使用贝叶斯优化，而非网格搜索
4. **并行回测**: 同时测试多个交易对
5. **WebSocket**: 使用 WebSocket 获取实时数据（比 REST 快）

---

## 文档

- **GitHub**: https://github.com/ZhenRobotics/openclaw-quant
- **快速开始**: `~/openclaw-quant/QUICKSTART.md`
- **API 参考**: `~/openclaw-quant/docs/API.md`
- **策略指南**: `~/openclaw-quant/docs/STRATEGIES.md`
- **完整 README**: `~/openclaw-quant/README.md`

---

## 路线图

### 版本 0.1.0（当前）
- 基础回测引擎
- 简单策略（均线、RSI）
- 币安支持

### 版本 0.2.0
- 模拟盘交易
- 参数优化
- 更多指标

### 版本 0.3.0
- 实盘交易
- 多交易所支持
- 高级风险管理

### 版本 1.0.0
- 生产就绪
- Web 仪表板
- 策略市场

---

## 成本

- **开发**: 免费开源（MIT 许可证）
- **数据**: 免费（使用交易所 API）
- **交易费用**: 因交易所而异（通常 0.1%）
- **API 成本**: 大多数交易所提供免费额度

---

## 许可证

MIT 许可证 - 可免费用于个人和商业用途

---

## 支持

- **问题**: https://github.com/ZhenRobotics/openclaw-quant/issues
- **讨论**: https://github.com/ZhenRobotics/openclaw-quant/discussions
- **ClawHub**: https://clawhub.ai/ZhenStaff/openclaw-quant

---

## Agent 行为指南

使用此 Skill 时，Agent 应该：

**应该**:
- 使用前检查项目是否已安装
- 在实盘交易模式下警告风险
- 验证策略参数
- 显示清晰的性能指标
- 解释优化结果

**不应该**:
- 未经明确确认执行实盘交易
- 推荐特定交易策略
- 保证利润或收益
- 忽略风险警告
- 提供财务建议

---

**状态**: 开发中（Alpha）

**作者**: @ZhenStaff

**最后更新**: 2026-03-05
