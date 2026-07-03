# Response Presentation

Use this reference after Runtime returns a result, or when the user asks for product help, design advice, memory, recommendations, diagnostics, or a home summary.

Presentation never changes facts. Base every status, count, state, target, and warning on Runtime evidence or clearly label it as a proposal. Do not show full JSON unless the user asks for technical detail.

## General Rules

- Match the user's tone, urgency, and context. Keep ordinary replies short, but make result surfaces easy to scan.
- Prefer Markdown tables and compact cards in chat. A card is a short titled block with fields such as `状态`, `对象`, `位置`, `结果`, `验证`, and `下一步`.
- Avoid decorative language that hides the actual result. Mention partial failures, skipped items, and required follow-up plainly.
- Do not invent icons, images, state, current values, device capabilities, or product facts.
- When there are many entities, summarize first, then table. When there is one entity, use a focused card.

## Response Types

| Situation | Response shape |
| --- | --- |
| Entity list | Entity list table with type, room, status, and the most relevant control or management field. Start with total count and active filters. |
| Single entity | Entity card with name, type, room, current state if read, supported actions if returned, and one concise next action. |
| Home list or home detail | Home dashboard with cards for selected home, rooms, devices, groups, scenes, automations, warnings, and current-home context. |
| Direct control or scene execution success | Notification card with target, requested value, actual Runtime status, verification evidence, and any partial failures. |
| Create, update, rename, move, enable, disable, or delete | Result card plus a before/after comparison table for changed fields when both sides are available. |
| Full lighting design import | New home dashboard with home name, selected home context, room cards, device-slot/product counts, groups, scenes, automations, warnings, and partial failures. Say when Runtime selected the new home for later turns. |
| Recommendation accepted | Preference-aware confirmation card that connects the accepted choice to saved memory or the user's stated goal without overstating certainty. |
| Memory remembered or forgotten | Memory change card with saved/removed preference, scope, evidence phrase, and future effect. If Runtime did not save it, say so. |
| Product information or help | Product help surface with short answer first, then parameter table, resource table, constraints, and suggested next question when useful. |
| Diagnostics or errors | Diagnostic card with symptom, Runtime status, evidence, likely cause only when known, and the smallest safe next action. |

## Tables

Use tables when the user asks "有哪些", "列一下", "全部", "当前有什么", "对比", or when more than two entities are returned.

Recommended columns:

- Entity list: `名称`, `类型`, `房间/范围`, `状态`, `可做的事`.
- Scene/automation list: `名称`, `范围`, `触发/动作摘要`, `状态`, `备注`.
- Product help: `参数`, `值`, `含义`, `适用场景`.
- Change comparison: `项目`, `变更前`, `变更后`, `验证`.

Keep tables narrow. If a field is long, summarize it in the table and add a short note below.

## Cards

Use a card when the user asks about one target, one completed operation, one memory change, or one recommendation decision.

Suggested card shape:

```text
**结果**
状态：已完成
对象：客厅主灯
结果：已调到 60% 亮度
验证：Runtime 返回 success，并完成状态读回
```

For failures, keep the same shape and replace `结果` with the exact safe summary:

```text
**未完成**
对象：客厅主灯
原因：Runtime 要求先明确目标
下一步：请选择客厅里的哪一盏灯
```

## Home Dashboard

Use a home dashboard when the user asks about a home, current home, newly imported home, or whole-home design result.

Include:

- Home card: name, selected/current context, region/profile only when useful.
- Summary cards: room count, device count, group count, scene count, automation count.
- Room table: room name, device/group/scene highlights.
- Alerts: offline entities, partial imports, skipped automations, missing trigger hardware, or ambiguity.
- Next action: one useful action, not a menu of every capability.

For a newly imported lighting design, explicitly say whether the new home is now the selected home for later operations.

## Product Help

When answering product questions, choose the shape that best matches the user:

- Quick buying or selection question: short recommendation plus product table.
- Manual-style question: step-by-step help, constraints, and troubleshooting table.
- Parameter question: parameter table first, then explanation.
- Product comparison: comparison table with tradeoffs and a final fit judgment.

Use official Runtime/catalog evidence when available. If evidence is insufficient, say what is known and what still needs lookup.
