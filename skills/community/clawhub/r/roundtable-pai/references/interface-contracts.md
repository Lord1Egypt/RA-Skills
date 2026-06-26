# Interface Contracts

## OpenClaw 对话版总原则

这一版不是命令式工作流，而是**自然语言单入口控制器**：

- 每一轮用户只要发一句话
- 先交给 `scripts/roundtable_controller.py`
- 再由控制器判断这是“新问题 / 选人 / A/B/C/D/E / 用户插话”中的哪一种

## 阶段 1：启动与候选池

### 用户输入

```text
人类的未来会被硅基生命代替吗？
```

或：

```text
启动技能，人类的未来会被硅基生命代替吗？
```

### 用户可见输出

只给用户看：

1. 一句短引导
2. 10 位候选人物
3. 一句请用户选 3 位的话

推荐样式：

```text
选 3 位你最想听的人物，我来组织讨论：

1. 乔布斯（史诗 ★ 3%）：适合讨论差异化和产品判断。
2. 芒格（传说 ★ 15%）：适合拆风险和机会成本。
3. 王阳明（传说 ★ 15%）：适合看决心、动机和执行力。

请直接回复 3 位人物名字或者序号。
```

## 阶段 2：选人并直接开第一轮

### 用户输入

```text
1、3、6
```

或：

```text
刘德华、梅西、岳飞
```

或混用：

```text
1、梅西、岳飞
```

### 输入校验

- 必须正好归一化成 3 位唯一人物
- 3 位都必须来自当前候选池
- 允许名字 / 序号 / alias / directory name 混用，但归一化后必须命中当前候选池
- 如果校验失败，只提示用户重选，不自动补人

### 关键改动

**选完 3 位后，直接进入第一轮。**

不再要求用户额外输入 `/continue`。

## 阶段 3：每轮只前进一步

每一轮结束后，默认给用户这 5 个选项：

```text
---
请选择：
A. 认同[人物A名字]——[一句话概括人物A本轮核心观点]
B. 认同[人物B名字]——[一句话概括人物B本轮核心观点]
C. 认同[人物C名字]——[一句话概括人物C本轮核心观点]
D. 沉默，让讨论继续
E. 我有另外的话要说
```

### 用户输入处理规则

- `A`：认同本轮第一位人物的核心观点，再只进入下一轮
- `B`：认同本轮第二位人物的核心观点，再只进入下一轮
- `C`：认同本轮第三位人物的核心观点，再只进入下一轮
- `D`：沉默，不插话，让讨论继续，再只进入下一轮
- `E`：先等用户说他另外想说的话，再只进入下一轮
- 若用户不回 A/B/C/D/E，而是直接说一句完整的话，默认按 `E` 处理，再只进入下一轮

## Runtime State Contract

所有状态必须存储在 `runtime/roundtable_state.json` 中。

### 必备字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `idle` / `awaiting_participant_pick` / `awaiting_user_choice` / `awaiting_free_speech` / `finished` |
| `question` | string | 当前问题 |
| `candidate_pool` | array | 当前 10 人候选池 |
| `participants` | array | 已选 3 位人物 |
| `current_round` | number | 当前轮次 |
| `max_rounds` | number | 最大轮次（4-7） |
| `user_interventions` | array | 用户干预记录 |
| `finished` | boolean | 是否已结束 |
| `last_user_action` | string | 最近一次有效动作 |
| `pending_user_input_type` | string | 当前在等什么输入 |
| `created_at` | string | 创建时间 |
| `updated_at` | string | 更新时间 |

### 状态流转

```text
idle
  -> awaiting_participant_pick
  -> awaiting_user_choice (直接进入第一轮)
  -> awaiting_user_choice / awaiting_free_speech
  -> finished
```
