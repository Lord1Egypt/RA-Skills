---
name: yanlin-macro-data
description: 研林Skill — 采集宏观流动性数据（利率、汇率、北向资金、海外市场）
---
# 研林 · 宏观数据采集 (yanlin-macro-data)
> **⚠️ 数据来源与限制（重要披露）：**
> 本Skill优先通过公开金融数据接口采集当日宏观指标（网络可用时）；网络不可用或接口受限时自动回退到**内置宏观数据库快照**（课程教学用，含利率/汇率/北向资金示例值），并在输出中标注数据日期与来源（实时/内置快照）。
> 数据仅用于课程教学演示，不构成投资建议。



## 功能
采集宏观与流动性核心指标（网络可用时黄金/原油实时获取，其余为内置快照）：
1. **国内利率** — 10Y国债收益率、央行OMO利率、SHIBOR 1W（内置快照）
2. **汇率** — 美元/人民币中间价及即期汇率（内置快照）
3. **海外市场** — 美元指数、美国10Y国债、黄金、原油（黄金/原油尝试实时获取，其余内置快照）
4. **美股个股行情** — 苹果/微软/英伟达等代表性个股实时报价（新浪财经，网络可用时）

> 说明：本Skill不含北向资金数据；网络不可用时全部指标回退内置快照并在输出中标注。

## 数据源
| 数据类别 | 来源 | 说明 |
|---------|------|------|
| 国内利率/汇率 | 内置快照（课程教学用） | 标注数据日期，非实时 |
| 黄金/原油 | 新浪财经 hf_GC/hf_CL（网络可用时） | 失败回退内置值 |
| 美股个股 | 新浪财经 gb_aapl/gb_msft 等（网络可用时） | 仅用于海外市场参考 |
| 美元指数/美债 | 内置快照（课程教学用） | 标注数据日期 |

## 调用方式
```bash
python3 {baseDir}/scripts/fetch_macro_data.py [--output json|text]
```

## 输出示例
```json
{
  "date": "2026-07-03",
  "domestic": {
    "bond_10y": {"value": 2.12, "unit": "%", "weekly_change": -0.03},
    "omo_rate": {"value": 1.80, "unit": "%"},
    "shibor_1w": {"value": 1.76, "unit": "%", "change": -2, "change_unit": "bp"}
  },
  "fx": {
    "usdcny_mid": 7.24,
    "usdcny_spot": 7.2420
  },
  "north_flow": {
    "total_net_buy": 68,
    "unit": "亿元"
  },
  "overseas": {
    "dollar_index": {"value": 104.2, "change": -0.5},
    "us_10y": {"value": 4.28, "unit": "%", "change": -6, "change_unit": "bp"},
    "gold": {"value": 2385, "unit": "USD/oz", "change_pct": 3.2},
    "brent_oil": {"value": 82.3, "unit": "USD/bbl", "change_pct": 1.1}
  }
}
```
