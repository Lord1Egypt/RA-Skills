---
name: yh85
description: YH8.5 双引擎量化信号系统——ST(10,3)趋势 + BB20(20,2)震荡均值回归双引擎，Playbook 路由 + 市场状态自适应参数，纯规则化信号直通。用于生成加密货币永续合约交易信号、回测或部署双引擎纯规则策略时使用。
---

# YH8.5 双引擎信号系统

YH8.5 是纯规则化双引擎量化信号生成器：**ST 趋势引擎**抓趋势、**BB20 震荡引擎**抓均值回归，由 Playbook 按市场状态（ADX/ATR 百分位）路由到对应引擎。

## 核心架构

| 引擎 | 定位 | 适用行情 |
|---|---|---|
| ST(10,3) 纯信号趋势 | 趋势跟随 | 高波动/趋势市 |
| BB20(20,2) 均值回归 | 震荡反转 | 低波动/震荡市 |

- **Playbook 路由**：ATR 百分位 > 阈值走趋势引擎，否则走震荡引擎
- **市场状态自适应**：牛/基/熊三场景切换参数
- **纯规则信号直通**：无黑箱 ML，全部可回测、可证伪

## 快速开始

```bash
# 依赖
pip install numpy pandas ccxt

# 生成信号
python3 -c "
import sys; sys.path.insert(0, '.')
from strategies.yh8_engine import YH8Engine
import pandas as pd
engine = YH8Engine()
# df = 30m K线 DataFrame(high/low/close)，索引为时间
sig = engine.scan('BTC/USDT', df)
print(sig)
"
```

## 详细文档

- **策略规则与参数详解**：见 [references/strategy.md](references/strategy.md)
- **回测与实盘绩效数据**：见 [references/performance.md](references/performance.md)
- **回测脚本**：`scripts/backtest.py`（对比不同过滤器的胜率/盈亏/回撤）

## 文件说明

- `strategies/yh8_engine.py` — 核心引擎（ST + BB20 信号生成）
- `strategies/playbook.json` — 策略配置（双引擎参数 + 币种分配）
- `strategies/playbook_manager.py` — 配置热加载
- `market_regime.py` — 市场状态分型
