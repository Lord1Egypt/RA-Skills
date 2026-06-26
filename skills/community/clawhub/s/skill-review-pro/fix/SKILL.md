---
name: skill-review-fix
description: >
  skill-review-pro 的子技能。读取评审报告中的修复清单，在用户逐条确认后对目标 Skill 执行修复。
  Sub-skill of skill-review-pro. Reads the fix checklist from the review report, executes fixes after per-item user confirmation.
  注意：此技能不独立使用，由 skill-review-pro 的修复阶段调用。
---

# skill-review-fix — Skill 修复执行器 / Skill Fix Executor

基于 skill-review-pro 评审报告中的修复清单，对目标 Skill 进行针对性修复。
Apply targeted fixes to the target Skill based on the fix checklist from skill-review-pro.

## 输入 / Input

从 skill-review-pro 的最终报告中提取修复清单。修复清单位于 `<!-- FIX_CHECKLIST_START -->` 和 `<!-- FIX_CHECKLIST_END -->` 标记之间，包含：
- 目标 Skill 名称和文件路径
- 问题列表（每条包含：问题描述、修复方案、优先级、风险、影响维度、预估提分）
- 详细修复方案（每条包含：原文引用、修改后内容、文件位置、依赖关系）

如果上下文中没有修复清单标记，说明评审阶段还没有输出修复清单，应提示用户先完成评审。

## 核心原则 / Core Principles

**不主动执行，必须询问用户。** / **Never act without asking.**

每一条修复在执行前，必须：
1. 告诉用户要改什么 / Tell the user what will change
2. 展示修改前后的对比 / Show before/after diff
3. 等待用户确认 / Wait for user confirmation

用户响应：
- "修" / "fix" / "确认" → 执行这一条
- "都修" / "fix all" / "全部" → 展示所有修改的 before/after，确认后批量执行
- "跳过" / "skip" → 跳过这一条
- "只修 1、3" → 选择性执行
- "不修了" / "stop" → 终止修复流程

## 风险等级与执行规则 / Risk Levels

修复清单中每条修复有风险等级，执行规则不同：

| 风险 / Risk | 执行规则 / Execution Rule |
|---|---|
| **Low** | 正常逐条确认流程 |
| **Medium** | 展示更详细的 diff，告知影响的章节范围，确认后执行 |
| **High** | 必须单独展示完整的 before/after 对比，告知潜在影响，用户明确说"确认"后才执行。即使批量模式下也必须逐条确认 |

## 依赖处理 / Dependency Handling

修复清单可能包含依赖关系：

- **无依赖** — 可独立执行，顺序不限
- **依赖 #X** — 必须先执行 #X 再执行本条。如果 #X 被跳过，询问用户是否仍执行本条
- **被 #X 依赖** — 本条跳过或修改后，提醒用户 #X 可能需要调整

## 执行流程 / Workflow

### Step 1：解析修复清单 / Parse Fix Checklist

从修复清单标记中提取：
- 目标文件路径
- 修复项列表（问题、方案、优先级、风险、位置）
- 详细修复方案（原文 → 修改后）
- 依赖关系

如果修复清单中没有"详细修复方案"部分，生成候选 diff（before/after），但**必须让用户确认 diff 符合 reviewer 原意后才能执行**，不能自行决定修复内容。

### Step 2：确认修复范围 / Confirm Scope

按优先级排序展示修复清单摘要：

```markdown
## 即将执行的修复

**目标文件**：`<路径>`
**执行模式**：逐条确认 / 批量

| 优先级 | # | 问题摘要 | 风险 | 修改位置 |
|--------|---|----------|------|----------|
| P0 | 1 | ... | Low | ... |
| P1 | 2 | ... | Medium | ... |

确认要开始修复吗？
```

**⏸ 等待用户确认。**

### Step 3a：逐条模式 / Per-item Mode（默认）

按优先级顺序（P0 → P1 → P2），对每条待修复项：
1. 展示优先级和风险等级
2. 展示**当前原文**（引用具体行或段落）
3. 展示**修改后内容**
4. 如果有依赖，标注依赖状态
5. 询问用户："这条修吗？（修/跳过/停止）"

High 风险修复额外步骤：展示完整的章节上下文，说明潜在影响范围。

用户确认后：
- 执行修改
- 标记状态为 ✅ 已修复
- 检查是否有被此条依赖的其他修复项，如有则提醒

### Step 3b：批量模式 / Batch Mode（用户说"都修"）

1. **按依赖排序**（无依赖的先执行），展示所有修改项的 before/after 对比
2. **排除 High 风险项**（告知用户："以下 High 风险修复需单独确认"）
3. 询问用户："确认执行 Low 和 Medium 修复？"
4. 用户确认后批量执行
5. 然后逐条展示 High 风险修复，要求单独确认

### Step 4：修复验证 / Fix Verification

所有修复执行完毕后：
1. 重新读取修改后的文件
2. 检查是否引入新问题，逐项验证：
   - frontmatter 完整性（name + description 无缺失）
   - 章节编号连续性（无跳号或重复）
   - 中英段落对应（中文有则英文也应有）
   - 无新增矛盾指令（修复 A 不应与 B 矛盾）
3. 如发现新问题，告知用户并询问是否处理
4. 检查被跳过的修复项是否影响其他项

### Step 5：更新评分 / Update Score

基于实际执行的修复，更新 Phase 1 评分：

```markdown
## 评分对比

| 维度 | 修复前 | 修复后 | 变化 |
|------|--------|--------|------|
| ... | X | X | +X |
| **Phase 1** | **XX** | **XX** | **+X** |
| **总计** | **XX** | **XX** | **+X** |

**执行情况**：X/X 项已修复，Y 项跳过
```

### Step 6：提示重新评审 / Prompt Re-review

Step 5 输出完成后，提示用户：

> 修复完成。如需对修复后的版本重新评审，请说「再评一遍」或「re-review」。

用户说「再评一遍」/「re-review」/「重新评审」时：
1. 以修复后的 Skill 文件为输入，重走完整评审流程（静态审查 + 对抗检查）
2. 最终报告中**自动带入回归对比**，以本次修复前的分数作为历史版本基准
3. 不需要用户再次指定目标 Skill，直接使用当前修复的文件路径

## 约束 / Constraints

- **绝不主动修改** — 每条必须经用户确认 / Never modify without confirmation
- **只修清单里的内容** — 不擅自扩大范围 / Only fix what's in the checklist
- **中英双语同步** — 修中文必须同步修英文 / Keep bilingual in sync
- **不动 frontmatter** — 除非清单明确指出 / Don't touch frontmatter unless specified
- **每条可回退** — 用户说"不对"则撤销上一条 / Every change is revertible
- **依赖优先** — 有依赖关系的修复按顺序执行 / Respect dependency order
- **High 风险必须单独确认** — 即使在批量模式中 / High-risk fixes always need individual confirmation

## 反模式 / Anti-patterns

- ❌ 不问就改 / Modifying without asking
- ❌ 改着改着扩大范围 / Scope creeping during fixes
- ❌ 只改中文不改英文 / Fixing Chinese but not English
- ❌ 改完后不验证 / Not verifying after fixes
- ❌ 忽略依赖关系乱改 / Ignoring dependencies
- ❌ 跳过 High 风险的单独确认 / Not individually confirming high-risk fixes
