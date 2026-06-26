# SEVO — arc42 架构文档

版本 0.1 | 2026-05-03

---

## 目录

1. 引言与目标
2. 约束条件
3. 上下文与范围
4. 解决方案策略

<!-- §5-§12 见 PART2 -->

---

## §1 引言与目标

### 1.1 需求概述

SEVO（Spec-Execute-Verify-Operate）是面向 vibe coding 用户的 Agent 研发流水线。它将需求定义、方案约束、实现执行、独立审计、回归验证、部署发布、清洁环境验收和交付留痕收拢到同一条可追溯流水线上。

SEVO 以 npm 包（`sevo`）分发，`npx sevo init` 一条命令完成环境初始化。核心流程通用化设计，可在任意宿主环境运行；宿主特有能力通过 Adapter 接入增强，但核心流程不因缺少某个宿主而断裂。

### 1.2 架构目标

| ID | 目标 | 优先级 | 驱动力 |
|----|------|--------|--------|
| AG-1 | 通用化核心流程 | 最高 | 核心阶段语义、状态机、门禁逻辑、工件交接协议不绑定任何单一宿主实现。换宿主只换 Adapter，核心不动。 |
| AG-2 | 单包开箱即用 | 最高 | 陌生用户 `npm install -g sevo && npx sevo init` 后 5 分钟内跑通第一条 pipeline。零配置即可启动 L0 级流水线。 |
| AG-3 | 渐进式披露 | 高 | 四级配置分层（L0 安装即用 → L1 按需配置 → L2 自定义阶段 → L3 编程控制），用户按需解锁，不被复杂度淹没。 |
| AG-4 | 角色知识内置 | 高 | PM/UX/架构师/审计的专业标准嵌入流水线阶段（Stage-Bound Design），单 Agent 也能产出专业质量工件。 |
| AG-5 | 工件驱动的可追溯性 | 高 | 每个阶段的输入/输出都是结构化工件，全链路可追溯到 Ledger。没有 Ledger Entry 的交付不算闭环。 |
| AG-6 | 自动推进与自愈 | 中 | PipelineEngine 状态机驱动阶段流转，门禁失败自动触发 Review Fix Loop，Gateway 重启后自动恢复中断的 pipeline。 |
| AG-7 | 编排引导而非直接派发 | 中 | 在 OpenClaw 宿主中，PipelineEngine 通过 hook + prompt 注入引导主会话调度，不直接调用 `sessions_spawn`。其他宿主通过 Adapter 实现等效能力。 |

### 1.3 FR 映射

下表将 spec 中的 16 个 FR 映射到架构关注点：

| FR | 名称 | 架构关注点 |
|----|------|-----------|
| FR-01 | Spec | 阶段执行器 + 原则注入 + 模糊检测 |
| FR-02 | Spec Review Gate | 门禁引擎 + 独立评审语义 |
| FR-02a/b/c | Test Case / UX / Commercial Authoring | 并行分支编排 |
| FR-03 | Contract | 阶段执行器 + Work Package 拆分 |
| FR-04 | Contract Review Gate | 三方并行会审 + 门禁引擎 |
| FR-05 | Implement | 阶段执行器 + TDD 循环 + worktree 隔离 |
| FR-05a | Systematic Debugging | Implement 内部可选活动 |
| FR-06 | Review | 双维度独立评审 + spec-code 覆盖检查 |
| FR-06a | Review Fix Loop | 自动解析→生成 Fix Task→定向复验→门禁重评 |
| FR-06b | Smoke Test | Review 后置验证 |
| FR-06c/d | UX Acceptance / PM Commercial Review | 并行验收分支 |
| FR-07 | Regression | 自动化回归测试 |
| FR-08 | Deploy | 发布制品生成 |
| FR-08a | Commercialization Gate | 五层商用化检查 |
| FR-09 | Verify | 清洁环境独立验证 |
| FR-10 | Ledger | 交付账本汇总 + 证据链 |
| FR-11 | Proactive Clarification | 跨阶段模糊检测与主动澄清 |
| FR-12 | Pipeline Create | 实例创建 + 目录初始化 + 路由判定 |
| FR-13 | PipelineEngine | 状态机驱动 + 宿主 Adapter + 自动推进 |
| FR-14 | Package Distribution & CLI | npm 分发 + 单包双入口 + CLI |
| FR-15 | Progressive Disclosure | 四级配置分层 |
| FR-16 | Onboarding Experience | demo 命令 + 首次使用引导 |

### 1.4 利益相关方

| 角色 | 关注点 |
|------|--------|
| Solo Founder / 独立产品操盘者 | 交付速度、返工成本、线上事故可控 |
| Agent 原生开发者 | 约束 Agent 的研发流程，减少假完成 |
| 质量与架构把关者 | 独立视角、统一工件链路、经验沉淀 |
| 宿主平台与外部 Agent 提供方 | 通用接口、核心逻辑与运行时解耦 |
| SEVO 维护者 | 模块边界清晰、可测试、可增量演进 |

---

## §2 约束条件

### 2.1 技术约束

| ID | 约束 | 来源 |
|----|------|------|
| TC-1 | npm 包分发，包名 `sevo`，TypeScript 编写，编译为 ESM | spec §2.5, FR-14 |
| TC-2 | 单包双入口：`dist/` 提供库 API，`plugin/` 提供 OpenClaw 插件入口，`bin/` 提供 CLI | 插件分发架构方案 §2.1 |
| TC-3 | 零运行时依赖（npm dependencies 为空），OpenClaw SDK 通过 `register(api)` 回调注入 | 插件分发架构方案 §2.2 |
| TC-4 | OpenClaw hook 系统限制：hook 不能发起工具调用，只能注入 prompt 引导主会话调度 | 插件分发架构方案 §5 |
| TC-5 | 状态持久化使用本地 JSON 文件，不引入外部数据库 | spec NFR-5.7 |
| TC-6 | 插件加载路径：OpenClaw 通过 `plugins.load.paths` 或 `~/.openclaw/extensions/` 自动扫描发现插件 | 插件分发架构方案 §1.1 |

### 2.2 组织约束

| ID | 约束 | 来源 |
|----|------|------|
| OC-1 | 核心流程不绑定单一宿主，但主动复用宿主高价值能力（hooks、guards、session-guard 等）通过 Adapter 接入 | spec §6.4.1, §9.1 |
| OC-2 | Stage-Bound Design：能力/原则/规范绑定流程阶段，不绑定特定 Agent 身份 | spec §6.6 |
| OC-3 | 审查与实现阶段默认分离，高风险改动不能只靠实现者自证 | spec §9.1 |
| OC-4 | 单 Agent 环境自动降级：所有角色池填入同一个 agentId，质量降级但功能完整 | spec FR-15 L0 |

### 2.3 惯例约束

| ID | 约束 | 来源 |
|----|------|------|
| CC-1 | FR 流程实例 ID 格式：`fr-<project-slug>-<yyyyMMdd>-<seq>` | spec §3.5 |
| CC-2 | 同一 Project 同一时刻只允许一个 active 的 FR 流程实例 | spec §3.5 |
| CC-3 | 标准目录结构：`docs/`、`src/`、`tests/`、`reports/`、`artifacts/`、`skill/` | spec §3.6 |
| CC-4 | 合规模式默认 `guide`（注入流程引导），不阻断执行 | spec FR-15 L0 |
| CC-5 | Review Fix Loop 最大轮次上限默认 3 轮，超限升级为人工介入 | spec FR-06a AC-4.24i |

---

## §3 上下文与范围

### 3.1 业务上下文

```
                        ┌─────────────────────────────────────────┐
                        │              SEVO Pipeline              │
                        │                                         │
  ┌──────────┐          │  ┌─────────┐  ┌──────────┐  ┌───────┐  │          ┌──────────────┐
  │          │  FR 描述  │  │ Router  │→ │ Pipeline │→ │ Gate  │  │  工件     │              │
  │   用户   │─────────→│  │         │  │ Engine   │  │Engine │  │────────→│  Ledger      │
  │          │          │  └─────────┘  └──────────┘  └───────┘  │          │  (交付账本)   │
  └──────────┘          │       ↕            ↕            ↕       │          └──────────────┘
       ↑                │  ┌─────────────────────────────────┐    │
       │                │  │        Host Adapter              │    │
       │   状态/通知     │  │  (OpenClaw / Standalone / ...)   │    │
       │                │  └──────────┬──────────────────────┘    │
       │                └─────────────┼───────────────────────────┘
       │                              │
       │                              ↓
       │                ┌─────────────────────────────┐
       └────────────────│      宿主环境                │
                        │  (Agent 运行 / 工具接入 /    │
                        │   消息调度 / 执行沙箱)       │
                        └─────────────────────────────┘
```

外部参与者与 SEVO 的交互：

| 参与者 | 输入 | 输出 |
|--------|------|------|
| 用户 | FR 描述、Project 创建、CLI 命令、手动干预（pause/resume/cancel） | Pipeline 状态、阶段工件、Ledger Entry、通知 |
| 宿主环境 | Agent 执行能力、工具接入、消息调度 | 阶段任务执行结果、完成事件 |
| npm Registry | — | sevo 包安装 |
| 发布目标（npm/GitHub/ClawHub） | — | Release Artifact 发布确认 |

### 3.2 技术上下文

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                         sevo (npm 包)                            │
  │                                                                  │
  │  ┌──────────┐  ┌──────────────┐  ┌───────────┐  ┌────────────┐  │
  │  │ bin/     │  │ dist/        │  │ plugin/   │  │ templates/ │  │
  │  │ CLI 入口 │  │ 库 API       │  │ OpenClaw  │  │ 角色模板   │  │
  │  │          │  │              │  │ 插件入口  │  │ 阶段原则   │  │
  │  └────┬─────┘  └──────┬───────┘  └─────┬─────┘  └────────────┘  │
  │       │               │                │                         │
  │       │    ┌──────────┴────────────────┤                         │
  │       │    │                           │                         │
  │       ▼    ▼                           ▼                         │
  │  ┌──────────────┐              ┌──────────────┐                  │
  │  │ Core Modules │              │ bridge.js    │                  │
  │  │              │◄─────────────│ (胶水层)     │                  │
  │  │ • Pipeline   │              └──────────────┘                  │
  │  │   Engine     │                     │                          │
  │  │ • Stage      │                     │ register(api)            │
  │  │   Runner     │                     ▼                          │
  │  │ • Clarific.  │              ┌──────────────┐                  │
  │  │   Coordinator│              │ OpenClaw     │                  │
  │  │ • Compliance │              │ Gateway      │                  │
  │  │   Router     │              │ (运行时注入)  │                  │
  │  │ • RoleKnow.  │              └──────────────┘                  │
  │  │   Injector   │                                                │
  │  └──────────────┘                                                │
  └──────────────────────────────────────────────────────────────────┘
                │                           │
                ▼                           ▼
  ┌──────────────────┐          ┌──────────────────────┐
  │ 本地文件系统      │          │ 宿主 Hook 系统       │
  │ • pipeline state │          │ • before_prompt_build │
  │ • 工件目录       │          │ • subagent_ended     │
  │ • sevo.config    │          │ • before_tool_call   │
  └──────────────────┘          └──────────────────────┘
```

### 3.3 SEVO 与相邻系统的边界

| 系统 | SEVO 负责 | 对方负责 | 边界 |
|------|----------|---------|------|
| KIVO（知识治理） | 研发流程中的经验沉淀接口 | 知识库治理、向量化、去重 | SEVO 产出经验条目，KIVO 消费 |
| AEO（效果运营） | 阶段效果数据输出接口 | 效果度量、运营分析 | SEVO 产出阶段数据，AEO 消费 |
| Claw Design（设计产物） | Claw Design 自身研发时的流水线 | 设计产物生成能力 | SEVO 是研发工具，Claw Design 是被研发的产品 |
| 宿主环境 | 阶段语义、工件语言、门禁逻辑、验收闭环 | Agent 运行、工具接入、消息调度、执行沙箱 | SEVO 定义通用流程，宿主做适配 |

---

## §4 解决方案策略

### 4.1 编排模型：Hook + Prompt 引导

SEVO 的核心设计决策是**不直接派发任务**。PipelineEngine 定义编排语义（何时推进、何时阻断、何时重试），具体的任务派发方式由宿主 Adapter 实现。

在 OpenClaw 宿主中，编排通过三个 hook 实现：

| Hook | 触发时机 | 职责 |
|------|---------|------|
| `before_prompt_build` | 主会话构建 prompt 前 | 注入「下一步该派发什么任务」的指令 + 阶段执行原则 |
| `subagent_ended` | 子 Agent 任务完成时 | 解析完成事件 → 更新 pipeline 状态 → 设置下一阶段推进指令 |
| `before_tool_call` | 工具调用前 | 合规检查（guide/auto-route 模式下检测未编排的开发任务） |

这个模型的关键约束：hook 不能发起工具调用（OpenClaw 平台限制），只能通过 prompt 注入引导主会话做出调度决策。主会话仍然是调度者，PipelineEngine 是编排顾问。

对于非 OpenClaw 宿主，Adapter 接口定义等效能力：

```typescript
interface HostAdapter {
  // 触发阶段执行（宿主决定具体派发方式）
  triggerStage(stage: StageId, context: StageContext): Promise<void>;
  // 监听阶段完成事件
  onStageComplete(callback: (result: StageResult) => void): void;
  // 注入阶段执行原则
  injectPrinciples(stage: StageId, principles: string): Promise<void>;
  // 通知用户
  notify(message: string, channel?: string): Promise<void>;
}
```

### 4.2 合规模式

SEVO 对未经编排的开发任务提供三种处理策略，通过配置切换：

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `guide` (默认) | 在 `before_prompt_build` 中注入流程引导提示，建议用户走 SEVO 流程，但不阻断执行 | 初次接入、渐进式采纳 |
| `auto-route` | 自动为未编排的开发任务创建 pipeline 并路由进 SEVO 流程 | 团队已全面采纳 SEVO |
| `off` | 不干预，SEVO 只管已显式创建的 pipeline | 部分项目不走 SEVO |

注意：没有「强制阻断」概念。即使在 `auto-route` 模式下，SEVO 也是创建 pipeline 并引导，不是阻断任务执行。

### 4.3 角色知识内置（Stage-Bound Design）

SEVO 把 PM、UX、架构师、审计等角色的专业标准嵌入流水线阶段，而非绑定到特定 Agent 身份。

实现方式：PipelineEngine 在触发阶段执行时，通过 Adapter 的 `injectPrinciples()` 自动注入该阶段应遵循的执行原则模板。

阶段与注入原则的映射：

| 阶段 | 注入原则 | 来源 |
|------|---------|------|
| Spec | 用户价值优先、需求完整度校验、概念-技术阶段隔离、主动澄清 | PM 最佳实践 |
| Contract | 通用化三问、Stage-Bound Design、Adapter 模式、最小改动原则 | 架构师最佳实践 |
| Implement | TDD 循环、Karpathy Guidelines（最小改动、最简实现、目标驱动）、系统化调试 | 工程最佳实践 |
| Review | spec-code 覆盖检查、AC 覆盖矩阵、独立审计、证据驱动 | 审计最佳实践 |
| Smoke Test / UX Acceptance | 陌生用户视角、开箱即用五维度检查 | UX 最佳实践 |
| Deploy | 五层商用化检查、敏感信息扫描、原子发布 | 发布工程最佳实践 |

效果：单 Agent 用户执行 Spec 阶段时，自动获得 PM 质量的 prompt 引导；多 Agent 环境有专职 PM 角色则效果更好，但不是必须。

### 4.4 状态机驱动的自动推进

PipelineEngine 是 SEVO 的核心运行时。它读取路由结果中的 Stage Queue，按状态机规则自动推进：

```
created → active（第一个阶段开始）→ ... → completed（Ledger 通过）
                                    ↘ failed（不可恢复）
```

每个阶段的状态机：

```
pending → active → passed → (下一阶段)
              ↓        ↗
           blocked / failed → (修复) → active
pending → skipped（路由裁剪）
```

关键行为：

- 阶段完成后 30 秒内评估门禁并决定推进或阻断（AC-13.2）
- 门禁失败自动触发 Review Fix Loop（FR-06a）
- Gateway 重启后 60 秒内自动恢复中断的 pipeline（AC-13.8）
- 支持并行阶段组（FR-02a/b/c 与 FR-03 并行；FR-06c 与 FR-06d 并行）

### 4.5 流程路径裁剪

SEVO 根据任务复杂度自动选择最短有效路径：

| 级别 | 触发条件 | 必经阶段 |
|------|---------|---------|
| L0 | 微小改动（bug 修复、配置调整） | implement → review → smoke-test → verify → ledger |
| L1 | 单域中等改动 | spec → spec-review-gate → contract(简化) → implement → review → smoke-test → regression → deploy → verify → ledger |
| L2+ | 新系统、跨域重构、大范围变更 | 完整 8 阶段 + 全部门禁 + 并行验收分支 |

裁剪规则由 Router 模块（`level-classifier.ts` + `stage-graph.ts`）实现，跳过的阶段记录理由，不破坏工件链的可追溯性。

### 4.6 单包双入口分发策略

npm 包同时提供库 API 和 OpenClaw 插件两个入口，解决「外部用户装了包但流水线跑不起来」的问题：

```
sevo/
├── dist/          # 库 API（PipelineEngine, GateEngine, LedgerEngine, Adapter...）
├── plugin/        # OpenClaw 插件入口（register + hooks + bridge.js）
├── bin/           # CLI 入口（sevo init / status / project / fr / doctor）
├── templates/     # 角色执行原则模板
└── package.json
```

`sevo init` 流程：检测宿主环境 → 注册插件到 `openclaw.json` → 动态发现 Agent 并分类角色 → 单 Agent 自动降级 → doctor 检查 → 输出下一步指引。

`plugin/bridge.js` 是胶水层：插件通过它动态加载 `../dist/` 下的编译产物，获取 PipelineEngine 等核心能力。加载失败则降级为 no-op。

### 4.7 关键架构决策摘要

| 决策 | 选择 | 理由 |
|------|------|------|
| 编排方式 | Hook + prompt 注入引导，不直接派发 | OpenClaw hook 不能发起工具调用；保持主会话为调度者，SEVO 为编排顾问 |
| 包结构 | 单包双入口（dist/ + plugin/） | 避免用户装两个包；OpenClaw 插件加载器期望独立目录 + `openclaw.plugin.json` |
| 状态持久化 | 本地 JSON 文件 | 零依赖、可读、可 git 追踪；不引入外部数据库 |
| 角色知识 | 内置到阶段（Stage-Bound Design） | 单 Agent 也能用；不假设用户有特定名称或数量的 Agent |
| 合规模式 | guide / auto-route / off（无强制路由） | 渐进式采纳；不强制用户改变工作方式 |
| 宿主适配 | Adapter 接口 | 核心通用 + 宿主能力通过 Adapter 接入 = 既通用又能用上所有本地优势 |
| Agent 发现 | 命名规则 + runtime type + 显式声明三层信号 | 兼容已有命名习惯；外部用户 Agent 命名不可预测时有 fallback |

## §5 构建块视图

### 5.1 顶层分解

```
sevo
├── PipelineEngine          状态机驱动的流程编排核心
│   ├── GateEngine          门禁规则评估（PipelineEngine 内部模块）
│   └── LedgerEngine        交付账本汇总与证据链（PipelineEngine 内部模块）
├── StageRunner             单阶段执行器（门禁 + prompt 注入）
├── ClarificationCoordinator 跨阶段模糊检测与主动澄清（FR-11）
├── RoleKnowledgeInjector   角色专业标准注入
├── ComplianceRouter        合规路由（guide / auto-route / off）
├── CLIInterface            sevo init / status / project / fr / doctor
└── PluginAdapter           OpenClaw hook 注册与事件分发
```

依赖方向：CLIInterface → PipelineEngine → StageRunner → RoleKnowledgeInjector；StageRunner → ClarificationCoordinator；PluginAdapter → PipelineEngine / StageRunner / ComplianceRouter / RoleKnowledgeInjector；ComplianceRouter 仅被 PluginAdapter 调用（不被 PipelineEngine 调用，避免循环依赖）。

GateEngine 和 LedgerEngine 是 PipelineEngine 的内部模块，不作为独立顶层构建块暴露。GateEngine 负责门禁规则评估（接收 StageRunner 的阶段结果，判定 pass/fail）；LedgerEngine 负责交付账本的写入和查询（pipeline 完成时汇总全链路工件记录）。CLIInterface 的 `sevo ledger` 命令通过 PipelineEngine 间接访问 LedgerEngine。

---

### 5.2 PipelineEngine

**职责**：SEVO 的核心运行时。管理 pipeline 实例的完整生命周期——创建 Stage Queue、按状态机规则推进阶段、评估门禁、触发 Review Fix Loop、处理并行阶段组、Gateway 重启后自动恢复。

**接口**：

| 方法 | 说明 |
|------|------|
| `createPipeline(projectSlug, frDescription, routeResult)` | 创建 pipeline 实例，生成 Stage Queue |
| `advance(pipelineId)` | 评估当前阶段出口条件，满足则推进到下一阶段 |
| `handleStageComplete(pipelineId, stageId, result)` | 接收阶段完成事件，更新状态，触发 advance |
| `getPipelineState(pipelineId)` | 返回 pipeline 当前状态快照 |
| `pause(pipelineId)` / `resume(pipelineId)` / `cancel(pipelineId)` | 生命周期控制 |
| `recoverInterrupted()` | 启动时扫描持久化状态，恢复中断的 pipeline |

**状态机**：

- pipeline 级别：`created → active → completed / failed`，支持 `paused` 中间态。
- stage 级别：`pending → active → passed / failed / blocked`，`pending → skipped`（路由裁剪）。
- 并行阶段组（如 FR-02a/b/c + FR-03，FR-06c + FR-06d）：组内阶段同时触发，全部 passed 后组才算通过。

**依赖**：

- StageRunner：委托执行单个阶段。
- 宿主 Adapter（`HostAdapter` 接口）：触发阶段执行、监听完成事件、注入原则、通知用户。
- 本地 JSON 文件（`active-pipelines.json`）：状态持久化，支持 Gateway 重启恢复。

**关键约束**：PipelineEngine 定义编排语义（何时推进、何时阻断），不直接派发任务。具体派发方式由宿主 Adapter 实现。

---

### 5.3 StageRunner

**职责**：单阶段执行器。接收 PipelineEngine 的阶段触发指令，组装阶段上下文（输入工件 + 执行原则 + 门禁规则），通过 Adapter 触发执行，评估出口条件。

**接口**：

| 方法 | 说明 |
|------|------|
| `run(stageId, context: StageContext)` | 组装上下文 → 注入角色知识 → 通过 Adapter 触发执行 |
| `evaluateGate(stageId, result: StageResult)` | 检查出口工件是否齐全、门禁规则是否满足 |

**StageContext 结构**：

```typescript
interface StageContext {
  pipelineId: string;
  stageId: string;
  inputArtifacts: ArtifactRef[];   // 上游阶段产出的工件引用
  principles: string;              // RoleKnowledgeInjector 注入的执行原则
  gateRules: GateRule[];           // 本阶段出口门禁规则
  agentHint?: string;              // 建议执行的 agent 角色
}
```

**依赖**：

- RoleKnowledgeInjector：获取阶段执行原则。
- GateEngine（`dist/` 库模块）：评估门禁规则。
- 宿主 Adapter：实际触发阶段执行。

**关键行为**：门禁失败时返回 `{ passed: false, issues: ReviewIssue[] }` 给 PipelineEngine，由 PipelineEngine 决定是否触发 Review Fix Loop。

**商用化门禁（FR-08a）**：Deploy 阶段的 Commercialization Gate 由 StageRunner 通过 GateEngine 执行。五层检查规则（代码清洁度、包完整性、文档质量、可构建性、开箱即用）作为 Deploy 阶段的门禁规则内置在 RoleKnowledgeInjector 的 `templates/deploy-principles.md` 中。GateEngine 评估时加载这些规则，执行敏感信息扫描（`.env` 文件、API key 模式匹配、密钥文件、内部配置路径）和五层完整性检查。检查规则可通过 L2 配置扩展。

---

### 5.4 RoleKnowledgeInjector

**职责**：将 PM、UX、架构师、审计等角色的专业标准映射到流水线阶段，产出可注入的 prompt 模板。实现 Stage-Bound Design——能力绑定阶段，不绑定 Agent 身份。

**接口**：

| 方法 | 说明 |
|------|------|
| `getPrinciples(stageId): string` | 返回该阶段的执行原则模板 |
| `getGateRules(stageId): GateRule[]` | 返回该阶段的默认门禁规则 |

**阶段→原则映射**：

| 阶段 | 注入原则来源 | 模板位置 |
|------|-------------|----------|
| Spec | PM 最佳实践（用户价值优先、完整度校验、主动澄清） | `templates/spec-principles.md` |
| Contract | 架构师最佳实践（通用化三问、Stage-Bound Design、最小改动） | `templates/contract-principles.md` |
| Implement | 工程最佳实践（TDD 循环、Karpathy Guidelines、系统化调试） | `templates/implement-principles.md` |
| Review | 审计最佳实践（spec-code 覆盖、AC 矩阵、证据驱动） | `templates/review-principles.md` |
| Smoke Test / UX Acceptance | UX 最佳实践（陌生用户视角、开箱即用五维度） | `templates/ux-principles.md` |
| Deploy | 发布工程最佳实践（五层商用化检查、敏感信息扫描） | `templates/deploy-principles.md` |

**依赖**：`templates/` 目录下的 markdown 模板文件。无外部依赖。

**关键约束**：模板随 npm 包分发，用户可通过 L2 配置覆盖默认模板。

---

### 5.5 ComplianceRouter

**职责**：对未经 SEVO 编排的开发任务进行路由判定。根据合规模式（`guide` / `auto-route` / `off`）决定处理策略。

**接口**：

| 方法 | 说明 |
|------|------|
| `evaluate(taskContext): ComplianceResult` | 判断任务是否属于 SEVO 编排范围，返回处理策略 |
| `classifyLevel(description, codeStats?): Level` | 根据任务描述和代码统计判定 Level 0/1/2+ |

**三种模式行为**：

- `guide`（默认）：检测到未编排的开发任务时，在 prompt 中注入流程引导提示，建议走 SEVO 流程，不阻断执行。
- `auto-route`：自动为未编排的开发任务创建 pipeline 并路由进 SEVO 流程。
- `off`：不干预，SEVO 只管已显式创建的 pipeline。

**依赖**：

- SEVO Config：读取合规模式配置。

**关键约束**：没有「强制阻断」概念。即使 `auto-route` 模式也是创建 pipeline 并引导，不阻断任务执行。ComplianceRouter 仅被 PluginAdapter 调用（在 `before_tool_call` hook 中），不被 PipelineEngine 调用。`auto-route` 模式下，ComplianceRouter 返回 `{ action: create }` 后，由 PluginAdapter 调用 `PipelineEngine.createPipeline()` 创建新 pipeline，避免 ComplianceRouter 与 PipelineEngine 之间的循环依赖。

---

### 5.6 CLIInterface

**职责**：SEVO 的用户交互入口。提供 `bin/sevo.js` CLI，覆盖初始化、项目管理、FR 管理、状态查询和手动干预。

**命令清单**：

| 命令 | 说明 |
|------|------|
| `sevo init` | 环境检测 → 插件注册 → Agent 发现 → 角色分配 → doctor 检查 |
| `sevo doctor` | 配置完整性和环境就绪状态检查 |
| `sevo project create <name>` | 创建 Project，初始化标准目录结构 |
| `sevo project list` | 列出所有 Project |
| `sevo fr add <project> <desc>` | 添加 FR，自动触发 pipeline 创建 |
| `sevo fr list <project>` | 列出 Project 下所有 FR 及 pipeline 状态 |
| `sevo status [instance-id]` | 查看 pipeline 当前阶段、卡点、下一步 |
| `sevo pause / resume / cancel` | pipeline 生命周期控制 |
| `sevo ledger [project]` | 查看交付账本 |
| `sevo demo [--dry-run]` | 首次体验引导（dry-run 用 mock 数据，无需 LLM） |

**依赖**：

- PipelineEngine：pipeline 创建、状态查询、生命周期控制。
- ComplianceRouter：`sevo init` 时设置默认合规模式。
- 宿主环境检测：`findOpenClawHome()` 定位 `openclaw.json`，计算插件路径。
- LedgerEngine（`dist/` 库模块）：账本查询。

**关键约束**：CLI 不依赖特定宿主环境，在纯 Node.js 环境中可运行。OpenClaw 特有操作（插件注册、Agent 发现）仅在检测到 OpenClaw 环境时执行。

---

### 5.7 PluginAdapter

**职责**：OpenClaw 宿主的 Adapter 实现。通过 `register(api)` 回调注册三个 hook，将 PipelineEngine 的编排语义映射为 OpenClaw 的 prompt 注入 + 事件驱动模型。

**Hook 注册**：

| Hook | 触发时机 | 行为 |
|------|---------|------|
| `before_prompt_build` | 主会话构建 prompt 前 | 检测活跃 pipeline → 注入 `[SEVO Auto-Advance]` 指令（下一步该派发什么任务）+ 阶段执行原则 |
| `subagent_ended` | 子 Agent 完成时 | 解析 SEVO 标签 → 调用 `PipelineEngine.handleStageComplete()` → 设置下一阶段推进指令 |
| `before_tool_call` | 工具调用前 | 匹配 `sessions_spawn` → 注入 SEVO 标签到 label；ComplianceRouter 检查未编排任务 |

**标签协议**：`sevo:<pipelineId>:<stageId>:<attempt>`，用于关联子 Agent 任务与 pipeline 阶段。

**bridge.js 胶水层**：PluginAdapter 通过 `bridge.js` 动态加载 `../dist/` 下的编译产物（PipelineEngine、GateEngine、LedgerEngine 等）。加载失败则降级为 no-op，插件不崩溃。

**依赖**：

- OpenClaw Gateway API（通过 `register(api)` 注入，无 import 依赖）。
- PipelineEngine、StageRunner、ComplianceRouter（通过 bridge.js 动态加载）。
- RoleKnowledgeInjector（注入阶段执行原则到 prompt）。

**关键约束**：hook 不能发起工具调用（OpenClaw 平台限制），只能通过 prompt 注入引导主会话做出调度决策。主会话仍然是调度者，PluginAdapter 是编排顾问的宿主侧实现。

---

### 5.8 ClarificationCoordinator

**职责**：跨阶段模糊检测与主动澄清（FR-11）。在阶段执行过程中检测工件中的模糊信号，生成结构化澄清问题，将澄清结果回写到目标工件。

**接口**：

| 方法 | 说明 |
|------|------|
| `detectAmbiguity(stageId, artifact): AmbiguitySignal[]` | 扫描工件内容，返回检测到的模糊信号列表（8 种触发条件：未定义术语、矛盾约束、缺失边界、多义词、隐含假设、不完整场景、模糊优先级、未解决的开放问题） |
| `generateClarification(signals): ClarificationRequest` | 根据模糊信号生成结构化澄清问题，按 6 种类型分类（纠偏/方法/决策/边界/经验/元认知） |
| `resolveAndWriteBack(response, targetArtifact)` | 将澄清收敛结果回写到目标工件（spec/contract/实现方案），确保澄清结论不仅停留在对话中 |

**触发时机**：StageRunner 在以下阶段执行过程中调用 ClarificationCoordinator：

| 阶段 | 检测时机 | 澄清对象 |
|------|---------|----------|
| Spec | 工件输出前 | 用户或上游 Agent（通过宿主 Adapter 发起澄清问题） |
| Contract | 架构方案输出前 | 用户或 Spec 作者 |
| Implement | 检测到实现歧义时 | 上游阶段工件作者 |

**依赖**：

- RoleKnowledgeInjector：提供各阶段的模糊检测规则（内嵌在阶段执行原则模板中）。
- 宿主 Adapter：通过 `notify()` 向用户发起澄清问题，通过 `injectPrinciples()` 将澄清结果注入后续阶段。
- 本地文件系统：回写工件。

**关键约束**：澄清流程不阻断阶段执行。检测到模糊信号时，如果模糊度低于阈值，记录但不触发澄清；超过阈值时暂停阶段执行，等待澄清完成后继续。澄清超时（默认 24h）后自动升级为人工介入。

---

### 5.9 模块间依赖总览

```
                    ┌──────────────┐
                    │ CLIInterface │
                    └──────┬───────┘
                           │
                           ▼
┌───────────────┐   ┌──────────────────┐
│ PluginAdapter │──▶│  PipelineEngine  │
└──┬──┬──┬──┬───┘   └────────┬─────────┘
   │  │  │  │                │
   │  │  │  │                ▼
   │  │  │  │        ┌──────────────┐
   │  │  │  └───────▶│  StageRunner │
   │  │  │           └───┬──────┬──┘
   │  │  │               │      │
   │  │  │               ▼      ▼
   │  │  │  ┌──────────────────────┐  ┌──────────────────────────┐
   │  │  └─▶│ RoleKnowledgeInjector│  │ ClarificationCoordinator │
   │  │     └──────────────────────┘  └──────────────────────────┘
   │  │
   │  ▼
   │  ┌───────────────────┐
   └─▶│ ComplianceRouter  │
      └───────────────────┘
```

箭头表示调用方向。PluginAdapter 依赖 PipelineEngine、StageRunner、ComplianceRouter、RoleKnowledgeInjector 四个模块。ComplianceRouter 仅被 PluginAdapter 调用，不与 PipelineEngine 产生直接依赖。ClarificationCoordinator 被 StageRunner 调用。所有模块通过 TypeScript 接口解耦，宿主 Adapter 实现 `HostAdapter` 接口，核心模块不直接引用任何宿主 API。

## §6 运行时视图

本节描述 SEVO 五个关键运行时流程的交互时序。所有流程均以 OpenClaw 宿主为例；其他宿主通过 HostAdapter 实现等效行为。

### 6.1 Pipeline 创建（FR-12）

```
用户                CLI              PipelineEngine       文件系统
 │                   │                    │                   │
 │  sevo fr add      │                    │                   │
 │  <project> <desc> │                    │                   │
 │──────────────────▶│                    │                   │
 │                   │  classifyLevel()   │                   │
 │                   │───────────────────▶│                   │
 │                   │  Level + stages    │                   │
 │                   │◀───────────────────│                   │
 │                   │  createPipeline()  │                   │
 │                   │───────────────────▶│                   │
 │                   │                    │  生成实例 ID       │
 │                   │                    │  fr-<slug>-<date>-<seq>
 │                   │                    │                   │
 │                   │                    │  检查/补全目录结构  │
 │                   │                    │──────────────────▶│
 │                   │                    │  写 active-pipelines.json
 │                   │                    │──────────────────▶│
 │                   │                    │                   │
 │                   │                    │  状态: created → active
 │                   │                    │  触发 advance()    │
 │                   │  pipeline 已创建   │                   │
 │                   │◀───────────────────│                   │
 │  实例 ID + 状态   │                    │                   │
 │◀──────────────────│                    │                   │
```

关键行为：
- ComplianceRouter.classifyLevel() 根据任务描述判定 Level 0/1/2+，产出必经阶段清单。
- 同一 Project 已有 active 实例时，createPipeline() 拒绝创建并返回错误。
- 目录结构按 §3.6 规范补全，已有内容不覆盖。
- 创建完成后立即调用 advance()，pipeline 自动进入第一个阶段。

### 6.2 阶段推进（FR-13 PipelineEngine 核心循环）

```
PluginAdapter        PipelineEngine      StageRunner       主会话
(subagent_ended)          │                  │               │
 │                        │                  │               │
 │  handleStageComplete() │                  │               │
 │───────────────────────▶│                  │               │
 │                        │  evaluateGate()  │               │
 │                        │─────────────────▶│               │
 │                        │  { passed: true }│               │
 │                        │◀─────────────────│               │
 │                        │                  │               │
 │                        │  stage.status = passed           │
 │                        │  advance() → 下一阶段            │
 │                        │                  │               │
 │                        │  StageRunner.run(nextStage)      │
 │                        │─────────────────▶│               │
 │                        │                  │ getPrinciples()│
 │                        │                  │ (RoleKnowledge)│
 │                        │                  │               │
 │                        │                  │ 组装 StageContext
 │                        │                  │               │
 │  设置 [SEVO Auto-Advance] 指令            │               │
 │◀──────────────────────────────────────────│               │
 │                        │                  │               │
 │  before_prompt_build 注入                 │               │
 │──────────────────────────────────────────────────────────▶│
 │                        │                  │  主会话读取指令 │
 │                        │                  │  派发子 Agent   │
 │                        │                  │  (sessions_spawn)
```

关键行为：
- 门禁评估在阶段完成后 30 秒内完成（AC-13.2）。
- 门禁失败时 PipelineEngine 自动触发 Review Fix Loop（FR-06a），不推进到下一阶段。
- 并行阶段组（如 FR-06c + FR-06d）：组内阶段同时触发，全部 passed 后才推进。
- 每一步推进决策写入持久化状态文件，支持断点恢复。

门禁失败分支：

```
PipelineEngine      StageRunner       ReviewFixLoop
 │                      │                  │
 │  evaluateGate()      │                  │
 │─────────────────────▶│                  │
 │  { passed: false,    │                  │
 │    issues: [...] }   │                  │
 │◀─────────────────────│                  │
 │                      │                  │
 │  stage.status = blocked                 │
 │  triggerFixLoop(issues)                 │
 │────────────────────────────────────────▶│
 │                      │                  │  解析问题 → 生成 Fix Task
 │                      │                  │  P0/P1 排入修复队列
 │                      │                  │  修复完成 → 定向复验
 │                      │                  │  复验通过
 │  fixLoop.resolved()  │                  │
 │◀────────────────────────────────────────│
 │                      │                  │
 │  stage.status = active                  │
 │  重新评估门禁 → advance()               │
```

### 6.3 sevo init 初始化流程（FR-14）

```
用户              CLI(sevo init)      文件系统         openclaw.json
 │                    │                  │                  │
 │  npx sevo init     │                  │                  │
 │───────────────────▶│                  │                  │
 │                    │                  │                  │
 │                    │  检测宿主环境     │                  │
 │                    │  findOpenClawHome()                 │
 │                    │─────────────────────────────────────▶│
 │                    │  读取 agents.list │                  │
 │                    │◀─────────────────────────────────────│
 │                    │                  │                  │
 │                    │  Agent 发现与角色映射                │
 │                    │  命名规则 + runtime type + 显式声明  │
 │                    │  单 Agent → 降级模式（全角色同一 ID） │
 │                    │                  │                  │
 │                    │  生成 sevo.config.json               │
 │                    │─────────────────▶│                  │
 │                    │                  │                  │
 │                    │  注册插件到 openclaw.json            │
 │                    │  plugins.load.paths += sevo/plugin
 │                    │─────────────────────────────────────▶│
 │                    │                  │                  │
 │                    │  注入角色 SOUL.md │                  │
 │                    │  roles/<agentId>/agent/SOUL.md       │
 │                    │─────────────────▶│                  │
 │                    │                  │                  │
 │                    │  sevo doctor     │                  │
 │                    │  (配置完整性检查) │                  │
 │                    │                  │                  │
 │  角色分配表 +       │                  │                  │
 │  下一步指引         │                  │                  │
 │◀───────────────────│                  │                  │
```

关键行为：
- 三层 Agent 发现信号：命名规则（dev-/audit-/sa-/pm-/ux- 前缀）→ runtime type（subagent/acp）→ 显式声明（sevo.config 中手动指定）。
- 单 Agent 环境自动降级：所有角色池填入同一个 agentId，质量降级但功能完整。
- 非 OpenClaw 环境跳过插件注册和 Agent 发现，只生成配置文件和模板。
- doctor 检查失败时输出逐项修复建议，不阻断 init 完成。

### 6.4 合规路由（auto-route 模式，FR-13 + ComplianceRouter）

```
主会话              PluginAdapter       ComplianceRouter    PipelineEngine
 │                      │                    │                  │
 │  sessions_spawn      │                    │                  │
 │  (开发任务,无 SEVO 标签)                   │                  │
 │─────────────────────▶│                    │                  │
 │                      │                    │                  │
 │  before_tool_call    │                    │                  │
 │                      │  evaluate(task)    │                  │
 │                      │───────────────────▶│                  │
 │                      │                    │  模式=auto-route  │
 │                      │                    │  classifyLevel()  │
 │                      │                    │  → Level 1        │
 │                      │  { action: create }│                  │
 │                      │◀───────────────────│                  │
 │                      │                    │                  │
 │                      │  createPipeline()  │                  │
 │                      │──────────────────────────────────────▶│
 │                      │                    │  pipeline 已创建  │
 │                      │◀──────────────────────────────────────│
 │                      │                    │                  │
 │                      │  注入 SEVO 标签到 spawn label         │
 │                      │  sevo:<pipelineId>:spec:1             │
 │                      │                    │                  │
 │  spawn 继续执行      │                    │                  │
 │  (带 SEVO 标签)      │                    │                  │
 │◀─────────────────────│                    │                  │
```

关键行为：
- `guide` 模式下不创建 pipeline，只在 prompt 中注入流程引导提示。
- `off` 模式下 evaluate() 直接返回 `{ action: pass }`，不干预。
- `auto-route` 模式下自动创建 pipeline 并注入标签，任务无感知地进入 SEVO 流程。
- 标签协议 `sevo:<pipelineId>:<stageId>:<attempt>` 用于 subagent_ended hook 关联完成事件。

### 6.5 澄清流程（FR-11 Proactive Clarification）

```
StageRunner          ClarificationCoordinator    宿主 Adapter       用户/上游 Agent
 │                          │                       │                  │
 │  detectAmbiguity()       │                       │                  │
 │────────────────────────▶│                       │                  │
 │  signals[]               │                       │                  │
 │◀────────────────────────│                       │                  │
 │                          │                       │                  │
 │  [模糊度 > 阈值]         │                       │                  │
 │  generateClarification()  │                       │                  │
 │────────────────────────▶│                       │                  │
 │  ClarificationRequest    │                       │                  │
 │◀────────────────────────│                       │                  │
 │                          │                       │                  │
 │  暂停阶段执行              │                       │                  │
 │                          │  notify(澄清问题)      │                  │
 │                          │─────────────────────▶│                  │
 │                          │                       │  澄清问题         │
 │                          │                       │────────────────▶│
 │                          │                       │                  │
 │                          │                       │  澄清回复         │
 │                          │                       │◀────────────────│
 │                          │  澄清回复              │                  │
 │                          │◀─────────────────────│                  │
 │                          │                       │                  │
 │  resolveAndWriteBack()   │                       │                  │
 │────────────────────────▶│                       │                  │
 │                          │  回写工件              │                  │
 │                          │─────────────────────▶│                  │
 │                          │                       │                  │
 │  恢复阶段执行              │                       │                  │
 │  (工件已更新)              │                       │                  │
```

关键行为：
- 模糊度低于阈值时，记录信号但不触发澄清，阶段继续执行。
- 模糊度超过阈值时，暂停阶段执行，通过宿主 Adapter 向用户或上游 Agent 发起澄清。
- 澄清回复到达后，ClarificationCoordinator 将收敛结果回写到目标工件，确保澄清结论不仅停留在对话中。
- 澄清超时（默认 24h）后自动升级为人工介入，阶段状态转为 blocked。
- 澄清记录作为阶段工件的一部分归档到 Ledger。

---

## §7 部署视图

### 7.1 npm 包结构

SEVO 以单个 npm 包 `sevo` 分发，包含三个入口：

```
sevo/                             # npm 包根目录
├── bin/
│   └── sevo.js                   # CLI 入口（#!/usr/bin/env node）
├── dist/                         # 编译产物（ESM）
│   ├── index.js                  # 库 API 主入口
│   ├── pipeline-engine.js        # PipelineEngine
│   ├── stage-runner.js           # StageRunner
│   ├── gate-engine.js            # GateEngine（门禁评估）
│   ├── ledger-engine.js          # LedgerEngine（交付账本）
│   ├── compliance-router.js      # ComplianceRouter
│   ├── role-knowledge-injector.js
│   ├── adapters/
│   │   ├── host-adapter.js       # HostAdapter 接口定义
│   │   └── openclaw-adapter.js   # OpenClaw 宿主适配实现
│   └── types/                    # TypeScript 类型声明（.d.ts）
├── plugin/                       # OpenClaw 插件目录
│   ├── openclaw.plugin.json      # 插件元数据（name, version, hooks）
│   ├── index.js                  # register(api) 入口
│   └── bridge.js                 # 胶水层：动态加载 ../dist/ 编译产物
├── templates/                    # 角色执行原则模板
│   ├── spec-principles.md
│   ├── contract-principles.md
│   ├── implement-principles.md
│   ├── review-principles.md
│   ├── ux-principles.md
│   └── deploy-principles.md
├── package.json                  # name, bin, main, exports, files
├── README.md
└── LICENSE
```

分发原则：
- npm 包只包含编译产物（dist/）+ 插件（plugin/）+ 模板（templates/）+ CLI（bin/）+ 文档。
- TypeScript 源码不随 npm 包分发，通过 GitHub 独立仓库提供。
- `dependencies` 为空（零运行时依赖），OpenClaw SDK 通过 `register(api)` 回调注入。

### 7.2 sevo init 注册流程

`sevo init` 在 OpenClaw 环境中执行以下注册操作：

```
1. 检测 OpenClaw 安装
   └─ findOpenClawHome() → 定位 ~/.openclaw/openclaw.json
   └─ 未找到 → 输出安装引导链接，跳过插件注册

2. 注册插件
   └─ 计算插件绝对路径：<npm-global>/sevo/plugin/
   └─ 写入 openclaw.json → plugins.load.paths 追加插件路径
   └─ 不覆盖已有条目（幂等）

3. Agent 发现与角色分配
   └─ 读取 openclaw.json → agents.list
   └─ 三层信号匹配：
      ├─ 命名规则：dev-* → coding, audit-* → review, sa-* → architecture, pm-* → pm, ux-* → ux
      ├─ runtime type：subagent / acp 均可分配
      └─ 显式声明：sevo.config.json 中手动指定优先
   └─ 单 Agent 环境 → 所有角色池填入同一 agentId

4. 生成配置文件
   └─ <workspace>/sevo.config.json
      ├─ complianceMode: "guide"
      ├─ roles: { developer: [...], reviewer: [...], product: [...], ux: [...] }
      ├─ stateDir: "<workspace>/.sevo/"
      └─ templates: "<npm-global>/sevo/templates/"

5. 健康检查（sevo doctor）
   └─ 插件路径可达？配置完整？Agent 角色覆盖？
   └─ 每个问题附修复建议

6. 输出结果
   └─ 角色分配表 + 合规模式 + 下一步指引
   └─ 提示用户重启 Gateway 使插件生效
```

### 7.3 与 OpenClaw extensions 的关系

SEVO 插件通过两种路径被 OpenClaw Gateway 加载：

| 加载方式 | 路径 | 触发条件 |
|---------|------|----------|
| plugins.load.paths | `openclaw.json` 中显式声明的插件目录 | `sevo init` 自动注册 |
| extensions 自动扫描 | `~/.openclaw/extensions/sevo/plugin/` | 手动 symlink 或 `npm link` |

推荐方式是 `sevo init` 自动注册到 `plugins.load.paths`，无需手动操作。

Gateway 加载插件时调用 `plugin/index.js` 的 `register(api)` 函数，api 对象提供 hook 注册、配置读取、日志等能力。SEVO 插件通过 `bridge.js` 动态加载 `../dist/` 下的核心模块，将 PipelineEngine 的编排语义映射为 OpenClaw 的 hook 事件模型。

加载失败处理：`bridge.js` 加载 `dist/` 失败时（如编译产物缺失），插件降级为 no-op——hook 注册成功但回调函数不执行任何操作，Gateway 不崩溃，用户通过 `sevo doctor` 发现问题。

### 7.4 运行时文件布局

SEVO 运行时在宿主 workspace 下产生以下文件：

```
<workspace>/
├── sevo.config.json              # SEVO 全局配置
├── .sevo/                        # SEVO 运行时状态（gitignore）
│   ├── active-pipelines.json     # 活跃 pipeline 实例状态
│   └── ledger.json               # 交付账本
└── projects/<project-slug>/      # 项目目录（§3.6 标准结构）
    ├── docs/
    ├── src/
    ├── tests/
    ├── reports/
    └── artifacts/
```

`.sevo/` 目录包含运行时状态，应加入 `.gitignore`。`active-pipelines.json` 是 PipelineEngine 的持久化状态文件，Gateway 重启后据此恢复中断的 pipeline（AC-13.8）。

## §8 横切关注点

本节描述贯穿 SEVO 所有模块和阶段的横切设计决策。

### 8.1 Fail-Open 设计

SEVO 作为宿主环境的插件运行，核心约束是：插件异常不能拖垮宿主。所有模块遵循 fail-open 原则——出错时降级放行，不阻塞宿主正常工作。

**降级层次**：

| 故障场景 | 降级行为 | 用户感知 |
|---------|---------|----------|
| `bridge.js` 加载 `dist/` 失败（编译产物缺失） | hook 注册成功但回调 no-op，Gateway 正常启动 | `sevo doctor` 报告问题，pipeline 不推进 |
| PipelineEngine 状态文件损坏 | 跳过自动恢复，记录错误日志，等待 `sevo doctor` 修复 | 已有 pipeline 暂停，新 pipeline 可创建 |
| StageRunner 门禁评估抛异常 | 门禁结果视为 `{ passed: false, issues: [内部错误] }` | pipeline 阻断在当前阶段，不会误放行 |
| ComplianceRouter 分类失败 | 默认返回 `{ action: pass }`，不干预任务 | 任务正常执行，不进入 SEVO 编排 |
| 宿主 Adapter hook 执行超时（>5s） | 中断 hook 执行，放行原始操作 | 当次阶段推进指令缺失，下一轮 `before_prompt_build` 补偿 |

**设计原则**：
- 门禁异常时倾向阻断（fail-closed），防止未经审查的工件流入下游。
- 非门禁环节异常时倾向放行（fail-open），保证宿主可用性。
- 所有降级事件写入结构化日志，`sevo doctor` 可检测并报告。

### 8.2 渐进式披露 L0–L3

四级配置分层对应不同用户成熟度，每级能力累加（spec FR-15）。

**L0 安装即用**：
- `sevo init` 后零配置可用。阶段定义、门禁规则、路由策略、角色执行原则全部内置。
- 单 Agent 环境自动降级：所有角色池填入同一 agentId，功能完整但质量保证降级。
- 合规模式默认 `guide`——注入流程引导提示，不阻断执行。
- 配置文件 `sevo.config.json` 由 `sevo init` 自动生成，用户无需手动创建。

**L1 按需配置**：
- 用户编辑 `sevo.config.json` 调整：路由级别阈值、门禁严格度（strict/standard/relaxed）、通知渠道、发布目标、合规模式。
- 修改任一配置不破坏 pipeline 运行——配置校验失败时回退到 L0 默认值并警告。
- 从 L0 升级到 L1 不需要重新初始化。

**L2 自定义阶段**：
- 用户可在标准阶段序列中插入自定义阶段（如 Security Audit、Performance Test）。
- 自定义阶段必须声明输入工件、输出工件和门禁规则，PipelineEngine 按统一状态机驱动。
- 用户可覆盖默认角色执行原则模板。

**L3 编程控制**：
- 通过库 API 编程控制 pipeline 行为：创建、查询、门禁覆写、工件读取。
- 支持自定义 HostAdapter（对接非 OpenClaw 宿主）。
- 支持自定义阶段执行器（替换默认 Skill 执行）。

**解锁条件**：L0 自动生效；L1 编辑配置文件即解锁；L2 在配置中声明 `customStages` 即解锁；L3 通过 `import { PipelineEngine } from 'sevo'` 编程使用即解锁。

### 8.3 配置 Schema

`sevo.config.json` 是 SEVO 的唯一配置文件，由 `sevo init` 生成，用户按需编辑。完整字段定义：

```jsonc
{
  // L0 默认值——sevo init 自动填充，用户无需修改
  "complianceMode": "guide",        // "guide" | "auto-route" | "off"
  "roles": {                         // Agent 角色池，sevo init 自动发现填充
    "coding": ["dev-01"],
    "review": ["audit-01"],
    "architecture": ["sa-01"],
    "pm": ["pm-01"],
    "ux": ["ux-01"],
    "general": []                    // 未匹配到专业角色的 Agent 归入通用池
  },

  // L1 按需配置
  "routing": {
    "levelThresholds": {
      "level1MinLines": 50,           // 改动行数 ≥ 此值进入 Level 1
      "level2MinLines": 500,          // 改动行数 ≥ 此值进入 Level 2+
      "level2MinFiles": 10            // 改动文件数 ≥ 此值进入 Level 2+
    }
  },
  "gate": {
    "strictness": "standard",        // "strict" | "standard" | "relaxed"
    "reviewFixMaxRounds": 3          // Review Fix Loop 最大轮次
  },
  "notification": {
    "channel": "none",               // "feishu" | "slack" | "discord" | "none"
    "webhookUrl": ""                 // 通知渠道 webhook 地址
  },
  "publishTarget": [],               // ["npm", "github", "clawhub"]

  // L2 自定义阶段
  "customStages": [],                // 自定义阶段声明数组

  // 内部状态（sevo init 写入，用户不应手动修改）
  "hostType": "openclaw",            // "openclaw" | "standalone" | "other"
  "pluginPath": "",                  // 插件绝对路径（OpenClaw 环境）
  "stateDir": ".sevo/",              // 运行时状态目录
  "version": "1.0.0"                 // 配置 schema 版本
}
```

**校验规则**：
- `sevo doctor` 对配置做完整性校验，缺失字段用 L0 默认值补全并警告。
- `complianceMode` 只接受三个枚举值，非法值回退到 `guide`。
- `roles` 中引用的 agentId 必须在宿主 `agents.list` 中存在（OpenClaw 环境），不存在时 doctor 报 warning。
- `publishTarget` 中的值必须是 `npm`、`github`、`clawhub` 之一。

### 8.4 测试策略

SEVO 的测试分三层，覆盖从单元到端到端的完整验证链路。

**单元测试**：
- 覆盖核心模块的纯逻辑：ComplianceRouter.classifyLevel()、GateEngine 门禁评估、PipelineEngine 状态机流转、RoleKnowledgeInjector 模板映射。
- 测试框架：项目标准测试框架（随技术选型确定）。
- 不依赖文件系统或宿主环境，全部通过接口 mock 隔离。
- 覆盖目标：核心状态机路径 100%，门禁判定逻辑 100%。

**集成测试**：
- 验证模块间协作：CLI → PipelineEngine → StageRunner → GateEngine 的完整调用链。
- 使用内存文件系统或临时目录模拟工件读写。
- 验证 `sevo init` 在 OpenClaw 环境和 standalone 环境下的行为差异。
- 验证 pipeline 创建 → 阶段推进 → 门禁评估 → 状态持久化的完整流程。
- 验证并行阶段（FR-02a/b/c + FR-03；FR-06c + FR-06d）的正确编排。

**端到端验证**：
- `sevo demo --dry-run`：无 LLM 环境下用 mock 数据跑通完整 pipeline 阶段流转，验证安装正确性和工件结构。
- `sevo demo`：有 LLM 环境下用内置示例项目跑通真实 Level 0 pipeline。
- 陌生人走查脚本（`scripts/npm-stranger-verify.sh`）：在干净 `/tmp/` 目录中模拟无 SEVO 环境，从 `npm install` 开始验证开箱即用。
- Gateway 重启恢复测试：创建 active pipeline → 模拟 Gateway 重启 → 验证 pipeline 在 60s 内自动恢复推进（AC-13.8）。

### 8.5 安全与权限

**文件系统访问范围**：
- SEVO 的读写范围限定在三个区域：`sevo.config.json`（配置）、`.sevo/`（运行时状态）、`projects/`（项目工件）。
- 插件注册时写入宿主 `openclaw.json`（仅 `sevo init` 阶段，运行时只读）。
- 角色 SOUL.md 注入写入 `roles/<agentId>/agent/SOUL.md`（仅 `sevo init` 阶段）。
- 运行时不访问上述范围之外的文件系统路径。

**配置敏感字段处理**：
- `sevo.config.json` 不存储任何密钥、token 或凭据。
- 通知渠道的 webhook URL 是唯一的半敏感字段——`sevo doctor` 输出时脱敏显示（只显示域名部分）。
- 发布凭据（npm token、GitHub token）由宿主环境管理，SEVO 通过环境变量或宿主 Adapter 间接获取，不写入自身配置。

**审计独立性**（NFR-5.13）：
- Review 阶段执行者必须与 Implement 阶段执行者不同（角色池级别隔离）。
- 单 Agent 降级模式下，同一 Agent 执行所有阶段，但 Review 阶段的执行原则仍然注入审计视角的 prompt，确保审计思维存在。
- Ledger 记录每个阶段的实际执行者 agentId，支持事后追溯。

**商用化门禁敏感信息扫描**（FR-08a）：
- Deploy 前的 Commercialization Gate 自动扫描待发布文件中的敏感内容：`.env` 文件、API key 模式匹配、密钥文件、内部配置路径。
- 发现敏感内容时阻断发布并报告具体文件和行号。
- 扫描规则可通过 L2 配置扩展。
