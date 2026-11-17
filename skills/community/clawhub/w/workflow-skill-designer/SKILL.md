---
name: workflow-skill-designer
slug: yumingtao-workflow-skill-designer
displayName: Workflow Skill Designer
version: 1.3.1
summary: 元技能：设计编排器+阶段（orchestrator+phases）结构化工作流技能。
license: MIT
tags:
  - 开发工具
  - 工作流
  - 元技能
disable-model-invocation: true
description: >
  元技能：设计编排器+阶段（orchestrator+phases）结构化工作流技能。生成以 SKILL.md 为协调器、phases/ 文件夹存放执行细节的完整技能包，支持渐进式阶段加载、TodoWrite 模式和数据流。触发词："设计工作流技能"、"创建 workflow skill"、"workflow skill designer"。
allowed-tools: Task, AskUserQuestion, TodoWrite, Read, Write, Edit, Bash, Glob, Grep
session-mode: none
---

# 工作流技能设计器

元技能：按编排器+阶段（orchestrator + phases）模式创建结构化工作流技能。生成以 SKILL.md 为协调器、phases/ 文件夹存放执行细节的完整技能包。

## 目录

- [环境兼容性](#环境兼容性)
- [目标输出结构](#目标输出结构)
- [核心设计模式](#核心设计模式)
- [执行流程](#执行流程)
- [输入来源](#输入来源)
- [编排器内容映射](#编排器内容映射)
- [SKILL.md 模板](#skillmd-模板)
- [阶段文件模板](#阶段文件模板)
- [设计决策框架](#设计决策框架)
- [何时不使用](#何时不使用)
- [常见问题](#常见问题)

## 工具名词约定

本技能及生成技能统一使用以下术语，避免混淆：

| 术语 | 含义 | 正确写法 | 错误写法 |
|------|------|----------|----------|
| **Task** | 子代理委派（allowed-tools 声明） | `Task({ subagent_type: "...", prompt: "..." })` | ~~Agent({...})~~, ~~Subagent({...})~~ |
| **Skill** | 跨技能调用（经由宿主路由） | `Skill(skill="other-skill", args="...")` | ~~Task({ skill: "..." })~~ |
| **Read** | 同技能内阶段交接 | `Read("phases/02-xxx.md")` 然后直接执行 | ~~Skill(skill="self", args="...")~~（绕行 SKILL.md 无意义） |

## 如何调用本技能

本技能 `disable-model-invocation: true`（防误触发），需显式调用。常见宿主的调用方式：

| 宿主 | 显式调用示例 |
|------|-------------|
| Claude Code | 在对话中说"设计工作流技能"或使用 `/skill-name`（若已配置） |
| Trae | 说"使用 workflow-skill-designer 设计工作流技能" |
| DSH | 将技能放入 `~/.agents/skills/`，说"创建 workflow skill" |
| 通义/豆包 | 自然语言触发词："帮我设计一个工作流技能" |

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│  Workflow Skill Designer                                         │
│  → Analyze requirements → Design orchestrator → Generate phases  │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┼───────────┬───────────┐
    ↓           ↓           ↓           ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Phase 1 │ │ Phase 2 │ │ Phase 3 │ │ Phase 4 │
│ Require │ │  Orch   │ │ Phases  │ │ Valid   │
│ Analysis│ │ Design  │ │ Design  │ │ & Integ │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     ↓           ↓           ↓           ↓
  workflow    SKILL.md    phases/     Complete
  config     generated   0N-*.md     skill pkg
```

## 环境兼容性

本技能基于 Claude Code 约定编写。其他智能体环境支持相同模式，但路径和工具名称不同。下表给出具体映射，通用规则在表后：

| Concept | Claude Code | DeepSeek Harness | 通用映射规则 |
|---------|-------------|------------------|-------------|
| 项目技能根 | `.claude/skills/` | `.dsh/skills/` / `.agents/skills/` | 宿主技能目录，阶段文件中 `.claude/skills/` 替换为 `{skill-root}/` |
| 用户技能根 | `~/.claude/skills/` | `$DSH_HOME/skills` / `~/.agents/skills/` | 同上 |
| 偏好收集 | `AskUserQuestion` | 宿主交互原语 | 宿主提供的交互式提问机制，无固定工具名时用描述性写法 |
| 任务跟踪 | `TodoWrite` | 宿主 task/todo 工具 | 宿主任务跟踪能力 |
| 子代理委派 | `Task()` | 宿主子代理调用 | 宿主子代理机制（见工具名词约定） |
| 跨技能调用 | `Skill(skill=..., args=...)` | 宿主技能调用 | 宿主提供的技能路由机制 |

**生成非 Claude 环境技能时**：按上表映射路径和工具名。通用映射规则——把 "Skill Root" 替换为宿主技能目录，"AskUserQuestion" 替换为宿主交互原语，"TodoWrite" 替换为宿主任务跟踪，"Task" 替换为宿主子代理调用。

### 上下文变量（编排器提供）

以下变量由 SKILL.md 编排器设置并由阶段文件消费。它们**不是**独立的辅助函数——而是在阶段分发前填充的内存上下文：

| 变量 | 设置者 | 使用者 | 说明 |
|------|--------|--------|------|
| `workflowPreferences` | SKILL.md（通过 `AskUserQuestion`）| 所有阶段 | 收集的偏好（autoYes, forceExplore 等）。阶段读取 `workflowPreferences.{key}`，不再重新提示。 |
| `executionContext` | SKILL.md | 阶段交接（模式 7）| 活跃会话状态（sessionId, currentPhase, accumulated notes）。当一个阶段直接交接给另一阶段时设置。 |
| `workflowConfig` | 阶段 1 输出 | 阶段 2–4 | 结构化工作流定义（阶段、数据流、条件）。 |

**规则**：阶段文件必须按名称引用这些变量并记录其来源。不得在生成的输出中引入未定义的辅助函数或变量。阶段设计文档代码示例中出现的辅助函数（如 `extractYAMLFrontmatter`、`parseRequirements`、`removeYAMLFrontmatter`）是**参考伪代码**，仅用于勾勒解析意图——生成的技能必须将其替换为宿主环境的真实工具，绝不能原样依赖。

## 目标输出结构

本元技能产出的技能遵循以下结构：

```
.claude/skills/{skill-name}/
├── SKILL.md                    # Orchestrator: coordination, data flow, TodoWrite
├── phases/
│   ├── 01-{phase-name}.md      # Phase execution detail (full content)
│   ├── 02-{phase-name}.md
│   ├── ...
│   └── 0N-{phase-name}.md
├── specs/                      # [Optional] Domain specifications
└── templates/                  # [Optional] Reusable templates
```

## 核心设计模式

从成功的工作流技能实现（workflow-plan、project-analyze 等）中提炼的模式：

### 模式 1：编排器 + 渐进式加载

**SKILL.md** = 纯协调器。包含：
- 架构图（ASCII）
- 带 `Ref: phases/0N-xxx.md` 标记的执行流程
- 阶段参考文档表（按需读取）
- 阶段间数据流
- 核心规则和错误处理

**阶段文件** = 完整执行细节。包含：
- 完整的智能体提示、bash 命令、代码实现
- 校验清单、错误处理
- 输入/输出规格
- 下一阶段链接

**关键规则**：SKILL.md 通过 `Ref:` 标记引用阶段文档。阶段文档**仅在该阶段执行时**读取，而非一次性全部读取。

### 模式 2：TodoWrite 附加/折叠

```
Phase starts:
  → Sub-tasks ATTACHED to TodoWrite (in_progress + pending)
  → Orchestrator executes sub-tasks sequentially

Phase ends:
  → Sub-tasks COLLAPSED back to high-level summary (completed)
  → Next phase begins
```

### 模式 3：阶段间数据流

```
Phase N output → stored in memory/variable → Phase N+1 input
                  └─ or written to session file for persistence
```

每个阶段通过以下方式接收前序阶段的输出：
- 内存变量（sessionId、contextPath 等）
- 会话目录文件（`.workflow/active/{sessionId}/...`）
- 规划笔记（累积的约束文档）

### 模式 4：条件阶段执行

```
Phase N output contains condition flag
  ├─ condition met → Execute Phase N+1
  └─ condition not met → Skip to Phase N+2
```

### 模式 5：输入结构化

在阶段 1 之前，将用户输入（自由文本）转为结构化格式：

```
GOAL: [objective]
SCOPE: [boundaries]
CONTEXT: [background/constraints]
```

### 模式 6：交互式偏好收集（SKILL.md 职责）

工作流偏好（auto 模式、force explore 等）**必须**在分发到阶段**之前**于 SKILL.md 中通过 AskUserQuestion 收集。阶段将它们作为 `workflowPreferences.{key}` 上下文变量引用。

**反模式**：在阶段文件内通过 `$ARGUMENTS.includes(...)` 解析命令行标志（`--yes`、`-e`、`--explore`）。

```javascript
// CORRECT: In SKILL.md (before phase dispatch)
const prefResponse = AskUserQuestion({
  questions: [
    { question: "是否跳过确认？", header: "Auto Mode", options: [
      { label: "Interactive (Recommended)", description: "交互模式" },
      { label: "Auto", description: "跳过所有确认" }
    ]}
  ]
})
workflowPreferences = { autoYes: prefResponse.autoMode === 'Auto' }

// CORRECT: In phase files (reference only)
const autoYes = workflowPreferences.autoYes

// WRONG: In phase files (flag parsing)
const autoYes = $ARGUMENTS.includes('--yes') || $ARGUMENTS.includes('-y')
```

### 模式 7：直接阶段交接

当一个阶段需要调用同一技能内的另一个阶段时，直接读取并执行该阶段文档。**不要**使用 `Skill()` 经由 SKILL.md 绕回。

```javascript
// CORRECT: Direct handoff (executionContext already set)
Read("phases/02-lite-execute.md")
// Execute with executionContext (Mode 1)

// WRONG: Skill routing (unnecessary round-trip)
Skill(skill="workflow-lite-plan", args="--in-memory")
```

### 模式 8：阶段文件卫生

阶段文件是内部执行文档。它们**不得**包含：

| 禁止项 | 原因 | 正确位置 |
|--------|------|----------|
| 标志解析 (`$ARGUMENTS.includes(...)`) | 偏好在 SKILL.md 中收集 | SKILL.md via AskUserQuestion |
| 调用语法 (`/skill-name "..."`) | 非用户文档 | Removed or SKILL.md only |
| 转换来源 (`Source: Converted from...`) | 实现细节 | Removed |
| 阶段间技能路由 (`Skill(skill="...")`) | 使用直接阶段读取 | Direct `Read("phases/...")` |
| TODO / `...` / 占位符标记 (`{TODO}`, `TBD`, `fill in`) | 生成的技能必须可直接执行 | Replace with concrete implementation or omit the step |

### 模式 9：紧凑恢复（阶段持久化）

多阶段工作流跨越长对话。上下文压缩（compact）会自然摘要早期阶段文档。策略采用**双重保险**：TodoWrite 跟踪 active phase 保护其不被压缩，sentinel 作为兜底在压缩发生时触发恢复。

**设计原则**：TodoWrite `in_progress` = 当前阶段 → 防止压缩 | Sentinel = 保护失效时的重读兜底。

**双层机制**：

| 层 | 作用 | 机制 |
|----|------|------|
| **1. 活跃阶段保护** | 预防 | TodoWrite `in_progress` 标记当前 phase → compact 时保留该 phase 完整内容，不压缩 |
| **2. Sentinel 重读** | 恢复 | Phase 文件嵌入标识符 → 若仍被压缩，检测到 sentinel-only 状态时立即 re-read |

**适用时机**：任何通过 direct handoff (Pattern 7) 跨 phase 执行的场景，尤其是后续 phase 包含复杂执行协议（多 Step、agent 调度、CLI 编排）时。

---

#### Layer 1: Active Phase Protection (TodoWrite 联动)

TodoWrite 已经跟踪每个 phase 的执行状态。利用此信息驱动 compact 策略：

```
TodoWrite status → Compact behavior:
  ┌─ completed  → ✅ 可压缩（已完成，不再需要完整内容）
  ├─ in_progress → 🛡️ 禁止压缩（正在执行，必须保留完整协议）
  └─ pending    → ✅ 可压缩（尚未加载，无内容）
```

**SKILL.md Execution Flow** 中标注 compact 联动:
```markdown
## Execution Flow

> **⚠️ COMPACT DIRECTIVE**: Context compression MUST check TodoWrite phase status.
> The phase currently marked `in_progress` is the active execution phase — preserve its FULL content.
> Only compress phases marked `completed` or `pending`.

Phase 1: Requirements Analysis    ← TodoWrite tracks status
   └─ Ref: phases/01-xxx.md
Phase 2: Execution Engine         ← TodoWrite tracks status
   └─ Ref: phases/02-xxx.md
...
```

**TodoWrite 状态转换** 时自动更新 compact 保护范围:
```
Phase 1: in_progress 🛡️  →  completed ✅   (compact 可压缩 Phase 1)
Phase 2: pending ✅       →  in_progress 🛡️ (compact 保护 Phase 2)
```

---

#### Layer 2: Sentinel Re-read (兜底恢复)

即使有 Layer 1 保护，compact 仍可能在极端场景（超长上下文、多轮 agent 调度）下压缩 active phase。Sentinel 确保恢复能力：

**Phase 文件顶部嵌入 sentinel**:
```markdown
> **📌 COMPACT SENTINEL [Phase N: {phase-name}]**
> This phase contains {M} execution steps (Step N.1 — N.{M}).
> If you can read this sentinel but cannot find the full Step protocol below, context has been compressed.
> Recovery: `Read("phases/0N-xxx.md")`
```

Sentinel 设计特点：
- 结构化、醒目 → compact 会将其作为关键信息保留在摘要中
- 包含 step 数量 → 提供自检依据（"应该看到 M 个 Step，但只有摘要"）
- 包含 re-read 路径 → 无需查表即可恢复

---

#### Phase Reference Table (整合双重保险)

```markdown
| Phase | Document | Purpose | Compact |
|-------|----------|---------|---------|
| 1 | phases/01-xxx.md | Planning | TodoWrite 驱动 |
| 2 | phases/02-xxx.md | Execution | TodoWrite 驱动 + 🔄 sentinel |

**Compact Rules**:
1. **TodoWrite `in_progress`** → 保留完整内容，禁止压缩
2. **TodoWrite `completed`** → 可压缩为摘要
3. **🔄 sentinel fallback** → 带此标记的 phase 包含 compact sentinel；若 compact 后仅存 sentinel 而无完整 Step 协议，**必须立即 `Read("phases/0N-xxx.md")` 恢复后再继续**
```

---

#### Checkpoint (执行步骤前双重验证)

```markdown
> **⚠️ CHECKPOINT**: Before proceeding, verify:
> 1. This phase is TodoWrite `in_progress` (active phase protection)
> 2. Full protocol (Step N.X — N.{M}) is in active memory, not just sentinel
> If only sentinel remains → `Read("phases/0N-xxx.md")` now.
```

#### Handoff 注释

```javascript
// Phase N is tracked by TodoWrite — active phase protection applies.
// Sentinel fallback: if compressed despite protection, re-read triggers automatically.
Read("phases/0N-xxx.md")
```

## 执行流程

```
Phase 1: Requirements Analysis
   └─ Ref: phases/01-requirements-analysis.md
      ├─ Input source: commands, descriptions, user interaction
      └─ Output: workflowConfig (phases, data flow, agents, conditions)

Phase 2: Orchestrator Design (SKILL.md)
   └─ Ref: phases/02-orchestrator-design.md
      ├─ Input: workflowConfig
      └─ Output: .claude/skills/{name}/SKILL.md

Phase 3: Phase Files Design
   └─ Ref: phases/03-phase-design.md
      ├─ Input: workflowConfig + source content
      └─ Output: .claude/skills/{name}/phases/0N-*.md

Phase 4: Validation & Integration
   └─ Ref: phases/04-validation.md
      └─ Output: Validated skill package
```

**Phase Reference Documents** (read on-demand):

| Phase | Document | Purpose |
|-------|----------|---------|
| 1 | [phases/01-requirements-analysis.md](phases/01-requirements-analysis.md) | Analyze workflow requirements from various sources |
| 2 | [phases/02-orchestrator-design.md](phases/02-orchestrator-design.md) | Generate SKILL.md with orchestration patterns |
| 3 | [phases/03-phase-design.md](phases/03-phase-design.md) | Generate phase files preserving full execution detail |
| 4 | [phases/04-validation.md](phases/04-validation.md) | Validate structure, references, and integration |

## 输入来源

本元技能接受多种来源的工作流定义：

| 来源 | 说明 | 示例 |
|------|------|------|
| **现有命令** | 转换 `.claude/commands/` 编排器 + 子命令 | `plan.md` + `session/start.md` + `tools/*.md` |
| **文本描述** | 用户用自然语言描述工作流 | "Create a 3-phase code review workflow" |
| **需求文档** | 结构化需求文件 | `requirements.md` with phases/agents/outputs |
| **现有技能** | 重构/重新设计现有技能 | Restructure a flat skill into phases |

## Frontmatter 转换规则

从命令格式转换为技能格式时：

| Command Field | Skill Field | Transformation |
|---------------|-------------|----------------|
| `name` | `name` | Prefix with group: `plan` → `workflow-plan` |
| `description` | `description` | Append trigger phrase: `Triggers on "xxx"` |
| `argument-hint` | _(removed)_ | Arguments handled in Input Processing section |
| `examples` | _(removed)_ | Examples moved to inline documentation |
| `allowed-tools` | `allowed-tools` | Expand wildcards: `Skill(*)` → `Skill`, add commonly needed tools |
| `group` | _(removed)_ | Embedded in `name` prefix |
| _(none)_ | `session-mode` | Add: `run` if the skill creates a Run / writes `{run_dir}` artifacts, else `none` (only when the target environment ships a run lifecycle contract; omit the field elsewhere). When `run`, also add the run lifecycle `<required_reading>` block. |

## 编排器内容映射

哪些内容放入 SKILL.md，哪些放入阶段文件：

### SKILL.md (Coordinator)

| Section | Content | Source |
|---------|---------|--------|
| Frontmatter | name, description, allowed-tools | Command frontmatter (converted) |
| Architecture Overview | ASCII diagram of phase flow | Derived from execution structure |
| Key Design Principles | Coordination rules | Extracted from command coordinator role |
| Execution Flow | Phase sequence with `Ref:` markers + Phase Reference table | Command execution process |
| Core Rules | Orchestration constraints | Command core rules |
| Input Processing | Structured format conversion | Command input processing |
| Data Flow | Inter-phase data passing | Command data flow |
| TodoWrite Pattern | Attachment/collapse lifecycle | Command TodoWrite sections |
| Post-Phase Updates | Planning notes / state updates between phases | Command inter-phase update code |
| Error Handling | Failure recovery | Command error handling |
| Coordinator Checklist | Pre/post phase actions | Command coordinator checklist |
| Related Commands | Prerequisites and follow-ups | Command related commands |

### Phase Files (Execution Detail)

| Content | Rule |
|---------|------|
| Full agent prompts | Preserve verbatim from source command |
| Bash command blocks | Preserve verbatim |
| Code implementations | Preserve verbatim |
| Validation checklists | Preserve verbatim |
| Error handling details | Preserve verbatim |
| Input/Output spec | Add if not present in source |
| Phase header | Add `# Phase N: {Name}` |
| Objective section | Add `## Objective` with bullet points |
| Next Phase link | Add `## Next Phase` with link to next |

**Critical Rule**: Phase files must be **content-faithful** to their source. Do NOT summarize, abbreviate, or simplify. The phase file IS the execution instruction - every bash command, every agent prompt, every validation step must be preserved.

**No-Placeholder Rule**: Generated phase files must be immediately executable. They MUST NOT contain `TODO`, `TBD`, `...`, `fill in`, `{placeholder}`, or any incomplete step. If a step cannot be concretely specified, omit it rather than leaving a stub. The Validation phase (Phase 4) must scan for these markers and reject any file containing them.

> **参考伪代码例外**: 本元技能自身的阶段设计文档（`phases/01-requirements-analysis.md` 等）中可能包含 `extractYAMLFrontmatter()`、`parseRequirements()` 等参考伪代码函数，用于勾勒解析意图。这些**仅存在于本技能的设计文档中**，用于教学演示。生成的技能阶段文件**不得**保留此类未定义函数——必须替换为宿主环境的真实工具（如 YAML frontmatter 库、正则提取等）。Phase 4 校验必须检测并拒绝生成文件中出现的未定义函数引用。

## SKILL.md 模板

```markdown
---
name: {skill-name}
description: {description}. Triggers on "{trigger1}", "{trigger2}".
allowed-tools: {tools}
session-mode: {run|none}
---

<!-- Include only when session-mode: run AND the target environment ships a run
     lifecycle contract. Omit this block in environments without one. -->

# {Title}

{One-paragraph description of what this skill does and what it produces.}

## Architecture Overview

{ASCII diagram showing phases and data flow}

## Key Design Principles

1. **{Principle}**: {Description}
...

## Interactive Preference Collection

Collect workflow preferences via AskUserQuestion before dispatching to phases:
{AskUserQuestion code with preference derivation → workflowPreferences}

## Auto Mode Defaults

When `workflowPreferences.autoYes === true`: {auto-mode behavior}.

## Execution Flow

{Phase sequence with Ref: markers}

**Phase Reference Documents** (read on-demand when phase executes):

| Phase | Document | Purpose | Compact |
|-------|----------|---------|---------|
| 1 | [phases/01-xxx.md](phases/01-xxx.md) | ... | TodoWrite 驱动 |
| N | [phases/0N-xxx.md](phases/0N-xxx.md) | ... | TodoWrite 驱动 + 🔄 sentinel |
...

**Compact Rules**:
1. **TodoWrite `in_progress`** → 保留完整内容，禁止压缩
2. **TodoWrite `completed`** → 可压缩为摘要
3. **🔄 sentinel fallback** → 带此标记的 phase 包含 compact sentinel；若 compact 后仅存 sentinel 而无完整 Step 协议，必须立即 `Read()` 恢复

## Core Rules

1. {Rule}
...

## Input Processing

{How user input is converted to structured format}

## Data Flow

{Inter-phase data passing diagram}

## TodoWrite Pattern

{Attachment/collapse lifecycle description with examples}

## Post-Phase Updates

{State updates between phases}

## Error Handling

{Failure recovery rules}

## Coordinator Checklist

{Pre/post phase action list}

## Related Commands

{Prerequisites and follow-ups}
```

## 阶段文件模板

```markdown
# Phase N: {Phase Name}

> **📌 COMPACT SENTINEL [Phase N: {phase-name}]**
> This phase contains {M} execution steps (Step N.1 — N.{M}).
> If you can read this sentinel but cannot find the full Step protocol below, context has been compressed.
> Recovery: `Read("phases/0N-xxx.md")`
> _(Include for phases marked 🔄 in SKILL.md Phase Reference table — see Pattern 9)_

{One-sentence description of this phase's goal.}

## Objective

- {Goal 1}
- {Goal 2}

## Execution

### Step N.1: {Step Name}

{Full execution detail: commands, agent prompts, code}

### Step N.2: {Step Name}

> **⚠️ CHECKPOINT**: Before proceeding, verify:
> 1. This phase is TodoWrite `in_progress` (active phase protection)
> 2. Full protocol (Step N.X — N.{M}) is in active memory, not just sentinel
> If only sentinel remains → `Read("phases/0N-xxx.md")` now.
> _(Add checkpoints before critical execution steps: agent dispatch, CLI launch, review — see Pattern 9)_

{Full execution detail}

## Output

- **Variable**: `{variableName}` (e.g., `sessionId`)
- **File**: `{run_dir}/outputs/{artifact}` — formal artifacts go under `{run_dir}/outputs/`; synthesis to `{run_dir}/report.md`, scratch to `{run_dir}/work/` (session-mode: run only). See the environment's run lifecycle contract.
- **TodoWrite**: Mark Phase N completed, Phase N+1 in_progress

## Next Phase

Return to orchestrator, then auto-continue to [Phase N+1: xxx](0N+1-xxx.md).
```

## 设计决策框架

设计新工作流技能时，回答以下问题：

| Question | Impact | Example |
|----------|--------|---------|
| How many phases? | Directory structure | 3-7 phases typical |
| Which phases are conditional? | Orchestrator logic | "Phase 3 only if conflict_risk >= medium" |
| What data flows between phases? | Data Flow section | sessionId, contextPath, configFlags |
| Which phases use subagents? | Phase file complexity | Subagent prompts need verbatim preservation |
| What's the TodoWrite granularity? | TodoWrite Pattern | Some phases have sub-tasks, others are atomic |
| Is there a planning notes pattern? | Post-Phase Updates | Accumulated state document across phases |
| What's the error recovery? | Error Handling | Retry once then report, vs rollback |
| Does it need preference collection? | Interactive Preference Collection | Collect via AskUserQuestion in SKILL.md, pass as workflowPreferences |
| Does phase N hand off to phase M? | Direct Phase Handoff (Pattern 7) | Read phase doc directly, not Skill() routing |
| Will later phases run after long context? | Compact Recovery (Pattern 9) | Add sentinel + checkpoints, mark 🔄 in Phase Reference table |

## 何时不使用

本元技能**不适合**以下场景：

- The workflow has only a single phase or is a flat sequence of steps with no
  coordination needs — write a single SKILL.md or command instead.
- The target environment has no interactive tool (cannot run `AskUserQuestion`
  or equivalent) — preferences cannot be collected at runtime.
- The workflow requires no persistent state across phases — a single-pass
  instruction is simpler.
- You need to design a non-workflow skill (e.g., a pure reference skill, a
  formatting skill) — this pattern is for multi-phase orchestration.

## 常见问题

**Q: 多少个阶段算太多？**
A: 通常 3–7 个。超过 7 个，考虑是否应拆分为两个技能。少于 3 个，可能不需要编排器+阶段模式。

**Q: 一个阶段可以调用另一个技能吗？**
A: 同一技能内使用直接阶段交接（模式 7）。调用*其他*技能时，从 SKILL.md 使用宿主的技能调用机制，而非在阶段文件内部调用。

**Q: 生成的阶段文件有 TODO 怎么办？**
A: 这是缺陷。No-Placeholder 规则要求每个步骤必须具体。要么实现该步骤，要么删除它。校验阶段（Phase 4）必须拒绝包含 TODO/TBD/`...` 标记的文件。

**Q: 所有阶段都需要 compact sentinel 吗？**
A: 不需要——仅在长上下文后运行或从更早阶段交接的阶段才需要（模式 9）。在阶段引用表中用 🔄 标记这些阶段。

## 语言支持

本元技能支持中文交互。需求、偏好和阶段内容可以用中文编写。生成的技能的 SKILL.md 和阶段文件应匹配用户的首选语言。触发词包括 "设计工作流技能"、"创建 workflow skill"。
