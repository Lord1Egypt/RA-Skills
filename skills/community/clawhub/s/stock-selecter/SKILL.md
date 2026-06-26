---
name: stock-selecter
version: 3.3.0
description: >
  统一选股技能包，整合14种策略（ROE筛选、MACD底背离、高股息、低估值、
  费雪成长股、长期低位、近期放量、趋势分析、K线形态、布林带下轨、筹码集中、
  现金流质量、北向资金、股东增持、分析师目标价），支持单策略、多策略组合筛选。
  触发词（精准触发，覆盖明确选股意图）：
  按策略名：ROE选股、ROE筛选、MACD选股、MACD筛选、MACD底背离、
  股息选股、高股息选股、估值选股、低估值、成长股筛选、费雪成长股、
  低位放量选股、长期低位选股、近期放量、趋势选股、形态选股、K线形态筛选、
  布林带选股、筹码集中选股、现金流质量、北向资金选股、股东增持选股、分析师目标价选股
  按组合意图：组合选股、筛选股票、多策略选股、综合选股、并发选股、全部策略选股
  按结果要求：按ROE排名、按评分排名、按股息率排名、取交集、取并集
  明确排除（这些场景应激活其他skill）：
  - 任何包含具体股票代码/名称的个股分析请求
  - "帮我看看XX股票"、"XX公司怎么样"、"XX值不值得买"
  - "查一下行情"、"看资金流向"等纯数据查询
---

# stock-selecter 统一选股技能包 v3.3

## 概述

将14种选股策略聚合为单一入口，支持单策略独立运行、多策略组合（AND/OR/SCORE），
以及并发加速和 HTML 可视化报告。

## 可用策略

| 策略名 | 说明 | 核心条件 | 评分维度 |
|--------|------|----------|----------|
| `roe` | ROE盈利能力 | ROE≥15%, ROA≥5% | ROE/ROA/毛利/净利/负债率/ROE趋势 |
| `macd` | MACD底背离 | K线下行+MACD向上+底背离+放量 | K线斜率/MACD斜率/放量倍数/RSI |
| `dividend` | 高股息 | 股息率≥3%+连续分红3年+ROE≥8% | 股息率/ROE/连续年数/估值/派息率 |
| `valuation` | 低估值 | PE≤25+PB≤3+PEG≤1.5+ROE≥8% | PE/PB/PEG/ROE/行业折价/PB历史分位 |
| `growth` | 费雪成长股 | 营收/净利双增≥20%+毛利≥30% | 营收增速/利润增速/毛利率/ROE |
| `low_position` | 长期低位 | 价格分位≤25%+RSI≤40 | 价格分位/RSI/距低点天数 |
| `volume_surge` | 近期放量 | 放量≥2倍+RSI≤45+反弹≥3% | 放量倍数/RSI/反弹幅度/连续放量天数 |
| `trend` | 趋势分析 | 均线多头+R²≥0.5+ADX≥25 | 趋势斜率/R²/ADX/RSI/波动率/均线排列 |
| `pattern` | K线形态 | 命中1种+形态（双底/吞没/早晨之星等） | 命中形态数量 |
| `bollinger` | 布林带下轨 | 股价触及布林带下轨+RSI超卖 | 触及程度/RSI/距下轨空间 |
| `shareholder_concentration` | 筹码集中 | 股东户数连续3期减少+ROE≥8% | 累计减少幅度/持续期数/ROE |
| `cashflow_quality` | 现金流质量 | 经营现金流≥净利润3期+商誉<30% | 满足季度数/平均比率/ROE |
| `northbound_flow` | 北向资金 | 北向连续净买入5日+累计≥5亿 | 连续天数/累计净买入/ROE |
| `shareholder_buyback` | 股东增持 | 增持比例≥0.5%+ROE≥8% | 增持比例/增持期数/ROE |
| `analyst_target` | 分析师目标价 | 隐含目标价空间≥20%+连续预测2期 | 上行空间/预测期数/ROE |

## 评分体系

所有策略统一返回 0-100 分，分数越高表示股票质量越好。
多策略组合时，`score` 为各策略得分之和（AND 模式）或之和（OR/SCORE 模式）。

评分参考基准：
- ROE  满分参考值 ≥25%
- 毛利率满分参考值 ≥40-60%
- ADX  满分参考值 ≥50
- 放量倍数满分参考值 ≥3x

## 组合模式

```
AND   ：多策略交集（股票必须同时通过所有策略，条件最严）
OR    ：多策略并集（通过任意一个即入选）
SCORE ：综合评分（全部策略打分，按总分排名，最宽松）
```

## 命令行用法

```bash
# 单策略（默认 AND）
python main.py --strategy roe --roe_threshold 15

# 多策略交集（最严）
python main.py --strategy roe,macd,dividend --mode and

# 多策略并集（宽松）
python main.py --strategy roe,macd --mode or --top 50

# 综合评分（适合 --strategy all）
python main.py --strategy all --mode score --top 50

# 并发执行（8线程，适合技术面策略）
python main.py --strategy macd,trend,volume_surge --workers 8

# 生成 HTML 可视化报告
python main.py --strategy roe,macd,dividend --report --output_dir ~/Desktop

# 调试（只分析前20只）
python main.py --strategy roe,trend --limit 20 --verbose
```

## 代码调用

```python
from main import execute

# 基础用法
result = execute({"strategy": "roe", "roe_threshold": 15})

# 多策略 AND 交集
result = execute({
    "strategy": "roe,macd,valuation",
    "mode": "and",
    "roe_threshold": 15,
    "max_pe": 20,
})

# 全策略综合评分，并发 + HTML
result = execute({
    "strategy": "all",
    "mode": "score",
    "top_n": 50,
    "workers": 8,
    "report": True,
})

# 策略专属参数（支持 namespace 前缀）
result = execute({
    "strategy": "roe,valuation",
    "roe.roe_threshold": 20,    # ROE策略参数
    "valuation.max_pe": 15,     # 估值策略参数
})
```

## 返回格式

```python
{
  "success": True,
  "results": [
    {
      "ts_code": "000001.SZ",
      "name": "平安银行",
      "industry": "银行",
      "score": 78.5,
      "strategies_hit": ["roe", "valuation"],
      "scores": {"roe": 45.2, "valuation": 33.3},
      # 以下为各策略专属字段
      "roe": 16.5, "roa": 8.2, "gross_margin": 35.1,
      "pe_ttm": 12.3, "pb": 1.1, "peg": 0.74,
    },
    ...
  ],
  "count": 42,
  "message": "[stock-selecter] AND 模式，耗时 89.3s",
  "metadata": {
    "strategies_used": ["roe", "valuation"],
    "mode": "and",
    "execution_time": 89.3,
    "per_strategy_counts": {"roe": 312, "valuation": 185},
    "saved_files": {
      "json": "/path/to/...",
      "csv":  "/path/to/...",
      "html": "/path/to/...",
    }
  }
}
```

## 参数说明

### 公共参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `strategy` | `roe` | 策略名，逗号分隔，`all`=全部 |
| `mode` | `and` | `and`/`or`/`score` |
| `top_n` | `0` | 结果截断（0=不限） |
| `workers` | `1` | 并发线程数（>1启用并发） |
| `report` | `False` | 是否生成 HTML 报告 |
| `save` | `True` | 是否保存 JSON/CSV |
| `output_dir` | `自动` | 输出目录 |

### 各策略专属参数

**ROE (`roe`)**
```
roe_threshold=15.0      # ROE 最低阈值（%）
roa_threshold=5.0      # ROA 最低阈值（%）
include_roa=True        # 是否同时筛选 ROA
min_report_periods=4   # 最少财报期数
```

**MACD (`macd`)**
```
k_slope_max=0.0         # K线斜率上限（正值=向上）
k_r2_min=0.3            # K线趋势 R² 下限
macd_slope_min=0.0      # MACD 斜率下限（正值=向上）
macd_r2_min=0.2         # MACD 趋势 R² 下限
require_divergence=True # 要求底背离
require_volume_surge=True# 要求放量
volume_surge_weeks=5    # 放量对比周数
volume_surge_threshold=1.5 # 放量倍数阈值
```

**股息 (`dividend`)**
```
min_dv_ratio=3.0        # 最低股息率（%）
min_consecutive_years=3 # 最少连续分红年数
min_roe=8.0             # 最低 ROE（%）
max_pe=30               # PE 上限
```

**估值 (`valuation`)**
```
max_pe=25.0             # PE 上限
max_pb=3.0             # PB 上限
max_peg=1.5            # PEG 上限（<1为低估）
industry_discount=0.85  # 行业基准折扣
min_roe=8.0            # 最低 ROE（%）
```

**成长股 (`growth`)**
```
min_revenue_growth=20.0   # 营收增速下限（%）
min_profit_growth=20.0   # 净利润增速下限（%）
min_gross_margin=30.0     # 毛利率下限（%）
min_consecutive_quarters=3# 连续净利润正增长季度数
min_roe=12.0             # 最低 ROE（%）
```

**长期低位 (`low_position`)**
```
lookback_days=250       # 历史价格窗口
low_position_pct=25.0  # 底部分位阈值（%）
rsi_max=40.0           # RSI 上限
rsi_window=14          # RSI 计算周期
data_period_years=2     # 数据拉取年数
```

**近期放量 (`volume_surge`)**
```
volume_surge_ratio=2.0   # 放量倍数阈值
volume_avg_days=20        # 均量计算周期
rsi_max=45.0            # RSI 上限
rebound_pct_min=3.0     # 最小反弹幅度（%）
rebound_days=5          # 反弹检测窗口
price_change_max=10.0  # 当日涨幅上限（%）
data_period_years=1     # 数据拉取年数
```

**趋势 (`trend`)**
```
ma_short=5             # 短期均线周期
ma_mid=20              # 中期均线周期
ma_long=60             # 长期均线周期
trend_r2_min=0.5       # 趋势 R² 下限
adx_min=25.0           # ADX 趋势强度下限
require_ma_bullish=True # 要求均线多头排列
```

**形态 (`pattern`)**
```
detect_double_bottom=True
detect_head_shoulders_bottom=True
detect_flag_breakout=True
detect_golden_cross=True
detect_morning_star=True
detect_bullish_engulfing=True
detect_cup_handle=True
min_pattern_score=1    # 最少命中形态数
```

**布林带下轨 (`bollinger`)**
```
bb_window=20           # 布林带周期
bb_std=2.0            # 标准差倍数
rsi_max=45.0          # RSI 上限
rsi_window=14         # RSI 周期
lookback_days=120     # 回看天数
price_change_max=9.0  # 当日涨幅上限（排除涨停）
```

**筹码集中 (`shareholder_concentration`)**
```
min_consecutive_quarters=3  # 连续减少季度数
max_holder_growth=-5.0     # 最大季度增长上限
min_roe=8.0               # 最低ROE
data_period_quarters=8      # 数据拉取期数
```

**现金流质量 (`cashflow_quality`)**
```
min_match_quarters=3      # 经营现金流>=净利润的季度数
total_periods=4            # 检测总期数
min_cashflow_ratio=0.8   # 经营现金流/净利润最小比率
min_roe=8.0              # 最低ROE
max_goodwill_pct=30.0    # 商誉/净资产上限（%）
```

**北向资金 (`northbound_flow`)**
```
min_consecutive_days=5     # 最少连续净买入天数
min_daily_net=1.0          # 单日最低净买入额（亿元）
min_total_net=5.0         # 累计最低净买入额（亿元）
lookback_days=20          # 回看天数
north_type=all            # all=全部/sh=沪股通/sz=深股通
```

**股东增持 (`shareholder_buyback`)**
```
min_buyback_ratio=0.5      # 最低增持占总股本比例（%）
min_consecutive_periods=1  # 最少增持期数
lookback_days=90          # 回看天数
holder_type=all           # all=任意/major=大股东/manager=高管
min_roe=8.0              # 最低ROE
```

**分析师目标价 (`analyst_target`)**
```
min_target_upside=20.0    # 最低目标价上行空间（%）
min_consecutive_forecasts=2# 最少连续盈利预测期数
forecast_years=2           # 预测年数
min_roe=8.0              # 最低ROE
```

## 输出文件

自动保存到 `/Volumes/Alan HD/股票筛选/`（Mac 外置硬盘），或指定目录：
- `screener_{策略}_{时间}.json` — 完整原始数据
- `screener_{策略}_{时间}.csv` — 表格格式
- `选股报告_{时间}.html` — 可交互可视化报告（需 `--report`）

## 目录结构

```
stock-selecter/
├── main.py              ← 统一入口（CLI + execute()）
├── SKILL.md             ← 本文件
├── config.json          ← 默认配置
├── strategies/
│   ├── base.py          ← 抽象基类（含并发执行引擎）
│   ├── roe.py
│   ├── macd.py
│   ├── dividend.py
│   ├── valuation.py
│   ├── growth.py
│   ├── low_position.py
│   ├── volume_surge.py
│   ├── trend.py
│   ├── pattern.py
│   ├── bollinger.py       ← v3.2 新增
│   ├── shareholder_concentration.py  ← v3.2 新增
│   ├── cashflow_quality.py          ← v3.2 新增
│   ├── northbound_flow.py           ← v3.3 新增
│   ├── shareholder_buyback.py       ← v3.3 新增
│   └── analyst_target.py             ← v3.3 新增
└── utils/
    ├── loader.py        ← 共享库动态加载
    └── report.py        ← HTML 报告生成器
```

## 并发说明

- `workers=1`（默认）：串行执行，稳定可靠
- `workers>1`：ThreadPoolExecutor 并发，**适合 IO 密集型**（大量 API 调用等待）
- MACD/趋势/放量等技术面策略建议开启并发（`--workers 8`）
- ROE/股息/估值等财务面策略数据量小，并发收益有限
- 建议并发数不超过 16，避免触发 API 限流
