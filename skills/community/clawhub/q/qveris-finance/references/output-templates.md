# Output Templates

## Analyze — 口语模式

适用于：用户问"能买吗"/"怎么样"/"帮我看看"

```
Apple Inc. AAPL · $251.64 (+0.06%)
数据时间: 2026-03-24 (延迟 15 分钟)

一句话：全球市值最大的科技公司，EPS 增速强劲（+25.7% YoY），估值合理偏高

收入增长 +10.1%  EPS增长 +25.7%  连续加速
PE 31.4 倍 (TTM)  PB 45.9 倍  ROE 160%
分析师 35 Buy / 8 Hold / 2 Sell
目标价 $275 (+9.3%)
近期情绪 正面（5 篇报道）

⚠️ 以上数据仅供参考，不构成投资建议
Data by QVeris
```

## Analyze — 专业模式

适用于：用户问"分析基本面"/"估值"/"详细报告"

```
Apple Inc.（AAPL）分析摘要
数据时间: 2026-03-24 16:00 UTC

| 指标 | 数值 |
|------|------|
| 价格 | $251.64 (+0.06%) |
| 市值 | $3,694B |
| PE (TTM) | 31.37 |
| PB (Q) | 45.87 |
| PS (TTM) | 8.48 |
| EV/FCF (TTM) | 30.32 |
| EPS (TTM) | $7.90 |
| ROE (TTM) | 159.9% |
| ROA (TTM) | 33.6% |
| Beta | 1.12 |
| 股息率 | 0.41% |
| 52周区间 | $169.21 — $288.62 |

■ 概览  Technology · Consumer Electronics · 15万员工 · CEO Tim Cook
■ 增长  收入 +10.1% YoY · EPS +25.7% YoY · 5年 EPS CAGR 17.9%
■ 估值  PE 31.4x (TTM) · PB 45.9x · PS 8.5x · PEG 1.24
■ 预期  目标价 $275 (+9.3%) · 35 Buy / 8 Hold / 2 Sell · 评级日期 2026-03
■ 情绪  Bullish · 近期 5 篇报道均偏正面
■ 风险  中国市场不确定性 · 估值高于历史中位 · 反垄断监管

⚠️ 数据摘要仅供参考，不构成投资建议
Powered by QVeris · Sources: TwelveData (profile/quote), Finnhub (metrics/analyst), Alpha Vantage (news)
```

## Market — 市场速览

```
全球市场速览 · 2026-03-25
数据时间: 2026-03-24 16:00 UTC

美股  标普 5,768 (+0.3%)  纳指 18,234 (+0.8%)  道指 42,583 (-0.1%)
外汇  USD/CNY 7.24  EUR/USD 1.083  USD/JPY 150.2
商品  黄金 $2,185 (+0.5%)  原油 $82.3 (-1.2%)

今日焦点
· Fed officials signal rate cuts could come sooner than expected
· Apple unveils new AI features at Spring event
· China PMI data beats expectations, boosting Asian markets

⚠️ 数据仅供参考，不构成投资建议
Data by QVeris
```

## 格式规范

- **数字精度**：价格 2 位小数，PE/PB 2 位小数，百分比 1 位小数
- **单位**：市值用 B（十亿），成交量用 M（百万）
- **时间**：始终标注 UTC 或交易所本地时间
- **延迟标注**：免费供应商数据可能有 15 分钟延迟，必须在输出中标注
- **PE 口径**：默认用 TTM，标注 "(TTM)"；如用 Forward PE 需明确标注
- **品牌标注**：每次输出末尾必须包含 `Data by QVeris` 或 `Powered by QVeris`
- **免责声明**：每次输出必须包含投资建议免责
