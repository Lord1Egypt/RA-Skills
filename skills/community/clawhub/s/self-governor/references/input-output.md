# Input-Output Reference

## 最小输入

三字段固定结构，不做扩展：

```json
{
  "stage_goal": "当前阶段要完成的目标",
  "current_gap": "离目标的最大缺口",
  "available_actions": ["从6个固定动作中选取"]
}
```

### 字段规格

| 字段 | 类型 | 约束 | 示例 |
|------|------|------|------|
| `stage_goal` | string | ≤50字，描述当前阶段目标 | "形成可下传最小合同" |
| `current_gap` | string | ≤80字，描述最大缺口 | "证据不足，无法稳定支撑主判断" |
| `available_actions` | string[] | 从6个固定动作中选取子集 | `["search", "synthesize", "degrade_continue"]` |

### 规则
- `available_actions` 必须是固定集合的子集，不得发明新动作
- 主链可根据上下文裁剪可用动作（如"不需要搜索"则不传入 search）
- 最少传入 2 个候选动作，最多传入 6 个

---

## 最小输出

两个固定字段 + 一个可选字段：

```json
{
  "next_action": "search",
  "reason": "最大缺口是证据不足，应先补材料再收束",
  "fallback_if_fail": "degrade_continue"
}
```

### 字段规格

| 字段 | 类型 | 约束 | 示例 |
|------|------|------|------|
| `next_action` | string | 必填，6个固定动作之一 | "search" |
| `reason` | string | 必填，≤30字，一句话 | "关键数据点缺失，定向搜索一次" |
| `fallback_if_fail` | string | 可选，6个固定动作之一 | "degrade_continue" |

### 规则
- `next_action` 必须且只能返回一个
- `reason` 禁止超过一句话，禁止分点展开
- `fallback_if_fail` 仅在 next_action 的执行依赖外部不稳定条件时填写（如：IP白名单不确定、网络超时风险、第三方服务不可控）。不需要量化概率，只需判断"外部条件是否在 self-governor 控制范围内"。

---

## Update 环

动作执行后，主链必须回写状态更新，供下一轮裁决使用。

### 回写格式

```json
{
  "goal_achievement": 70,
  "gap_change": "缺口缩小：已获取3份数据源",
  "actions_taken": ["search"],
  "total_steps_in_stage": 4
}
```

### 字段规格

| 字段 | 类型 | 说明 |
|------|------|------|
| `goal_achievement` | int | 0-100，当前阶段目标完成百分比 |
| `gap_change` | string | ≤50字，缺口的变化描述 |
| `actions_taken` | string[] | 本阶段内执行过的**去重**动作记录，如 `["search","synthesize"]`。仅记录本 stage 内已执行的不同动作，重复动作只记一次。 |
| `total_steps_in_stage` | int | 本阶段已消耗的总步数 |

### Update 的作用
- **增量检测**: 对比前后 `goal_achievement`，判断是否有增益
- **循环防护**: `total_steps_in_stage` + `actions_taken` 用于检测空转
- **触发器 3 判定**: 连续两步 `goal_achievement` 未变化 → 触发

### Update 不做什么
- ❌ 不改写 stage_goal（除非主链明确重定义）
- ❌ 不生成新动作
- ❌ 不输出分析报告
