---
name: self-governor
description: LLM 通用内部自裁决技能。在关键节点判断"当前这一层最优的下一步动作是什么"，再让主链继续执行。触发条件：(1) 路径分叉时——多个可行方案且无明显优先级；(2) 高代价动作前——搜索/生成/发布等消耗军费或不可逆操作；(3) 连续两步无明显增益时——进展停滞、输出质量未提升。禁止：改写主任务、输出并列动作、长篇规划、变成审批器、连续两轮要求补资料。适用于战略分析/搜索补全/研究/代码/多步工作流等agent。
---

# Self-Governor

在关键决策节点插入一个轻量自裁决层，输出**一个动作**，让主链继续。

## 核心闭环

```
Goal → Gap → Action → Update → (下一轮)
```

不是复杂协议，是一个**关键节点微循环**。

## 触发时机

以下三种信号出现时，主链立即插入一次裁决：

1. **路径分叉** — 2+ 可行方向，无明显优先级
2. **高代价动作前** — 不可逆操作或稀缺资源消耗
3. **连续两步无明显增益** — stage_goal 完成度未提升

详见 [references/triggers.md](references/triggers.md)

## 输入输出

详见 [references/input-output.md](references/input-output.md)

### 最小输入（3字段）
- `stage_goal` — 当前阶段目标
- `current_gap` — 最大缺口
- `available_actions` — 候选动作子集

### 最小输出
- `next_action` — 唯一动作（必填）
- `reason` — 一句话（必填，≤30字）
- `fallback_if_fail` — 失败兜底（可选）

### Update 环
**主链强制义务**: 每次 self-governor 输出动作并执行后，主链**必须**在下一步开始前完成 Update 回写。不回写则触发器3（连续无增益）将失效。

回写字段: `goal_achievement` / `gap_change` / `actions_taken` / `total_steps_in_stage`

详见 [references/input-output.md](references/input-output.md)

## 固定动作集合

6 个动作，详见 [references/actions.md](references/actions.md)：

`anchor` · `time_bind` · `search` · `clean` · `synthesize` · `degrade_continue`

## 禁止项

- ❌ 改写主任务（你是裁决器，不是任务规划器）
- ❌ 输出多个并列动作（只返回一个）
- ❌ 生成长篇规划（reason 一句话）
- ❌ 变成审批器（不要"建议暂停等待确认"）
- ❌ 连续两轮默认要求补资料（最多一轮，第二轮必须 degrade_continue）

## 反官僚原则

- ✅ 默认选择动作，不默认停住
- ✅ 每次只返回一个动作
- ✅ reason 保持一句话
- ✅ 条件不理想时，优先 `degrade_continue` 而非空转

## 不做什么

- 不写业务内容
- 不给最终结论
- 不替代主链分析
- 不充当审批器
- 不做多动作排序/评分/长链规划/状态机

**它只负责：先停一下，再选一步。**

## 示例

详见 [references/examples.md](references/examples.md)
