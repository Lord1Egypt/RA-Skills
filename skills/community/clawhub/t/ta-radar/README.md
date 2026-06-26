[🇺🇸 English](#english) · [🇨🇳 中文](#chinese)

---

<a name="english"></a>

# TA Radar v1.2.0
## Multi-Dimensional Technical Analysis Radar for Cryptocurrencies

Zero-dependency technical analysis skill for OpenClaw, supporting spot trading pairs and on-chain contract addresses. Generates objective TA reports including EMA, RSI, MACD, Bollinger Bands, support/resistance levels and trend analysis.

## Features
- ✅ **Dual Data Source Fallback**: First try Binance, automatically switch to Gate.io on failure (GFW-friendly for Chinese users)
- ✅ **On-Chain Contract Support**: Resolve EVM contract addresses via DexScreener public proxy
- ✅ **Beginner-Friendly Annotations**: Each indicator includes plain language explanations, no financial background required
- ✅ **Zero Dependencies**: Pure Python implementation, no external libraries needed
- ✅ **Multiple Timeframes**: Supports 1h / 4h / 1d analysis periods

## Data Sources
- **Primary**: Binance API (`api.binance.info`)
- **Fallback**: Gate.io API (`api.gateio.ws`)
- **DEX Resolution**: DexScreener via `allorigins.win` public proxy

## Installation

Install directly via OpenClaw:

```bash
openclaw skill install https://github.com/AntalphaAI/TA-Radar
```

## Usage
### As OpenClaw Skill
After installation, the skill is ready to use inside your OpenClaw session.

### Standalone Usage
```bash
# Analyze BTC 4h chart
TA_SYMBOL="BTC" TA_INTERVAL="4h" python3 ta_radar_run.py

# Analyze ETH 1d chart
TA_SYMBOL="ETHUSDT" TA_INTERVAL="1d" python3 ta_radar_run.py

# Analyze on-chain contract address
TA_SYMBOL="0x904567252D8F48555b7447c67dCA23F0372E16be" python3 ta_radar_run.py
```

## Sample Output
```
════════════════════════════════════════════════════════════
  TA Radar v1.2  |  BTCUSDT  |  4H
  Data Source: Gate.io
  Generated: 2026-03-31 08:42 UTC
════════════════════════════════════════════════════════════

【Core Data Panel】
────────────────────────────────────────────────────────────
  Current Price  : 67,394.00

  ▸ EMA (7 / 25 / 99)
    EMA7  = 67,262.38
    EMA25 = 67,374.61
    EMA99 = 69,901.27
    Conclusion  : Bearish alignment ↓
    Explanation : Short-term EMA below long-term EMA indicates recent price weakness.
```

## Indicators
| Indicator | Parameters | Description |
|-----------|------------|-------------|
| EMA | 7/25/99 periods | Exponential Moving Average for trend identification |
| RSI | 14 periods | Relative Strength Index for overbought/oversold detection |
| MACD | 12/26/9 periods | Moving Average Convergence Divergence for momentum analysis |
| Bollinger Bands | 20 periods / 2σ | Volatility bands for support/resistance levels |

## Security Notes
- **External Requests**: Data is fetched from Binance, Gate.io and DexScreener (via allorigins.win proxy)
- **Local Only**: No data is sent to third parties other than the public API endpoints mentioned above
- **No Sensitive Data**: The skill does not store or transmit any private user information

## License
MIT License

## Maintainer
Antalpha AI Team

---

<a name="chinese"></a>

# TA Radar v1.2.0
## 加密货币多维技术分析雷达

基于 OpenClaw 的零依赖技术分析技能，支持现货交易对和链上合约地址。自动生成包含 EMA、RSI、MACD、布林带、支撑/阻力位及趋势分析的客观 TA 报告。

## 功能特性
- ✅ **双数据源自动切换**：优先使用 Binance，失败时自动切换至 Gate.io（对国内用户友好，无需翻墙）
- ✅ **链上合约地址支持**：通过 DexScreener 公共代理解析 EVM 合约地址
- ✅ **新手友好注释**：每个指标附带通俗解释，无需金融背景
- ✅ **零外部依赖**：纯 Python 实现，无需安装额外库
- ✅ **多周期分析**：支持 1h / 4h / 1d 分析周期

## 数据来源
- **主要数据源**：Binance API（`api.binance.info`）
- **备用数据源**：Gate.io API（`api.gateio.ws`）
- **DEX 解析**：通过 `allorigins.win` 公共代理访问 DexScreener

## 安装

通过 OpenClaw 一键安装：

```bash
openclaw skill install https://github.com/AntalphaAI/TA-Radar
```

## 使用方式
### 作为 OpenClaw Skill 使用
安装完成后，直接在 OpenClaw 会话中使用即可。

### 独立脚本运行
```bash
# 分析 BTC 4小时图
TA_SYMBOL="BTC" TA_INTERVAL="4h" python3 ta_radar_run.py

# 分析 ETH 日线图
TA_SYMBOL="ETHUSDT" TA_INTERVAL="1d" python3 ta_radar_run.py

# 分析链上合约地址
TA_SYMBOL="0x904567252D8F48555b7447c67dCA23F0372E16be" python3 ta_radar_run.py
```

## 输出示例
```
════════════════════════════════════════════════════════════
  TA Radar v1.2  |  BTCUSDT  |  4H
  数据来源: Gate.io
  生成时间: 2026-03-31 08:42 UTC
════════════════════════════════════════════════════════════

【核心数据面板】
────────────────────────────────────────────────────────────
  当前价格  : 67,394.00

  ▸ EMA（7 / 25 / 99）
    EMA7  = 67,262.38
    EMA25 = 67,374.61
    EMA99 = 69,901.27
    结论  : 空头排列 ↓
    解读  : 短期均线位于长期均线下方，表明近期价格偏弱。
```

## 指标说明
| 指标 | 参数 | 说明 |
|------|------|------|
| EMA | 7/25/99 周期 | 指数移动平均线，用于识别趋势方向 |
| RSI | 14 周期 | 相对强弱指数，判断超买/超卖状态 |
| MACD | 12/26/9 周期 | 移动平均收敛散度，分析动量变化 |
| 布林带 | 20 周期 / 2σ | 波动率通道，标识支撑/阻力区间 |

## 安全说明
- **外部请求**：数据仅从 Binance、Gate.io 和 DexScreener（通过 allorigins.win 代理）获取
- **本地运行**：除上述公开 API 端点外，不向任何第三方发送数据
- **无敏感数据**：本技能不存储或传输任何用户私人信息

## 开源协议
MIT License

## 维护团队
Antalpha AI Team
