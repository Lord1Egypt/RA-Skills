---
name: retail-store-poscore-baseline-analysis
description: |
  门店历史基线分析工具。基于Agent API数据库视图，提供多周期基线+四分位分析。
  
  核心能力：
  1. 多周期基线（13周/季度、26周/半年、52周/全年、12个月）
  2. 多维度分组（按星期几分组、自然周、自然月）
  3. 四分位分析（P25/P50/P75，识别异常区间）
  4. 基线类型（weekday按星期几分组、week自然周、month自然月）
  5. 数据质量检查（最小样本数要求）
  
  数据源：v_gmv_daily_by_store、v_gmv_weekly_by_store、v_gmv_monthly_by_store
  
  触发条件：
  - 用户需要基线对比（如"和历史比怎么样"）
  - 用户分析周期规律（如"周一通常卖多少"）
  - 用户识别异常（如"今天的业绩正常吗"）
---

# 历史基线分析 Skill

## 技能名称
`store-poscore-baseline-analysis`

## 版本
v1.0

## 功能描述
基于Agent API（数据库视图），提供多周期基线+四分位分析。

## 数据源
- `v_gmv_daily_by_store`（日粒度）
- `v_gmv_weekly_by_store`（周粒度）
- `v_gmv_monthly_by_store`（月粒度）

## 核心能力

### 1. 基线类型
- **WEEKDAY** (`weekday`) - 按星期几分组（周一、周二...）
- **WEEK** (`week`) - 自然周（周一至周日）
- **MONTH** (`month`) - 自然月（每月1日到最后1日）

### 2. 基线周期
- **P13W** (`13w`) - 13周（季度）
- **P26W** (`26w`) - 26周（半年）
- **P52W** (`52w`) - 52周（全年）
- **P12M** (`12m`) - 12个月

### 3. 四分位分析
- P25（第25百分位）
- P50（中位数）
- P75（第75百分位）
- 识别异常区间

### 4. 最小样本要求
- weekday: 至少6个样本
- week: 至少6周
- month: 至少6个月

## 使用示例

```python
from analyze import analyze_baseline, BaselineType, BaselinePeriod

# 分析门店历史基线
result = analyze_baseline(
    store_id="416759_1714379448487",
    baseline_type=BaselineType.WEEKDAY,
    baseline_period=BaselinePeriod.P13W,
    end_date="2026-03-25"
)
```

## 版本
v1.0.0 - 多周期基线、四分位分析
