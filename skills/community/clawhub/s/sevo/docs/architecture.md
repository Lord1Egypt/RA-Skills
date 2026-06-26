# SEVO — arc42 架构文档

Claude Code（OpenClaw ACP Agent）| 2026-04-24

---

## 目录

1. [引言与目标](#1-引言与目标)
2. [约束](#2-约束)
3. [上下文与边界](#3-上下文与边界)
4. [解决方案策略](#4-解决方案策略)
5. [构建块视图](#5-构建块视图)
6. [运行时视图](#6-运行时视图)
7. [部署视图](#7-部署视图)
8. [横切关注点](#8-横切关注点)
9. [架构决策](#9-架构决策)
10. [质量需求](#10-质量需求)
11. [风险与技术债务](#11-风险与技术债务)
12. [术语表](#12-术语表)

---

## 1. 引言与目标

### 1.1 需求概述

SEVO（Spec-Execute-Verify-Operate）是 Agent 自动研发流水线。它把散落在 AGENTS.md 的流程规则固化为代码级状态机，保障全研发生命周期产出质量——从需求定义、架构设计到验证发布全流程自动化。

当前 AI Coding 工具只覆盖"写代码"环节。SEVO 的定位是把 Specify → Execute → Verify → Operate 四个阶段串成可编程、可审计、可自动推进的流水线，让 vibe coding 用户获得完整的研发质量保障。

### 1.2 质量目标

| 优先级 | 质量属性 | 目标 |
|--------|----------|------|
| 1 | 可控性 | 每个阶段有明确的门禁（Gate），不满足条件不放行 |
| 2 | 可审计性 | 全流程事件追踪，Ledger 记录每次流水线执行的完整证据链 |
| 3 | 通用性 | 核心状态机不绑死 OpenClaw，通过 Host Adapter 接入任意 Agent 宿主 |
| 4 | 可靠性 | 插件层 fail-open，核心引擎 fail-safe；单模块故障不拖垮整条流水线 |
| 5 | 可扩展性 | 阶段可配置（跳过/新增），门禁规则可插拔，Agent 映射可覆盖 |

### 1.3 利益相关者

| 角色 | 关注点 |
|------|--------|
| 用户（产品负责人） | 研发质量可见、进度透明、不需要手动推进流水线 |
| OpenClaw 主会话 | 通过 hook 接收流水线事件，自动派发下一阶段任务 |
| 子 Agent（编码/审计/架构/PM） | 接收阶段任务 prompt，产出 artifact，结果回流流水线 |
| KIVO（知识引擎） | 消费 Ledger 产出的结构化研发记录，沉淀为可复用知识 |
| AEO（效果运营） | 监控流水线执行指标，发现效果漂移 |

---

## 2. 约束

### 2.1 技术约束

| 约束 | 原因 |
|------|------|
| TypeScript 核心 + JS 插件 | 核心库（projects/sevo/src/）用 TS 编译为 JS；插件层（extensions/sevo-pipeline/）直接 JS，与 OpenClaw 插件体系一致 |
| 核心不绑死单一宿主，但主动复用宿主高价值能力 | SOUL.md 核心设计原则：通用优先 + Host Adapter 模式 |
| Stage-Bound Design | 能力/规范绑定流程阶段，不绑定特定 Agent 身份（AGENTS.md §核心设计原则） |
| 单文件状态持久化（state.json） | 单 writer 模型，避免并发写冲突；事件日志 append-only（events.jsonl） |
| 插件层 fail-open | 所有 hook handler 包裹 try-catch，错误记录但不阻断宿主调度 |

### 2.2 组织约束

| 约束 | 原因 |
|------|------|
| SEVO 流水线强制 | 新建模块、跨域改动、>500 行或 >10 文件、数据模型变更必须走完整 SEVO 流水线 |
| 开发与审计分离 | 编码 Agent 不做自审，审计由独立 Agent 执行 |
| 长文档分段写作 | >300 行文档必须分段派发，降低单次写入失败风险 |
| 研发流程改进双写 | 每条改进同时落地到 AGENTS.md（L6 临时兜底）和 SEVO 产品层（L1/L2 永久固化） |

### 2.3 惯例约束

| 约束 | 原因 |
|------|------|
| 意图路由必须走 LLM | SOUL.md 术语纪律：禁止用关键词匹配实现意图理解 |
| 文件产出强制 | 任务要求写文件时必须实际写入磁盘，只在回复中输出 = 任务失败 |
| AC 逐条覆盖 | 编码任务必须逐条对照验收标准，审计只做质量把关不做需求补漏 |

---

## 3. 上下文与边界

### 3.1 业务上下文

```
┌──────────────────────────────────────────────────────────────┐
│                      用户（产品负责人）                         │
│              提出需求 / 做重大决策 / 最终验收                    │
└──────────────────────┬───────────────────────────────────────┘
                       │ 需求描述
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   OpenClaw 主会话（调度层）                     │
│  接收用户消息 → 判断意图 → 触发 SEVO → 按流水线自动推进         │
└──────┬──────────────┬──────────────┬─────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  SEVO 核心  │ │   KIVO     │ │    AEO     │
│  研发流水线  │ │  知识引擎   │ │  效果运营   │
└──────┬─────┘ └────────────┘ └────────────┘
       │
       │  派发阶段任务 / 收集 artifact / 门禁评估
       ▼
┌──────────────────────────────────────────────────────────────┐
│                    Agent 执行层                                │
│  PM(pm-01) | 架构师(sa-01) | 编码(cc/free-code/dev-*)        │
│  审计(audit-01/02) | UX(ux-01)                               │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 技术上下文

| 外部系统 | 交互方式 | 协议 |
|----------|----------|------|
| OpenClaw Gateway | 插件 hook（subagent_ended / before_prompt_build / before_tool_call） | JS Plugin API |
| OpenClaw sessions_spawn | 通过 Host Adapter 派发子 Agent 任务 | Gateway RPC |
| 文件系统 | state.json / events.jsonl / artifact 文件 | POSIX FS |
| KIVO | Ledger 产出 → KIVO 知识入库（未来集成） | API / 文件 |
| AEO | 流水线指标 → AEO 监控（未来集成） | API / 文件 |

### 3.3 系统边界（明确不做）

- 不做 Agent 调度（调度是 OpenClaw 主会话的职责，SEVO 只定义"下一步该做什么"）
- 不做代码编辑/编译/测试执行（这些是 Agent 执行层的能力）
- 不做用户认证/权限管理
- 不做实时通信（通知通过 Host Adapter 委托宿主完成）
- 不做知识管理（KIVO 的职责）

---

## 4. 解决方案策略

| 策略 | 决策 | 理由 |
|------|------|------|
| 状态机驱动 | 12 阶段有限状态机，每个阶段有明确的状态转换规则 | 把 AGENTS.md 的文字规则变成可编程、可验证的状态约束 |
| 三级路由 | L0（跳过）/ L1（轻量）/ L2+（完整），按任务规模自动分级 | 小改动不走完整流水线，大改动强制全流程 |
| 规模路由 | Tier 1（直接执行）/ Tier 2（轻量含审计）/ Tier 3（完整 15 阶段） | 进一步细化路由粒度，琐碎操作不创建流水线 |
| Gate 规则可插拔 | GateRule SPI，内置 FileExists/TypeCheck/TestPass/MinCoverage，可扩展 | 不同阶段的质量标准不同，规则需要灵活组合 |
| Host Adapter 模式 | 核心通用 + OpenClawAdapter / StandaloneAdapter | 核心不绑死 OpenClaw，但主动复用其 hook/session/notification 能力 |
| Spec Review 后并行分叉 | spec-review-gate 通过后，test-case-authoring 和 contract 并行启动 | 缩短流水线总耗时，两个活动无依赖 |
| Clarification 协调 | 阶段执行中发现歧义 → 阻塞当前阶段 → 收集澄清 → 恢复 | 避免带着歧义继续执行导致返工 |
| Ledger 审计账本 | 流水线完成后收集全部 artifact + stage record，写入不可变 Ledger | 提供完整的研发过程证据链 |
| 事件溯源 | events.jsonl append-only，state.json 单 writer | 支持事后审计和状态重建 |

---

## 5. 构建块视图

### 5.1 Level 1 — 系统分解

SEVO 由两层组成：核心库（通用）和插件层（OpenClaw 特化）。

```
┌─────────────────────────────────────────────────────────────────┐
│                     SEVO 系统                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              核心库 (projects/sevo/src/)                  │    │
│  │                                                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │    │
│  │  │  Router   │  │ Pipeline │  │   Gate   │  │ Ledger  │ │    │
│  │  │  路由器   │  │  Engine  │  │  Engine  │  │  Engine │ │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │    │
│  │  │Orchestr- │  │ Context  │  │Clarific- │              │    │
│  │  │  ator    │  │ Injector │  │  ation   │              │    │
│  │  └──────────┘  └──────────┘  └──────────┘              │    │
│  │  ┌──────────────────────────────────────────┐           │    │
│  │  │         Adapter Layer                     │           │    │
│  │  │  OpenClawAdapter  |  StandaloneAdapter    │           │    │
│  │  └──────────────────────────────────────────┘           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           插件层 (extensions/sevo-pipeline/)              │    │
│  │                                                          │    │
│  │  index.js ── bridge.js ── task-mapper.js ── methodology.js │    │
│  │              label-protocol.js                           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Level 2 — 核心库模块职责

#### Router（路由器）

位置：`src/router/`

职责：接收任务描述，根据触发规则判定流水线级别（L0/L1/L2+），输出所需阶段列表和跳过阶段列表。

核心文件：
- `stage-router.ts` — 路由入口，组合 level-classifier 和 stage-graph
- `level-classifier.ts` — 根据 TaskScope 判定 TaskLevel
- `stage-graph.ts` — 定义阶段依赖图，根据 level 裁剪阶段列表
- `stage-context.ts` — 阶段上下文信息封装
- `router.ts` — 对外暴露的 `route()` 函数

关键类型：
```typescript
type TaskLevel = 'L0' | 'L1' | 'L2+';
type TriggerRule = 'new-module' | 'cross-domain' | 'large-change'
  | 'data-model-change' | 'governance-change'
  | 'release-target-change' | 'user-explicit';

interface RoutingResult {
  taskId: string;
  level: TaskLevel;
  requiredStages: StageId[];
  skippedStages: SkippedStage[];
  matchedRules: TriggerRule[];
}
```

触发规则（命中任一即 L2+ 完整流水线）：
- 从零新建模块（new-module）
- 跨域改动（cross-domain，涉及 2+ 域）
- 大型变更（large-change，>500 行或 >10 文件）
- 数据模型变更（data-model-change）
- 治理规则变更（governance-change）
- 发布目标变更（release-target-change）
- 用户显式要求（user-explicit）

规模路由（FR-D08）：

Router 在收到需求后先评估规模，自动选择执行档位：

| 档位 | 适用场景 | 阶段集 | 项目目录 |
|------|----------|--------|----------|
| Tier 1（直接执行） | 改配置、查状态、单文件修复 | 不创建流水线 | 不创建 |
| Tier 2（轻量流水线） | 小功能、脚本、局部改动 | spec → implement → review → verify → ledger | 在现有目录中工作 |
| Tier 3（完整流水线） | 新产品、新模块、跨域改动 | 完整 15 阶段 | projects/\<slug\>/ |

Tier 2 必须包含 review（审计），保障最低质量门禁。用户可通过 `sevo:create my-tool --tier 2` 强制指定档位。

#### Pipeline Engine（流水线引擎）

位置：`src/pipeline/`

职责：管理流水线实例的创建、阶段状态转换、并行分叉、持久化。这是 SEVO 的核心状态机。

核心文件：
- `stage-machine.ts` — 阶段状态转换规则（有限状态机）
- `parallel-branch.ts` — Spec Review 通过后的并行分叉逻辑
- `pipeline-create.ts` — 流水线实例创建（FR-12）
- `directory-init.ts` — 项目目录结构初始化
- `instance-id.ts` — 实例 ID 生成

状态转换规则：
```
pending → active | skipped
active  → passed | failed | blocked | clarification-blocked
blocked → active                    (解除阻塞)
clarification-blocked → active      (澄清完成)
failed  → active                    (修复后重试)
passed  → (终态)
skipped → (终态)
```

12 个阶段的完整序列：
```
spec → spec-review-gate → [test-case-authoring ∥ contract] →
contract-review-gate → implement → review → regression →
publish-generalization-gate → deploy → verify → ledger
```

其中 `∥` 表示 spec-review-gate 通过后 test-case-authoring 和 contract 并行启动。

#### Gate Engine（门禁引擎）

位置：`src/gate/`

职责：评估阶段门禁，聚合多维度审查结论，输出 passed/conditional/rejected 裁决。

核心文件：
- `gate-engine.ts` — 门禁评估入口
- `gate-rule.ts` — GateRule SPI 接口定义
- `built-in-rules.ts` — 内置规则：FileExistsRule / TypeCheckRule / TestPassRule / MinCoverageRule
- `verdict-aggregator.ts` — 多 ReviewBundle 聚合为最终裁决
- `review-role-assigner.ts` — 根据阶段确定所需审查角色

关键类型：
```typescript
type GateConclusion = 'passed' | 'conditional' | 'rejected';

interface GateVerdict {
  gateId: string;
  conclusion: GateConclusion;
  blockers: { item: string; owner: string }[];
  reviewBundles: ReviewBundle[];
}
```

门禁裁决语义：
- `passed` — 放行，自动推进到下一阶段
- `conditional` — 有条件通过，列出必须解决的问题，修复后重新评估
- `rejected` — 不通过，回退到上一阶段重做

#### Ledger Engine（审计账本）

位置：`src/ledger/`

职责：流水线完成后收集全部 artifact 和 stage record，写入不可变的 Ledger 条目，提供查询接口。

核心文件：
- `ledger-engine.ts` — Ledger 读写入口
- `artifact-collector.ts` — 从各阶段收集 artifact 引用

关键类型：
```typescript
interface LedgerEntry {
  pipelineId: string;
  version: string;
  createdAt: string;
  scope: string;
  stages: StageRecord[];
  conclusion: 'delivered' | 'aborted';
  evidence: ArtifactRef[];
  clarificationRefs?: ArtifactRef[];
}
```

#### Task Orchestrator（任务编排器）

位置：`src/orchestrator/`

职责：组合 Router + Pipeline Engine + Gate Engine，提供高层 API：startPipeline → evaluateAndAdvance → getPipelineStatus。

核心文件：
- `task-orchestrator.ts` — 编排入口，串联路由→创建→推进→门禁
- `pipeline-run.ts` — 单次流水线运行的状态封装
- `orchestrator-events.ts` — 编排器事件定义（PipelineStarted / StageEntered / GateEvaluated / StageAdvanced / PipelineCompleted / PipelineFailed）

#### Context Injector（上下文注入器）

位置：`src/context-injection/`

职责：根据当前阶段，向 Agent 任务 prompt 注入流水线上下文（前序 artifact 路径、阶段要求、质量标准）。

#### Clarification Coordinator（澄清协调器）

位置：`src/clarification/`

职责：阶段执行中发现歧义时，阻塞当前阶段，收集澄清问题，协调解决后恢复执行。

核心文件：
- `clarification-coordinator.ts` — 澄清流程协调
- `clarification-record.ts` — 澄清记录持久化
- `ambiguity-detector.ts` — 歧义检测规则
- `clarification-manager.ts` — 澄清生命周期管理

#### Adapter Layer（适配层）

位置：`src/adapter/`

职责：将核心库的抽象操作（派发任务、收集 artifact、发送通知）映射到具体宿主环境。

```typescript
interface SevoHostAdapter {
  dispatchTask(stage: StageId, payload: TaskPayload): Promise<string>;
  collectArtifacts(taskId: string): Promise<ArtifactRef[]>;
  notifyGateResult(stage: StageId, verdict: GateVerdict): void;
  getProjectConfig(): ProjectConfig;
  analyzeRequirements?(input: RequirementAnalysisRequest): Promise<RequirementAnalysisResponse>;
}
```

两个实现：
- `OpenClawAdapter` — 通过 OpenClaw Gateway Plugin API 派发任务、收集 artifact、发送飞书通知
- `StandaloneAdapter` — 独立运行模式，用于测试和非 OpenClaw 环境

#### Stage 实现层

位置：`src/stages/`

职责：每个阶段的具体行为定义（输入/输出类型、执行逻辑、验收标准）。

已实现的阶段：

| 阶段 | 文件 | 职责 |
|------|------|------|
| spec | spec-stage.ts | 需求规格编写，输出 product-requirements.md |
| contract | contract-stage.ts | 架构设计，输出 arc42 + ADR |
| test-case | test-case-stage.ts | 测试用例编写，基于冻结 spec |
| implement | implement-stage.ts | 编码实现，按 spec + arc42 执行 |
| debugging | debugging-stage.ts | 调试阶段（review 发现问题后的修复循环） |
| review | review-stage.ts | 质量审计（代码质量/安全/spec 合规） |
| review-fix-loop | review-fix-loop.ts | 审计→修复→复验自动闭环 |
| regression | regression-stage.ts | 回归测试执行 |
| deploy | deploy-stage.ts | 部署执行 |
| verify | verify-stage.ts | 部署后验证（smoke test） |
| ledger | ledger-stage.ts | Ledger 记录写入 |
| publish-generalization-gate | publish-generalization-gate.ts | 发布前通用化检查（FR-08a） |

#### Gate 实现层

位置：`src/gates/`

职责：具体门禁的评估逻辑。

| 门禁 | 文件 | 评估维度 |
|------|------|----------|
| spec-review-gate | spec-review-gate.ts | 需求完整度、FR 边界清晰度、AC 可测试性 |
| contract-review-gate | contract-review-gate.ts | spec-架构对齐、ADR 完整性、部署可行性 |

### 5.3 Level 2 — 插件层模块职责

插件层是 SEVO 核心库在 OpenClaw 宿主中的运行时桥梁。

#### index.js（插件入口）

位置：`extensions/sevo-pipeline/index.js`（3143 行）

职责：注册 3 个 OpenClaw hook，实现流水线自动推进。

Hook 注册：

| Hook | 优先级 | 触发时机 | 行为 |
|------|--------|----------|------|
| subagent_ended | 200 | 子 Agent 任务完成 | 解析 SEVO label → 调用 PipelineEngine.advance() → 队列下一阶段 |
| before_prompt_build | 850 | 主会话构建 prompt 前 | 消费 pendingAdvances 队列 → 注入下一阶段任务指令到主会话 |
| before_prompt_build | 100 | 用户消息到达时 | 命令路由：解析 sevo:* 命令 → 执行对应 handler → 结果放入 pendingNotices |
| before_tool_call | 800 | 工具调用前 | 路由 sessions_spawn → 注入 SEVO label 到子 Agent 参数 |

运行模式：
- 启动时检查 SEVO dist/ 是否存在
- 存在 → active 模式，全部 hook 生效
- 不存在 → degraded 模式，大部分 hook 变为 no-op
- 降级模式下仍可用的命令：sevo:doctor、sevo:version、sevo:status、sevo:list（只读状态文件）

#### 命令系统

插件通过 `before_prompt_build`（priority 100）hook 路由用户消息中的 `sevo:*` 命令，路由到对应 handler。命令解析使用正则匹配，handler 执行结果放入 `pendingNotices` 队列，由 priority 850 的 hook 注入主会话 prompt。

命令清单：

| 命令 | 正则 | Handler | 降级可用 | 功能 |
|------|------|---------|----------|------|
| `sevo:create <slug> ["title"]` | `SEVO_CREATE_RE` | 创建完整流水线 | ❌ | 路由评估 → 创建 pipeline → 初始化项目目录 → 激活首阶段 |
| `sevo:quickstart` | `SEVO_QUICKSTART_RE` | 创建 7 阶段精简流水线 | ❌ | 内置 hello-sevo 示例项目，跳过三方会审 |
| `sevo:status [id]` | `SEVO_STATUS_RE` | 查询流水线状态 | ✅ | 无参数列出所有活跃流水线，有参数显示单个详情 |
| `sevo:list` | `SEVO_LIST_RE` | 列出历史流水线 | ✅ | 读取 active-pipelines.json |
| `sevo:doctor` | `SEVO_DOCTOR_RE` | 自检 | ✅ | 检查插件注册、hook、Agent 池、路径、写权限 |
| `sevo:version` | `SEVO_VERSION_RE` | 版本查询 | ✅ | 输出 SEVO_VERSION 常量 |
| `sevo:diagnose <id>` | `SEVO_DIAGNOSE_RE` | 深度诊断 | ❌ | 分析失败流水线的根因，输出结构化诊断报告 |
| `sevo:retry <id> [stage]` | `SEVO_RETRY_RE` | 重试失败阶段 | ❌ | 重新激活 failed 阶段，attempt 计数递增 |
| `sevo:pause <id>` | `SEVO_PAUSE_RE` | 暂停流水线 | ❌ | 设置 info.status='paused'，记录 pausedAt |
| `sevo:skip <id> <stage>` | `SEVO_SKIP_RE` | 跳过阶段 | ❌ | 标记阶段 skipped，自动激活下一阶段 |
| `sevo:resume <id>` | `SEVO_RESUME_RE` | 恢复流水线 | ❌ | 清除 paused 状态，从暂停点继续 |

命令路由流程：
```
用户消息 → before_prompt_build(priority 100)
  → extractUserMessage(evt)
  → 按优先级匹配正则（doctor/version 最先，create 最后）
  → 匹配成功 → 调用 handler → 结果 push 到 pendingNotices
  → before_prompt_build(priority 850) 消费 pendingNotices → 注入主会话 prompt
```

#### bridge.js（桥接层）

位置：`extensions/sevo-pipeline/bridge.js`

职责：懒加载 SEVO TypeScript 编译产物（dist/），提供 PipelineEngine / LedgerEngine / route 的运行时访问。

特性：
- 模块级缓存 + TTL 过期（默认 30s）
- 文件 mtime 变化检测，自动重新加载
- 单模块故障不影响其他模块（per-module failure isolation）
- 加载失败后 backoff，避免频繁重试

#### task-mapper.js（任务映射器）

位置：`extensions/sevo-pipeline/task-mapper.js`

职责：将 StageId 映射为具体的 Agent 任务描述（prompt），包含前序 artifact 引用和阶段要求。

默认阶段→Agent 映射：

| 阶段 | 梯队 | 默认 Agent | 超时 |
|------|------|-----------|------|
| spec | PM | pm-01 | 1800s |
| spec-review-gate | 架构 | sa-01 | 1200s |
| test-case-authoring | 审计 | audit-01 | 1200s |
| contract | 架构 | sa-01 | 3600s |
| contract-review-gate | 审计 | audit-01 | 1200s |
| implement | T1 | (auto) | 1200s |
| review | 审计 | audit-01 | 1200s |
| regression | T1 | (auto) | 1200s |
| publish-generalization-gate | 架构 | sa-01 | 1200s |
| deploy | T1 | (auto) | 600s |
| verify | 审计 | audit-01 | 600s |
| ledger | T4 | dev-01 | 600s |

映射可通过 `state/config.json` 或插件配置覆盖（Stage-Bound Design：绑定阶段不绑定 Agent 身份）。

#### methodology.js（方法论模块）

位置：`extensions/sevo-pipeline/methodology.js`

职责：为每个流水线阶段提供方法论指导 prompt，由 task-mapper.js 在构建 task prompt 时 spread 注入。

导出函数（9 个，对应 9 类阶段方法论）：

| 函数 | 注入阶段 | 方法论要点 |
|------|----------|-----------|
| specMethodology() | spec | 批判性思维、第一性原理、概念架构隔离、Phase 隔离（禁止技术选型） |
| contractMethodology() | contract | arc42 模板、ADR 纪律、Gate Check 7 项 |
| specReviewGateMethodology() | spec-review-gate | 7 维发散审查、交叉审计、三档结论 + 用户体验流完整性（第 9 维度） |
| contractReviewGateMethodology() | contract-review-gate | 三方独立视角、7 维发散审查、综合裁决 |
| reviewMethodology() | review | OWASP Top 10:2025、git diff-aware、置信度阈值 |
| implementMethodology() | implement | 最小改动、最简实现、目标驱动执行 |
| testCaseAuthoringMethodology() | test-case-authoring | AC 覆盖规则、边界值、负面路径、优先级分级 |
| smokeTestMethodology() | smoke-test | 端到端用户视角、独立验证者、证据附带 |
| getUserJourneyTemplate() | spec + ux-acceptance | 6 阶段用户体验旅程模板 |

`getUserJourneyTemplate()` 返回结构化用户旅程模板，覆盖 6 个阶段：

| 阶段 ID | 名称 | 审查问题示例 |
|---------|------|-------------|
| discover | 发现与获取 | 用户从哪里找到产品？获取方式是什么？ |
| install | 安装与配置 | 能一条命令完成吗？零配置能跑吗？ |
| first-use | 首次使用 | 5 分钟内能看到第一个成功结果吗？ |
| core-flow | 核心流程 | 主要功能的完整使用流程是什么？ |
| error-recovery | 错误恢复 | 错误信息能指导用户修复吗？ |
| upgrade | 升级与维护 | 升级会不会破坏已有配置？ |

注入点：spec 阶段要求 PM agent 在 spec 中画出完整用户旅程；spec-review-gate 将"用户体验流完整性"作为硬性审查维度（缺失 = P0 阻断）；ux-acceptance 阶段要求 UX agent 按流程逐步验收。

注入机制：task-mapper.js 的 `STAGE_PROMPTS` 中通过 `...specMethodology()` 等 spread 语法将方法论 string[] 追加到阶段 prompt 末尾。方法论内容集中管理，阶段 prompt 与方法论解耦。

#### label-protocol.js（标签协议）

位置：`extensions/sevo-pipeline/label-protocol.js`

职责：编码/解码 SEVO 流水线信息到 session label。

格式：`sevo:<pipelineId>:<stageId>[:<attempt>]`

用途：子 Agent session 通过 label 携带流水线上下文，completion event 到达时据此路由回正确的流水线实例。

---

## 6. 运行时视图

### 6.1 场景一：新建流水线（Happy Path）

```
用户                 OpenClaw 主会话              SEVO 插件层              SEVO 核心
 │                       │                          │                      │
 │  "新建 XX 模块"       │                          │                      │
 │──────────────────────>│                          │                      │
 │                       │  判断意图 → 触发 SEVO     │                      │
 │                       │─────────────────────────>│                      │
 │                       │                          │  bridge.getRoute()   │
 │                       │                          │─────────────────────>│
 │                       │                          │                      │ route(taskScope)
 │                       │                          │                      │ → RoutingResult
 │                       │                          │                      │   {level: L2+,
 │                       │                          │                      │    requiredStages: [...]}
 │                       │                          │<─────────────────────│
 │                       │                          │  getPipelineEngine() │
 │                       │                          │─────────────────────>│
 │                       │                          │                      │ engine.create(routing)
 │                       │                          │                      │ → atomicWrite(state.json)
 │                       │                          │                      │ → appendEvent(pipeline_created)
 │                       │                          │                      │ → activateNext() → spec=active
 │                       │                          │<─────────────────────│
 │                       │                          │  queue pendingAdvance│
 │                       │                          │  (spec, pm-01)       │
 │                       │  before_prompt_build      │                      │
 │                       │<─────────────────────────│                      │
 │                       │  注入 spec 阶段任务指令    │                      │
 │                       │  sessions_spawn(pm-01)    │                      │
 │                       │─────────────────────────>│                      │
 │                       │                          │  before_tool_call    │
 │                       │                          │  注入 sevo label     │
 │                       │                          │  → sevo:<pid>:spec:1 │
 │                       │<─────────────────────────│                      │
 │                       │  派发 pm-01 子 Agent      │                      │
```

关键步骤：
1. Router 根据 TaskScope 判定 level（L0/L1/L2+），输出 requiredStages 和 skippedStages
2. PipelineEngine.create() 原子写入 state.json，激活第一个阶段（spec）
3. 插件层将下一阶段任务放入 pendingAdvances 队列
4. before_prompt_build hook 消费队列，注入任务指令到主会话
5. before_tool_call hook 在 sessions_spawn 时注入 SEVO label

### 6.2 场景二：阶段推进（Stage Advance）

```
pm-01 子 Agent          OpenClaw Gateway            SEVO 插件层              SEVO 核心
 │                          │                          │                      │
 │  任务完成 (spec 产出)     │                          │                      │
 │─────────────────────────>│                          │                      │
 │                          │  subagent_ended event    │                      │
 │                          │─────────────────────────>│                      │
 │                          │                          │  decode(label)       │
 │                          │                          │  → pipelineId,       │
 │                          │                          │    stageId=spec      │
 │                          │                          │  engine.advance()    │
 │                          │                          │─────────────────────>│
 │                          │                          │                      │ record.status=passed
 │                          │                          │                      │ activateNext()
 │                          │                          │                      │ → spec-review-gate=active
 │                          │                          │<─────────────────────│
 │                          │                          │  queue pendingAdvance│
 │                          │                          │  (spec-review-gate)  │
 │                          │  before_prompt_build      │                      │
 │                          │<─────────────────────────│                      │
 │                          │  注入下一阶段任务          │                      │
```

推进逻辑：
1. subagent_ended hook 解码 label，识别流水线和阶段
2. 根据 evt.status 判定 outcome（passed/failed）
3. PipelineEngine.advance() 更新状态 + 激活后续阶段
4. 插件层队列化下一阶段任务，等待 before_prompt_build 注入

### 6.3 场景三：Gate 失败回退

```
audit-01 (review)       SEVO 插件层              SEVO 核心
 │                          │                      │
 │  spec-review-gate        │                      │
 │  结论: rejected          │                      │
 │─────────────────────────>│                      │
 │                          │  engine.advance()    │
 │                          │─────────────────────>│
 │                          │                      │ outcome=failed
 │                          │                      │ record.status=failed
 │                          │                      │ appendEvent(stage_failed)
 │                          │                      │ 不激活后续阶段
 │                          │<─────────────────────│
 │                          │                      │
 │                          │  pendingNotices +=    │
 │                          │  "[SEVO Rework Needed]│
 │                          │   stage spec-review-  │
 │                          │   gate failed"        │
 │                          │                      │
 │                          │  主会话收到通知 →      │
 │                          │  重新派发 spec 阶段    │
```

回退语义：
- Gate rejected → 当前 gate 阶段标记 failed，不激活后续阶段
- 插件层发出 rework notice，主会话据此重新派发前序阶段
- 修复后可通过 engine.activate() 重新激活 failed 阶段（failed → active 是合法转换）
- 重试时 attempt 计数递增，label 编码为 `sevo:<pid>:<stage>:<attempt>`

### 6.4 场景四：并行分叉与合并

```
spec-review-gate passed
         │
         ├──────────────────────┐
         ▼                      ▼
  test-case-authoring       contract
    (audit-01)              (sa-01)
         │                      │
         │                      ▼
         │              contract-review-gate
         │                (audit-01)
         │                      │
         └──────────┬───────────┘
                    ▼
               implement
          (需要两条分支都 passed)
```

并行规则（parallel-branch.ts）：
- spec-review-gate passed → 同时激活 contract 和 test-case-authoring
- contract-review-gate 只等 contract（不等 test-case-authoring）
- implement 需要 contract-review-gate passed；如果 test-case-authoring 未完成，implement 被 shouldBlockImplement() 阻塞
- 两条分支完全独立执行，由不同 Agent 并行处理

### 6.5 场景五：澄清阻塞与恢复

```
执行中 Agent              SEVO 核心                    用户/主会话
 │                          │                              │
 │  发现歧义                 │                              │
 │─────────────────────────>│                              │
 │                          │ scanClarifications()         │
 │                          │ → blocking=true              │
 │                          │ record.status=               │
 │                          │   clarification-blocked      │
 │                          │ appendEvent(                 │
 │                          │   clarification_opened)      │
 │                          │                              │
 │                          │  adapter.requestClarification│
 │                          │─────────────────────────────>│
 │                          │                              │ 用户回答
 │                          │  onClarificationResponse     │
 │                          │<─────────────────────────────│
 │                          │ resolve() →                  │
 │                          │   record.status=active       │
 │                          │ appendEvent(                 │
 │                          │   clarification_settled)     │
 │                          │                              │
 │  恢复执行                 │                              │
 │<─────────────────────────│                              │
```

澄清协调器（ClarificationCoordinator）管理完整生命周期：open → resolved → settled。BlockingLevel 决定是否阻塞当前阶段。

### 6.6 场景六：命令路由处理

```
用户                 OpenClaw Gateway            SEVO 插件层
 │                       │                          │
 │  "sevo:pause sevo-abc"│                          │
 │──────────────────────>│                          │
 │                       │  before_prompt_build     │
 │                       │  (priority 100)          │
 │                       │─────────────────────────>│
 │                       │                          │ extractUserMessage(evt)
 │                       │                          │ SEVO_PAUSE_RE.test() match
 │                       │                          │ handlePauseCommand()
 │                       │                          │   info.status = 'paused'
 │                       │                          │   saveActivePipelines()
 │                       │                          │   appendEvent()
 │                       │                          │ pendingNotices.push()
 │                       │                          │
 │                       │  before_prompt_build     │
 │                       │  (priority 850)          │
 │                       │<─────────────────────────│
 │                       │  注入 pendingNotices      │
 │  "Pipeline paused"    │                          │
 │<──────────────────────│                          │
```

命令优先级（从高到低）：doctor/version → quickstart → status/list → diagnose/retry/pause/skip/resume → create。降级模式下只处理 doctor/version/status/list。

### 6.7 场景七：FTUE 快速启动（sevo:quickstart）

```
用户                 SEVO 插件层                    SEVO 核心
 │                       │                              │
 │  "sevo:quickstart"    │                              │
 │──────────────────────>│                              │
 │                       │  内置 hello-sevo 需求         │
 │                       │  route({isNewModule:true})    │
 │                       │─────────────────────────────>│
 │                       │                              │ RoutingResult
 │                       │  engine.create(routing)       │
 │                       │─────────────────────────────>│
 │                       │                              │ state.json
 │                       │  覆盖 requiredStages =        │
 │                       │  QUICKSTART_STAGES            │
 │                       │  (7 阶段精简流水线)            │
 │                       │                              │
 │                       │  创建 projects/hello-sevo/    │
 │                       │    docs/ src/ tests/ reports/ │
 │                       │                              │
 │                       │  激活 spec 阶段               │
```

QUICKSTART_STAGES 精简流水线（7 阶段）：
```
spec → spec-review-gate → implement → review → smoke-test → verify → ledger
```

跳过的阶段：test-case-authoring、contract、contract-review-gate、regression、publish-generalization-gate、deploy。完成后输出产出物清单（spec、代码、review 报告路径）。

### 6.8 场景八：手动干预状态机

```
                    +----------+
                    |  active  |
                    +----+-----+
           sevo:pause    |    sevo:skip <stage>
              +----------+----------+
              v          |          v
        +----------+     |    +----------+
        |  paused  |     |    | skipped  |
        +----+-----+     |    +----+-----+
  sevo:resume|           |         | 自动激活下一阶段
              v          |         v
        +----------+     |   +--------------+
        |  active  |     |   | next stage   |
        +----------+     |   |   active     |
                         |   +--------------+
                         |
                    sevo:retry
                         |
                    +----v-----+
                    |  active  |  (attempt++)
                    +----------+
```

持久化机制：
- pause/resume：修改 `active-pipelines.json` 中 `info.status` 字段（'paused' / 'active'），记录 `pausedAt` 时间戳
- skip：调用 `updateStageProgress()` 标记阶段为 'skipped'，自动查找 `requiredStages` 中的下一阶段并激活
- retry：重新激活 failed 阶段，attempt 计数递增，label 编码为 `sevo:<pid>:<stage>:<attempt>`
- 所有干预操作写入事件日志（type: 'manual_intervention'，action: pause/skip/resume）

skip 的审计警告：跳过 review/audit 类阶段时输出 WARNING 提示质量保障降级。

### 6.9 场景九：项目隔离与目录初始化

`sevo:create <slug>` 或 `sevo:quickstart` 触发时，插件自动创建隔离的项目目录：

```
projects/<slug>/
+-- docs/
|   +-- design/              <- spec 产出
|   +-- architecture/
|       +-- decisions/       <- ADR 产出
+-- src/                     <- 编码产出
+-- tests/                   <- 测试用例
+-- reports/                 <- 审计/评审报告
+-- scripts/                 <- 验证脚本
```

projectRoot 传递链路：
```
sevo:create → projectRoot = "projects/<slug>"
  → active-pipelines.json[pipelineId].projectRoot
  → getProjectRoot(pipelineId) 读取
  → buildTaskPrompt(stageId, state, projectSlug, projectRoot)
  → task prompt 中所有产出路径基于 projectRoot
```

多项目并行时，每个项目的产出物在独立目录中，互不干扰。projectRoot 作为参数贯穿整个任务派发链路，确保所有阶段的 artifact 路径一致。

---

## 7. 部署视图

### 7.1 部署拓扑

```
┌─────────────────────────────────────────────────────────────────────┐
│                        宿主机 (Linux)                                │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   OpenClaw Gateway 进程                       │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐ │   │
│  │  │              Plugin Runtime                              │ │   │
│  │  │                                                          │ │   │
│  │  │  ┌──────────────────────────────────────┐               │ │   │
│  │  │  │  sevo-pipeline (extensions/)          │               │ │   │
│  │  │  │  index.js + bridge.js + task-mapper   │               │ │   │
│  │  │  │  + label-protocol.js                  │               │ │   │
│  │  │  └──────────────┬───────────────────────┘               │ │   │
│  │  │                 │ lazy-load (bridge.js)                  │ │   │
│  │  └─────────────────┼───────────────────────────────────────┘ │   │
│  │                    │                                          │   │
│  └────────────────────┼──────────────────────────────────────────┘   │
│                       │                                              │
│                       ▼                                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              SEVO 核心 (projects/sevo/dist/)                  │   │
│  │  pipeline-engine.js | gate-engine.js | ledger-engine.js      │   │
│  │  router.js | clarification-coordinator.js                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              数据层 (projects/sevo/data/)                     │   │
│  │  pipelines/<id>/state.json    — 流水线状态（单 writer）        │   │
│  │  pipelines/<id>/events.jsonl  — 事件日志（append-only）       │   │
│  │  ledger/                      — Ledger 条目                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              插件运行态 (extensions/sevo-pipeline/state/)     │   │
│  │  config.json          — 运行时配置覆盖                        │   │
│  │  active-pipelines.json — 活跃流水线追踪                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 与 OpenClaw Gateway 的集成方式

SEVO 插件通过 `openclaw.plugin.json` 声明式注册到 Gateway Plugin Runtime：

| 集成点 | 机制 | 说明 |
|--------|------|------|
| 插件发现 | `openclaw.plugin.json` | Gateway 启动时扫描 extensions/ 目录，加载 plugin manifest |
| 插件初始化 | `plugin.register(api)` | Gateway 调用 register()，传入 logger + config + hook 注册 API |
| 事件订阅 | `api.on(hookName, handler, { priority })` | 3 个 hook 按优先级注册到 Gateway 事件总线 |
| 子 Agent 派发 | `sessions_spawn` 工具调用 | 主会话通过 Gateway RPC 派发子 Agent，插件在 before_tool_call 注入 label |
| 任务完成通知 | `subagent_ended` 事件 | Gateway 在子 Agent 结束时广播，插件据此推进流水线 |
| Prompt 注入 | `before_prompt_build` 返回 `{ prependContext }` | 插件向主会话 prompt 前置注入流水线指令 |

### 7.3 降级模式

插件启动时检查 `dist/pipeline/pipeline-engine.js` 是否存在：
- 存在 → active 模式，3 个 hook 全部生效
- 不存在 → degraded 模式，所有 hook 变为 no-op，记录 `sevo_degraded` 事件

降级不影响 Gateway 其他插件和主会话正常运行。

### 7.4 配置解析优先级

```
plugin.register(api.config)  >  state/config.json  >  环境变量  >  硬编码默认值
```

可配置项：workspaceRoot、sevoRoot、sevoDistPath、sevoDataPath、cacheTtlMs、stageAgentMap。

---

## 8. 横切关注点

### 8.1 错误处理

**插件层：fail-open**

所有 hook handler 通过 `safeSevoHook()` 包裹：
- 同步异常 → try-catch 捕获，记录 `sevo_hook_error` 事件，返回 null
- 异步异常 → Promise.catch() 捕获，同样记录并返回 null
- 单个 hook 失败不阻断 Gateway 事件总线，不影响其他插件

**核心层：fail-safe**

- PipelineEngine.advance() 中的状态转换通过 `assertTransition()` 强制校验，非法转换抛异常
- 文件写入使用 `atomicWriteJson()`（write-tmp + rename），避免半写状态
- Bridge 模块级故障隔离：PipelineEngine 加载失败不影响 LedgerEngine 和 Router

**Result 类型**

核心库使用 `Result<T, E>` 联合类型（ok/error 二选一），避免异常穿透：
```typescript
type Result<T, E = RouterError> = { ok: true; value: T } | { ok: false; error: E };
```

**错误诊断体系**

插件层定义结构化错误码表 `SEVO_ERRORS`，每个错误码包含描述、原因、修复建议：

| 错误码 | 描述 | 修复建议 |
|--------|------|----------|
| SEVO-E001 | No coding agent available | 等待任务完成或添加 agent |
| SEVO-E002 | Spec file not found | 检查 spec 任务输出，sevo:retry |
| SEVO-E003 | Stage gate failed | 修复 P0 问题，sevo:retry |
| SEVO-E004 | Task timeout | 增加超时或拆分任务 |
| SEVO-E005 | Pipeline state corrupted | 检查文件权限和 JSON 语法 |
| SEVO-E006 | Agent task failed | 检查 agent 日志，sevo:retry |
| SEVO-E007 | Hook registration missing | 运行 init.sh 重新注册 |
| SEVO-E008 | Project directory creation failed | 检查磁盘空间和目录权限 |

`formatError(code, context)` 统一格式化错误输出，包含错误码、描述、原因、修复建议，可选附加 stage/pipelineId/error 上下文。`sevo:diagnose <id>` 命令对失败流水线做深度诊断，分析当前阶段状态、失败原因、产出物完整性。

**版本管理与状态迁移**

- `SEVO_VERSION` 常量（当前 `0.2.0`）标识插件版本，`sevo:version` 命令输出
- `CURRENT_SCHEMA_VERSION` 常量（当前 `2`）标识 active-pipelines.json 的 schema 版本
- `migrateState(state)` 在加载状态文件时自动执行 schema 迁移：
  - v1 → v2：为每个 pipeline 条目添加 `frTracking` 默认值（`{ total: [], completed: [], remaining: [], lastUpdatedAt: null }`）
- `loadActivePipelinesWithMigration()` 封装加载+迁移+保存的完整流程，迁移发生时写入 `sevo_state_migrated` 事件
- 升级安全：迁移函数只做向前兼容的增量修改，不删除已有字段

**配置验证（sevo:doctor）**

`handleDoctorCommand()` 执行 5 项自检，输出 Errors/Warnings/OK 三级结果：

| 检查项 | 通过条件 | 失败级别 |
|--------|----------|----------|
| 插件注册 | openclaw.json plugins 中存在且 enabled | Error |
| Hook 注册 | 非 degraded 模式 | Warning |
| Agent 池 | coding agent ≥1 | Error（coding）/ Warning（audit） |
| 状态文件可写 | STATE_DIR 可写入 | Error |
| 路径配置 | workspaceRoot 和 extensionRoot 存在 | Error |

### 8.2 日志与审计

**事件日志（events.jsonl）**

每个流水线实例有独立的 events.jsonl，append-only 语义：
- 事件类型：pipeline_created / pipeline_completed / stage_activated / stage_completed / stage_failed / stage_blocked / stage_skipped / artifact_registered / clarification_opened / clarification_resolved / clarification_settled
- 每条事件包含 timestamp、pipelineId、stage、eventType、payload
- 用于事后审计和状态重建

**插件事件日志**

插件层维护独立的事件日志（`logs/sevo-pipeline-events.jsonl`），记录：
- sevo_hook_error — hook 执行异常
- sevo_completion_received — 收到子 Agent 完成事件
- sevo_advanced — 流水线推进
- sevo_engine_unavailable — 核心引擎不可用
- sevo_prompt_injected — prompt 注入
- sevo_label_injected — label 注入
- sevo_degraded — 降级模式激活

**Ledger（审计账本）**

流水线完成后，LedgerEngine 收集全部 artifact 和 stage record，写入不可变 LedgerEntry：
- conclusion: delivered | aborted
- evidence: 全部 artifact 引用
- stages: 每个阶段的完整记录

### 8.3 安全

| 关注点 | 措施 |
|--------|------|
| 开发与审计分离 | 编码 Agent 不做自审；review/audit 阶段由独立 Agent 执行 |
| 审查 Agent 工具隔离 | review/audit Agent 的工具白名单 schema-level 隔离写权限（无 Edit/Write/Bash） |
| 状态完整性 | state.json 原子写入（write-tmp + rename），避免并发损坏 |
| Label 注入防护 | label 编解码有严格格式校验（`sevo:` 前缀 + 结构化 decode） |
| 插件隔离 | 插件层 fail-open，单插件故障不影响 Gateway 和其他插件 |
| 文件路径解析 | 所有路径通过 `resolveConfiguredPath()` 规范化，防止路径穿越 |

### 8.4 可测试性

| 层次 | 测试策略 |
|------|----------|
| 核心库单元测试 | `src/__tests__/` 下覆盖 Router、Pipeline Engine、Gate Engine、Orchestrator、Adapter |
| 阶段单元测试 | `src/stages/__tests__/` 每个阶段独立测试 |
| Gate 单元测试 | `src/gate/__tests__/gate-engine.test.ts` |
| E2E 测试 | `src/__tests__/e2e.test.ts` + `full-pipeline-e2e.test.ts` 全流水线端到端 |
| StandaloneAdapter | 独立运行模式，脱离 OpenClaw 环境可测试核心逻辑 |
| 插件层 | 通过 mock Gateway API 测试 hook 注册和事件处理 |

### 8.5 持久化策略

| 数据 | 文件 | 写入模式 | 一致性保证 |
|------|------|----------|-----------|
| 流水线状态 | `pipelines/<id>/state.json` | 单 writer + atomic write | write-tmp + rename，无半写 |
| 事件日志 | `pipelines/<id>/events.jsonl` | append-only（O_APPEND） | 单行 JSON，断电最多丢最后一行 |
| Ledger | `ledger/` | 不可变写入 | 写入后不修改 |
| 活跃流水线 | `state/active-pipelines.json` | write-tmp + rename | 同 state.json |
| 插件配置 | `state/config.json` | 手动编辑 | 读取时 try-catch 容错 |

### 8.6 模块缓存与热重载

Bridge 层实现模块级缓存 + 自动失效：
- 缓存 TTL 默认 30s（可通过 cacheTtlMs 配置）
- 文件 mtime 变化检测，自动重新加载编译产物
- 加载失败后 backoff（同 TTL 时间内不重试）
- cache-bust 通过 URL query parameter（`?v=<mtime>`）实现

---

## 9. 架构决策

以下为 SEVO 关键架构决策摘要。完整 ADR 存放于 `docs/decisions/` 目录。

### ADR-001: 状态机驱动 vs 规则引擎

- Context：需要一种机制保障 12 个阶段按序执行、不跳步
- Decision：采用有限状态机（FSM），每个阶段有明确的状态转换规则（stage-machine.ts）
- Consequences：状态转换可形式化验证；新增阶段需修改状态图；比规则引擎更刚性但更可预测

### ADR-002: 核心通用 + Host Adapter 模式

- Context：SEVO 需要在 OpenClaw 内运行，但不应绑死单一宿主
- Decision：核心库不依赖 OpenClaw API，通过 SevoHostAdapter 接口抽象宿主能力
- Consequences：可独立测试（StandaloneAdapter）；OpenClaw 特化逻辑集中在 OpenClawAdapter；新宿主只需实现 adapter 接口

### ADR-003: 三级路由（L0/L1/L2+）

- Context：不是所有改动都需要走完整 12 阶段流水线
- Decision：Router 根据 TaskScope 自动分级——L0 跳过、L1 轻量、L2+ 完整
- Consequences：小改动快速通过；大改动强制全流程；分级规则可配置

### ADR-004: Spec Review 后并行分叉

- Context：test-case-authoring 和 contract 无依赖关系，串行执行浪费时间
- Decision：spec-review-gate 通过后同时激活两条分支；implement 等待两条分支都完成
- Consequences：缩短流水线总耗时；parallel-branch.ts 管理分叉/合并逻辑；增加了状态管理复杂度

### ADR-005: 单文件状态 + 事件溯源

- Context：需要持久化流水线状态，同时支持审计
- Decision：state.json 单 writer 模型 + events.jsonl append-only
- Consequences：无并发写冲突；事件日志支持状态重建和审计；不适合高并发场景（当前单流水线足够）

### ADR-006: 插件层 fail-open

- Context：插件运行在 Gateway 进程内，异常可能影响整个系统
- Decision：所有 hook handler 包裹 safeSevoHook()，异常记录但不传播
- Consequences：单 hook 故障不拖垮 Gateway；错误可能被静默吞掉（通过事件日志补偿可观测性）

### ADR-007: GateRule SPI 可插拔门禁

- Context：不同阶段的质量标准不同，需要灵活组合
- Decision：定义 GateRule 接口，内置 FileExists/TypeCheck/TestPass/MinCoverage，支持扩展
- Consequences：新增质量规则只需实现 GateRule 接口；规则组合通过 verdict-aggregator 聚合

### ADR-008: Label Protocol 流水线上下文传递

- Context：子 Agent session 需要携带流水线上下文，completion 时路由回正确实例
- Decision：通过 session label 编码 `sevo:<pipelineId>:<stageId>:<attempt>`
- Consequences：零额外通信开销；依赖 Gateway label 机制；label 格式变更需要前后兼容

### ADR-009: 命令系统通过 Hook 拦截实现

- Context：用户需要通过对话控制流水线（创建/暂停/跳过/查询），需要一种命令路由机制
- Decision：在 `before_prompt_build`（priority 100）hook 中用正则匹配 `sevo:*` 命令，路由到对应 handler，结果通过 `pendingNotices` 注入主会话 prompt
- Consequences：命令处理在 prompt 构建前完成，主会话无需感知命令解析逻辑；正则匹配足够覆盖结构化命令格式；降级模式下只读命令（doctor/version/status/list）仍可用

### ADR-010: 项目产出物目录隔离

- Context：多个 SEVO 项目并行时，产出物散落在 workspace 根目录会互相干扰
- Decision：每个项目创建独立的 `projects/<slug>/` 目录，所有阶段产出物路径基于 projectRoot；projectRoot 持久化到 active-pipelines.json 并贯穿整个任务派发链路
- Consequences：多项目并行互不干扰；项目目录可直接作为独立 Git 仓库；需要在 buildTaskPrompt 中始终传递 projectRoot 参数

### ADR-011: 状态 Schema 迁移策略

- Context：active-pipelines.json 的数据结构随功能演进需要变更（如新增 frTracking 字段）
- Decision：引入 `schemaVersion` 字段和 `migrateState()` 函数，加载时自动执行向前兼容的增量迁移
- Consequences：升级无需手动干预；迁移只做增量修改不删除字段；迁移事件写入日志可追溯

---

## 10. 质量需求

### 10.1 质量属性场景树

```
                        SEVO 质量属性
                             │
         ┌───────────┬───────┼───────┬───────────┐
         ▼           ▼       ▼       ▼           ▼
      可控性       可审计性  通用性   可靠性     可扩展性
```

### 10.2 质量属性场景

| ID | 质量属性 | 场景 | 度量 |
|----|----------|------|------|
| QA-01 | 可控性 | Gate 评估为 rejected 时，流水线不放行后续阶段 | 100% 阻断率，零漏放 |
| QA-02 | 可控性 | 非法状态转换（如 passed → active）被拒绝 | assertTransition() 抛异常，状态不变 |
| QA-03 | 可审计性 | 任意流水线可通过 events.jsonl 重建完整执行历史 | 事件覆盖所有状态转换，无遗漏 |
| QA-04 | 可审计性 | Ledger 记录流水线全部 artifact 和结论 | LedgerEntry 包含 stages + evidence + conclusion |
| QA-05 | 通用性 | 核心库在无 OpenClaw 环境下可独立运行和测试 | StandaloneAdapter 通过全部单元测试 |
| QA-06 | 通用性 | 新增宿主只需实现 SevoHostAdapter 接口 | 接口方法 ≤6 个，无隐式依赖 |
| QA-07 | 可靠性 | 插件层单 hook 异常不影响 Gateway 和其他插件 | safeSevoHook() 100% 捕获，Gateway 事件总线不中断 |
| QA-08 | 可靠性 | state.json 写入过程中断电不产生损坏文件 | atomic write（write-tmp + rename）保证 |
| QA-09 | 可靠性 | Bridge 单模块加载失败不影响其他模块 | per-module failure isolation，独立 backoff |
| QA-10 | 可扩展性 | 新增阶段只需：定义 stage 实现 + 更新 stage-graph + 注册 agent 映射 | 改动 ≤3 个文件 |
| QA-11 | 可扩展性 | 新增门禁规则只需实现 GateRule 接口 | 零核心代码修改 |
| QA-12 | 可扩展性 | 阶段→Agent 映射可通过 config 覆盖 | stageAgentMap 配置项，无需改代码 |
| QA-13 | 可用性 | 用户通过 sevo:doctor 一条命令完成安装自检 | 5 项检查全覆盖，Errors/Warnings/OK 三级输出 |
| QA-14 | 可用性 | 流水线失败时用户看到结构化错误码和修复建议 | SEVO_ERRORS 8 种错误码，formatError 统一格式 |
| QA-15 | 可用性 | sevo:quickstart 5 分钟内跑通首个流水线 | 7 阶段精简流水线，内置示例需求 |
| QA-16 | 可控性 | 用户可暂停/跳过/重试流水线任意阶段 | pause/skip/resume/retry 4 种干预操作，状态持久化 |
| QA-17 | 可靠性 | 状态 schema 变更时自动迁移，无需手动干预 | migrateState 增量迁移 + 事件日志记录 |
| QA-18 | 隔离性 | 多项目并行时产出物互不干扰 | projects/\<slug\>/ 独立目录，projectRoot 贯穿链路 |

---

## 11. 风险与技术债务

### 11.1 已知风险

| ID | 风险 | 影响 | 缓解措施 |
|----|------|------|----------|
| R-01 | 核心库未编译（dist/ 不存在） | 插件降级为 no-op，流水线不可用 | 降级模式 + 事件日志记录；CI 应确保 dist/ 始终可用 |
| R-02 | 单 writer 模型在多流水线并发时可能竞争 | state.json 写入冲突 | 当前单流水线场景足够；未来需引入文件锁或数据库 |
| R-03 | 子 Agent 超时或静默失败 | 流水线卡在某阶段不推进 | 依赖 Gateway run-watchdog 插件检测超时；需补充流水线级超时机制 |
| R-04 | Gate 评估目前只支持 pass/fail 二元 | conditional（有条件通过）语义未在插件层实现 | 核心层已支持 conditional；插件层 TODO 标记待实现 |
| R-05 | 澄清协调依赖宿主 adapter 实现 | StandaloneAdapter 的澄清能力有限 | 核心层接口已定义；OpenClawAdapter 需完善交互式澄清 |

### 11.2 技术债务

| ID | 债务 | 位置 | 优先级 |
|----|------|------|--------|
| TD-01 | 插件层 subagent_ended 只解析 pass/fail，未处理 conditional/rejected 门禁裁决 | index.js:284 TODO | P1 |
| TD-02 | Bridge 模块缓存使用 URL cache-bust，依赖 Node.js ESM loader 行为 | bridge.js:131 | P2 |
| TD-03 | 活跃流水线追踪（active-pipelines.json）与核心 state.json 存在数据冗余 | index.js:164-170 | P3 |
| TD-04 | 插件事件日志与核心事件日志分离，缺乏统一查询接口 | index.js / pipeline-engine.ts | P2 |
| TD-05 | KIVO 集成（Ledger → 知识入库）和 AEO 集成（指标 → 监控）尚未实现 | 架构预留，代码未写 | P2 |
| TD-06 | 流水线级超时机制缺失，依赖外部 watchdog | pipeline-engine.ts | P1 |
| TD-07 | ~~规模路由（FR-D08）~~ 已实现 | router / index.js | P2 |
| TD-08 | 命令解析使用正则匹配，复杂参数场景可能需要升级为解析器 | index.js:1170-1180 | P3 |

---

## 12. 术语表

| 术语 | 定义 |
|------|------|
| SEVO | Spec-Execute-Verify-Operate，Agent 自动研发流水线 |
| SDD | Specify-Design-Develop，SEVO 的前身流程规范（AGENTS.md 中定义） |
| Stage | 流水线阶段，12 个阶段构成完整流水线 |
| Gate | 门禁，阶段间的质量检查点，输出 passed/conditional/rejected |
| StageId | 阶段标识符，枚举类型（spec / spec-review-gate / ... / ledger） |
| StageStatus | 阶段状态：pending / active / blocked / clarification-blocked / passed / failed / skipped |
| TaskLevel | 任务级别：L0（跳过）/ L1（轻量）/ L2+（完整流水线） |
| TriggerRule | 触发规则，决定任务是否需要完整流水线（new-module / cross-domain / large-change 等） |
| RoutingResult | Router 输出，包含 level、requiredStages、skippedStages、matchedRules |
| PipelineState | 流水线完整状态，持久化到 state.json |
| StageRecord | 单个阶段的执行记录，包含 status、artifacts、attempt 等 |
| StageTransition | advance() 的返回值，描述从哪个阶段转换到哪个阶段 |
| GateVerdict | 门禁评估结果，包含 conclusion、blockers、reviewBundles |
| GateRule | 门禁规则 SPI 接口，可插拔的质量检查规则 |
| ReviewBundle | 单个审查者的审查结论，包含 reviewer、role、conclusion、issues |
| LedgerEntry | 审计账本条目，记录流水线完整执行证据 |
| ArtifactRef | 产物引用，包含 id、type、path、createdAt |
| Host Adapter | 宿主适配器，将核心抽象操作映射到具体宿主环境 |
| OpenClawAdapter | OpenClaw 宿主适配器实现 |
| StandaloneAdapter | 独立运行适配器，用于测试和非 OpenClaw 环境 |
| Bridge | 插件层懒加载桥梁，管理核心编译产物的加载和缓存 |
| Label Protocol | 流水线上下文编码协议，格式 `sevo:<pipelineId>:<stageId>:<attempt>` |
| pendingAdvances | 插件层内存队列，缓存待注入主会话的下一阶段任务 |
| fail-open | 错误处理策略：异常记录但不阻断，保证系统可用性 |
| fail-safe | 错误处理策略：异常阻断操作，保证数据一致性 |
| atomic write | 原子写入：write-tmp + rename，避免半写状态 |
| ClarificationCoordinator | 澄清协调器，管理歧义发现→阻塞→解决→恢复的完整生命周期 |
| BlockingLevel | 澄清阻塞级别，决定歧义是否阻塞当前阶段执行 |
| SEVO_ERRORS | 结构化错误码表，每个错误码包含描述、原因、修复建议 |
| formatError | 统一错误格式化函数，输出错误码 + 描述 + 原因 + 修复建议 + 上下文 |
| SEVO_VERSION | 插件版本常量（当前 0.2.0），sevo:version 命令输出 |
| migrateState | 状态 schema 迁移函数，加载时自动执行向前兼容的增量迁移 |
| QUICKSTART_STAGES | FTUE 精简流水线阶段集（7 阶段），跳过三方会审和 UX 验收 |
| projectRoot | 项目产出物根目录（projects/\<slug\>/），贯穿整个任务派发链路 |
| getUserJourneyTemplate | 6 阶段用户体验旅程模板函数，注入 spec 和 ux-acceptance 阶段 |
| pendingNotices | 插件层内存队列，缓存命令执行结果，由 before_prompt_build 注入主会话 |
| KIVO | Agent 知识迭代引擎（未来集成） |
| AEO | Agent 效果运营平台（未来集成） |
