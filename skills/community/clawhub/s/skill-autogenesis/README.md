# skill-autogenesis

## English

### Overview

`skill-autogenesis` enables an agent to summarize completed work, detect recurring workflows, and decide whether the right output is a reusable skill, a patch to an existing skill, a memory note, or no persistence at all.

It is intended for Hermes, OpenClaw, and similar tool-using agents that benefit from structured procedural memory without changing core runtime code.

### What problem it solves

Agents often finish complex work but leave the successful procedure trapped inside conversation history.

This skill turns that transient success into durable operational knowledge.

### Key features

- Summarizes completed work into reusable procedures
- Detects recurrence from session context, memory, and session history when available
- Creates or recommends skills only when repetition, stability, and verification thresholds are met
- Applies `skill_manage`-style lifecycle handling for create, patch, edit, write_file, and remove_file
- Uses hard stop rules to block invalid skill creation for preferences, policies, and one-off results
- Updates related existing skills instead of creating duplicates
- Preserves safety boundaries by excluding secrets and requiring verification

### Recommended workflow

1. Load the skill at the start of a session.
2. Let the agent work normally.
3. After meaningful successes, first classify the outcome: executable procedure, preference or policy note, or one-off result.
4. Fill the classification template before any persistence action.
5. Apply the hard stop rules.
6. Only treat executable procedures as skill candidates.
7. Resolve references in this order: GitHub source, then local fallback, then `[UNVERIFIED]`.
8. Use `skill_manage`-style lifecycle rules to decide between create, patch, edit, write_file, remove_file, memory, or no-op.
9. Create or update a skill only when recurrence, stability, and verification are all strong enough.

### Files in this package

- `SKILL.md` for the operational instructions
- `README.md` for human-facing overview
- `CHANGELOG.md` for release history
- `references/sources.md` for the source links used to ground the logic
- `references/classification-examples.md` for examples that separate skills from rules, preferences, and policies
- `references/hard-stop-rules.md` for strict blocking rules that prevent invalid skill creation

## 中文

### 概述

`skill-autogenesis` 让 agent 在完成任务后自动总结流程、识别重复工作模式，并先判断结果应该沉淀为 skill、补丁更新、memory，还是暂时不沉淀。

它适用于 Hermes、OpenClaw 以及其他具备工具调用能力、希望增强 procedural memory 的 agent，而且不需要修改底层运行时代码。

### 解决的问题

很多 agent 虽然完成了复杂任务，但真正有效的做法只留在会话历史里，没有沉淀成长期可复用的方法。

这个 skill 就是把一次性成功经验转成长期可执行知识。

### 核心特性

- 把完成的工作总结为可复用流程
- 在可用时结合当前会话、memory、session history 判断重复度
- 仅在重复度、稳定性和验证条件满足时创建或建议 skill
- 先做分类，再决定是 skill、memory、prompt 还是 no-op
- 强制先输出分类模板和判定理由，再决定是否写文件
- 对偏好、策略、审批边界、一次性结论启用硬拦截，禁止误建 skill
- 优先更新相关旧 skill，而不是重复创建
- 通过排除密钥和要求验证步骤来保持安全边界

### 推荐使用方式

1. 在会话开始时加载这个 skill。
2. 让 agent 正常执行任务。
3. 在关键成功点后，先判断产出到底是可执行流程，还是偏好、边界、规则说明。
4. 在任何持久化动作之前，先填写分类模板和理由。
5. 先执行硬拦截规则。
6. 只有可执行流程才进入 skill 候选。
7. 当重复度、稳定性和验证条件都足够强时，agent 才创建或更新 skill。
8. 如果只是偏好、审批边界、命名约定或抽象原则，应写入 memory 或 prompt，而不是新建 skill。

### 包内文件

- `SKILL.md`，核心操作说明
- `README.md`，给人看的总览
- `references/sources.md`，逻辑依据的来源链接
- `references/classification-examples.md`，区分 skill、规则、偏好和策略说明的示例
- `references/hard-stop-rules.md`，阻止误建 skill 的硬拦截规则
- `references/fallback/`，GitHub 无法访问时可直接查看的本地备用参考文件
- `templates/generated-skill-template.md`，自动生成新 skill 时可复用的模板
