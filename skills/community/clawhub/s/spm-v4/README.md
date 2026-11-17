# SPM V4 🚀 — Super Project Manager

> **AI 编程 Agent 的生产级项目管理引擎**
>
> **Production-grade project management engine for AI coding agents.**
>
> WBS 台账 · 六阶段状态机 · SHA-256 哈希认证 · 三域 Event Store · YAML 安全门 · 子代理编排
>
> WBS Ledger · 6-Phase State Machine · SHA-256 Attestation · 3-Domain Event Store · YAML Security Gate · Sub-agent Orchestration

---

## 简介 · Introduction

### 中文

**SPM V4**（Super Project Manager v4）是一个专为 AI 编程 Agent 设计的 **OpenClaw Skill**，用于管理多步骤、多文件、跨会话的软件开发项目。

当 AI Agent 执行复杂项目时，SPM V4 提供结构化的工作分解、进度追踪、完整性验证和审计追溯——确保每一个任务都可追踪、可验证、可恢复。

### English

**SPM V4** (Super Project Manager v4) is an **OpenClaw Skill** purpose-built for AI coding agents managing multi-step, multi-file, cross-session software development projects.

When an AI agent takes on complex projects, SPM V4 provides structured work decomposition, progress tracking, integrity verification, and audit trail — ensuring every task is traceable, verifiable, and recoverable.

---

## 核心特性 · Key Features

| 特性 Feature | 中文 | English |
|---|---|---|
| **WBS 台账 Ledger** | 任务分解、进度追踪、上下文保存 | Task decomposition, progress tracking, context persistence |
| **SHA-256 哈希认证 Attestation** | 每次台账变更锁定，防篡改 | Lock each ledger change, tamper-proof |
| **六阶段状态机 State Machine** | 从需求到交付的完整生命周期 | Full lifecycle from requirements to delivery |
| **三域 Event Store** | 审计/完整性/质量门禁全部可追溯 | Full traceability across audit, integrity, and quality domains |
| **YAML 安全门 Security Gate** | 危险命令自动拦截 | Automatic dangerous command interception |
| **子代理 Prompt 模板** | 4 种角色：实现者/规范审查/质量审查/计划审查 | 4 roles: implementer, spec-reviewer, quality-reviewer, plan-reviewer |

---

## 快速开始 · Quick Start

### 中文

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
npm test    # 269 个测试全部通过
```

### English

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
npm test    # All 269 tests pass
```

---

## 模块架构 · Module Architecture

### 中文

```
src/
├── SKILL.md             ← Agent 指令（核心使用文档）
├── src/
│   ├── engine/          ← 六阶段状态机（context-init → delivery）
│   ├── event-store/     ← 三域事件存储（audit/integrity/quality）
│   ├── security/        ← YAML 安全门（safe/risky/dangerous）
│   ├── wbs/             ← WBS 台账 + SHA-256 + Merkle 树
│   ├── hooks/           ← 中间件注册表
│   ├── session/         ← 心跳日志 + 会话恢复
│   ├── config/          ← YAML 配置加载 + 校验
│   └── validation/      ← Zod 输入校验
├── prompts/             ← 4 种子代理 Prompt
├── templates/           ← WBS 台账/验证报告模板
├── tests/               ← 269 个 Jest 测试（6 套件）
├── config/              ← 安全策略 YAML
├── package.json
└── TUTORIAL.md          ← 完整教程
```

### English

```
src/
├── SKILL.md             ← Agent instructions (core usage doc)
├── src/
│   ├── engine/          ← 6-phase state machine (context-init → delivery)
│   ├── event-store/     ← 3-domain event store (audit/integrity/quality)
│   ├── security/        ← YAML security gate (safe/risky/dangerous)
│   ├── wbs/             ← WBS ledger + SHA-256 + Merkle tree
│   ├── hooks/           ← Middleware registry
│   ├── session/         ← Heartbeat log + session recovery
│   ├── config/          ← YAML config loading + validation
│   └── validation/      ← Zod input validation
├── prompts/             ← 4 sub-agent prompt templates
├── templates/           ← WBS ledger / validation report templates
├── tests/               ← 269 Jest tests (6 suites)
├── config/              ← Security policy YAML
├── package.json
└── TUTORIAL.md          ← Full tutorial
```

---

## 核心模块详解 · Core Modules

### Engine — 六阶段状态机 · 6-Phase State Machine

```text
Context Init → Requirement → Planning → Execution → Quality → Delivery
     ↑                                                          │
     └────────────────── 迭代循环 Iteration Loop ───────────────┘
```

### WBS — 台账与哈希认证 · Ledger & Hash Attestation

| 操作 Operation | 说明 Description |
|---|---|
| `wbs.load(path)` | 加载台账文件 Load ledger file |
| `wbs.update(id, fields)` | 更新任务状态 Update task status |
| `wbs.attest()` | SHA-256 哈希认证 Generate hash attestation |

### Event Store — 三域事件存储 · 3-Domain Event Store

- **audit** — 子代理调度记录 Sub-agent dispatch records
- **integrity** — 哈希认证历史 Hash attestation history
- **quality** — 质量门禁结果 Quality gate results

### Security Gate — YAML 安全门

| 等级 Level | 行为 Action | 说明 Description |
|---|---|---|
| `safe` | `allow` | 放行 Allow |
| `risky` | `warn` | 警告并确认 Warn and confirm |
| `dangerous` | `block` | 阻止拦截 Block |

---

## CLI 命令 · CLI Commands

| 命令 Command | 中文说明 | English Description | 典型场景 Typical Use |
|---|---|---|---|
| `init <name>` | 初始化项目结构 | Initialize project structure | 新项目开头 Starting a new project |
| `attest [path]` | SHA-256 哈希认证 | Generate SHA-256 attestation | 每次台账变更后 After each ledger change |
| `verify [path]` | 验证完整性 | Verify WBS integrity | 跨会话恢复前 Before cross-session recovery |
| `quality-check [path]` | 质量门禁（5 项检查） | Run quality gates (5 checks) | 交付前 Before delivery |
| `status` | 查看项目状态 | Show project status | 随时查看进度 Check progress anytime |
| `doctor` | 健康检查（18 项） | Run health check (18 items) | 部署前诊断 Pre-deployment diagnostics |

---

## 与 Shell v3 对比 · Comparison with Shell v3

| 维度 Dimension | Shell v3 | SPM V4 |
|---|---|---|
| 语言 Language | Bash + Python | **Node.js ES Modules** |
| 代码量 Codebase size | 22 workflow + 15 skill files | **6 modules + tests** |
| 可测试性 Testability | 几乎不可测 Nearly untestable | **269 tests** |
| 结构化日志 Structured logging | 无 None | **Pino** |
| 输入校验 Input validation | 无 None | **Zod** |
| 并发控制 Concurrency control | 无 None | **proper-lockfile** |
| 崩溃恢复 Crash recovery | 无 None | **JSONL checksum + skip corrupt lines** |
| YAML 安全 YAML security | 无 None | **parse() safe mode** |
| 子代理 Prompt Sub-agent prompts | 4 个文件 4 files | **4 个移植文件 4 ported files** |
| 规模 Size | 964 KB | **97 KB**（纯引擎 pure engine）|

---

## 安装 · Installation

### 中文

**方式 1：直接运行**

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
```

**方式 2：全局安装**

```bash
npm install -g
spm init my-project
```

### English

**Option 1: Run directly**

```bash
git clone https://github.com/zhbcher/SPM-V4.git
cd SPM-V4
npm install
```

**Option 2: Global install**

```bash
npm install -g
spm init my-project
```

---

## 六阶段生命周期 · 6-Phase Lifecycle

### 中文

SPM V4 将项目开发分为 6 个阶段，由 Engine 状态机管理：

| 阶段 Phase | 说明 Description |
|---|---|
| Phase 0: 上下文初始化 Context Init | 解析需求、加载上下文 Parse requirements, load context |
| Phase 1: 需求分析 Requirement | 确认功能需求 Confirm functional requirements |
| Phase 2: 计划分解 Planning | 创建 WBS 任务分解 Create WBS task breakdown |
| Phase 3: 执行开发 Execution | todo → doing → done + evidence 循环 |
| Phase 4: 质量门禁 Quality | 5 项检查全部通过 5 checks must all pass |
| Phase 5: 交付 Delivery | 最终验证并交付 Final verification and delivery |

### English

SPM V4 divides project development into 6 phases managed by the Engine state machine:

| Phase | Description |
|---|---|
| Phase 0: Context Init | Parse requirements, load context |
| Phase 1: Requirement | Confirm functional requirements |
| Phase 2: Planning | Create WBS task breakdown |
| Phase 3: Execution | todo → doing → done + evidence loop |
| Phase 4: Quality | All 5 checks must pass |
| Phase 5: Delivery | Final verification and delivery |

### 在代码中使用 · Use in Code

```js
import { Engine } from 'spm-v4/src/engine/index.js';

const engine = new Engine(config);
engine.phase('requirement');    // 进入需求阶段 Enter requirement phase
engine.transition('planning');  // 转换到计划阶段 Transition to planning
engine.currentPhase();          // 当前阶段 Current phase
```

---

## 核心 API · Core API

```js
// Engine — 状态机 State Machine
const engine = new Engine(config);
engine.phase('planning');
engine.transition('execute');
engine.currentPhase();

// Event Store — 事件存储
const store = new EventStore(config);
store.push('audit', event);
store.push('integrity', { type: 'wbs_attestation', data: { hash: 'a3f8c2...' } });
store.push('quality', { type: 'gate_result', data: { passed: true, checks: 5 } });
store.query('quality', filter);

// Security Gate — 安全门
const gate = new SecurityGate(policy);
gate.check('rm -rf /');          // { action: 'block', level: 'dangerous' }
gate.check('echo hello');        // { action: 'allow', level: 'safe' }

// WBS — 台账管理 Ledger Management
const wbs = new WBS(config);
wbs.load('docs/spm/ledger.md');
wbs.update('task-3', { status: 'done', evidence: 'npm test passed' });
wbs.attest();                    // SHA-256 + Merkle
```

---

## 子代理编排 · Sub-agent Orchestration

### 中文

SPM V4 提供 4 种子代理 Prompt 模板，通过 `sessions_spawn` 调度：

| Prompt | 协作模式 Collaboration Mode |
|---|---|
| `implementer` | 接收任务描述，返回实现代码 + 验证结果 Receives task, returns code + verification |
| `spec-reviewer` | 审查设计文档，确认符合需求 Reviews design docs against requirements |
| `quality-reviewer` | 审查代码质量，检查测试覆盖 Reviews code quality, checks test coverage |
| `plan-reviewer` | 审查 WBS 计划完整性 Reviews WBS plan completeness |

### English

SPM V4 provides 4 sub-agent prompt templates dispatched via `sessions_spawn`:

| Prompt | Collaboration Mode |
|---|---|
| `implementer` | Receives task, returns code + verification |
| `spec-reviewer` | Reviews design docs against requirements |
| `quality-reviewer` | Reviews code quality, checks test coverage |
| `plan-reviewer` | Reviews WBS plan completeness |

---

## 安全门配置 · Security Gate Configuration

### 中文

在项目目录创建 `config/security-policy.yaml`：

### English

Create `config/security-policy.yaml` in your project root:

```yaml
rules:
  - pattern: "^rm -rf /"
    level: dangerous
    action: block
    reason: "Destructive filesystem operation"
  - pattern: "^git push --force"
    level: risky
    action: warn
    reason: "Force push may overwrite history"
  - pattern: "^npm publish"
    level: risky
    action: warn
    reason: "Publishing to npm requires confirmation"
```

---

## 质量门禁 · Quality Gate

### 中文

完成所有任务后执行 Quality Gate，5 项检查全部通过才能交付：

### English

Execute Quality Gate after completing all tasks. All 5 checks must pass before delivery:

```text
□ 所有 done 任务有 Evidence / All done tasks have Evidence
□ Evidence 匹配 Exit Criteria / Evidence matches Exit Criteria
□ 无循环依赖 / No circular dependencies
□ 所有依赖任务已 done（或 skipped）/ All dependency tasks are done (or skipped)
□ 哈希认证匹配 / Hash attestation matches
```

---

## License

MIT