# Phase 2 · Review（决策建模 + HTML 工作台 + 迭代）

输入：Phase 1 操作清单。产出：用户显式批准的建模决策集与
`amendments.md`。流程：收集 → 建模 → 评审 → 修订，直到通过。

## §1 决策本体

不要把结论清单冒充决策界面。按以下概念建模：

- `brief`：用户目标、交付物、范围、证据边界。
- `object`：事实、维度、度量或路由；只负责归组与共享证据。
- `decision`：对象上的一个原子问题，如 grain 或 additivity。
- `option`：同一问题下互斥的候选方案。
- `relation`：决策间的依赖、冲突或权衡。
- `constraint`：grain-first、evidence-only 等全局硬规则。
- `evidence`：可定位的接口字段、文档或 DDL 出处。
- `basis`：`explicit | inferred | missing`，描述证据基础。
- `confidence`：`high | medium | low`，描述推荐可靠度。
- `status`：`pending | approved | rejected | blocked`，只描述用户决策状态。
- `risk`：选择错误的后果；`action`：用户的确认、选择、修正、补证或拒绝。

`basis`、`confidence`、`status` 不得混用。用户批准只改变状态，不提高
证据质量或置信度。

## §2 收集顺序

1. **Facts & Grain**：grain 必须可证伪，如「`items[]` 每元素一条」。
   请求头与明细行建 parent/child facts。grain 不明时先给 2–4 个候选。
2. **Dimensions**：确认 `kind`、`business_key`、`source_operations`、
   `attributes`、`parent_dimension`。同义维度复用；退化键留在 fact。
3. **Measures**：确认 `additive | semi_additive | non_additive` 与单位口径。
   枚举值仍归契约层。
4. **Routing & Boundary**：确认 `entry_points` 与不能回答的问题。

只在改变模型的 never-assume 缺口处一次一问。其余不确定项进入工作台，
不得以默认值静默通过。

### 固定决策指导

工作台在四个分区标题旁提供固定问号提示。提示属于模板规范，不由 agent
随项目改写，也不新增 action 或放宽批准门禁。每条提示都用白话解释术语，
给出证据判据、YAGNI 边界与一个短例：

- **事实**：事实记录可重复发生的业务事件；grain 说明一条记录代表什么。
  只依据数组元素、主键/唯一键或明确接口语义判断。只有独立事件、独立聚合
  或真实一对多关系才拆新事实，不因「以后可能分析」提前拆分。例如订单头与
  订单行按真实一对多关系分开，订单状态通常不是独立事实。
- **维度**：维度描述「谁、什么、哪里」，必须有稳定 business key 和可信
  来源。跨事实身份与口径一致才做 conformed；上级实体可独立维护或复用才
  snowflake；只有交易编号且无独立描述/查询来源时留在事实中（degenerate）。
  不为潜在复用提前拆维，枚举值仍留在契约层。
- **度量**：度量必须回答当前分析问题，并明确单位、币种/口径和聚合范围。
  可跨相关维度相加是 additive；余额、库存等快照通常 semi-additive；比率、
  均值、去重数 non-additive。优先保留可重算基础量；无明确用途或来源证据
  时不预建度量。
- **路由与边界**：按事实、维度、度量、时间和范围选择能直接提供证据的最小
  entry point。只有来源能力明确且输出字段足够才建立路由；名称相似、相邻
  接口或「以后可能用到」都不是依据。不能由现有证据回答的内容明确写入边界。

问号提示必须支持鼠标悬停、键盘聚焦与点击显示，并在移开、失焦或按
`Escape` 后关闭；不得依赖仅 hover 的交互。

## §3 紧凑模型

不要手写报告 HTML。生成 JSON，替换 `assets/review-template.html` 中的
`/*__MODEL_JSON__*/`，写入 `$TMPDIR/semantic-review-<timestamp>.html`。
模板离线自足，无 CDN、无网络。

```json
{"meta":{"title":"订单语义评审","generated_at":"<ISO>","iteration":1},
"brief":{"goal":"建立可聚合订单语义层","deliverable":"OKF v0.1",
"scope":"订单与门店","boundary":"不含退款、履约"},
"constraints":["grain-first：grain 未决时阻塞依赖项","evidence-only：不臆造字段或值"],
"objects":[{"id":"fact/order","kind":"fact","title":"Order",
"evidence":[{"id":"e1","source":"ListOrders.orders[]"}],
"decisions":[{"id":"grain","question":"订单事实一行代表什么？",
"impact":"决定维度挂接与度量可加性","risk":"错误 grain 会重复聚合金额",
"basis":"inferred","confidence":"medium","status":"pending","priority":"blocking",
"value":"orders[] 每元素一条","options":[
{"id":"order","label":"每订单一条","when":"orders[] 元素是订单头",
"benefit":"直接聚合订单金额","cost":"不能分析行项目","risk":"隐藏明细粒度",
"evidence":["e1"],"recommended":true,"reason":"响应直接返回订单数组"},
{"id":"line","label":"每订单行一条","when":"元素实际代表行项目",
"benefit":"支持商品分析","cost":"需建立子事实","risk":"会重复订单级金额",
"evidence":["e1"],"recommended":false,"reason":"仅在元素含行项目时成立"}],
"relations":[]}]}]}
```

### 原子性与候选规则

- 一个 `decision` 只回答一个问题；引用格式为 `<object-id>#<decision-id>`。
- `question` 必须点明正在决定什么；`impact` 必须解释为何现在决定。
- `basis=explicit` 且 `confidence=high` 可只给 `value`，走轻量确认。
- 其他决策必须给 2–4 个互斥 `options`，且恰有一个 `recommended=true`。
- 每个 option 必须独立包含 `when / benefit / cost / risk / evidence /
  recommended / reason`；值保持一句话，证据只引用对象内 evidence ID。
- `basis=missing` 不得标 `confidence=high`。`TODO(verify)` 写入 evidence。

### 关系与优先级

- `priority` 仅为 `blocking | high | normal`。
- relation 结构为
  `{"type":"depends_on|conflicts_with|tradeoff_with","target":"...","note":"..."}`。
- `depends_on` 目标未批准时，当前决策硬阻塞且不参与本轮批准。
- 冲突与权衡必须双向可见；每条关系必须有 `note`。
- 出报告前拒绝不存在的 target、self-reference 与循环依赖。

## §4 用户行动与导出

所有决策初始 `pending`，禁止默认批准。模板提供：

- `confirm`：接受无候选项的当前值。
- `select`：选择一个候选；选非推荐项必须说明理由。
- `correct`：提交候选外的明确替代值与理由。
- `supplement`：补充证据或约束，不自动改变结论。
- `reject`：否定当前问题定义（framing）；不得自动删除对象，必须修订后重出报告。

可主动批量确认 `basis=explicit + confidence=high` 的轻量项。仍有 pending、
blocked、correct、supplement 或 reject 时只能导出草稿：

```json
{"decisions":[
{"id":"fact/order#grain","action":"select","option":"line","reason":"接口说明元素为行项目"},
{"id":"dim/currency#source","action":"supplement","value":"GET /v1/currencies"}
],"approved":false}
```

全部可行动决策均为 `confirm | select` 后，用户才能显式“批准并导出”，产生
`approved:true`。复制失败时显示可全选文本并下载 `decisions.json`；支持导入
上轮 JSON。

## §5 Amendments 迭代

1. 将每项反馈追加到报告同目录的 `amendments.md`：
   `日期 + 决策 ID / 原值 → 新值 / 理由`。
2. 应用 correct、supplement、reject；reject 只触发重构，不隐式删对象。
3. `iteration +1` 后重出报告。证据冲突且无法机械裁决时，一次只问一个
   blocking question。
4. Phase 3 将 `amendments.md` 复制到输出目录；重跑时复用已确认决策。

## §6 出报告前检查与退出门禁

- [ ] brief 明确目标、交付物、范围与边界。
- [ ] 每个对象有证据，每个 decision 原子且有 question、impact、risk。
- [ ] 低证据/低置信决策有完整、互斥、可解释的候选。
- [ ] 关系 target 有效，依赖无环，阻塞状态可计算。
- [ ] 每个事实有 grain；维度有 kind/business_key；度量有 additivity。

出报告后必须停下。只有收到 `approved:true`，且无 unresolved/blocked
决策与 never-assume 缺口，才能进入 Phase 3；不得替用户批准。
