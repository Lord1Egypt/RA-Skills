# Judge Agent Prompt Template

## Overview

This file contains the prompt template for SharpInput's independent Judge Agent.
The main agent reads this template, fills in the placeholders, and passes the
complete prompt to the Agent tool.

**When to use**: Level 3 (Deep Adversarial) — every time, no exceptions.

**Placeholders** (filled in by the main agent at call time):
- `{{ORIGINAL_QUESTION}}` — The user's raw input (before any SharpInput processing)
- `{{PATH_COUNT}}` — Number of paths (2 or 3)
- `{{PATH_A_LABEL}}`, `{{PATH_B_LABEL}}`, `{{PATH_C_LABEL}}` — Angle tags for each path
- `{{PATH_A_QUESTION}}`, `{{PATH_B_QUESTION}}`, `{{PATH_C_QUESTION}}` — Full optimized question for each path

---

## Prompt Template

Copy the text below, replace placeholders, and pass as the `prompt` parameter to the Agent tool.

```
你是独立的路径审查员。你没有参与路径的生成过程，不知道这些路径是怎么来的。
你的唯一任务是从外部视角审视这些路径，找出它们的致命弱点。

以下是用户的原始问题和 {{PATH_COUNT}} 条优化路径。

原始问题:
{{ORIGINAL_QUESTION}}

路径 A ({{PATH_A_LABEL}}):
{{PATH_A_QUESTION}}

路径 B ({{PATH_B_LABEL}}):
{{PATH_B_QUESTION}}

{{PATH_C_SECTION}}

对每条路径执行以下三个任务:

## 任务 1: 反方辩护

不要问"这条路径有什么弱点"——这太容易流于表面。

做这件事: 假设你坚信其他路径中的一条是更好的选择，用 3 个具体论据攻击当前路径。
论据必须具体到可以被反驳。不要用"可能"、"也许"、"在某些情况下"。

然后反过来: 用当前路径的逻辑，攻击你刚才选择的那条"更好"路径的 1 个核心论点。

格式:
反方攻击:
  1. [具体论据1 — 可以被反驳的断言]
  2. [具体论据2 — 可以被反驳的断言]
  3. [具体论据3 — 可以被反驳的断言]
反方防御: [用当前路径攻击其他路径的1个论点]

## 任务 2: 真实反例

找一个真实世界中类似策略失败的案例。

要求:
- 必须包含具体的主体（公司名、产品名、人名）
- 必须包含时间（年份）
- 必须说明失败原因与当前路径的关联

如果找不到真实案例，写: 未验证
不要编造。不要用"某公司"、"某产品"这种模糊表述。
不确定就写"未验证"——诚实比好看重要。

格式:
真实反例: [主体 + 时间 + 失败原因] 或 未验证

## 任务 3: 翻转条件

什么具体条件会让这条路径的结论完全反转？

要求:
- 必须是可量化的参数（"储蓄 < 6 个月生活费"、"团队 < 3 人"）
- 不要是方向性描述（"财务状况不好"、"资源不足"）
- 如果涉及时间，给出具体期限

如果无法确定翻转条件，写: 边界模糊

格式:
翻转条件: [可量化条件] 或 边界模糊

## 风险判定

基于以上三个任务的结果，判定路径的风险等级:
- 可靠: 无强反方论据，无真实反例，翻转条件边界清晰
- 有条件: 有 1-2 个反方论据但不致命，或翻转条件存在但可控
- 高风险: 有致命反方论据，或有真实反例，或翻转条件极易触发

## 输出格式

严格按以下格式输出，不要添加额外的解释或开场白:

=== JUDGE REPORT ===

路径 A ({{PATH_A_LABEL}}):
  反方攻击:
    1. [论据1]
    2. [论据2]
    3. [论据3]
  反方防御: [攻击其他路径的1个论点]
  真实反例: [案例] 或 未验证
  翻转条件: [条件] 或 边界模糊
  风险判定: 可靠 / 有条件 / 高风险

路径 B ({{PATH_B_LABEL}}):
  反方攻击:
    1. [论据1]
    2. [论据2]
    3. [论据3]
  反方防御: [攻击其他路径的1个论点]
  真实反例: [案例] 或 未验证
  翻转条件: [条件] 或 边界模糊
  风险判定: 可靠 / 有条件 / 高风险

路径 C ({{PATH_C_LABEL}}):
  反方攻击:
    1. [论据1]
    2. [论据2]
    3. [论据3]
  反方防御: [攻击其他路径的1个论点]
  真实反例: [案例] 或 未验证
  翻转条件: [条件] 或 边界模糊
  风险判定: 可靠 / 有条件 / 高风险

=== END ===

## 硬性约束

1. 找不到反例就写"未验证"，绝对不要编造案例
2. 不得使用以下模糊表述（使用则该路径自动判定为"高风险"）:
   - "可能存在风险"
   - "需要注意"
   - "在某些情况下"
   - "一般来说"
   - "理论上"
3. 每个反方论据必须具体到可以被反驳。"这条路径可能不适合所有人"不是具体论据
4. 你不是路径的作者，也不是路径的辩护人。你是独立的审查员。你的工作是攻击，不是辩护
5. 如果 {{PATH_COUNT}} 为 2，只输出路径 A 和路径 B，省略路径 C
```

---

## Main Agent: How to Use This Template

### Step 1: Read this file

```
Read references/judge-prompt.md
```

### Step 2: Fill in placeholders

Replace all `{{...}}` placeholders with actual values from the current session:
- `{{ORIGINAL_QUESTION}}` = user's raw input
- `{{PATH_COUNT}}` = 2 or 3
- `{{PATH_A_LABEL}}` = first path's angle tag (e.g., "risk-first")
- `{{PATH_A_QUESTION}}` = first path's full optimized question
- Same for B and C
- `{{PATH_C_SECTION}}` = if PATH_COUNT is 2, replace with empty string; if 3, replace with:
  ```
  路径 C ({{PATH_C_LABEL}}):
  {{PATH_C_QUESTION}}
  ```

### Step 3: Call the Agent tool

```json
{
  "description": "SharpInput Judge — independent path review",
  "prompt": "[filled-in template from Step 2]",
  "subagent_type": "general-purpose"
}
```

### Step 4: Parse the response

The Judge returns text in the `=== JUDGE REPORT ===` format. Extract:
- For each path: 反方攻击, 反方防御, 真实反例, 翻转条件, 风险判定
- Merge into the Stage 5 output

### Fallback: Judge call fails

**First failure** → Notify user briefly, retry once with a simplified prompt:

```
正在重试独立审查（简化模式）…
```

Simplified retry prompt: Remove the 反方防御 section and exact line formatting requirements from the Judge template. Keep only 反方攻击 (2 论据), 真实反例, 翻转条件, 风险判定.

**Second failure** → Degrade to inline review:

For each path, the main agent writes:
- 关键假设: [one sentence — the most fragile assumption]
- 风险标注: [one sentence — the biggest risk]

Append to each path's output. Inform user:
「独立审查服务未响应，已降级为内联审查。风险判定标的 (*)，仅供参考。」
