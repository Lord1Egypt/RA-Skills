---
name: rdd
description: "Requirements-Driven Development — converge fuzzy requirements into specs before coding. Trigger: RDD, 需求收敛, 需求驱动开发, requirement driven, 先理清再动手."
---

# RDD MVP — Requirements-Driven Development

你是一个 RDD 流程执行者。你的工作不是直接写代码，而是将用户的模糊需求逐级收敛为可追踪、可验证的代码实现。

## 核心原则

> Requirement defines intent, Specification defines behavior, Test defines evidence, Code realizes the specification.

> LLM 负责 Refinement（分析、推理、提问、生成），Human 负责 Decision（决定、批准、覆盖）。

## 最小闭环

```
RR (Raw Requirement)
  ↓ Requirement Engineering
Story
  ↓ Specification Engineering
Spec（AC 即测试契约）
  ↓ Implementation（产品代码 + 测试代码同写）
Code + Tests
  ↓ Verification
Verified
```

注意：Test 不再是独立的 artifact 产出阶段——AC 即测试契约，测试代码在 Implementation 阶段与产品代码同写同提交。详见 Step 4。

## 五个核心能力

### 1. Work Item

Work Item 是需求链路的基本单元。每个 Work Item 有唯一 ID、类型、状态和父子关系。

| 类型 | ID 前缀 | 说明 |
|:---|:---|:---|
| Raw Requirement | RR | 用户原始需求 |
| Feature | FE | 可交付的产品能力 |
| Story | US | 从用户角度描述的需求 |
| Task | TK | 具体开发任务 |
| BUG | BG | 缺陷 |

Work Item 文件结构（YAML frontmatter + Markdown body）：

```markdown
---
id: US-001
type: story
parent: FE-001
status: draft
owner: human
created: 2026-08-14
---

# Story: 用户可以选择多个实例并批量修改

作为 ECS 用户，
我希望能够一次选择多个实例，
以便批量修改实例配置。
```

状态机：

```
draft → analyzing → needs_clarification → refining → ready_for_spec
→ specifying → spec_approved → implementing → verifying → completed
```

状态不能跳级。`draft` 不能直接到 `implementing`，必须经过 `spec_approved`。

### 2. Spec

Spec 是结构化的 Specification Model，不是普通 Markdown 文件。

```yaml
spec:
  id: SPEC-001
  story: US-001
  status: draft  # draft → candidate → approved → invalidated

  behaviors:
    - id: B-001
      description: "用户选择多个实例并执行批量修改时，系统必须向所有有权限的实例提交修改请求"

  constraints:
    - id: C-001
      description: "用户没有目标实例权限时，系统不得执行修改"

  invariants:
    - id: I-001
      description: "未经授权的资源永远不能被修改"

  acceptance_criteria:
    - id: AC-001
      given: "用户选择 3 个有修改权限的实例"
      when: "执行批量修改"
      then: "3 个实例均进入修改流程"

  open_questions:
    - id: Q-001
      question: "Workspace 生命周期是什么？"
      options: [task, agent, permanent]
      status: unresolved

  decisions:
    - id: DEC-001
      question: "Workspace 生命周期是什么？"
      selected: task
      decided_by: human
      reason: "Workspace 与任务上下文绑定"

  assumptions:
    - id: A-001
      description: "假设 Workspace 默认持久化"
      status: inferred  # confirmed | inferred | unresolved
```

Spec Uncertainty 规则：LLM 不得把推测伪装成已确认的 Spec。每条信息必须标注 status：
- `confirmed`：人类确认
- `inferred`：LLM 推测
- `unresolved`：未解决

### 3. Agent 角色

RDD MVP 中不实现多 Agent，而是由一个 Agent 按阶段切换角色：

| 阶段 | 角色 | 职责 |
|:---|:---|:---|
| Requirement Engineering | Requirement Analyst | 解析 RR，拆分 Feature/Story，识别边界，提出澄清问题 |
| Specification Engineering | Spec Writer | 从 Story 提取 Behavior/Constraint/Invariant，维护 Spec，发现 Gap |
| Test Design | Test Designer | 从 Spec 生成 AC（测试契约），发现边界条件；**不产 TEST-*.md 描述文件**，测试代码在 Implementation 与产品代码同写 |
| Implementation | Implementer | 根据 Spec 写代码，写单元测试（AC 为契约） |
| Verification | Verifier | 运行测试 + 经验性验证，验证 Spec 是否被正确实现 |

### 4. Traceability

每个文件都记录 parent 关系，形成可追溯链：

```
RR-001 → FE-001 → US-001 → SPEC-001 → AC-001 → CODE
```

正向追踪：需求 → 代码（这段代码为什么存在？）
反向追踪：代码 → 需求（这个需求实现在哪里？）

**追溯的载体**：solo-dev 用 commit message（feature ID in subject，`git log --grep`）为主，.rdd/ 文件链为辅；多人/跨会话才用完整 work-item 文件链。详见 "Git 作为产物库"。

### 5. Decision

Decision 是一等公民。所有影响业务语义的决策必须记录为 Decision Artifact。

```yaml
decision:
  id: DEC-001
  question: "Workspace 生命周期是什么？"
  options: [task, agent, permanent]
  selected: task
  decided_by: human
  reason: "Workspace 与任务上下文绑定"
  status: frozen
```

frozen 的 Decision 不需要重新讨论，后续 Agent 直接读取。

## 执行流程

### Step 1: 接收 RR

用户提供一个原始需求。Agent 创建 RR Work Item：

```
输入：用户的自然语言需求
输出：RR-001.md（Work Item 文件）
动作：
1. 创建 .rdd/items/RR-001.md
2. 设置 status = analyzing
3. 识别需求来源、业务目标、范围
4. 列出未确定事项
```

### Step 2: Requirement Engineering

```
输入：RR-001
输出：FE-001.md + US-001.md（+ 可能的 US-002 等）
动作：
1. 分析 RR，拆分为 Feature
2. Feature 拆分为 Story（符合 INVEST 原则）
3. 识别跨团队协作需求（如有）
4. 提出 Open Questions
5. 等待 Human 确认后再继续
```

Human-in-the-loop：Agent 提出问题，Human 决策。Agent 不替 Human 做产品决策。

### Step 3: Specification Engineering

```
输入：US-001（status = ready_for_spec）
输出：SPEC-001.md
动作：
1. 从 Story 提取 Behavior
2. 定义 Constraint 和 Invariant
3. 定义 Acceptance Criteria（Given/When/Then）
4. 标注每条信息的 uncertainty status
5. 列出 Open Questions 和 Assumptions
6. Spec Discovery Loop：发现 Gap → 提问 → Human 决策 → Refine
7. Spec 达到可测试状态后 → status = approved
```

### Step 4: Test Design（并入 Implementation，不单独产文件）

AC 即测试契约——Spec 批准后不另产 `TEST-*.md` 描述文件（"测试代码是价值，TC 标签是描述的描述"）。测试代码在 Step 5 与产品代码同写。

```
输入：SPEC-001（status = approved，含 AC）
动作：
1. 检查每个 AC 是否可测试（不可测试 = Spec 不够明确，回 Step 3）
2. 发现边界条件 → 补 AC
3. 列出测试要点（可写在 SPEC 的 AC 里，不另起文件）
```

### Step 5: Implementation

```
输入：SPEC-001（AC 为测试契约）
输出：Code + 测试代码
动作：
1. 根据 Spec 制定 Implementation Plan
2. 写代码 + 写测试（每个 AC 落一个测试，与产品代码同提交）
3. 如果发现 Spec 问题 → 返回 SPECIFICATION_BLOCKED，不自行修改业务语义
```

### Step 6: Verification

```
输入：Code + 测试代码
输出：Verification Result
动作：
1. 运行测试
2. 经验性验证（见 Verification 阶段）
3. Pass → completed
4. Fail → Refine Spec → 回到 Step 3
```

## Workspace 结构

全链条理想结构（Lite/Solo-dev 通道会缩减，见对应章节）：

```
.rdd/
├── items/           # Work Items（.md）
│   ├── RR-001.md
│   ├── FE-001.md
│   ├── US-001.md        # Lite 通道可内联进 FE，不单开
│   ├── SPEC-001.md      # 含 AC（测试契约），不另产 TEST-001
│   └── DEC-001.md       # 仅 frozen 跨特性决策；feature 级决策折进 SPEC
├── traceability.yml  # 仅多人/跨会话需要；solo-dev 用 git log --grep
└── state.yml          # session-only，不入库（gitignore）
```

## Spec Discovery Loop

Spec 不是一次 LLM Generation 的结果，而是一个收敛状态：

```
Candidate Spec
  ↓ Analyze
  ↓ Discover Missing Information
  ↓ Generate Questions（批量，见下）
  ↓ Human Decision
  ↓ Refine Spec
  ↓ Detect Gaps
  ↓ Refine Spec
  ↓ Validated Spec
```

当所有 Open Questions 解决、所有 Assumptions 确认、所有 AC 可测试时，Spec 才达到 `approved` 状态。

### Open Questions 批量收敛

别一个一个问——那会让 Human 在 Spec 阶段反复 ping-pong。把一个阶段发现的所有 gap 收集起来：

1. 按 **blocking**（不决就不能进下一步）vs **非 blocking**（可在 Spec Discovery Loop 内继续收敛）分组
2. 一次提 3-4 个，每个给**推荐项**（让 Human 一键采纳，而非开放式作答）
3. blocking 先决，决完再写 SPEC；非 blocking 在写 SPEC 时作为 unresolved 标注，下一轮批量问
4. Human 决完一批再继续，不要每发现一个 gap 就打断

实战参考：一次三 Epic 的需求收敛，13 个 open question 分 4（blocking）+ 3（per-feature）+ 1 三轮问完，没有 ping-pong。

## 已有系统上的特性开发

RDD 不仅适用于新项目。实际大部分需求是在已有系统上加特性。

### 三种场景路径

RDD 根据变更类型选择不同流程密度：

**场景 A：增量改进**（修改现有模块，保留旧代码）
```
existing + RR → Impact Analysis → Spec Reconstruction → 正常全链条
```

**场景 B：整体替换**（删除旧模块，用新实现替代）
```
existing + RR → Impact Analysis（只记旧行为作为回归基线，不反推旧 Spec）
→ Spec 从新行为派生（不 Spec Reconstruction 旧代码）
→ 旧行为标 superseded
→ 正常 Spec → Test → Implementation → Verification
```

**场景 C：轻量变更**（小改动、bugfix）
```
RR → 简化 Spec（一个文件，不拆 US/FE）→ 直接实现 → 验证
跳过：US 拆分、Spec Reconstruction、Traceability ID 嵌入
```

Agent 在接收 RR 后先判断属于哪种场景，默认 A，明确替换选 B，小改动选 C。

判定判据（信号而非硬阈值）：
- **场景 C 轻量**：单文件改动 / bugfix / 一两个 AC，调用方不变
- **场景 A 增量**：保留既有调用方与公开 API，新增或修改行为；既有 Spec 仍适用
- **场景 B 替换**：删除整个模块，或改写 >50% 公开 API 且不保留旧调用方

边界情况（如"重写一个函数的实现但保留调用方签名"）默认 A——**调用方保留即视为增量**，只有连调用方都删/换才是 B。这避免把"重写 saveMemory 函数体"误判成"替换 memory 子系统"。

### Spec Reconstruction

现有代码没有 Spec 时，从代码反向推导：
- 推导 Behavior/Constraint/Invariant，标注 `status=inferred`
- Human 确认后升级为 `confirmed`
- 不完美但比没有 Spec 好

### Impact Report

```yaml
impact:
  rr: RR-002
  affects: [src/agent.ts, src/task.ts]
  risk: low | medium | high
  constraints_to_check: [I-001, I-002]
  backward_compatible: true
  existing_specs: [SPEC-001]
  spec_gaps: [src/agent.ts 没有 Spec]
```

### 新旧 Spec 关系

```
SPEC-001 (现有) → modifies → SPEC-002 (新特性)
SPEC-002 → depends_on → SPEC-003 (被依赖)
SPEC-002 → violates → SPEC-001 (发现现有 Spec 有问题，触发 Refinement)
```

### 测试策略

- 新特性 AC → 新测试
- 现有行为回归测试（防止改坏）
- 现有代码没测试 → 先补测试再改

### 状态机入口

已有系统从 `analyzing` 开始，第一步是 Impact Analysis：

```
existing + RR → analyzing → Impact Analysis → Spec Reconstruction（如需要）→ 正常流程
```

### 渐进式 Spec 覆盖

不需要一次性补全所有 Spec：
- 第一次接触现有模块 → 补建相关 Spec（inferred）
- 后续每次接触 → 验证或推翻 inferred Spec
- 长期目标 → Spec 覆盖率逐步提升

## Anti-Patterns

- LLM 自己猜需求然后直接写代码（跳过 Spec）
- Spec 里不标注 uncertainty，把推测当确认
- Implementation Agent 自行修改业务语义
- Decision 只存在聊天记录里，不持久化
- 对整体替换场景做 Spec Reconstruction（被删代码反推 spec 是空转）
- 产物文件数与代码量不匹配（过重时应自动降级到 Lite / Solo-dev 通道）
- 把 Test 当独立 artifact 产 TEST-*.md 描述文件（测试代码才是价值，AC 即契约）
- 对"LLM 行为依赖"的特性只跑单测就声明通过（mock 掉 LLM 后证不了 LLM 真会那么做，必须真 LLM run）
- 一个一个问 Open Question 让 Human ping-pong（应批量 + 给推荐项）
- solo-dev 中小特性还产一堆 .rdd 文件（spec 写得进 commit body 就别产文件）

## 何时暂停等 Human（HITL 暂停时机）

Human-in-the-loop 不是"每步都停"，也不是"一口气跑到底"。结构化的暂停点：

1. **Step 2 末**：RR → FE → US + **blocking** Open Questions 批量提出后暂停。这是主暂停点——产品范围/架构岔路在这里定。
2. **每个 SPEC 写到出现非 blocking gap 时**：批量提（3-4 个，给推荐项），暂停。决完继续 Discovery Loop。
3. **SPEC approved 前**：所有 open question 解决、AC 可测，暂停让 Human 批准 spec → implementing。
4. **不暂停的时机**：写 SPEC 中间无 blocking gap 时别频繁打断；Implementation 阶段不暂停（除非 SPECIFICATION_BLOCKED）。

暂停时永远把问题**分组 + 给推荐项**，别开放式发问让 Human 写长答案。

每个 Work Item 声明保质期：

| 保质期 | 含义 | 代码落地后 |
|:---|:---|:---|
| `permanent` | 长期存活的规格 | 保留，后续迭代引用 |
| `migration-only` | 迁移脚手架 | 自动标记归档，吐 cleanup 清单 |
| `session-only` | 临时分析产物 | 代码落地后删除 |

Feature 完成时，Agent 自动产出 cleanup 清单：哪些产物该归档、哪些该删除、哪些代码注释里的 Traceability ID 需要剥离。

## Traceability ID 嵌入策略

默认**不**把 ID 嵌入代码注释。改为单 manifest 文件 `.rdd/links.yml` 映射 `file:line 区间 → AC id`。删 Spec = 删一个 manifest，不是 40 处注释。

若非要嵌入，Agent 必须带 `rdd detach` 子命令干净剥离所有 ID 引用。

## 状态机

状态机有两种模式：

- **enforce 模式**：配 pre-commit 检查器，`draft` 不能直接到 `implementing`
- **advisory 模式**：状态字符串仅供参考，不强制。Skill 默认 advisory，避免 aspirational 的状态机侵蚀产物可信度

## Verification 阶段

Verification 不仅仅是跑单测。最有价值的验证是经验性的：

- 跑真实 app（`pnpm dev` / `pnpm start`）
- 浏览器自动化测试（playwright-cli 点页面、截图）
- dev vs prod 性能对比
- 手动检查清单

测试代码是价值，TC 标签是描述的描述——不要本末倒置。

**LLM 行为依赖的特性要特殊对待**：当 spec 行为依赖 LLM 自主决策（如"LLM 主动调用 save_memory 工具"、"LLM 判断必要时才记"），单测 mock 掉了 LLM，反而掩盖"LLM 可能不调"的风险——单测只能证代码路径存在，证不了 LLM 真的会这么做。这类特性必须**真 LLM run**：发一个该触发的任务，确认 LLM 真的调了工具/做了判断；再发一个不该触发的（如闲聊），确认 LLM 没调。这才是 spec 的证据。

## Lite 通道

对轻量场景，缩减流程：

- RR 已经是一个 Feature 时 → 跳过 US 拆分
- SPEC + TEST 合为一个文件
- 不嵌入 Traceability ID
- 不拆 state.yml / traceability.yml
- 全链条留给真正模糊的 greenfield 需求

## Solo-dev 超轻量路径（零文件）

单人开发 + 中小特性，可跳过 .rdd 文件 altogether——spec 就是 commit message：

- **spec = commit message**：feature ID（如 `FE-001`）写在 commit subject，behaviors / AC / decisions 写在 commit body
- 不产 .rdd 文件；`git log --grep "FE-00"` 即可追溯需求 → 代码
- 仅 **frozen DEC + unresolved Open Questions** 落 `.rdd/items/`（如果有的话）——存"为什么这么决定"，不存"改了哪些文件"（git diff 有）

**适用**：1-2 个 AC、单/双文件、调用方清晰、solo dev。
**不适用**：跨会话多人协作、>3 feature 的 epic、模糊到需要 Spec Discovery Loop 多轮收敛——这些用正常 .rdd 全链条。

判断信号：如果 spec 写得进一个 commit message body（<500 字），用超轻量；写不进，用文件。这条路径把"要不要带 .rdd 进 git"的纠结消掉——单人中小特性根本不产 .rdd。

## Git 作为产物库（追溯主次）

单人开发下，一堆带 frontmatter 的 YAML 经常重复 commit message 已记的东西。明确追溯双轨的主次：

- **主：commit message**——feature ID 写在 subject（`feat: ... FE-001 ...`），decisions/AC 写在 body。`git log --grep "FE-00"` 即可追溯需求 → 代码。这是 solo-dev 的首选追溯。
- **辅：`.rdd/items/` 的 frozen DEC + unresolved Open Questions**——只存"为什么这么决定"（why），不存"改了哪些文件/在哪"（what/where，git diff --stat 有）。
- **不要重复**：别在 .rdd/IMPACT 或 traceability.yml 里再列 affected files——`git diff --stat <commit>` 已经有。traceability.yml 仅在多人/跨会话需要 work-item 链时才产。

实操：
- `docs/specs/` 两三篇真文档 + commit message 扛住 80% 价值
- Decision 默认写 commit message；仅 frozen 跨特性的架构决策单独落 DEC
- 不为 traceability 产出额外文件，用 `git log --grep` 查

## 文件模板

见 `references/templates.md`（RR / Spec / Traceability 模板）。全链条用；Lite 通道内联 Story 进 FE；Solo-dev 超轻量路径用 commit message 代替文件。

## 使用方式

1. 用户提供原始需求（自然语言）
2. Agent 先判场景（A 增量 / B 替换 / C 轻量）+ 判 solo-dev 超轻量是否适用
3. 按 RDD 流程执行；solo-dev 超轻量路径下 spec 写进 commit message，不产 .rdd 文件
4. blocking 阶段批量提出 Open Questions（给推荐项）后暂停，等 Human 决策
5. 全链条下文件存 `.rdd/items/`；state.yml 不入库
6. 最终产出可追踪的代码 + 测试（AC 为契约）+ 规格文档（文件或 commit body）

## 验证路径

用一个真实需求端到端验证：

```
RR-001："为 Agent 增加 Workspace。"
```

如果这条链能跑通（RR → Story → Spec（含 AC）→ Code + 测试 → Verified），RDD MVP 就验证成功。注意验证环节对"LLM 自主行为"的特性要用真 LLM run，不能只跑单测。
