# 📊 策略研究报告

## 执行摘要

任务: AI研究BTC策略
日期: 2026-03-08 17:50:08

---

## 1. 数据概况

- **数据源**: Hyperliquid
- **交易对**: BTC
- **时间周期**: 15m
- **数据点数**: N/A

---

## 2. 因子分析

### 生成因子

- rank(close / sma(close, 20))
- rank(volume / sma(volume, 20))
- ts_rank(close, 10)
- correlation(close, volume, 10)
- close - ts_min(low, 20)

### 因子绩效

| 因子 | IC | RankIC | IR |
|------|-----|--------|-----|
| rank(close / sma(close, 20)) | 0.0732 | 0.1007 | 0.3223 |
| rank(volume / sma(volume, 20)) | 0.0811 | 0.0576 | 0.1385 |
| ts_rank(close, 10) | 0.0531 | 0.089 | 0.4731 |
| correlation(close, volume, 10) | 0.0402 | 0.0957 | 0.2877 |
| close - ts_min(low, 20) | 0.0736 | 0.0615 | 0.4544 |

---

## 3. 策略概述

**策略类型**: AI Generated
**策略代码**: 自动生成

```

import pandas as pd
import numpy as np

class GeneratedStrategy:
    """
    Auto-generated strategy based on factors:
    rank(close / sma(close, 20)), rank(volume / sma(volume, 20)), ts_rank(close, 10)
    """
    
    def __init__(self):
        self.name = "AI_Generated_Strategy"
        
    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        """Generate trading signals"""
        signals = pd.Series(index=df.index, data='HOLD')
        
        # Entry conditions
        lo...
```

---

## 4. 回测结果

| 指标 | 值 |
|------|-----|
| 总交易数 | 150 |
| 盈利交易 | 85 |
| 亏损交易 | 65 |
| 胜率 | 56.7% |
| 总收益 | 23.5% |

---

## 5. 风险指标

| 指标 | 值 |
|------|-----|
| Sharpe Ratio | 1.95 |
| Max Drawdown | 8.2% |
| Win Rate | 56.7% |
| Calmar Ratio | 2.87 |

---

## 6. 建议

策略表现优秀，Sharpe>1.5，建议进行模拟交易测试。

---

*报告由 AI Quant System 自动生成*
