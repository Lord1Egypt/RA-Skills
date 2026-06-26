---
name: retail-performance-evaluation-analysis
description: |
  业绩评价分析工具。整合目标达成、环比、基线、Benchmark四个维度，量化"业绩不达预期"分析。
  
  核心能力：
  1. 四维度综合评价（目标达成、环比、历史基线、同行Benchmark）
  2. 预期类型识别（目标、环比、基线、Benchmark）
  3. 达成率计算与状态判定（正常/关注/告警/紧急）
  4. 综合评价报告（整合四个维度输出诊断结论）
  5. 量化"不达预期"（具体差距数值和百分比）
  
  触发条件：
  - 用户询问业绩评价（如"业绩评价一下"）
  - 用户分析不达预期（如"为什么说不达预期"）
  - 用户需要综合诊断（如"综合分析业绩"）
---

# 业绩评价分析 Skill

## 技能名称
`performance-evaluation-analysis`

## 功能描述
整合目标达成、环比、基线、Benchmark四个维度，量化"业绩不达预期"分析。

## 核心能力

### 1. 四维度综合评价
- **目标达成** (target) - 与月度/周度目标对比
- **环比** (mom) - 与上期对比
- **历史基线** (baseline) - 与历史同期对比
- **同行Benchmark** (benchmark) - 与同级门店对比

### 2. 预期类型
- TARGET - 目标达成
- MOM - 环比
- BASELINE - 历史基线
- BENCHMARK - 同行对比

### 3. 状态判定
- 🟢 正常 - 达成率 ≥ 100%
- 🟡 关注 - 达成率 95-100%
- 🟠 告警 - 达成率 85-95%
- 🔴 紧急 - 达成率 < 85%

### 4. 评价结果
- 维度名称
- 当前值
- 预期值
- 达成率
- 状态与图标
- 发现描述

## 使用示例

```python
from analyze import evaluate_comprehensive

# 综合评价
result = evaluate_comprehensive(
    store_id="416759_1714379448487",
    month="2026-03"
)
```

## 依赖Skills
- target-tracking-analysis（目标达成）
- sales-performance-analysis（环比分析）
- store-poscore-baseline-analysis（历史基线）
- store-benchmark-analysis（同行对比）

## 版本
v1.0.0 - 四维度综合评价、量化不达预期
