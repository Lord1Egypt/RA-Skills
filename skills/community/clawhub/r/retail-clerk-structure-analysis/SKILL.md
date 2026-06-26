---
name: retail-clerk-structure-analysis
description: |
  导购结构分析工具。分析门店导购的表现结构，识别导购波动对门店业绩波动的贡献度。
  
  核心能力：
  1. 导购表现结构分析（人效分布、帕累托分析）
  2. TOP/腰部/尾部导购识别
  3. 业绩集中度评估
  4. 导购波动归因（各导购对门店业绩变化的贡献度）
  5. 增长型vs下滑型导购分类
  6. 基于累计贡献度的关键人识别
  
  触发条件：
  - 用户分析导购结构（如"导购团队结构如何"）
  - 用户需要波动归因（如"业绩下滑是谁导致的"）
  - 用户识别关键人（如"哪些导购对业绩影响最大"）
---

# 导购结构分析 Skill

## 技能名称
`clerk-structure-analysis`

## 功能描述
分析门店导购的表现结构，识别导购波动对门店业绩波动的贡献度，输出下钻分析目标列表。

## 核心能力

### 1. 导购表现结构分析
- 人效分布与帕累托分析
- TOP/腰部/尾部导购识别
- 业绩集中度评估

### 2. 导购波动归因
- 各导购对门店业绩变化的贡献度计算
- 增长型 vs 下滑型导购分类
- 基于累计贡献度的关键人识别

### 3. 下钻目标生成
- 自动识别需要深度分析的导购
- 支持多种选择标准（累计贡献度/固定数量/损失阈值）
- 输出完整的导购指标用于下钻

## 使用方法

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/clerk-structure-analysis')
from analyze import analyze

# 基础用法（默认累计贡献度80%）
result = analyze(
    store_id="416759_1714379448487",
    from_date="2026-03-01",
    to_date="2026-03-25",
    store_name="正义路60号店"
)

# 自定义选择标准
result = analyze(
    store_id="416759_1714379448487",
    from_date="2026-03-01",
    to_date="2026-03-25",
    store_name="正义路60号店",
    selection_mode="cumulative",      # 累计贡献度模式
    cumulative_threshold=0.7          # 阈值70%
)
```

## 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `store_id` | str | 是 | - | 门店ID |
| `from_date` | str | 是 | - | 分析开始日期 (YYYY-MM-DD) |
| `to_date` | str | 是 | - | 分析结束日期 (YYYY-MM-DD) |
| `store_name` | str | 否 | "" | 门店名称（用于输出） |
| `selection_mode` | str | 否 | "cumulative" | 选择模式: cumulative/top_n/threshold |
| `cumulative_threshold` | float | 否 | 0.8 | 累计贡献度阈值 (0-1) |
| `top_n` | int | 否 | 3 | 固定取前N名 |
| `min_loss_threshold` | float | 否 | None | 最小损失阈值（元） |

### 选择模式说明

| 模式 | 标准 | 适用场景 |
|------|------|---------|
| `cumulative` | 累计贡献度达到阈值 | 找"关键少数"，帕累托法则 |
| `top_n` | 固定取前N名 | 明确要分析几名导购 |
| `threshold` | 超过最小损失阈值 | 过滤掉小额波动 |

## 输出结构

```json
{
  "status": "ok",
  "store_id": "...",
  "store_name": "...",
  "analysis_period": {"from": "...", "to": "..."},
  "structure": {
    "clerk_count": 7,
    "total_sales": 313226,
    "top3_share": 0.609,
    "bottom3_share": 0.252,
    "pareto_ratio": 0.216,
    "efficiency_cv": 0.43,
    "mean_sales": 44747
  },
  "contributions": [...],
  "key_persons": {
    "selection_criteria": {...},
    "total_decline": -253022,
    "total_growth": 45678,
    "growth_clerks": [...],
    "decline_clerks": [...],
    "key_contributors": [...],
    "key_drags": [...],
    "drill_down_targets": [
      {
        "rank": 1,
        "name": "陈二妹",
        "sales_change": -83464,
        "change_pct": -72.3,
        "cumulative_share": 33.0,
        "current_sales": 31922,
        "prev_sales": 115386,
        "current_orders": 50,
        "prev_orders": 146,
        "atv": 638,
        "attach": 1.4
      }
    ]
  },
  "findings": [...],
  "total_change": -207344
}
```

## 核心指标解释

### 结构指标
| 指标 | 说明 | 健康范围 |
|------|------|---------|
| `top3_share` | TOP3导购业绩占比 | < 70% |
| `efficiency_cv` | 人效变异系数 | < 0.5 |
| `pareto_ratio` | 20%导购贡献的业绩占比 | - |

### 下钻目标指标
| 指标 | 说明 |
|------|------|
| `rank` | 下滑排名 |
| `sales_change` | 销售额变化（元） |
| `change_pct` | 变化率（%） |
| `cumulative_share` | 累计贡献度（%） |
| `current_sales` | 本期销售额 |
| `prev_sales` | 上期销售额 |
| `current_orders` | 本期订单数 |
| `prev_orders` | 上期订单数 |
| `atv` | 客单价 |
| `attach` | 连带率 |

## 诊断规则

| 问题 | 判断条件 | 严重程度 |
|------|----------|----------|
| 导购大面积下滑 | 下滑导购占比 > 50% | 🔴 高 |
| 头部集中度过高 | TOP3占比 > 70% | 🟡 中 |
| 人效差异过大 | 变异系数 > 0.5 | 🟡 中 |
| 关键拖累者 | 累计贡献度前80%的下滑导购 | 🔴 高 |

## 版本
v1.0.0 - 导购表现结构与波动归因分析
