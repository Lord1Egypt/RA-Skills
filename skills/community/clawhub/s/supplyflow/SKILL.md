---
name: supplyflow
description: |
  Manufacturing supply chain management toolkit. Handle inventory tracking, supplier evaluation,
  procurement workflows, demand forecasting, risk assessment, cost optimization, and supplier performance.

  **Triggers when user mentions:**
  - Inventory: "库存", "库存管理", "库存追踪", "库存查询", "库存水平", "安全库存", "库存预警"
  - Supplier: "供应商", "供应商评估", "供应商管理", "供应商评分", "供应商绩效", "供应商筛选"
  - Procurement: "采购", "采购订单", "采购计划", "PO", "采购单", "供应商报价"
  - Forecasting: "需求预测", "销量预测", "需求分析", "未来需求", "预测模型"
  - Risk: "供应链风险", "风险评估", "供应中断", "供应链安全", "风险预警"
  - Cost: "成本优化", "采购成本", "降本", "成本分析", "总成本"
  - General: "供应链", "供应链管理", "supply chain", "BOM", "物料管理", "进销存"

  Freemium: Free tier covers inventory tracking, basic supplier evaluation, purchase order templates.
  Paid tier unlocks demand forecasting, risk assessment, cost optimization, inventory optimization, supplier performance reports.
---

# SupplyFlow — 制造业供应链管理

面向制造业的供应链管理工具集，覆盖库存、采购、供应商、预测、风险、成本全链路。

## Freemium 分层

| 层级 | 功能 | 脚本 |
|------|------|------|
| **免费** | 库存追踪 | `scripts/inventory_tracker.py` |
| **免费** | 供应商评估基础 | `scripts/supplier_eval.py` |
| **免费** | 采购订单模板 | `scripts/purchase_order.py` |
| **付费** | 需求预测 | `scripts/demand_forecast.py` |
| **付费** | 供应链风险评估 | `scripts/supply_risk.py` |
| **付费** | 成本优化分析 | `scripts/cost_optimize.py` |
| **付费** | 库存优化建议 | `scripts/inventory_optimize.py` |
| **付费** | 供应商绩效报告 | `scripts/supplier_perf.py` |

## 快速使用

### 免费功能

```bash
# 库存追踪
python3 scripts/inventory_tracker.py --items '[{"name":"螺丝M6","qty":5000,"min":1000,"unit":"个","cost":0.15}]'

# 供应商评估
python3 scripts/supplier_eval.py --suppliers '[{"name":"宏达五金","price_score":8,"quality_score":9,"delivery_score":7,"service_score":6}]'

# 生成采购订单
python3 scripts/purchase_order.py --supplier "宏达五金" --items '[{"name":"螺丝M6","qty":10000,"price":0.12}]'
```

### 付费功能

```bash
# 需求预测（基于历史数据）
python3 scripts/demand_forecast.py --history '[{"month":"2025-01","demand":1200},{"month":"2025-02","demand":1350}]' --months 3

# 供应链风险评估
python3 scripts/supply_risk.py --suppliers '[{"name":"A","country":"CN","single_source":false,"lead_days":7},{"name":"B","country":"US","single_source":true,"lead_days":30}]'

# 成本优化
python3 scripts/cost_optimize.py --items '[{"name":"钢材","monthly_qty":5000,"unit_cost":12,"annual_spend":720000}]'

# 库存优化
python3 scripts/inventory_optimize.py --items '[{"name":"轴承6205","monthly_demand":2000,"lead_days":14,"unit_cost":8.5,"holding_rate":0.25}]'

# 供应商绩效报告
python3 scripts/supplier_perf.py --data '{"suppliers":[{"name":"宏达","otd":95,"defect":0.8,"response_h":4,"quarterly_spend":180000}]}'
```

## 参考文档

- 供应链指标与公式 → `references/metrics.md`
- 行业基准数据 → `references/benchmarks.md`
- 采购订单模板 → `references/po_templates.md`
- 供应商评估标准 → `references/supplier_criteria.md`

## 注意事项

- 所有脚本接受 JSON 格式输入，输出 Markdown 表格 + 分析
- 脚本不依赖外部 API，纯本地计算
- 免费版脚本输出基础分析，付费版提供深度洞察和建议
