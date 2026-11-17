# Conductor 主动邀请用户发言协议

本文件定义圆桌讨论中，Conductor 在哪些节点应主动暂停并向用户提问，以及如何处理用户的回复。

## 为什么需要主动邀请

圆桌不是角色之间的自说自话，用户的视角、经历与价值选择本身就是讨论的一部分。Conductor 应在关键节点邀请用户入场，避免讨论滑入纯粹的 AI 推演。

## 触发条件

满足以下任一条件时，Conductor 应主动邀请用户发言：

1. **价值分叉点**：角色们在核心立场上形成不可调和的分歧，需要用户选择更倾向哪一方，或提出自己的立场。
2. **经验缺口**：讨论涉及用户的具体行业、职业或经历，而角色们的推演缺乏第一手信息。
3. **抽象升级**：讨论从具体问题上升到哲学/制度层面，需要用户确认是否继续深入，还是拉回地面。
4. **角色直接向用户提问**：某位角色明确说“我想听听问题提出者的看法”。
5. **关键决策点**：例如是否增加新席位、是否换题、是否结束当前议题段。

> **trigger code 映射**：上述五种条件对应 Memory 中 `interjections[].trigger` 的标准枚举值，写入时必须严格使用这些 token，[scripts/lint_memory.py](../scripts/lint_memory.py) 会拒绝其它取值：
>
> | 场景 | trigger code |
> |------|-------------|
> | 价值分叉点 | `value_fork` |
> | 经验缺口 | `experience_gap` |
> | 抽象升级 | `abstraction_escalation` |
> | 角色直接向用户提问 | `character_question` |
> | 关键决策点 | `key_decision` |

## 邀请方式

Conductor 的提问应满足：

- **具体**：不要问“你怎么看”，而应给出一个有边界的问题。
- **可选**：尽量给出 2–4 个明确选项，也允许用户自由回答。
- **单选或多选声明**：若允许多选，应在邀请文本中说明，并在 Memory 中记录 `selection_mode: multiple`。
- **与当前议题相关**：问题必须直接服务于正在讨论的 focus question。
- **记录到 Memory**：每次主动邀请都必须写入 Memory，作为后续继续的事实源。

## Memory 记录格式

在 `interjections` 数组中追加一条 `conductor_invitation` 记录：

```json
{
  "interjection_id": "ci-001",
  "round_number": 1,
  "type": "conductor_invitation",
  "trigger": "value_fork",
  "raw_text": "Conductor 提出的问题",
  "selection_mode": "single",
  "options": ["选项A", "选项B", "选项C"],
  "resolved_into": "awaiting-user-response"
}
```

`selection_mode` 取值为 `single`（默认）或 `multiple`。

当用户回复后，更新该记录：

```json
{
  "interjection_id": "ci-001",
  "round_number": 1,
  "type": "conductor_invitation",
  "trigger": "value_fork",
  "raw_text": "Conductor 提出的问题",
  "selection_mode": "single",
  "options": ["选项A", "选项B", "选项C"],
  "user_response": "用户的原始回复",
  "resolved_into": "user-chose-option-B"
}
```

若用户选择多个选项，例如“B, C”：

```json
{
  "interjection_id": "ci-001",
  "round_number": 1,
  "type": "conductor_invitation",
  "trigger": "value_fork",
  "raw_text": "Conductor 提出的问题",
  "selection_mode": "multiple",
  "options": ["选项A", "选项B", "选项C"],
  "user_response": "B, C",
  "resolved_into": "user-chose-options-B-C"
}
```

若用户自由回答，Conductor 应将其摘要写入 `resolved_into`：

```json
{
  "interjection_id": "ci-001",
  "round_number": 1,
  "type": "conductor_invitation",
  "trigger": "value_fork",
  "raw_text": "Conductor 提出的问题",
  "selection_mode": "single",
  "options": ["选项A", "选项B", "选项C"],
  "user_response": "用户的自由回答",
  "resolved_into": "user-answered-openly:{summary}"
}
```

## 处理用户回复

1. Conductor 解析用户回复，将其归类为：单选、多选、补充信息、提出新方向、拒绝回答。
2. 若为多选，Conductor 把多个选项共同作为下一段的 focus question 输入；若选项之间跨度较大，可拆分为先后两个议题段，或生成一个能同时覆盖它们的更高层 focus question。
3. 如果是选择选项或补充信息，Conductor 将其作为上下文，让下一轮角色发言时参考。
4. 如果是提出新方向，Conductor 按 [user-interjection-protocol.md](user-interjection-protocol.md) 的 `topic_pivot` 处理。
5. 如果用户拒绝回答，Conductor 记录 `resolved_into: user-declined`，并继续原讨论方向。
6. 如果用户自由回答，Conductor 先提炼其立场为 1–2 句话，写入 `resolved_into` 的 `user-answered-openly:{summary}` 格式，再让角色回应。

## 频率控制

- 每个议题段内，Conductor 主动邀请不超过 1 次，避免打断讨论节奏。
- 优先在议题段末尾、合成之前邀请用户，让用户有机会影响合成方向。

## 安全原则

- Conductor 保持中立，不在邀请中暗示“正确答案”。
- 用户回复不替代角色发言，而是作为补充上下文。
- 所有主动邀请和回复都写入 Memory，确保透明与可审计。
