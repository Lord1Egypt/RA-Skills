---
name: shipguard
description: "Structured software development workflow for AI-assisted codebases: gated requirement intake with test cases, change impact analysis, typed implementation boundaries, verified delivery, full regression testing, and experience accumulation. Prevents silent breakage and scope creep."
homepage: https://github.com/morelapAI/shipguard
license: MIT
---

# ShipGuard

**Ship with confidence. Every time.**

ShipGuard is a gate-driven development workflow for AI-assisted software projects. It solves the core problem of AI-assisted development: one sentence in, massive undocumented changes out, invisible breakage everywhere.

Load `references/` docs on demand. On first project association, run the onboarding questionnaire to generate `PROJECT.md`.

---

## When to activate

- Any code change request on a shared or production codebase
- When the user says: build / fix / refactor / add / change / optimize
- When a change could touch DB schema, models, shared services, auth, or >3 files
- When the project has a `.dev-workflow/PROJECT.md` (auto-load it)

---

## Core principle

> **No code without a confirmed plan.**
> **No merge without verified delivery.**
> **No close without regression.**
> **No surprise, ever.**

Six gates. Each gate requires explicit user confirmation (`✅`) before proceeding. Skipping a gate requires explicit user override. The only exception: low-risk changes (see Execution Policy).

```
Request → [G0 Intake+TC] → [G1 Impact] → [G2 Build] → [G3 Feature QA] → [G4 Regression] → [G5 Lessons] → Closed
```

---

## Project Onboarding (First Use)

When ShipGuard is associated with a project for the first time, run this questionnaire before handling any request:

```
【ShipGuard 项目初始化】

我需要了解这个项目，让我问你几个问题：

① 项目名称和一句话描述？
② 技术栈？（前端框架 / 后端语言 / 数据库 / 部署方式）
③ 当前阶段？开发中 / 生产运行中 / 维护期
④ 核心业务主流程是什么？（用户视角，列出 3-5 个关键步骤）
⑤ 哪些模块绝对不能出问题？（出问题直接影响生产或客户）
⑥ 已知的「永远不做」有哪些？（过去踩过的坑）
⑦ 谁是需要确认的负责人？
⑧ 有没有特殊部署限制？（如：DB 迁移必须备份、重启必须在低峰期）
```

After answers, AI scans the project structure automatically, then generates `PROJECT.md`:

```markdown
# PROJECT.md — ShipGuard Project Profile

Project: <name>
Stack: <tech stack>
Stage: <development / production / maintenance>

## Critical Paths (changes always require confirmation)
1. <core flow step 1>
2. <core flow step 2>
...

## Protected Modules
- <module>: <why it's protected>

## Hard Rules (永远不做)
- <rule derived from user input or past lessons>

## Owner
<name / contact>

## Deployment Constraints
- <constraint>

Generated: YYYY-MM-DD
Last updated: YYYY-MM-DD
```

User confirms `PROJECT.md` before any work begins. This file is the source of truth for all future sessions.

---

## Project Directory Structure

ShipGuard maintains a `.dev-workflow/` directory in the project root:

```
.dev-workflow/
  PROJECT.md              # Project profile (generated at onboarding)
  CHANGELOG.md            # Auto-maintained change log
  requirements/           # One file per NR
    NR-YYYYMMDD-NN.md
  changes/                # One file per CR (impact + manifest + results)
    CR-YYYYMMDD-NN.md
  test-cases/
    all-test-cases.md     # Cumulative TC registry (auto-updated)
  regression/
    CR-YYYYMMDD-NN-regression.md
  lessons/
    hard-rules.md         # Permanent rules, never expire
    lessons.md            # Historical lessons, dated entries
```

On new session start: auto-load `PROJECT.md` + `lessons/hard-rules.md` + `lessons/lessons.md`. These files are the AI's persistent memory across sessions.

---

## Task Types & Execution Policy

Classify every request before acting. Type determines allowed scope and whether confirmation is required.

| Type | Marker | Allowed scope | Forbidden | Execution |
|------|--------|--------------|-----------|-----------|
| UI Tweak | 🎨 | Styles, labels, layout, field order | Backend logic, API structure, DB | **Auto — notify after** |
| Bug Fix (isolated) | 🐛 | The broken code only | UI redesign, unrelated features, requirements | **Auto — notify after** |
| Bug Fix (critical path) | 🐛⚠️ | The broken code only | Same as above | **Confirm required** |
| Feature | ✨ | New end-to-end functionality | Existing unrelated features | **Confirm required, full G0–G4** |
| Product Change | 📋 | Business logic, field definitions, flows | Architecture layer | **Confirm required, full G0–G4** |
| Architecture | 🏗️ | Refactor, performance, structure | Business behavior must stay identical | **Confirm required, full G0–G4** |
| Docs / Config | 📄 | Documentation, config files | Code logic | **Auto — notify after** |

**Critical Path Rule:** Any change touching the paths defined in `PROJECT.md > Critical Paths` is automatically elevated to "Confirm required", regardless of perceived size. The AI must not self-downgrade a critical path change.

**Split Rule:** When a request spans two types (e.g., fix a bug AND add a field), split into two separate CRs. Never merge types in one CR.

**Scope Creep Rule:** If during implementation the actual scope exceeds G1 estimates, stop immediately and issue a Scope Change Notice. Never silently expand scope.

---

## Gate 0 — Requirement Intake + Test Case Definition

Output a **Requirement Card** immediately. No code yet.

```
【需求理解卡 #NR-YYYYMMDD-NN】
原始需求：<user's exact words>
任务类型：🎨 UI微调 / 🐛 Bug Fix / ✨ Feature / 📋 Product / 🏗️ Architecture / 📄 Docs
执行策略：直接执行 / 需要确认

理解：<concrete behavioral description, not paraphrase>
范围：<which modules / pages / APIs>
排除：<what is explicitly NOT changing>
假设：<any ambiguities and how they're resolved>
已知风险：<from hard-rules.md and lessons.md relevant to this request>

Test Cases：
  TC-01【正常流程】<action> → <expected result>
  TC-02【正常流程】<action> → <expected result>
  TC-03【边界条件】<action> → <expected result>
  TC-04【异常流程】<action> → <expected result>

✅ 确认（含 Test Cases）后开始 / ❌ 有误，请纠正
```

TC rules:
- **正常流程 (Happy path):** core functionality works as expected
- **边界条件 (Edge case):** empty data, max values, unusual states
- **异常流程 (Error path):** what happens when things fail
- Every TC must have a specific, verifiable expected result — never "should work normally"
- TC is co-defined with the user. AI proposes, user confirms. AI does not unilaterally decide.

Write confirmed NR to `.dev-workflow/requirements/NR-YYYYMMDD-NN.md`.

---

## Gate 1 — Change Impact Analysis

After NR confirmed, output a **Change Impact Card**. Still no code.

```
【变更影响分析 #CR-YYYYMMDD-NN】
关联需求：#NR-YYYYMMDD-NN

改动文件：
  - path/to/file（风险：低/中/高，原因：<why>）

影响范围：
  直接：<directly affected features>
  间接：<potentially affected modules>
  无影响：<explicitly excluded>

改动量：小(<20行) / 中(20-100行) / 大(>100行)
风险等级：🟢低 / 🟡中 / 🔴高
DB变更：无 / 有（迁移脚本：<name>）
需要重启：无 / api / worker / all
预计耗时：<minutes>

风险说明：<required when 🔴>
回滚方案：<how to revert if things go wrong>
关联回归模块：<modules G4 must cover>

✅ 开始开发 / ❌ 重新评估
```

Risk levels:
- 🟢 Low: single file, UI only, no shared logic
- 🟡 Medium: multi-file, API changes, logic modification
- 🔴 High: DB migration, model changes, shared services, auth, critical path, >5 files

Write confirmed CR skeleton to `.dev-workflow/changes/CR-YYYYMMDD-NN.md`.

---

## Gate 2 — Implementation

Execute within the boundaries defined by task type. Rules:

- Touch only files listed in G1. Any additional file = stop and issue Scope Change Notice
- Atomic changes: one logical unit at a time, not one file at a time
- If discovering unexpected complexity, stop and report before continuing

On completion, append **Change Manifest** to the CR file:

```
【变更清单 #CR-YYYYMMDD-NN】
状态：已完成 ✅

文件变更：
  path/to/file
    + <added>
    ~ <modified: what and why>
    - <removed>

配套操作：
  迁移：<script name, execution status>
  重启：<which containers>
  其他：

未改动（排除确认）：
  - <file/module>: <reason confirmed out of scope>
```

---

## Gate 3 — Feature QA

Execute the test cases from Gate 0. No new TCs invented here.

```
【功能验收清单 #CR-YYYYMMDD-NN】
对应需求：#NR-YYYYMMDD-NN

执行 Gate 0 定义的 Test Cases：
  □ TC-01【正常流程】<description> → <expected>
  □ TC-02【正常流程】...
  □ TC-03【边界条件】...
  □ TC-04【异常流程】...

请逐项验收后回复：
✅ 全部通过 → 进入回归测试
❌ TC-? 失败：<describe what happened>
```

On `✅`: proceed to G4.
On `❌`: return to G2 for targeted fix. Re-run only failed TCs after fix.

---

## Gate 4 — Regression Testing

Generate regression scope from G1's "关联回归模块", then execute.

```
【回归测试范围 #CR-YYYYMMDD-NN】

本次改动模块：<from G1>

需要回归：
  ├── <Module A>
  │   ├── <feature / page 1>
  │   └── <feature / page 2>
  └── <Module B>

不需要回归（确认无关联）：
  - <module>: <reason>

---

【回归验收清单 #CR-YYYYMMDD-NN】

<Module A>：
  □ R01. <specific action> → <expected>
  □ R02. <specific action> → <expected>

<Module B>：
  □ R03. <specific action> → <expected>

请逐项验收后回复：
✅ 全部通过 → CR 关闭
❌ R? 失败：<describe>
```

Regression depth by risk:
- 🟢 Low: smoke (open page, no errors)
- 🟡 Medium: functional (core CRUD operations work)
- 🔴 High: full scenario (create / edit / delete / edge cases / error handling)

Write results to `.dev-workflow/regression/CR-YYYYMMDD-NN-regression.md`.

On `✅`: trigger commit and proceed to G5.

---

## Gate 5 — Lessons (Auto, no confirmation needed)

Run automatically after CR closes. No user action required.

```
【经验沉淀 #CR-YYYYMMDD-NN】
任务类型：<type>

本次教训：
  - <what operation caused what problem>
  - <what to watch for next time with similar requests>

新增底层规则：
  ✅ 永远要做：<rule>
  ❌ 永远不做：<rule>

写入：
  lessons/lessons.md → <dated entry>
  lessons/hard-rules.md → <if new permanent rule established>
  test-cases/all-test-cases.md → <append TCs from this CR>
  CHANGELOG.md → <append entry>
```

Hard rules never expire. On every new session, load `hard-rules.md` and apply before handling any request.

---

## Commit Format

```
<type>(<scope>): <summary> #CR-YYYYMMDD-NN

Changed:
- <file>: <what and why>

Side effects:
- Migration: <SQL or "none">
- Restart: <containers or "none">
- Breaking: yes / no

Feature QA: ✅ (TC-01 to TC-0N)
Regression: ✅ (<modules tested>)
Date: YYYY-MM-DD
```

Types: `feat` `fix` `refactor` `style` `chore` `docs` `migration`

---

## Scope Change Notice

Issue this when implementation scope exceeds G1 estimate:

```
【范围变更通知 #CR-YYYYMMDD-NN】
发现：<what was discovered>
原估计：<G1 scope>
实际需要：<additional scope>
影响：<what this changes about risk/time/restart>

建议：
  A. 继续，扩大本 CR 范围
  B. 拆分：当前 CR 只做原范围，新开 CR 处理额外部分
  C. 回滚当前改动，重新评估

✅ 选 A / 🔀 选 B / ❌ 选 C
```

---

## Scope Discovery Commands

```bash
# Who imports this module?
grep -rn "from <module> import\|import <module>" <backend_dir>/ --include="*.py"

# What has a relationship to this model?
grep -rn 'relationship.*"<Model>"' <backend_dir>/ --include="*.py"

# Which frontend pages call this API route?
grep -rn "api\.\(get\|post\|put\|patch\|delete\)" <frontend_dir>/ --include="*.vue" | grep "<route-keyword>"

# Run full scope check
python ~/.openclaw/skills/shipguard/scripts/scope_check.py <Identifier> <project_root>
```

---

## Dependency Rules for Regression Scope

| Changed | Must also regress |
|---------|------------------|
| DB model | All pages/APIs using that table |
| ORM relationship | All tasks and services that import that model |
| Shared service | All callers |
| Auth / middleware | All protected routes |
| Celery task | Task schedule config page + related data display pages |
| API router | All frontend pages calling that endpoint |
| Frontend store / composable | All components using it |

---

## Anti-patterns (never do)

- ❌ Write code before requirement is confirmed
- ❌ Change DB schema without a migration script
- ❌ Restart only `api` when models change — always restart dependent workers too
- ❌ Use broad exception handlers to change entity status (use typed exceptions only)
- ❌ Close a CR without regression testing
- ❌ Silently expand scope mid-implementation
- ❌ Self-downgrade a critical path change to "low risk"
- ❌ Mix two task types in one CR
- ❌ Invent new TCs at Gate 3 that weren't in Gate 0
- ❌ Skip Gate 5 — lessons must always be recorded
