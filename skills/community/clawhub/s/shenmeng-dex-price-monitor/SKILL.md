---
name: dex-price-monitor
description: DEX价格监控与差价追踪助手。当用户需要实时监控多个DEX的代币价格、发现套利价差、设置价格预警、分析价格趋势或获取最优交易路径时使用。支持Uniswap、SushiSwap、Curve等主流DEX，涵盖以太坊、Arbitrum、BSC等多链生态的价格监控。
---

# DEX Price Monitor DEX价格监控

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

帮助用户实时监控DEX代币价格，发现套利机会，设置价格预警。

## 核心能力

1. **实时价格监控** — 多DEX价格同步追踪
2. **价差发现** — 自动识别套利机会
3. **价格预警** — 目标价提醒、价差阈值通知
4. **历史分析** — 价格走势、波动率统计
5. **最优路径** — 最优交易路径推荐
6. **监控工具** — 脚本模板、配置文件

## 适用场景

| 场景 | 示例 |
|------|------|
| **套利监控** | "监控ETH在Uniswap和SushiSwap的价差" |
| **价格预警** | "ETH涨到4000美元提醒我" |
| **多DEX对比** | "哪个DEX的USDC汇率最好？" |
| **趋势分析** | "过去一周ETH价格波动如何？" |
| **实时追踪** | "实时显示BTC在各大DEX的价格" |
| **最优交易** | "买100个ETH哪里最划算？" |

## 监控框架

### 监控维度

**1. 单代币多DEX监控**
```
代币: ETH
监控DEX:
- Uniswap V3 (以太坊)
- SushiSwap (以太坊)
- Curve (以太坊)
- Uniswap V3 (Arbitrum)
- SushiSwap (Arbitrum)

输出: 实时价格对比表
```

**2. 多代币监控**
```
代币列表:
- ETH/USDC
- WBTC/USDC
- LINK/USDC
- UNI/USDC

输出: 价格矩阵
```

**3. 价差监控**
```
监控条件:
- 价差 > 0.5%
- 价差 > 1%
- 价差 > 2%

通知方式:
- 控制台输出
- 日志记录
- Webhook推送
```

### 监控频率

| 频率 | 适用场景 | 资源消耗 |
|------|----------|----------|
| 实时 (WebSocket) | 高频套利 | 高 |
| 5秒 | 活跃监控 | 中 |
| 30秒 | 一般监控 | 低 |
| 5分钟 | 趋势追踪 | 极低 |

## 价格数据源

### 链上数据源

**1. The Graph (推荐)**
```graphql
# Uniswap V3 查询示例
{
  pools(where: {token0_: {symbol: "ETH"}}) {
    id
    token0Price
    sqrtPriceX96
    volumeUSD
    feeTier
  }
}
```

**2. DEX API**
```
1inch API: https://api.1inch.io/
0x API: https://api.0x.org/
ParaSwap API: https://api.paraswap.io/
```

**3. 聚合器**
```
CoinGecko: https://api.coingecko.com/
CoinMarketCap: https://pro-api.coinmarketcap.com/
CryptoCompare: https://min-api.cryptocompare.com/
```

**4. 直接合约查询**
```solidity
// Uniswap V3 slot0
function getPrice(address pool) view returns (uint256 price) {
    (uint160 sqrtPriceX96,,,,,,) = IUniswapV3Pool(pool).slot0();
    price = uint256(sqrtPriceX96) ** 2 / 2**192;
}
```

### 数据质量对比

| 数据源 | 实时性 | 准确性 | 成本 | 稳定性 |
|--------|--------|--------|------|--------|
| The Graph | ⭐⭐⭐ | ⭐⭐⭐⭐ | 免费 | 高 |
| 1inch API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 免费/付费 | 高 |
| CoinGecko | ⭐⭐ | ⭐⭐⭐ | 免费/付费 | 中 |
| 直接合约 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Gas | 极高 |

## 价格预警系统

### 预警类型

**1. 目标价预警**
```
条件: ETH > $4,000
通知: "ETH突破4000美元！"

适用: 买入/卖出决策
```

**2. 价差预警**
```
条件: Uniswap vs SushiSwap 价差 > 1%
通知: "发现套利机会！"

适用: 搬砖套利
```

**3. 波动率预警**
```
条件: 1小时波动 > 5%
通知: "ETH剧烈波动！"

适用: 风险管理
```

**4. 异常检测**
```
条件: 某DEX价格偏离 > 3%
通知: "可能存在异常！"

适用: 发现bug/攻击
```

### 通知渠道

```
✓ 控制台输出
✓ 本地日志
✓ Telegram Bot
✓ Discord Webhook
✓ 邮件通知
✓ 短信（严重预警）
```

## 价差分析

### 价差计算

```
绝对价差 = Price_A - Price_B
相对价差 = (Price_A - Price_B) / Price_B * 100%

示例:
Uniswap: $3,500
SushiSwap: $3,520

绝对价差: $20
相对价差: 0.57%
```

### 价差趋势

```
监控指标:
- 当前价差
- 1小时平均价差
- 24小时最大价差
- 价差标准差（波动率）
```

### 盈亏平衡点

```
最小可套利价差 = Gas成本/本金 + 协议费 + 滑点

示例（$10K本金，以太坊）:
= $50/$10000 + 0.6% + 0.3%
= 0.5% + 0.6% + 0.3%
= 1.4%

结论: 价差需 > 1.4% 才有利可图
```

## 历史分析

### 价格统计

```
时间范围: 24h / 7d / 30d

指标:
- 最高价 / 最低价
- 平均价 / 中位数
- 标准差（波动率）
- 最大回撤
```

### 价差统计

```
频率分布:
- 价差 < 0.1%: 60%
- 0.1% < 价差 < 0.5%: 30%
- 0.5% < 价差 < 1%: 8%
- 价差 > 1%: 2%

结论: 大价差机会稀少
```

### 相关性分析

```
DEX价格相关性:
- Uniswap vs SushiSwap: 0.99+
- 以太坊 vs Arbitrum: 0.98+
- 中心化 vs 去中心化: 0.995+
```

## 监控脚本

### 基础监控

```python
# 每5秒检查一次
while True:
    prices = fetch_prices('ETH/USDC')
    spreads = calculate_spreads(prices)
    
    for spread in spreads:
        if spread.value > THRESHOLD:
            alert(spread)
    
    sleep(5)
```

### 高级监控

```python
# 多线程监控
import threading

def monitor_pair(pair):
    while running:
        prices = fetch_prices(pair)
        analyze(prices)
        sleep(interval)

# 启动多个监控线程
for pair in PAIRS:
    t = threading.Thread(target=monitor_pair, args=(pair,))
    t.start()
```

## 参考资料

- **价格数据源**: `references/data-sources.md`
- **监控工具**: `references/monitoring-tools.md`
- **API文档**: `references/api-documentation.md`
- **预警配置**: `references/alert-configuration.md`

## 脚本工具

- **实时监控器**: `scripts/realtime_monitor.py`
- **价差追踪器**: `scripts/spread_tracker.py`
- **价格预警器**: `scripts/price_alerts.py`
- **历史分析器**: `scripts/historical_analyzer.py`
- **最优路径器**: `scripts/best_path_finder.py`

## 风险提示

⚠️ **重要声明**：
1. 价格数据可能存在延迟，实际交易价格可能有差异
2. 监控发现机会不等于一定能执行成功
3. 大价差可能意味着流动性不足或系统异常
4. 高频监控可能触发API限制
5. 不构成投资建议，请自行评估风险

## 使用示例

### 示例1：实时价格对比

**用户**："实时对比ETH在几个DEX的价格"

**输出**：
```
📊 ETH/USDC 实时价格对比
更新时间: 2024-03-25 19:15:30

DEX                 价格(USD)      24h量        差异
─────────────────────────────────────────────────────
Uniswap V3         $3,520.45     $450M        基准
SushiSwap          $3,524.12     $89M        +0.10%
Curve              $3,519.88     $45M        -0.02%
Uniswap V3 (Arb)   $3,518.50     $120M       -0.05%
Camelot (Arb)      $3,521.30     $25M        +0.03%

最大价差: 0.12% (SushiSwap vs Uniswap V3 Arb)
结论: 价差较小，不适合套利
```

### 示例2：设置价格预警

**用户**："ETH涨到3600或跌到3400提醒我"

**输出**：
```
🔔 价格预警已设置

代币: ETH/USDC
当前价: $3,520.45

预警条件:
  ✓ 上涨突破: $3,600 (+2.26%)
  ✓ 下跌跌破: $3,400 (-3.42%)

通知方式:
  - 控制台输出
  - Telegram推送
  - 日志记录

监控频率: 5秒
```

### 示例3：价差预警

**用户**："Uniswap和SushiSwap价差超过0.8%提醒我"

**输出**：
```
🔔 价差预警已设置

监控对: Uniswap V3 vs SushiSwap
基准对: ETH/USDC

当前价差: 0.10%
预警阈值: 0.80%

状态: 🟢 监控中...

预计触发频率: 
  - 基于历史数据: 约2-3次/天
  - 最佳套利时段: UTC 14:00-16:00
```

---

*价格监控是套利的第一环，信息优势就是利润优势。*
