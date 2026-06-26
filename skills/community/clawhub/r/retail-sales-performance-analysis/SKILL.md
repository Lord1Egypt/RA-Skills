---
name: retail-sales-performance-analysis
description: |
  门店销售业绩环比分析工具。支持门店/导购业绩同比分析（本期 vs 上期），识别业绩波动原因，量化归因，输出诊断结论和改进建议。
  
  使用场景：
  1. 门店整体业绩分析（销售额、订单数、客单价、连带率）
  2. 导购个人业绩分析（排名、业绩占比、能力雷达图）
  3. 多门店/多导购对比分析
  4. 业绩波动归因（订单贡献 vs 客单贡献）
  5. 异常识别与风险预警
  
  触发条件：
  - 用户询问业绩（如"本周业绩怎么样"）
  - 用户分析业绩下滑原因（如"为什么销售下降"）
  - 用户对比业绩（如"比上月业绩如何"）
  - 用户需要业绩诊断（如"业绩达标了吗"）
---

# 销售业绩环比分析 Skill

## 技能名称
`sales-performance-analysis`

## 功能描述
分析门店或导购的销售业绩，支持同比（本期 vs 上期）分析，识别业绩波动原因，输出诊断结论和改进建议。

## 适用范围
- 门店整体业绩分析
- 导购个人业绩分析
- 多门店/多导购对比分析

## 输入参数

```json
{
  "subject_type": "store|clerk",
  "subject_id": "门店ID或导购ID",
  "subject_name": "门店名称或导购姓名",
  "time_window": {
    "from": "YYYY-MM-DD",
    "to": "YYYY-MM-DD"
  },
  "compare_mode": "period_over_period",
  "metrics": ["net_money", "effective_order_count", "customer_unit_price", "attach_qty_ratio"]
}
```

## 核心指标

### 财务指标
| 指标编码 | 指标名称 | 计算逻辑 | 用途 |
|----------|----------|----------|------|
| `net_money` | 销售总额 | 直接取值 | 核心收入指标 |
| `effective_order_count` | 有效订单数 | 直接取值 | 成交频次 |
| `customer_unit_price` | 客单价 | 销售总额 / 订单数 | 单笔价值 |
| `effective_qty_count` | 有效销量 | 直接取值 | 商品件数 |
| `avg_discount` | 平均折扣 | 直接取值 | 促销力度 |

### 效率指标
| 指标编码 | 指标名称 | 计算逻辑 | 用途 |
|----------|----------|----------|------|
| `attach_qty_ratio` | 连带率 | 销量 / 订单数 | 连带销售能力 |
| `piece_price` | 件单价 | 销售总额 / 销量 | 商品单价水平 |

### 会员指标
| 指标编码 | 指标名称 | 计算逻辑 | 用途 |
|----------|----------|----------|------|
| `new_customer_count` | 新增会员数 | 直接取值 | 新客获取 |
| `new_member_purchase_share` | 新会员消费占比 | 直接取值 | 新客贡献 |

## 数据来源

### API 接口
```
GET /api/v1/store/dashboard/bi?storeId={store_id}&fromDate={from}&toDate={to}
```

### 数据字段映射
| API 字段 | 指标编码 | 说明 |
|----------|----------|------|
| `metrics.net_money` | `net_money` | 销售总额 |
| `metrics.effective_order_count` | `effective_order_count` | 有效订单数 |
| `metrics.customer_unit_price` | `customer_unit_price` | 客单价 |
| `metrics.attach_qty_ratio` | `attach_qty_ratio` | 连带率 |
| `metrics.new_customer_count` | `new_customer_count` | 新增会员数 |
| `effectiveQtyCount` | `effective_qty_count` | 有效销量 |
| `avgDiscount` | `avg_discount` | 平均折扣 |

### 环比字段
| 本期字段 | 上期字段 | 反推公式 |
|----------|----------|----------|
| `metricsValue` | `linkRelativeValue` | 直接使用 |
| `metricsValue` | `linkRelativeRate` + `trend` | 反推：上期 = 本期 / (1 ± 变化率) |

## 分析逻辑

### 1. 业绩拆解
```
销售额 = 客单价 × 订单数
       = (件单价 × 连带率) × 订单数
       = 件单价 × 销量
```

### 2. 波动归因
计算各指标对销售额波动的贡献度：
```
销售额变化 = 订单数变化贡献 + 客单价变化贡献

订单数变化贡献 = (本期订单数 - 上期订单数) × 上期客单价
客单价变化贡献 = (本期客单价 - 上期客单价) × 本期订单数
```

### 3. 异常识别规则
| 异常类型 | 判断条件 | 严重程度 |
|----------|----------|----------|
| 销售大幅下滑 | 环比下降 > 30% | 🔴 高 |
| 销售下滑 | 环比下降 10%-30% | 🟡 中 |
| 新客获取困难 | 新客环比下降 > 40% | 🔴 高 |
| 连带率偏低 | 连带率 < 1.3 | 🟡 中 |
| 折扣率偏高 | 平均折扣 < 0.8 | 🟡 中 |

## 输出格式

```json
{
  "status": "ok",
  "subject_type": "store|clerk",
  "subject_id": "...",
  "subject_name": "...",
  "analysis_period": {
    "current": { "from": "...", "to": "..." },
    "previous": { "from": "...", "to": "..." }
  },
  "core_metrics": {
    "net_money": { "current": 0, "previous": 0, "change_pct": 0, "trend": "up|down|flat" },
    "effective_order_count": { ... },
    "customer_unit_price": { ... },
    "attach_qty_ratio": { ... }
  },
  "attribution": {
    "order_contribution": 0,
    "atv_contribution": 0,
    "primary_driver": "order|atv"
  },
  "findings": [
    {
      "title": "...",
      "type": "fact|anomaly|hypothesis|recommendation",
      "metric": "...",
      "evidence": "...",
      "confidence": "high|medium|low",
      "implication": "..."
    }
  ],
  "risks": [],
  "recommendations": []
}
```

## 使用示例

### 门店业绩分析
```python
from skills.sales_performance_analysis import analyze

result = analyze({
    "subject_type": "store",
    "subject_id": "416759_1714379448487",
    "subject_name": "正义路60号店",
    "time_window": { "from": "2026-03-01", "to": "2026-03-25" }
})
```

### 导购业绩分析
```python
result = analyze({
    "subject_type": "clerk",
    "subject_id": "clerk_001",
    "subject_name": "李翠",
    "time_window": { "from": "2026-03-01", "to": "2026-03-25" }
})
```

## 依赖
- `api_client.get_copilot_data()` - 数据获取
- `~/.openclaw/workspace-front-door/` - API 客户端路径

## 版本
v1.0.0 - 支持门店和导购业绩同比分析
