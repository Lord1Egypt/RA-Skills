---
name: repo-analysis
description: "Read, explain, and evaluate a software repository or GitHub project in an engineering-oriented way. Use when the user asks to read a repo, understand a codebase, analyze architecture, evaluate whether a project is worth following or adopting, prepare onboarding notes, or summarize stack, module boundaries, risks, and entry points. Supports three output modes: 速读版, 架构版, and 接手评审版. Also supports a lightweight GitHub health layer for public repositories when the user asks whether a project is worth following, adopting, or referencing. Triggers include requests like 读一下这个项目, 看看这个 GitHub 仓库, 分析一下 repo, 这个项目怎么样, 帮我快速理解代码结构, 给我一个架构分析, or 给我一个接手评审."
---

# Repo Analysis

## Overview

Use this skill to turn an unfamiliar repository into a concrete engineering assessment.
The goal is not to restate the README, but to identify what the project is, how it is structured, how it runs, where the main boundaries are, and what risks or follow-up questions matter.

Default mindset:
- engineering-first
- evidence-first
- broad scan before deep reading
- explicit separation of fact, inference, and unknowns

## Output modes

Choose one mode as early as possible.
If the user does not specify, choose the lightest mode that still answers the request.
Prefer explicit user choice over automatic detection.

### Mode 1: 速读版

Use when the user wants a fast understanding.
Typical asks:
- "读一下这个项目"
- "帮我看看这个 repo 是干嘛的"
- "快速理解一下这个仓库"

Goal:
- tell the user what the project is
- identify stack and repo shape
- map the top-level modules
- summarize major strengths and risks
- recommend what to read next

Depth:
- broad scan
- minimum high-signal files
- one or two entry points at most

Expected output size:
- short to medium

### Mode 2: 架构版

Use when the user wants system structure, runtime flow, or design analysis.
Typical asks:
- "给我一个架构分析"
- "这个项目主链路是什么"
- "帮我拆一下模块边界"
- "分析它怎么运行的"

Goal:
- explain the system shape
- map module boundaries and ownership
- trace one or two critical execution paths
- identify important abstractions and complexity hotspots

Depth:
- targeted deep reading of core services and entry points
- may include backend, frontend, plugin, runtime, queue, or deployment chain

Expected output size:
- medium to long

### Mode 3: 接手评审版

Use when the user wants adoption, maintenance, or takeover judgment.
Typical asks:
- "这个项目值不值得接手"
- "给我一个接手评审"
- "我们要不要基于它二开"
- "从工程上看风险大不大"

Goal:
- judge maturity, maintainability, and operational complexity
- identify high-risk modules and safer entry points
- estimate onboarding/takeover cost
- suggest a pragmatic reading and change strategy

Depth:
- architecture + repo health + risk evaluation
- optional GitHub enhancement when public metadata matters

Expected output size:
- medium to long

## Automatic mode selection

When the user does not explicitly choose a mode, infer it from intent.

### Default to 速读版

Use 速读版 when the user says things like:
- "读一下这个项目"
- "看看这个 repo"
- "这个项目怎么样"
- "快速理解一下"
- "帮我看看它是做什么的"

Behavior:
- give a concise engineering summary
- if it is a public GitHub repo, optionally add a light GitHub health layer
- do not expand into deep architecture unless needed
- by default, follow only one main execution path; avoid second-layer architecture decomposition unless the user asks
### Default to 架构版

Use 架构版 when the user says things like:
- "给我一个架构分析"
- "主链路是什么"
- "模块边界怎么划分"
- "怎么运行的"
- "message flow / runtime / workflow 怎么走"

Behavior:
- trace entry points and critical flows
- prioritize runtime, message, deployment, or plugin boundaries when relevant
- answer primarily "系统怎么工作"
- do not spend too much space on adoption judgment unless asked

### Default to 接手评审版

Use 接手评审版 when the user says things like:
- "值不值得接手"
- "适不适合二开"
- "风险大不大"
- "给我一个接手评审"
- "我们要不要基于它做"

Behavior:
- prioritize maintainability, maturity, complexity, and safe entry points
- explicitly identify high-risk modules
- answer primarily "我们敢不敢接、该怎么接、代价是什么"
- suggest an onboarding and modification strategy

### Explicit override wins

If the user explicitly asks for:
- "速读版"
- "架构版"
- "接手评审版"

Then use that mode directly, even if other phrasing suggests something else.

### Mixed requests

If the user mixes intents, choose a primary mode and keep the rest lightweight.

Example:
- "先快速看一下，再说值不值得接手"
  - primary mode: 速读版
  - secondary: add a short takeover judgment

If both parts are clearly important, say which mode you are using first and note what is being kept brief.

## Default workflow

Follow this order unless the user asks for a narrower slice.

1. Clarify the analysis target
2. Choose output mode
3. Scan repository shape and stack
4. Read the minimum set of high-signal files
5. Map architecture and runtime flow as needed
6. Judge health, risks, and adoption cost as needed
7. Output a structured engineering summary

Keep the investigation evidence-based. Prefer direct repo evidence over guesswork.
Use a simple evidence ladder when reporting:
- **已确认**: direct observation from files, manifests, docs, tests, or official metadata
- **推测**: a reasonable inference from the available evidence
- **待验证**: plausible but not yet confirmed

## 1. Clarify the analysis target

First determine which of these the user actually wants:

- **Quick understanding**: what the project does, stack, rough structure
- **Architecture reading**: modules, runtime flow, key abstractions
- **Adoption / takeover review**: maintainability, risk, maturity, onboarding cost
- **Implementation entry points**: where to start reading or modifying code
- **GitHub project review**: combine repo structure with community / activity signals

Also determine the target scope as early as possible:
- **whole repository / monorepo**
- **subproject / service / package**
- **single module / directory**

Call out the scope explicitly in the answer when it materially affects depth.
Examples:
- "当前目标是整仓，我先按速读版给整体判断。"
- "当前目标是前端子项目，所以这次聚焦 portal 本身。"

If the request is broad and you can proceed safely, default to:
- project positioning
- tech stack
- module structure
- main execution path
- strengths
- risks
- recommended reading order

## 2. Scan repository shape and stack

Start broad, then narrow.

Collect these first:
- root directory tree
- key docs: `README*`, `CONTRIBUTING*`, `ARCHITECTURE*`, `CLAUDE.md`, `AGENTS.md`
- stack manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `docker-compose*`, `Dockerfile*`
- main app directories: `src/`, `app/`, `server/`, `backend/`, `frontend/`, `cmd/`, `crates/`, `packages/`

Questions to answer early:
- Single app or monorepo?
- Product app, library, platform, or infra project?
- Primary languages and frameworks?
- Local run path and deployment path?
- Evidence of production readiness: tests, migrations, CI, observability, auth, docs?

## 3. Read the minimum high-signal files

Do not read everything. Read the smallest set that explains the system.

Priority order:
1. Root `README*`
2. Service/module README files
3. Stack manifests (`package.json`, `pyproject.toml`, etc.)
4. Main entry points (`main.*`, `index.*`, router/bootstrap files)
5. Architecture or deployment docs
6. A few core service files that reveal control flow

Use these patterns to find entry points:
- Backend: `main.py`, `app/main.py`, `server.ts`, `cmd/*/main.go`
- Frontend: `src/main.ts`, `src/App.*`, router/store setup
- Infra/runtime: `docker-compose.yml`, Helm, deployment scripts, CI workflows
- Plugin/adapter systems: registries, factories, adapters, interfaces, hooks

## 4. Map architecture and runtime flow

Build an internal map of the project using these lenses.

### A. Product boundary
- What problem does the project solve?
- Who uses it?
- Is it a framework, a business app, an internal platform, or a runtime layer?

### B. Module boundary
Identify the major modules and what each owns.

Good output shape:
- `portal/` → user UI
- `backend/` → API and orchestration
- `proxy/` → LLM/provider relay
- `plugin/` → integration with external runtime

### C. Execution path
Trace one or two important paths end to end.
Examples:
- request → router → service → model → DB
- browser action → frontend API client → backend route → runtime adapter
- incoming message → transport → queue/bus → worker → response channel

### D. Data and control points
Look for:
- auth / identity
- persistence layer
- messaging / event bus / queue
- deployment / compute abstraction
- configuration / feature flags
- plugin / extension loading

### E. Operating complexity
Check whether the project includes:
- multi-service coordination
- async jobs / event streaming
- multi-tenant or RBAC logic
- runtime abstraction layers
- dual CE/EE branches
- security hooks / policy engines

These areas usually dominate maintenance cost.

## 5. Judge health, risks, and adoption cost

Evaluate with engineering judgment, not marketing language.

### Health signals
Look for:
- clear docs
- coherent directory structure
- explicit configuration examples
- migrations / schema management
- tests or at least test scaffolding
- CI/CD or deploy scripts
- issue / PR hygiene when GitHub metadata is available

### Risk signals
Look for:
- architecture more ambitious than implementation depth
- many abstraction layers with unclear payoff
- naming inconsistency
- weak tests around critical flows
- implicit runtime assumptions
- hand-rolled infra/security with little validation
- monorepo sprawl without clear boundaries

### Adoption / takeover cost
Comment on:
- how long a new engineer would need to become effective
- which modules are safest to modify first
- which modules are high-risk to touch
- where observability/debugging will likely be painful

### Optional GitHub enhancement
When the target is a public GitHub repository and the user wants evaluation, not just code reading, optionally add a lightweight GitHub health layer.

Use it when the user asks things like:
- "这个项目怎么样"
- "值不值得跟"
- "适不适合采用"
- "值不值得参考 / 二开"

Keep it lightweight. Only add the signals that materially help engineering judgment:
- project health signals: stars, forks, license, commit recency, release rhythm
- maintenance signals: whether issue / PR activity is still moving, and whether maintainers appear engaged
- documentation signals: whether README / docs / CONTRIBUTING are present and useful

Do **not** turn the answer into a market report or community roundup by default.
Treat this as an enhancement layer. Do not let external hype replace code-level judgment.

## 6. Mode-specific output templates

Use the template that matches the chosen mode.

### A. 速读版

Use this when speed matters more than depth.

#### 问题判断
- 这是什么类型的项目
- 大概处于什么成熟度阶段

#### 原因分析
- 从目录、README、依赖清单、入口文件里看到的直接证据

#### 快速结论
- 项目定位
- 技术栈
- 顶层模块
- 一个主链路简述
- 亮点
- 风险

如果目标是公共 GitHub 仓库，且用户明显在问“值不值得看 / 跟 / 用”，可额外补一个短块：
- GitHub 健康度补充

控制规则：
- 速读版默认只展开一条主链路
- 如果目标是整仓，只给第一层模块地图，不展开每个子系统内部细节
- GitHub 健康度补充保持简短，不能盖过代码本身

#### 阅读建议
- 接下来最值得看的 3–5 个文件或模块

#### 验证方式
- 已确认：
- 推测：
- 待验证：

### B. 架构版

Use this when structure and flow matter most.

#### 问题判断
- 系统是单体、平台、插件体系还是多运行时架构
- 复杂度主要集中在哪些层

#### 原因分析
- 入口文件、核心服务、路由、运行时/消息/部署层的证据

#### 架构拆解
- 产品边界
- 模块边界
- 关键抽象
- 核心链路 1
- 核心链路 2（如果有）
- 复杂度热点

#### 结论
- 架构优点
- 架构风险
- 最需要继续验证的设计点

#### 阅读建议
- 继续深读顺序
- 哪些文件是架构关键节点

#### 验证方式
- 已确认：
- 推测：
- 待验证：

### C. 接手评审版

Use this when the user wants engineering judgment for takeover or adoption.

#### 问题判断
- 这项目适不适合接手/二开/参考
- 当前工程成熟度大致在哪一档

#### 原因分析
- 文档质量
- 模块边界
- 测试与部署信号
- 关键复杂度来源
- 命名/历史包袱/多服务协同成本

#### 接手评审结论
- 项目定位
- 技术栈与部署形态
- 高风险模块
- 相对安全的切入点
- 接手成本
- 二开建议
- 不建议贸然改动的区域

如果目标是公共 GitHub 仓库，且用户明显在问是否采用，可额外补一个短块：
- GitHub 健康度补充

#### 建议方案
- 新人第一阶段阅读顺序
- 第一刀适合从哪里切
- 如果要上线/落地，先补哪些验证

#### 验证方式
- 已确认：
- 推测：
- 待验证：

## Output quality rules

Always:
- Separate fact from inference
- Cite concrete file paths when making non-obvious claims
- Prefer "this suggests" over overclaiming when evidence is partial
- Call out uncertainty clearly
- Optimize for helping an engineer take over the project faster
- Prefer official repo evidence over third-party commentary
- Use external GitHub/community signals only as supporting context
- Match output depth to the chosen mode
- Keep GitHub health signals lightweight and subordinate to repo evidence

Never:
- Just paraphrase README marketing copy
- Pretend you verified runtime behavior if you only read files
- Expand into irrelevant refactoring advice
- Judge quality only by stars or hype
- Let community sentiment override direct code evidence
- Use long-form architecture output when the user only asked for a quick read

## Suggested investigation checklist

Use this as a lightweight checklist, not a rigid form.

- [ ] Repo type identified
- [ ] Output mode chosen
- [ ] Primary stack identified
- [ ] Main entry points found
- [ ] Core modules mapped
- [ ] Run/deploy path identified
- [ ] Main data/control flow sketched when needed
- [ ] High-risk modules identified when needed
- [ ] Suggested reading order prepared
- [ ] Clear boundary between facts and inferences

## Reference files

Read these only when needed:
- `references/output-template.md` — reusable report templates for all modes
- `references/signals.md` — what to look for when judging maturity, risk, and takeover cost
- `references/github-health.md` — when to add a lightweight GitHub health layer and how to keep it brief
- `references/adapted-notes.md` — distilled methods borrowed from surveyed external skills
