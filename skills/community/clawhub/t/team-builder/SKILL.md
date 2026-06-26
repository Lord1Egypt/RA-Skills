---
name: team-builder
description: 在 OpenClaw 上一键部署多 Agent SaaS 团队工作区。内置双开发轨（devops 交付 + fullstack-dev 实现）、实时 spawn 调度、cron 巡检、Deep Dive 产品知识目录、onboarding 引导。支持自定义角色、模型、时区，可选 Telegram 接入。
---

# Team Builder

一条命令部署完整多 Agent 团队骨架，包含角色、信箱、看板、产品知识目录、cron 巡检、双开发轨模板。

> 详细安装步骤和首次配置引导见 `README.md`（中文完整版）。

## 前置条件

- OpenClaw 已安装并运行
- Node.js 16+
- 已配置至少一个模型 provider

> **此技能会修改系统配置**：`apply-config.js` 会写入 `openclaw.json`，`create-crons.*` 会创建 cron 任务。均需手动执行，不自动运行。

### Internal Dispatch Protocol (MANDATORY)
- **Standard agents** (product-lead, growth-lead, intel-analyst, devops, etc.): `sessions_spawn(runtime="subagent", mode="run")` — **禁止带 `streamTo`**
- **ACP agents** (fullstack-dev): `sessions_spawn(runtime="acp")` — 可带 `streamTo="parent"`
- 结果通过 auto-announce 推送；不要轮询 `sessions_list` 或 `subagents list`
- chief-of-staff 是群内唯一入口；其他 agent 内部 spawn，不直接监听群聊
- 详见 `shared/knowledge/team-workflow.md` 零章

### 参谋长执行边界（MANDATORY）
- **参谋长不下地干活**：任何多步骤任务（编码、调研、分析、内容、部署）→ 全部派给对应 agent
- **参谋长不亲自开子代理干活**：spawn 子代理执行具体业务 = 等价于自己干活
- **参谋长做且只做**：任务拆解（L1-L4 复杂度判断）、编排、派活、监控、结果汇总
- 先执行后汇报；默认输出只保留：已做什么 / 拿到什么结果 / 卡在哪里

### 子代理使用规则（MANDATORY，全团队适用）
- **优先主 agent 自己干**：干得过来时不开子代理
- **分析透再派**：开子代理前必须先分析清楚边界/依赖/输入输出
- **子代理只做原子任务**：一句话说清、执行完就结束，不做判断或策略决策
- **主 agent 全权负责**：判断、策略、经验积累——子代理不做这三件
- **子代理结果由主 agent 汇总**后再上报参谋长

### Credentials involved
- **Telegram bot tokens** (optional) -- stored in openclaw.json, used for agent-to-Telegram binding
- **Model API keys** -- must already be configured in your OpenClaw model providers (not handled by this skill)

### Recommended
- Review generated `apply-config.js` before running
- Check the backup of openclaw.json after running
- Test with 2-3 agents before enabling all cron jobs

## Team Architecture

Default reference architecture for a SaaS/growth multi-agent team (customizable to 2-10 agents):

```
CEO
 |-- Chief of Staff (dispatch + strategy + efficiency)
 |-- Data Analyst (data + user research)
 |-- Growth Lead (GEO + SEO + community + social media)
 |-- Content Chief (strategy + writing + copywriting + i18n)
 |-- Intel Analyst (competitor monitoring + market trends)
 |-- Product Lead (product management + tech architecture)
 |-- DevOps (delivery / deploy / environment / acceptance)
 |-- Fullstack Dev (implementation / module deep dive / ACP coding session)
```

### Multi-Team Support

One OpenClaw instance can run multiple teams:

```bash
node <skill-dir>/scripts/deploy.js                  # default team
node <skill-dir>/scripts/deploy.js --team alpha      # named team "alpha"
node <skill-dir>/scripts/deploy.js --team beta       # named team "beta"
```

Named teams use prefixed agent IDs (`alpha-chief-of-staff`, `beta-growth-lead`) to avoid conflicts. Each team gets its own workspace subdirectory.

### Flexible Team Size

The wizard lets you select 2-10 agents from the available roles. Skip roles you don't need. The 8-agent default covers most SaaS scenarios with dual-dev routing, but you can run leaner (3-4 agents) or expand with custom roles.

### Model Auto-Detection

The wizard scans your `openclaw.json` for registered model providers and auto-suggests models by role type:

| Role Type | Best For | Auto-detect Pattern |
|-----------|----------|-------------------|
| Thinking | Strategic roles (chief, growth, content, product) | /glm-5\|opus\|o1\|deepthink/i |
| Execution | Operational roles (data, intel, fullstack) | /glm-4\|sonnet\|gpt-4/i |
| Fast | Lightweight tasks | /flash\|haiku\|mini/i |

You can always override with manual model IDs.

## Setup / Config / Scripts

### Required Inputs
- Team name
- Workspace dir
- Timezone
- Morning brief hour
- Evening brief hour
- Thinking model
- Execution model
- CEO title

### Optional Inputs
- Telegram user ID
- Telegram bot tokens
- Proxy
- ACP coding agent(给 fullstack-dev 使用)

### Core Scripts
```bash
node <skill-dir>/scripts/deploy.js
node <workspace-dir>/apply-config.js
powershell <workspace-dir>/create-crons.ps1
bash <workspace-dir>/create-crons.sh
openclaw gateway restart
```

### Execution Priority
- First: matched execution skill (for coding work, `coding-lead` if loaded)
- Second: agent-role fallback when no matching skill is loaded
- Third: templates/README explain boundaries and ownership only; they should not override matched skills

### Context File Hygiene
- Active context files live under `<project>/.openclaw/`
- Reuse one context file per active code chain when possible
- Naming pattern: `context-<task-slug>.md`
- Active context file cap per project: **60**
- Context-file lifecycle window per project: **100 total files** across active + archive
- Completed or stale files should be deleted or moved to `.openclaw/archive/`

### Current Dual-Dev Standard
- fullstack-dev:实现、模块深挖、开发文档、接口文档、Claude coding 执行;默认 coding skill 可采用 `coding-lead`,其中 simple 任务直做,medium 倾向 Claude ACP `run` 或 direct acpx,complex 通过现有会话连续协作 + 上下文文件推进,不把 ACP `session` 持久线程作为正式主路径;context 活跃上限 60、生命周期总窗口 100;并行允许但必须先定义边界,总上限 5 个工作单元
- devops:交付、部署、环境、回归、冒烟、自动QA、发布门禁
- product-lead:澄清、PRD、验收标准,不完整不得派工
- chief-of-staff:路由、裁决、控制 token 浪费

## 部署流程

> 完整步骤见 `README.md`。以下是关键参数选取对照表。

### 必填参数

| 参数 | 默认值 | 说明 |
|--------|--------|------|
| teamName | Alpha Team | 团队名 |
| workspaceDir | `~/.openclaw/workspace-team` | 工作区路径 |
| timezone | Asia/Shanghai | cron 时区 |
| morningHour | 8 | 晨报时间 |
| eveningHour | 18 | 晚报时间 |
| thinkingModel | 自动检测 | 策略型角色（chief/product/growth/content）|
| executionModel | 自动检测 | 执行型角色（devops/fullstack/intel/data）|
| ceoTitle | Boss | CEO 称呼 |

### 可选参数
- `roles`：自定义角色列表（默认全郥 8 个）
- `roleNames`：自定义角色名称（如中文起名）
- `--team <prefix>`：多团队并存时用于隔离角色 ID
- Telegram bot tokens（可选，配置后自动写入 openclaw.json）

### 核心命令
```bash
# 交互式生成
node <skill-dir>/scripts/deploy.js

# 非交互生成
node <skill-dir>/scripts/deploy.js --config team-builder.json

# 验证生成结果
node <skill-dir>/scripts/deploy.js --verify --config team-builder.json

# 应用配置（写入 openclaw.json）
node <workspace-dir>/apply-config.js

# 创建 cron
powershell <workspace-dir>/create-crons.ps1  # Windows
bash <workspace-dir>/create-crons.sh          # macOS/Linux

# 重启
openclaw gateway restart
```

`--verify` 检查生成物是否包含双开发模型、角色归属、cron 条目。

完整安装步骤见 `README.md`。

## Cron Schedule

| Offset | Agent | Task | Frequency |
|--------|-------|------|-----------|
| H-1 | Data Analyst | Data + user feedback | Daily |
| H-1 | Intel Analyst | Competitor scan | Mon/Wed/Fri |
| H | Chief of Staff | Morning brief (announced) | Daily |
| H+1 | Growth Lead | GEO + SEO + community | Daily |
| H+1 | Content Chief | Weekly content plan | Monday |
| H+2 | DevOps | Delivery / environment / Deep Dive / acceptance | Daily |
| H+10 | Chief of Staff | Evening brief (announced) | Daily |

(H = morning brief hour)

## Generated File Structure

```
<workspace>/
├── AGENTS.md, SOUL.md, USER.md  (auto-injected)
├── apply-config.js, create-crons.ps1/.sh, README.md
├── agents/<8 agent dirs>/       (SOUL.md + MEMORY.md + memory/)
└── shared/
    ├── briefings/, decisions/, inbox/ (v2: with status tracking)
    ├── status/team-dashboard.md     (chief-of-staff maintains, all agents read first)
    ├── data/                        (public data pool, data-analyst writes, all read)
    ├── kanban/, knowledge/
    └── products/
        ├── _index.md                (product matrix overview)
        ├── _template/               (knowledge directory template)
        └── {product}/               (per-product knowledge, up to 20 files)
            ├── overview.md, architecture.md, database.md, api.md, routes.md
            ├── models.md, services.md, frontend.md, auth.md, integrations.md
            ├── jobs-events.md, config-env.md, dependencies.md, devops.md
            ├── test-coverage.md, tech-debt.md, domain-flows.md, data-flow.md
            ├── i18n.md, changelog.md, notes.md
```



## Knowledge Governance

Each shared knowledge file has a designated owner. Only the owner agent updates it; others read only.

| File | Owner | Update Trigger |
|------|-------|---------------|
| geo-playbook.md | growth-lead | After GEO experiments/discoveries |
| seo-playbook.md | growth-lead | After SEO experiments |
| competitor-map.md | intel-analyst | After each competitor scan |
| content-guidelines.md | content-chief | After proven writing patterns |
| user-personas.md | data-analyst | After new user insights |
| tech-standards.md | product-lead | After architecture decisions |

### Update Protocol
When updating a knowledge file, the owner must:
1. Add a dated entry at the top: `## [YYYY-MM-DD] <what changed>`
2. Include the reason and data evidence
3. Never delete existing entries without CEO approval (append, don't replace)

### Chief of Staff Governance
The chief-of-staff monitors knowledge file health during weekly reviews:
- Are files being updated regularly?
- Any conflicting information between files?
- Any stale entries that should be archived?

## Self-Evolution Pattern

Agents improve their own strategies over time through a feedback loop:

```
1. Execute task (cron or inbox triggered)
2. Collect results (data, metrics, outcomes)
3. Analyze: what worked vs what didn't
4. Update knowledge files with proven strategies (with evidence)
5. Next execution reads updated knowledge → better performance
```

This is NOT the agent randomly changing rules. Updates must be:
- **Data-driven**: backed by metrics or concrete outcomes
- **Incremental**: append new findings, don't rewrite everything
- **Traceable**: dated with evidence so others can verify

### What Agents Can Self-Update
- Their own knowledge files (per ownership table above)
- Their own MEMORY.md (lessons learned, decisions)
- shared/data/ outputs (data-analyst only)

### What Requires CEO Approval
- shared/decisions/active.md (strategy changes)
- Adding/removing agents or changing team architecture
- External publishing or spending decisions

## Public Data Layer

The `shared/data/` directory serves as a read-only data pool for all agents:

- **data-analyst** writes: daily metrics, user feedback summaries, anomaly alerts
- **All agents** read: to inform their own decisions
- Format: structured markdown or JSON, dated filenames (e.g., `metrics-2026-03-01.md`)
- Retention: keep 30 days, archive older files

## Project Deep Dive - Code Scanning

Agents can deeply understand each SaaS product through automated code scanning. This is critical - without deep project knowledge, all team decisions are surface-level.

### How It Works

1. CEO adds a product to `shared/products/_index.md` (name, URL, code directory, tech stack)
2. Product Lead triggers a delivery-oriented Deep Dive scan by dispatching to DevOps (via `sessions_spawn` if online, inbox as fallback)
3. DevOps enters the project directory (read-only) and generates shared knowledge / delivery-oriented scan outputs
4. Fullstack Dev picks up module-level deep dive or implementation follow-up when needed
5. Knowledge files are generated in `shared/products/{product}/`
6. All agents consume these files **via manifest-based lazy loading** (never read all at once)

### Manifest-Based Lazy Loading (MANDATORY)

Each product directory includes a `manifest.json` (~200 tokens) that lists all files with one-line summaries and a `taskFileMap` mapping task types to relevant files.

**Agent workflow:**
1. Read `_index.md` → identify which product
2. Read `{product}/manifest.json` → see all files + summaries (~200 tokens)
3. Based on `taskFileMap` or summaries, read only 1-3 relevant files
4. Never read more than 5 product files per session

**Why:** With 15+ products × 20 files each, full loading = 40K+ tokens per product. Manifest loading = 200 tokens + only what's needed.

**DevOps MUST regenerate `manifest.json`** after every delivery-oriented scan (L0-L4). Fullstack Dev updates it when doing module-level follow-up that changes knowledge scope. Template in `_template/manifest.json`.

### Manifest Quality Standards

摘要不能为了省 token 丢掉关键信息。每条摘要须满足:
- **核心文件**(database/models/services/routes/integrations):50-130字,列出关键实体名/数量/域名
- **中等文件**(auth/frontend/commands/config):30-80字,点明方案和范围
- **轻量文件**(changelog/notes/metrics):可以短(<20字)
- **taskFileMap**:必须覆盖该产品的所有核心业务场景(不少于8个映射)
- **codeStats**:必须包含文件数、行数、模型数、表数等量化指标

### Product Knowledge Directory

Each product gets a knowledge directory with up to 20 files + manifest:

```
shared/products/{product}/
├── manifest.json        ← **INDEX** (~200 tokens): file list, summaries, taskFileMap
├── overview.md          ← Product positioning (from _index.md)
├── architecture.md      ← System architecture, tech stack, design patterns, layering
├── database.md          ← Full table schema, relationships, indexes, migrations
├── api.md               ← API endpoints, params, auth, versioning
├── routes.md            ← Complete route table (Web + API + Console)
├── models.md            ← ORM relationships, scopes, accessors, observers
├── services.md          ← Business logic, state machines, workflows, validation
├── frontend.md          ← Component tree, page routing, state management
├── auth.md              ← Auth scheme, roles/permissions matrix, OAuth
├── integrations.md      ← Third-party: payment/email/SMS/storage/CDN/analytics
├── jobs-events.md       ← Queue jobs, event listeners, scheduled tasks, notifications
├── config-env.md        ← Environment variables, feature flags, cache strategy
├── dependencies.md      ← Key dependencies, custom packages, vulnerabilities
├── devops.md            ← Deployment, CI/CD, Docker, monitoring, logging
├── test-coverage.md     ← Test strategy, coverage, weak spots
├── tech-debt.md         ← TODO/FIXME/HACK inventory, dead code, complexity hotspots
├── domain-flows.md      ← Core user journeys, domain boundaries, module coupling
├── data-flow.md         ← Data lifecycle: external → import → process → store → output
├── i18n.md              ← Internationalization, language coverage
├── changelog.md         ← Scan diff log (what changed between scans)
└── notes.md             ← Agent discoveries, gotchas, implicit rules
```

### Scan Levels

| Level | Scope | When | Output |
|-------|-------|------|--------|
| L0 Snapshot | Surface: directory tree, packages, env | First onboard | architecture, dependencies, config-env |
| L1 Skeleton | Structure: DB, routes, models, components | First onboard | database, routes, api, models, frontend |
| L2 Deep Dive | Logic: services, auth, jobs, integrations | On-demand per module | services, auth, jobs-events, integrations, domain-flows, data-flow |
| L3 Health Check | Quality: tech debt, tests, security | Periodic / pre-release | tech-debt, test-coverage, devops |
| L4 Incremental | Delta: git diff → update affected files | After code changes | changelog + targeted updates |

### Content Standards

Knowledge files capture not just WHAT exists but WHY:
- **Design decisions**: Why this approach was chosen
- **Implicit business rules**: Logic buried in code (e.g., "orders auto-cancel after 72h")
- **Gotchas**: What breaks if you touch this module carelessly
- **Cross-module coupling**: Where changing A silently breaks B
- **Performance hotspots**: N+1 queries, missing indexes, bottleneck endpoints

### Role Responsibilities

| Role | Responsibility |
|------|---------------|
| Product Lead | **Clarification / PRD / acceptance**: complete clarification, PRD, user stories, acceptance criteria, and review knowledge freshness before delegating |
| DevOps | **Delivery / QA gate / Deep Dive**: enter code directory for deployment-oriented scans, maintain release checklist, smoke/regression testing, auto-QA access, and generate/update shared product knowledge files |
| Fullstack Dev | **Implementation / docs / Deep Dive follow-up**: continue module-level deep dive, code analysis, implementation, dev docs, interface docs, and ACP session work |
| Chief of Staff | **Routing / escalation**: split implementation vs delivery tasks, prevent duplicate labor, escalate blockers |
| All Agents | **Consumption**: read product knowledge before any product-related decision |

### Per-Stack Auto-Detection

Fullstack Dev auto-detects tech stack and applies stack-specific scan strategies:
- **Laravel/PHP**: migrations, route:list, Models, Services, Middleware, Policies, Jobs, Console/Kernel
- **React/Vue**: components, router, stores, API client, i18n
- **Python/Django/FastAPI**: models.py, urls.py, views.py, middleware, celery
- **General**: tree, git log, grep TODO/FIXME, .env.example, Docker, CI, tests

## Team Coordination v2

### Inbox Protocol v2 (backup channel, status tracking)

> **Primary dispatch**: `sessions_spawn` (real-time). Inbox is for archival, cross-session handoff, and fallback when spawn is unavailable.

Every inbox message now has a `status` field:
- `pending` → `received` → `in-progress` → `done` (or `blocked`)
- Chief-of-staff monitors timeouts: high>4h, normal>24h pending = intervention
- Blocked >8h = escalation to CEO
- Recipients MUST update status immediately upon reading

### Team Dashboard (`shared/status/team-dashboard.md`)

Chief-of-staff maintains a "live scoreboard" updated every session:
- 🔴 Urgent/Blocked items
- 📊 Per-agent status table (last active, current task, status icon)
- 📬 Unprocessed inbox summary (pending/blocked messages across all inboxes)
- 🔗 Cross-agent task chain tracking (A→B→C with per-step status)
- 📅 Today/Tomorrow focus

**Agent 启动顺序（内置于 AGENTS.md）：**
1. 确认角色
2. 读 `agents/[role]/SOUL.md`
3. 读 `shared/onboarding.md`（项目背景，CEO 填写）
4. 读 `shared/status/team-dashboard.md`（当前状态）
5. 读 `shared/decisions/active.md`（仅涉及策略时）
6. 读 `shared/inbox/to-[role].md`
7. 读 `agents/[role]/MEMORY.md`（仅需历史上下文时）

### Chief-of-Staff as Router

The chief is upgraded from "briefing writer" to "active team router":
- **Real-time dispatch**: uses `sessions_spawn(runtime="subagent")` to directly wake agents and assign tasks - this is the primary dispatch method
- **Blocker detection**: scans all inboxes for overdue messages
- **Inbox as backup**: writes to inbox only for archival, cross-session handoff, or when agent is unreachable
- **Task chain tracking**: identifies multi-agent workflows and tracks each step
- **Escalation**: persistent blockers get flagged to CEO
- **Runs 4x/day** (morning brief, midday patrol, afternoon patrol, evening brief)

### Cron Schedule (10 jobs, up from 7)

| Time | Agent | Type | Purpose |
|------|-------|------|---------|
| 07:00 | data-analyst | daily | Data pull + feedback scan |
| 08:00 | chief-of-staff | **announce** | Morning: router scan + brief + quality |
| 09:00 | growth-lead | daily | GEO/SEO/community |
| 09:00 | product-lead | **daily (NEW)** | Inbox + clarification/PRD + task delegation |
| 10:00 | content-chief | **daily M-F (was weekly)** | Content creation + collaboration |
| 10:00 | devops | **daily (delivery track)** | Inbox + Deep Dive + delivery + QA gate |
| 12:00 | chief-of-staff | **patrol (NEW)** | Router scan only, no brief |
| 15:00 | chief-of-staff | **patrol (NEW)** | Router scan only, no brief |
| 18:00 | chief-of-staff | **announce** | Evening: router scan + summary + next day plan |
| 07:00 M/W/F | intel-analyst | 3x/week | Competitor scan |

### Why These Changes Matter

| Before | After | Impact |
|--------|-------|--------|
| Inbox = primary dispatch | Inbox = backup + spawn = primary | Real-time dispatch via spawn; inbox for archival only |
| Chief 2x/day | Chief 4x/day with router role | Blockers caught within hours, not days |
| Content-chief 1x/week | Daily M-F | Actually produces content |
| Product-lead no cron | Daily | Knowledge governance happens |
| No team dashboard | Dashboard every session | All agents know the full picture |
| No timeout detection | Automatic timeout rules | Nothing falls through cracks |

## Key Design Decisions

- **Shared workspace** so qmd indexes everything for all agents
- **Real-time spawn dispatch** as primary inter-agent communication; inbox as backup for archival and cross-session handoff
- **Chief as Router** - active coordinator who dispatches via `sessions_spawn`, detects blockers, and resolves them
- **Team Dashboard** - single source of truth for team-wide status, maintained by chief every session
- **GEO as #1 priority** (AI search = blue ocean)
- **Fullstack Dev spawns Claude Code** via ACP for complex implementation tasks
- **DevOps owns delivery and QA gate** so implementation and release responsibilities stay separated
- **Project Deep Dive** gives all agents deep codebase understanding, not just surface-level product overviews

## Customization

Edit ROLES array in `scripts/deploy.js` to add/remove agents.
Edit `references/soul-templates.md` for SOUL.md templates.
Edit `references/shared-templates.md` for shared file templates.
