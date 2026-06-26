---
name: retail-sku-comparison-analysis
description: |
  SKU对比分析工具。支持SKU的时间维度、横向、导购等多维度对比分析。
  
  核心能力：
  1. 时间维度对比（本期vs上期、活动前后、月度环比）
  2. 横向对比（多个SKU排名、标杆学习）
  3. 导购维度对比（不同导购对同一SKU的销售差异）
  4. 销售表现对比（销售额、销量、转化率）
  5. AIoT数据对比（试用次数、成交转化）
  
  触发条件：
  - 用户对比SKU（如"心遥2和舒珀哪个卖得好"）
  - 用户分析SKU变化（如"这个款比上月怎么样"）
  - 用户需要SKU排名（如"Top10 SKU是哪些"）
---

# SKU对比分析 Skill

支持SKU的时间维度、横向、导购等多维度对比分析。

## 使用方式

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/sku-comparison-analysis')
import compare as sku_compare

# 1. 时间维度对比
result = sku_compare.compare_sku_over_time(
    store_id="416759_1714379448487",
    goods_base_id="34311",
    period_a_from="2026-03-01",
    period_a_to="2026-03-15",
    period_b_from="2026-03-16",
    period_b_to="2026-03-26",
    comparison_label="3月上半月vs下半月"
)

# 2. 多SKU横向对比
result = sku_compare.compare_skus(
    store_id="416759_1714379448487",
    goods_base_ids=["34311", "34312", "34313"],
    from_date="2026-03-01",
    to_date="2026-03-26",
    comparison_focus="sales"
)

# 3. 导购对比分析
result = sku_compare.compare_sku_clerks(
    store_id="416759_1714379448487",
    goods_base_id="34311",
    from_date="2026-03-01",
    to_date="2026-03-26"
)
```

## 分析场景

### 1. 时间维度对比 (compare_sku_over_time)

**适用场景：**
- 促销前后效果评估
- 上市初期vs近期表现
- 季节性波动分析
- 不同月份对比

**输出指标：**
- 销售额变化率
- 销量变化率
- 成交均价变化
- 折扣率变化
- 库存变化
- 深度试用转化率变化

### 2. 横向对比 (compare_skus)

**适用场景：**
- 同品类SKU对比（同款不同色/尺寸）
- 同价格带竞争分析
- TOP商品标杆学习
- 新品vs老款对比

**输出指标：**
- 销售额排名
- 销量排名
- 成交均价排名
- 折扣率排名
- 库存排名

**洞察类型：**
- 销售集中度分析
- 价格差异分析
- 库存风险识别

### 3. 导购对比 (compare_sku_clerks)

**适用场景：**
- 高销售vs低销售导购分析
- 高转化vs低转化导购分析
- 销售技巧标杆学习
- 零销售导购识别

**导购分层：**
- 高销售导购（TOP 30%）
- 低销售导购（后 30%）
- 高转化导购（转化率≥50%）
- 低转化导购（转化率<20%）
- 零销售导购

## 输出结构

### 时间对比输出
```json
{
  "status": "ok",
  "goods_base_id": "34311",
  "comparison_label": "3月上半月vs下半月",
  "period_a": {...},
  "period_b": {...},
  "changes": {
    "sales": {"before": 3000, "after": 5714, "change": 2714, "change_pct": 90.5},
    "qty": {...},
    "avg_price": {...},
    "discount": {...},
    "inventory": {...},
    "deep_trial_trans_rate": {...}
  },
  "insights": [...]
}
```

### 横向对比输出
```json
{
  "status": "ok",
  "total_skus": 3,
  "rankings": {
    "by_sales": [...],
    "by_qty": [...],
    "by_price": [...],
    "by_discount": [...],
    "by_inventory": [...]
  },
  "insights": [...]
}
```

### 导购对比输出
```json
{
  "status": "ok",
  "goods_base_id": "34311",
  "clerk_analysis": {
    "total_clerks": 6,
    "active_clerks": 4,
    "high_sales": [...],
    "low_sales": [...],
    "high_conversion": [...],
    "low_conversion": [...],
    "zero_sales": [...],
    "top_performer": {...},
    "bottom_performer": {...}
  },
  "insights": [...]
}
```

## 洞察类型

| 类型 | 说明 |
|------|------|
| significant_change | 销售大幅变化（>20%） |
| price_strategy | 价格策略调整 |
| inventory | 库存变化 |
| conversion | 转化率变化 |
| concentration | 销售集中度 |
| price_variance | 价格差异 |
| inventory_risk | 库存风险 |
| zero_sales | 零销售问题 |
| best_practice | 标杆实践 |
| improvement | 改进机会 |

## Skill 路径
`~/.openclaw/skills/sku-comparison-analysis/`

## 依赖
- `sku-store-analysis` Skill（用于基础数据解析）
- API 客户端（`workspace-front-door/api_client`）
