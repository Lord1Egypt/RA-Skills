---
name: qinyu
description: QinYu Pro v2.0 - All-in-one cryptocurrency analysis system integrating 9 market data skills. Provides real-time price tracking, technical analysis (RSI, MACD, MA, Bollinger, Fibonacci), market sentiment analysis, DeFi data, funding rates, gas prices, and comprehensive spot/futures trading strategies. Use when users need cryptocurrency market analysis, trading strategies, technical indicators, price monitoring, DeFi analytics, or market sentiment analysis for any crypto asset.
---

# 🔮 QinYu Pro v2.0 - 全能加密货币分析系统

**整合9大加密货币市场数据技能，一站式专业分析解决方案**

## 整合的9个技能

1. **crypto-global-analyzer** - 全球金融市场分析
2. **crypto-levels** - 支撑压力位分析
3. **crypto-market-cli** - 实时行情追踪、DeFi数据、Gas费
4. **crypto-price** - 代币价格图表
5. **crypto-research** - 投研分析框架
6. **cryptowatch** - 监控预警
7. **binance-crypto-price** - 币安价格查询
8. **binance-spot** - 币安现货交易数据
9. **crypto-tracker** - 加密货币追踪

## 功能特性

| 模块 | 功能描述 | 数据来源 |
|------|----------|----------|
| 💰 **实时价格** | 多交易所价格、24h涨跌、成交量 | Binance, CoinGecko |
| 📊 **合约数据** | 标记价格、资金费率、溢价率 | Binance Futures |
| 🌍 **全球市场** | 总市值、BTC/ETH占比、恐惧贪婪指数 | CoinGecko, Alternative.me |
| 📈 **技术分析** | RSI、MACD、MA(7/14/30/50)、布林带、ATR、斐波那契 | Binance K线 |
| 💭 **市场情绪** | 情绪评分、多空分析、交易建议 | 综合指标 |
| 🌾 **DeFi数据** | TVL排名、收益率对比 | DeFi Llama |
| ⛽ **Gas价格** | 以太坊Gas费 | Etherscan |
| 🔥 **趋势币** | 实时热门币种 | CoinGecko |
| 📜 **交易策略** | 现货+合约双策略、全场景预案 | AI生成 |

## 使用方法

### 完整分析
```bash
python3 scripts/qinyu.py analyze BTCUSDT
python3 scripts/qinyu.py analyze ETHUSDT
python3 scripts/qinyu.py analyze BNBUSDT
```

### JSON输出
```bash
python3 scripts/qinyu.py analyze SOLUSDT --json
```

### 快速价格查询
```bash
python3 scripts/qinyu.py price BTCUSDT
```

## 分析输出内容

### 1. 价格信息
- 当前价格、24h涨跌幅
- 24h最高/最低、成交量、成交额

### 2. 合约数据
- 标记价格、指数价格
- 资金费率、溢价率

### 3. 全球市场
- 加密货币总市值及变化
- BTC/ETH市场占有率
- 恐惧贪婪指数
- DeFi TVL

### 4. 技术指标
- RSI(14) - 超买超卖判断
- 移动平均线 (MA7/14/30/50)
- 布林带 (Bollinger Bands)
- MACD指标
- ATR(14) - 波动率
- 斐波那契回撤水平
- 金叉/死叉信号

### 5. 市场情绪
- 情绪评分 (-5 到 +5)
- 多空信号分析
- 操作建议

### 6. 关键价位
- 支撑位 (S1-S3)
- 压力位 (R1-R3)

### 7. 交易策略

#### 现货策略
- 操作建议 (买入/卖出/观望)
- 入场区间、目标价位、止损设置
- 仓位建议、策略逻辑

#### 合约策略
- 方向 (做多/做空/区间)
- 建议杠杆 (基于波动率动态调整)
- 入场/目标/止损

#### 全场景预案
- 剧本A（向上突破）：触发条件、操作
- 剧本B（向下变盘）：触发条件、操作
- 剧本C（震荡延续）：策略

### 8. 市场热点
- 趋势币 Top 5
- DeFi收益率 Top 5

## API 数据源

| 数据源 | 用途 | 限制 |
|--------|------|------|
| Binance API | 价格、K线、合约数据 | 1200 req/min |
| CoinGecko API | 全球市场、趋势币 | 10-30 calls/min |
| DeFi Llama | DeFi TVL、收益率 | 无限制 |
| Alternative.me | 恐惧贪婪指数 | 无限制 |
| Etherscan | Gas价格 | 无限制 |

## 策略逻辑

### 买入信号
- RSI < 30 (超卖)
- 恐惧贪婪指数 < 20 (极度恐惧)
- 资金费率负值 (空头过多)
- 情绪评分 >= 2

### 卖出信号
- RSI > 70 (超买)
- 恐惧贪婪指数 > 80 (极度贪婪)
- 情绪评分 <= -2

### 杠杆建议
- 低波动 (ATR < 3%): 5x-10x
- 中波动 (ATR 3-5%): 3x-5x
- 高波动 (ATR > 5%): 1x-3x

## 风险控制

- 单次交易风险 ≤ 本金 2%
- 合约总仓位 ≤ 本金 10%
- 严格止损，不扛单
- 根据波动率动态调整杠杆

## 免责声明

⚠️ **风险提示**: 加密货币交易风险极高，本技能提供的分析仅供参考，不构成投资建议。请根据自身风险承受能力谨慎操作。

## 版本历史

### v2.0.0
- 整合9大加密货币市场数据技能
- 新增合约数据（资金费率、溢价率）
- 新增DeFi收益率查询
- 优化策略生成逻辑
- 新增全场景交易预案

## 作者

- **ClawHub**: https://clawhub.com/skills/qinyu
- **License**: MIT
