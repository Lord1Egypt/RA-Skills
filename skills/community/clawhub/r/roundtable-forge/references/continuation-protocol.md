# 圆桌继续协议

本文件定义圆桌讨论在生成 `synthesis.next_steps` 之后，如何以半自动化方式继续下一议题段。

## 核心原则

`next_steps` 是建议性的，不自动执行。只有当用户明确同意继续某个方向时，Conductor 才启动继续流程。

## 触发条件

满足以下全部条件时，Conductor 应提议继续：

1. 当前议题段已完成并写入 `synthesis`。
2. `synthesis.next_steps` 非空。
3. 用户未明确说“结束”“到此为止”或类似表达。
4. `metadata.completed` 不为 `true`。

## 继续提议方式

Conductor 向用户展示：

- 本轮合成的核心结论（1–2 句话）。
- `next_steps` 列表，编号呈现。
- 一个明确的邀请：
  - “是否继续深入以上某个方向？”
  - “你希望我从哪个方向继续？”
  - “或者你有新的方向？”

## 用户选择处理

### 选择某个 next_step

1. Conductor 将该 `next_step` 转写为一个新的 `focus_question`。
2. Conductor 评估现有角色阵容是否足够覆盖新 focus question：
   - 如果足够，复用现有角色。
   - 如果不够，按 [character-selection-guide.md](character-selection-guide.md) 增加 1–2 个新角色，并写入 Memory 的 `characters` 列表。
3. Conductor 在 Memory 中追加新的议题段（`round_number` 递增）。
4. 新议题段运行时，所有角色应能看到之前的 `synthesis` 和本轮新 `focus_question`。

### 用户提出新方向

按 [user-interjection-protocol.md](user-interjection-protocol.md) 的 `topic_pivot` 处理，但尽量在同一 Memory 文件内延续，而不是新建 Memory。

### 用户拒绝继续

1. Conductor 将 `metadata.completed` 设为 `true`，并记录 `metadata.completed_at`。
2. 渲染最终 Markdown 报告。
3. 告知用户 Memory 文件路径，供日后手动继续。

## Memory 记录格式

在 `interjections` 数组中追加一条 `continuation` 记录：

```json
{
  "interjection_id": "cont-001",
  "round_number": 2,
  "type": "continuation",
  "trigger": "next_step_selection",
  "raw_text": "用户选择继续的方向",
  "resolved_into": "new-focus-question:{focus_question}",
  "added_seats": ["new_character_id"]
}
```

## 自动转写 next_step 为 focus_question 的规则

| next_step 类型 | 转写方式 |
|----------------|----------|
| 邀请某领域专家 | 以该专家视角重新审视核心问题 |
| 设计具体方案 | 以“如何设计……”开头的聚焦问题 |
| 深入讨论某概念 | 以“……的本质/边界是什么”开头 |
| 跨行业比较 | 以“同样的逻辑在……行业是否成立”开头 |

## 频率与深度控制

- 同一 Memory 文件内建议最多连续继续 2 次，避免讨论无限发散。
- 每次继续后，Conductor 应重新评估 `synthesis`，而不是简单累加。
- 如果用户连续两次选择继续，第三次时应更主动地总结并询问是否收尾。

## 与渲染脚本的协作

渲染 Markdown 报告时，应在“如何继续”部分列出 `next_steps`，并说明：

- 这些是 Conductor 建议的后续方向。
- 用户可以基于 Memory 文件继续，或回复“继续方向 X”。
