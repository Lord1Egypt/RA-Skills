# Phase 1 · Ingest（物料归一 + 角色判定）

输入：接口契约原文。产出：**操作清单**——每个 operation 一行 `name / method / safety(read|write) / inputs[] / outputs[] / doc`，并判定角色。

## §1 归一规则（按物料类型）

| 物料 | 抽取 | grain 线索 |
| --- | --- | --- |
| **REST/OpenAPI** | path+method=op；`parameters`/`requestBody`=inputs；`responses.2xx.schema`=outputs | 响应 `array` → 一行=元素；单对象 → 一行=资源时点 |
| **CLI** | 子命令=op；flags=inputs；`--output`/示例 JSON=outputs；`list/describe/show`=读，`create/update/delete/pay`=写 | `list*`→明细事实；`show*/get*`→快照 |
| **表/DDL/CSV** | 表=事实或维度；列=attribute/measure；PK=business_key 或 degenerate；FK=维度引用 | 唯一键组合=grain |

- 写操作标 `safety: write`；若语义层定位只读，则归 `evidence_boundary`，不建模为事实。
- 证据缺口 → `TODO(verify): <来源>`，列入待确认，不猜。

## §2 角色判定

| 角色 | 判定 |
| --- | --- |
| **fact** | 度量某业务过程/事件（`list*` 明细或可聚合快照） |
| **dimension-lookup** | 翻译/枚举 code 的字典 |

## §3 退出条件

- [ ] 每个 op 在清单中且有 `safety` 标记
- [ ] 每个 op 有角色（fact / dimension-lookup / 归 boundary）
- [ ] 证据缺口均已标 `TODO(verify)`

满足 → 进 Phase 2（`review.md`）。
