# Worked Example（Ingest → Review → Emit → Verify）

最小端到端：2 个 REST 操作走完四个阶段，默认产物 OKF bundle，另附 YAML 节选。示范节奏，非模板填空。

## §0 输入物料（REST）

```text
GET /v1/orders?store_id&from&to  →  200: { orders: [ { order_id, store_id, placed_at, total_amount, currency, line_count } ] }
GET /v1/stores                   →  200: { stores: [ { store_id, store_name, region } ] }
```

## §1 Phase 1 · Ingest → 操作清单 + 角色

| name | method | safety | inputs | outputs(数组) | 角色 |
| --- | --- | --- | --- | --- | --- |
| ListOrders | GET | read | store_id, from, to | orders[] | fact（业务过程：下单） |
| ListStores | GET | read | — | stores[] | dimension-lookup（门店字典） |

## §2 Phase 2 · Review — 决策工作台（示意）

生成紧凑 model JSON，注入壳模板出 HTML 工作台（规范见 `review.md` §3）：

> **SalesOrder** · Fact
>
> 决策：订单事实一行代表什么？
>
> 为何决定：grain 决定维度挂接与金额可加性
>
> 推荐：`orders[]` 每元素一条；证据 `ListOrders.orders[]`
>
> 候选：每订单一条 / 每订单行一条（各自展示适用条件、收益、代价、风险、
> 证据与推荐理由）

grain 未批准时，依赖它的维度与度量决定硬阻塞。所有决定初始 pending；
用户可确认、选择、修正、补证或拒绝问题 framing。草稿回传如：

```json
{"decisions":[
  {"id":"dim/currency#source","action":"supplement","value":"GET /v1/currencies"}
],"approved":false}
```

写入 `amendments.md`、应用并重出报告；只有全部决定显式确认后，
`{"decisions":[...],"approved":true}` 才允许进入 Phase 3。

## §3 Phase 3 · Emit — OKF（默认）

`facts/sales_order.md`：

```markdown
---
type: Semantic Fact
title: Sales Order
description: 一笔订单（ListOrders.orders[] 的一个元素）。
role: primary
grain: orders[] 每个元素一条
tags: [sales]
timestamp: 2026-06-29T00:00:00Z
---

# Grain
orders[] 每个元素一条记录（一笔订单）。

# Dimensions
[Store](/dimensions/store.md) · [Currency](/dimensions/currency.md) · [Date](/dimensions/date.md)

# Schema
| field | type | required | dimension |
| --- | --- | --- | --- |
| store_id | string | true | Store |

# Citations
[1] [ListOrders 文档](<doc>)
```

`dimensions/store.md`、`metrics/total_amount.md` 同法（Metric body 含 additivity=additive、unit=currency）；根 `index.md`（含 `# Entry Points`：`sales_orders → [Sales Order]`）与子目录 index 结构见 `emit-okf.md` §4。

## §4 Phase 3 · Emit — repo-YAML（可选，节选）

```yaml
# sales-model.yml
name: SalesModel
type: semantic_ontology
shared_dimensions_file: shared-dimensions.yml
facts:
  - name: SalesOrder
    role: primary
    grain: orders[] 每个元素一条（一笔订单）
    degenerate_dimensions: [order_id]
    dimensions: [Dim_Store, Dim_Currency, Dim_Date]
    measures:
      - { name: total_amount, additivity: additive, unit: currency }
      - { name: line_count,   additivity: additive, unit: count }
evidence_boundary:
  - 仅下单事实；退款/履约/库存超出本对象。
```

catalog（薄路由）与 shared-dimensions 结构见 `emit-yaml.md` §1–§2。

## §5 Phase 4 · Verify

- verify §1 结构：catalog 1 个 ✓；SalesOrder 有 grain ✓；Dim_Currency `source_operations`=`TODO(verify)` ⚠ → 交付说明点名。
- verify §3 OKF：所有 concept 有 `type` ✓；根 index 仅 `okf_version` ✓。
