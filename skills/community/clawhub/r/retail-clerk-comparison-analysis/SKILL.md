---
name: retail-clerk-comparison-analysis
description: |
  导购对比分析工具。基于clerk-performance-analysis的扩展，提供导购业绩的多维度对比分析。
  
  核心能力：
  1. 时间维度对比（培训前后、活动前后、月度环比）
  2. 横向对比（多人排名、标杆学习、差距分析）
  3. 高频场景（晨会对比、周会报告、绩效对标）
  4. 导购能力雷达图对比
  5. 业绩贡献度对比
  
  触发条件：
  - 用户对比导购（如"李翠和杨丽谁业绩好"）
  - 用户需要排名（如"导购业绩排名"）
  - 用户分析差距（如"标杆导购和其他人的差距"）
---

# 导购对比分析 Skill

## 技能名称
`clerk-comparison-analysis`

## 功能描述
基于 `clerk-performance-analysis` 的扩展，提供导购业绩的对比分析功能：
- **时间维度对比**：培训前后、活动前后、月度环比等
- **横向对比**：多人排名、标杆学习、差距分析
- **高频场景**：晨会对比、周会报告、绩效对标

## 依赖关系

本Skill依赖 `clerk-performance-analysis`：
```python
import sys
sys.path.insert(0, '~/.openclaw/skills/clerk-performance-analysis')
from analyze import analyze
```

## 核心功能

### 1. 导购自身时间维度对比

**函数：** `compare_guide_over_time()`

**使用场景：**
| 场景 | period_a | period_b | comparison_label |
|------|----------|----------|------------------|
| 培训效果评估 | 培训前7天 | 培训后7天 | "新品销售培训前后" |
| 活动效果复盘 | 活动前7天 | 活动期间 | "315大促活动期间" |
| 月度环比 | 上月同期 | 本月 | "3月vs2月环比" |
| 波动归因 | 低谷期 | 高峰期 | "低谷vs高峰对比" |

**示例：**
```python
from compare import compare_guide_over_time

result = compare_guide_over_time(
    store_id="416759_1714379448487",
    guide_name="李翠",
    period_a_from="2026-03-01",
    period_a_to="2026-03-07",
    period_b_from="2026-03-16",
    period_b_to="2026-03-22",
    comparison_label="新品销售培训前后"
)
```

**输出：**
```json
{
  "status": "ok",
  "comparison_label": "新品销售培训前后",
  "period_a": {"from": "...", "to": "...", "metrics": {...}},
  "period_b": {"from": "...", "to": "...", "metrics": {...}},
  "changes": {
    "sales": {"before": 28456, "after": 36103, "change": 7647, "change_pct": 26.9, "trend": "up"},
    "orders": {...},
    "atv": {...},
    "new_customers": {...}
  },
  "key_findings": [...],
  "recommendations": [...]
}
```

### 2. 多人导购横向对比

**函数：** `compare_guides()`

**使用场景：**
- 晨会快速对比昨日表现
- 周会排名和差距分析
- 月度绩效对标
- 标杆学习和经验分享

**示例：**
```python
from compare import compare_guides

result = compare_guides(
    store_id="416759_1714379448487",
    guide_names=["李翠", "杨丽", "赵泽瑞", "陈二妹"],
    from_date="2026-03-25",
    to_date="2026-03-25"
)
```

**输出：**
```json
{
  "status": "ok",
  "total_guides": 4,
  "rankings": {
    "by_sales": [...],
    "by_new_customers": [...],
    "by_atv": [...]
  },
  "top_performer": {...},
  "bottom_performer": {...},
  "gap_analysis": [...],
  "needs_attention": [...],
  "quick_insights": [...]
}
```

### 3. 标杆对比（找差距）

**函数：** `compare_with_benchmark()`

**使用场景：**
- 待提升导购与标杆对比
- 生成个性化改进计划
- 一对一辅导准备

**示例：**
```python
from compare import compare_with_benchmark

result = compare_with_benchmark(
    store_id="416759_1714379448487",
    guide_name="陈二妹",           # 待提升导购
    benchmark_guide_name="李翠",   # 标杆导购
    from_date="2026-03-01",
    to_date="2026-03-25"
)
```

**输出：**
```json
{
  "status": "ok",
  "guide": {"name": "陈二妹", "metrics": {...}},
  "benchmark": {"name": "李翠", "metrics": {...}},
  "gaps": {
    "sales": {"guide_value": 31922, "benchmark_value": 64559, "gap": 32637, "gap_pct": 50.6},
    "new_customers": {...}
  },
  "learning_points": [...],
  "action_plan": [...]
}
```

## 高频使用场景

### 场景1：晨会快速对比（每日）

```python
# 店长每日晨会前自动生成
report = compare_guides(
    store_id="...",
    guide_names=["李翠", "杨丽", "赵泽瑞", "陈二妹"],
    from_date=yesterday,
    to_date=yesterday
)

# 推送到店长企业微信
send_morning_meeting_report(report)
```

**输出示例：**
```
═══════════════════════════════════════════════════════
导购横向对比 - 正义路60号店
2026-03-25（昨日）
═══════════════════════════════════════════════════════

【销售额排名】
#1  活动导购  ¥3,529  (25%)  7单  ¥504  ✅
#2  李翠      ¥3,111  (22%)  4单  ¥778  
#3  杨丽      ¥2,115  (15%)  3单  ¥705  
#4  陈二妹    ¥0      (0%)   0单  ¥0    ⚠️ 无销售

【需要关注】
⚠️ 陈二妹: 昨日无销售，近14天有4天无销售

【今日建议】
1. 店长重点关注陈二妹
2. 李翠分享高客单价经验
```

### 场景2：培训效果评估（培训后7天）

```python
result = compare_guide_over_time(
    store_id="...",
    guide_name="李翠",
    period_a_from="2026-03-01",  # 培训前
    period_a_to="2026-03-07",
    period_b_from="2026-03-16",  # 培训后
    period_b_to="2026-03-22",
    comparison_label="新品销售培训前后"
)

if result['changes']['sales']['change_pct'] > 20:
    print("✅ 培训效果显著，销售额提升20%+")
else:
    print("⚠️ 培训效果不明显，需要复盘")
```

### 场景3：月度绩效对标（每月底）

```python
# 生成本月完整对比报告
report = compare_guides(
    store_id="...",
    guide_names=all_guides_in_store,
    from_date="2026-03-01",
    to_date="2026-03-31"
)

# 生成绩效考核表
generate_performance_table(report)
```

### 场景4：标杆学习（按需）

```python
# 找出差距最大的导购与标杆对比
result = compare_with_benchmark(
    store_id="...",
    guide_name="陈二妹",
    benchmark_guide_name="李翠",
    from_date="...",
    to_date="..."
)

# 生成一对一辅导计划
coaching_plan = result['action_plan']
```

## 输出指标说明

### 时间对比指标

| 指标 | 说明 | 用途 |
|------|------|------|
| change | 绝对变化值 | 量化改进幅度 |
| change_pct | 变化百分比 | 评估改进比例 |
| trend | 变化趋势 | up/down/stable |

### 横向对比指标

| 指标 | 说明 | 用途 |
|------|------|------|
| gap_to_top | 与标杆的销售额差距 | 量化提升空间 |
| gap_pct | 差距百分比 | 评估追赶难度 |
| potential | 达到标杆的潜在收益 | 激励改进 |

## 诊断规则

### 时间对比诊断

| 发现类型 | 判断条件 | 建议 |
|----------|----------|------|
| 显著提升 | 销售额提升>30% | 固化成功经验 |
| 显著下滑 | 销售额下滑>30% | 分析原因并干预 |
| 问题改善 | 发现数量减少 | 肯定改进效果 |

### 横向对比诊断

| 发现类型 | 判断条件 | 建议 |
|----------|----------|------|
| 业绩集中 | TOP3贡献>70% | 关注尾部导购 |
| 新客差异 | 最大/最小>3倍 | 推广标杆经验 |
| 高风险 | 有high severity finding | 立即干预 |

## 版本
v1.0.0 - 导购对比分析Skill（支持时间对比和横向对比）
