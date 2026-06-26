---
name: retail-store-benchmark-analysis
description: |
  门店Benchmark分析工具。与集团/区域其他门店对比，分析门店等级、排名变化、件单价×连带率矩阵象限。
  
  核心能力：
  1. 多维度对比范围（集团全部、区域、省份、城市）
  2. 门店等级评估（基于销售额、订单数、客单价、连带率）
  3. 排名变化追踪（本期排名vs上期排名）
  4. 件单价×连带率矩阵象限分析（识别门店定位）
  5. 同等级门店对比（找出同级别标杆）
  
  触发条件：
  - 用户需要排名（如"门店排名多少"）
  - 用户对比其他店（如"和别的店比怎么样"）
  - 用户分析门店等级（如"门店是什么等级"）
  - 用户需要Benchmark（如"Benchmark一下"）
---

# 门店Benchmark分析 Skill

## 技能名称
`store-benchmark-analysis`

## 功能描述
与集团/区域其他门店对比，分析门店等级、排名变化、"件单价×连带率"矩阵象限。

## 核心能力

### 1. 对比范围
- **GROUP** (`group`) - 集团全部
- **REGION** (`region`) - 区域（西南区等）
- **PROVINCE** (`province`) - 省份
- **CITY** (`city`) - 城市

### 2. 门店等级评估
基于以下指标综合评估：
- 销售额
- 订单数
- 客单价
- 连带率

### 3. 排名变化追踪
- 本期排名 vs 上期排名
- 排名升降分析

### 4. 件单价×连带率矩阵
识别门店定位：
- 高件单价 × 高连带率：精品店
- 高件单价 × 低连带率：高端但连带弱
- 低件单价 × 高连带率：平价高连带
- 低件单价 × 低连带率：需全面提升

## 使用示例

```python
from analyze import analyze_benchmark, ComparisonScope

# 分析门店Benchmark
result = analyze_benchmark(
    store_id="416759_1714379448487",
    comparison_scope=ComparisonScope.REGION,
    from_date="2026-03-01",
    to_date="2026-03-25"
)
```

## 版本
v1.0.0 - 多维度对比、门店等级、矩阵象限分析
