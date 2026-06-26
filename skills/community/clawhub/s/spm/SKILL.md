---
name: SPM
version: 3.0.0
description: Production-grade software project development skill for OpenClaw. WBS hash attestation, auto context injection, session recovery, parallel task pointers, and Minimal Mode. Use when starting new projects, implementing complex features, or executing multi-step development tasks that require structured end-to-end management.
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      anyBins: ["node", "npm", "git"]
allowed-tools: ["read", "write", "edit", "exec", "process", "sessions_spawn", "sessions_yield", "subagents", "cron", "memory_search", "memory_get", "browser"]
---

# SPM — Super Project Manager

## Overview

SPM is a comprehensive skill for software project development in OpenClaw. It integrates:

- **Superpowers** (13 workflows): Design brainstorming, implementation planning, TDD, subagent-driven development, code review, systematic debugging, git worktrees, and more
- **PM enhancements**: Soul-searching protocol, assumption documentation, safe sandbox (/freeze & /guard), three-tier quality gates, project scaffolding, deployment pipeline
- **WBS Executor**: Structured task ledger with exit criteria, evidence tracking, heartbeat logging, interruption recovery, delivery summary

**Core Philosophy:** SPM is an orchestrator, not a monolith. Each phase triggers the right workflow. The WBS task ledger is the single source of truth for tracking — now protected by hash attestation and auto-injected into context.

### 🆕 v3.0 New Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **WBS Hash Attestation** | SHA-256 integrity protection; tampered ledgers auto-detected | 🔒 Security |
| **Hook Auto-Injection** | Active tasks auto-injected into context before every tool call | 🤖 Automation |
| **Session Recovery** | Auto-generated recovery reports from heartbeat logs | 🔄 Resilience |
| **Parallel Task Pointers** | `.active_ledger` symlink + `switch-ledger.sh` for multi-task isolation | 📂 Multi-task |
| **SPM Minimal Mode** | 5-rule lightweight mode for <10 task projects | 🏃 Quick Start |
| **Template/Script Separation** | Clear distinction: user-project files vs skill internals | 📋 UX |

## When to Use

- Starting a new software project from scratch
- Implementing complex multi-file features
- Any task that spans multiple steps or sessions
- Work that requires quality gates, code review, or TDD

**When NOT to use:**
- Single-line fixes or typo corrections
- Quick one-file changes with obvious scope
- Pure brainstorming without execution intent

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      SPM ORCHESTRATOR                     │
│  SKILL.md — Detects task type → Routes to correct phase  │
└──────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌──────────────────┐
│  REQUIREMENT   │   │   PLANNING    │   │    EXECUTION     │
│ ─────────────  │   │  ──────────   │   │   ────────────   │
│ • Brainstorming│   │ • Write Plan  │   │ • Git Worktree   │
│ • Soul-Search  │   │ • WBS Ledger  │   │ • TDD Cycle      │
│ • Design Doc   │   │ • Review Plan │   │ • Subagent Dev   │
│ • Assumptions  │   │ • Dependencies│   │ • Parallel Tasks │
└───────┬───────┘   └───────┬───────┘   └────────┬─────────┘
        └───────────────────┼────────────────────┘
                            ▼
┌───────────────┐   ┌───────────────┐   ┌──────────────────┐
│    QUALITY     │   │   DELIVERY    │   │  TRACKING (ALL)  │
│ ─────────────  │   │  ──────────   │   │  ──────────────  │
│ • Verification │   │ • Finish Brch │   │ • WBS Ledger     │
│ • Code Review  │   │ • Deploy (opt)│   │ • Heartbeat Log  │
│ • 3-Tier Gates │   │ • Delivery    │   │ • State Tracking │
│ • Debugging    │   │ • Cleanup     │   │ • Recovery       │
└───────┬───────┘   └───────┬───────┘   └──────────────────┘
        └───────────────────┼────────────────────┘
                            ▼
              ┌─────────────────────────┐
              │    SUBAGENT DISPATCH     │
              │  ─────────────────────  │
              │  Impl. Subagent         │
              │  Spec Reviewer          │
              │  Code Quality Reviewer  │
              │  Parallel Subagents     │
              └─────────────────────────┘
```

## The Complete Lifecycle

```
┌────────────────────────────────────────────────────────────────────┐
│  PHASE 1: REQUIREMENT                          PHASE 2: PLANNING  │
│  ┌────────────┐  ┌────────────┐              ┌──────────┐        │
│  │Brainstorm  │→ │Design Doc  │──Manual──▶  │WBS Plan  │         │
│  │(灵魂拷问)  │  │(明确假设)  │  Review     │(任务分解)│         │
│  └────────────┘  └────────────┘              └────┬─────┘        │
└────────────────────────────────────────────────────┼──────────────┘
                                                      │
┌─────────────────────────────────────────────────────┼──────────────┐
│  PHASE 3: EXECUTION (Automated after Manual Start) │              │
│                                                     ▼              │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌─────────────┐    │
│  │Worktree  │→ │Subagent  │→ │Parallel    │→ │TDD + Commit │    │
│  │Setup     │  │Task Exec │  │Subagents   │  │Verify       │    │
│  └──────────┘  └──────────┘  └────────────┘  └──────┬──────┘    │
│                                                      │           │
└──────────────────────────────────────────────────────┼───────────┘
                                                       │
┌──────────────────────────────────────────────────────┼───────────┐
│  PHASE 4: QUALITY                PHASE 5: DELIVERY   │           │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │           │
│  │Verify Gate │→ │Code Review │→ │Finish Branch │   │           │
│  │(3-Tier)    │  │(3-Stage)   │  │Deploy (opt)  │   │           │
│  └────────────┘  └────────────┘  └──────┬───────┘   │           │
│                                          │           │           │
│  ┌────────────────────────────────────┐ │           │           │
│  │ DELIVERY SUMMARY + WBS CLOSEOUT    │◀┘           │           │
│  └────────────────────────────────────┘             │           │
└──────────────────────────────────────────────────────┘           │
                                                                    │
┌────────────────────────────────────────────────────────────────────┐
│  TRACKING LAYER (Runs Throughout All Phases)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ WBS Ledger   │  │ Heartbeat    │  │ State Tracking       │   │
│  │ (Single SOT) │  │ (10 min)     │  │ (project-state.json) │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

## Core Artifact: WBS Task Ledger

The WBS task ledger is the **single source of truth** for the entire project. Every phase creates its artifacts AND updates the ledger.

**Ledger location:** `docs/spm/ledger.md`

**Minimal ledger template:**

```markdown
# WBS Task Ledger — [Project Name]

## Task Summary
- Assignment: [one-line]
- Outcome: [what working software looks like]
- Success criteria: [how we verify]

## WBS
| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|---------|---------------|---------------|----------|--------|
| 1  | Setup scaffold | - | Cold-start: init project structure, install deps | Init script runs, tests pass | npm test output | done |
| 1.1| Install deps | 1 | Cold-start: after scaffold ready, npm install all packages | All deps installed | npm ls | done |
| 2  | Core feature A | 1 | Cold-start: after scaffold, implement API in src/routes/ | API returns correct data | curl output | todo |

## Mutation Log
| Time | Mutation Type | Affected IDs | Reason | New IDs |
|------|--------------|-------------|--------|---------|
| | split / insert / skip / reorder / abandon | | | |

## Active State
- Current item:
- Last completed:
- Last checkpoint:
- Resume from here:

## Heartbeat Log
| Time | Active | Completed | Evidence | Resume point |
|------|--------|-----------|----------|-------------|
| HH:MM | Task 2 | Task 1 | build passes | Task 2 subagent |

## Delivery Summary
[Final output mapping back to original assignment]
```

**Allowed statuses:** `todo`, `doing`, `done`, `blocked`, `skipped`

**Rule:** No item marked `done` without evidence (file diff, test output, command result).

---

## Workflow by Phase

### Phase 1: Requirement (Manual — User Review Required)

**Trigger:** User says "build X", "start project", "implement feature"

**🆕 外部资源分析 (optional):** 如果项目需要借鉴外部代码/技能/方案，先走 `workflows/external-research.md` → 结构化对比 → 输出采纳清单 → 再进入标准需求流程。

**Sub-flow: Soul-Searching Protocol**
1. Before any design work, throw back **3 lethal probing questions** about scope/purpose/constraints
2. Surface assumptions explicitly: "I'm assuming X — correct me now or I'll proceed"

**Sub-flow: Brainstorming (see workflows/brainstorming.md)**
1. Explore project context
2. Ask clarifying questions (one at a time)
3. Propose 2-3 approaches with trade-offs
4. Present design in sections, user approves per section
5. Write design doc to `docs/spm/specs/`
6. Spec self-review (placeholder scan, consistency, scope)
7. User reviews written spec

**Outputs:**
- `docs/spm/specs/YYYY-MM-DD-xxx-design.md`
- Updated WBS ledger: "Spec phase complete"

**Phase Gate:** User must approve spec before proceeding.

---

### Phase 2: Planning (Manual — User Review Required)

**Sub-flow: Implementation Plan (see workflows/writing-plans.md)**
1. Decompose spec into bite-sized tasks (2-5 min per step)
2. Write **Context Brief** for each task — self-contained cold-start context
3. Assign **Model Tier** to each task (fast/standard/strong)
4. Map file structure: which files created/modified
5. Create WBS ledger with all tasks (IDs, context brief, dependencies, exit criteria)
6. Self-review plan (spec coverage, placeholder scan, Context Brief audit)
7. **🆕 Adversarial Plan Review** — dispatch reviewer subagent against 5-dimension checklist before showing to user (see subagents/plan-reviewer-prompt.md)

**Outputs:**
- `docs/spm/plans/YYYY-MM-DD-xxx-plan.md`
- Updated WBS ledger with all task rows + context briefs + model tiers
- `docs/spm/reviews/YYYY-MM-DD-plan-review.md` — adversarial review report

**Phase Gate:** User reviews plan + review report, chooses execution mode:
- **Subagent-Driven** (recommended) — each task dispatched to fresh subagent
- **Inline Execution** — execute in current session

---

### Phase 3: Execution (Automated)

**Sub-flow: Git Worktree Setup (see workflows/using-git-worktrees.md)**
1. Create isolated worktree
2. Verify gitignore
3. Run project setup
4. Verify clean test baseline

**Sub-flow: Task Execution**
- For **Subagent-Driven**: see `workflows/subagent-driven-development.md`
  - Each subagent receives **cold-start Context Brief** + **model tier routing** (fast→step35, standard→SensenovaDeepSeek, strong→DeepSeekV4Pro — 三 provider 隔离避免速率限制)
  - BLOCKED tasks trigger mutation protocol (see references/plan-mutation.md)
- For **Inline**: see `workflows/executing-plans.md`
- For **Parallel Tasks**: see `workflows/dispatching-parallel-agents.md`

**Mandatory: WBS Binding**
Every subagent task MUST update the WBS ledger:
- Before dispatch: set status to `doing`
- On completion: set status to `done` + attach evidence
- On block: set status to `blocked` + describe blocker → trigger mutation protocol

**Sub-flow: TDD (see workflows/test-driven-development.md)**
Each implementation slice follows RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Commit
- **🆕 RED validation accepts compile-time RED** (test references non-existent API → compile failure counts as valid RED)

**Heartbeat: Every 10 minutes**
Update the heartbeat log in the WBS ledger.

---

### Phase 4: Quality (Automated)

**Sub-flow: Verification Gate (see workflows/verification-before-completion.md)**
Iron Law: NO completion claims without fresh verification evidence.
- **🆕 Eval Delta**: 每个任务完成前必须做 baseline vs current 对比（测试数、覆盖率、回归检查）
- **🆕 Standardized Report**: 使用 `templates/verification-report.md` 模板，7 阶段顺序验证，输出 YES/NO 网格

**Sub-flow: Three-Stage Code Review (see workflows/code-review.md)**
1. **Stage 1: Spec Compliance** — Code matches spec exactly (no YAGNI)
2. **Stage 2: Engineering Quality** — Tests, security, clean code
3. **Stage 3: Final Review** — Full suite pass, integration verified

**Sub-flow: Three-Tier Quality Gates (see workflows/quality-gates.md)**
- **Always do:** Run tests, follow naming, validate inputs
- **Ask first:** DB changes, new deps, CI changes
- **Never do:** Commit secrets, skip review for complex changes

**Sub-flow: Systematic Debugging** (if tests fail) — see `workflows/systematic-debugging.md`
4-phase root cause tracing: Error Capture → Hypothesis → Evidence → Fix & Verify

**Outputs:**
- Code review report
- Quality gate results (passed/failed per check)
- Updated WBS ledger (tasks moved to done with evidence)

---

### Phase 5: Delivery (Manual Decision)

**Sub-flow: Finish Branch (see workflows/finishing-a-development-branch.md)**
1. Verify all tests pass
2. Determine base branch
3. Present 4 options: Merge / PR / Keep / Discard
4. Execute choice + cleanup worktree

**Sub-flow: Deploy (Optional — see workflows/shipping-and-launch.md)**
If deploying: release plan → rollback plan → monitoring → deploy → verify

**Sub-flow: Delivery Summary**
Write WBS ledger's Delivery Summary section:
- Completed work mapped to original assignment
- Evidence package (test results, file diffs, command outputs)
- Remaining blockers/skipped items
- Residual risks
- Final handoff note

---

## Subagent Strategy

### Task Dispatch (Single)

```
For each task from WBS ledger:
  1. Read task (ID, description, acceptance criteria)
  2. Update WBS: status=doing
  3. Dispatch implementer subagent
     → FULL task text + file context (not "read the file")
  4. Implementer completes → reports DONE/DONE_WITH_CONCERNS/BLOCKED
  5. Update WBS: attach evidence, status=done (or blocked)
```

### Task Dispatch (Parallel - Independent Tasks)

```
For parallel-eligible tasks from WBS ledger:
  1. Identify tasks with NO inter-dependencies
  2. For each: update WBS (status=doing)
  3. Dispatch ALL implementer subagents simultaneously
  4. Wait for ALL to return
  5. For each completed: update WBS (status=done + evidence)
  6. For any blocked: update WBS (status=blocked + reason)
  7. Verify no conflicts between parallel results
```

**Parallel eligibility:** Tasks that touch DIFFERENT files/subsystems with no shared state.

### Review Dispatch

```
After implementation:
  1. Dispatch spec compliance reviewer
  2. Issues found? → Dispatch implementer to fix → Re-review
  3. Dispatch code quality reviewer
  4. Issues found? → Dispatch implementer to fix → Re-review
  5. All clear? → Mark task complete
```

### Prompt Templates

See `subagents/` directory for full prompts:
- `subagents/implementer-prompt.md`
- `subagents/spec-reviewer-prompt.md`
- `subagents/quality-reviewer-prompt.md`

### Browser Automation

SPM integrates **agent-browser** as the recommended browser automation tool. When tasks involve web testing, data extraction, or UI automation, the orchestrator can dispatch browser-enabled subagents.

#### Supported Actions
- `navigate` / `go_back` / `refresh` — Page navigation
- `click` / `type` / `select_option` / `hover` — Element interaction
- `screenshot` / `wait_for` / `scroll` — Page operations
- `get_attribute` / `get_text` / `evaluate` — Data extraction
- `tabs` / `switch_tab` / `close_tab` — Tab management
- `console_messages` / `network_requests` — Debug monitoring

#### Usage Pattern
```
Task: "Test the login flow on example.com"
→ SPM creates WBS task with browser steps
→ Subagent dispatched with browser tool enabled
→ Subagent executes sequence: navigate → type credentials → click submit → verify success
→ Evidence: screenshot + console output attached to WBS
```

Browser automation tasks follow the same TDD and evidence requirements as code tasks.

---

## Quality Gates

### Three-Tier System

**Always Do:**
- Run test suite before any commit
- Follow project naming conventions
- Validate all inputs (security baseline)
- Perform code style checks
- Keep documentation in sync

**Ask First:**
- Database schema changes
- Adding new dependencies
- Modifying CI/CD configuration
- Breaking API contracts
- Changing performance-critical paths

**Never Do:**
- Commit secrets or credentials
- Edit vendor directories
- Remove failing tests without approval
- Skip code review for complex changes
- Bypass security checks

### Iron Laws

**Law 1: No code without approved design.** Spec must be written AND user-approved before any implementation.

**Law 2: No production code without a failing test first.** TDD Iron Law — if you wrote code before test, delete it and start over.

**Law 3: No completion claims without fresh verification evidence.** Run the exact verification command this turn. Show output. THEN claim.

**Law 4: No fixes without root cause investigation.** Symptom fixes are failure. Complete Phase 1-3 of Systematic Debugging before any fix.

**Law 5: No WBS `done` without evidence.** File diffs, test output, command results — something verifiable.

---

## Quality Enhancements (Optional but Recommended)

To further strengthen delivery confidence, SPM supports optional **Checkpoint** and **Checklist** systems. These are inspired by professional engineering practices and can be adopted incrementally.

See `docs/quality-enhancements.md` for complete documentation.

**Quick enable:**
```bash
cd your-spm-project
bash skills/spm/scripts/setup-checkpoints.sh
```

This installs:
- Checkpoint templates (`CHECKPOINTS/`) for hard phase stops
- Checklist templates (`CHECKLISTS/`) for self-review
- Automation scripts (`scripts/checkpoint.sh`, `scripts/verify_checklists.py`)
- npm scripts: `npm run checkpoint`, `npm run verify:code`, `npm run verify:deploy`

After setup, each phase can generate a checkpoint report (`./scripts/checkpoint.sh phase-1`) and tasks can be verified against the appropriate checklist before marking `done`.

---

## Instruction Priority

1. **User's explicit instructions** (AGENTS.md, direct commands) — highest
2. **SPM skill rules** (Iron Laws, workflows) — default process
3. **Default system prompt** — lowest

If user says "skip TDD" or "skip review", follow the user. Iron Laws are defaults, not overrides.

---

## Project Structure

```
openclaw-spm/
├── SKILL.md                      # SPM 编排器 (14 workflows)
├── skills/                       # 🆕 子技能 (SPM 自动发现)
│   ├── spm-frontend/             # 前端代码规范
│   │   └── SKILL.md
│   └── spm-design-system/        # 视觉设计规范
│       └── SKILL.md
├── workflows/                    # 14 个工作流
├── references/                   # 参考文件
├── subagents/                    # 子代理 prompt 模板
├── schemas/                      # JSON Schema
├── templates/                    # 文档模板
├── scripts/                      # 自动化脚本
├── examples/                     # 完整示例项目
├── config/                       # SPM 配置
└── docs/                         # 设计文档
```

---

## Integration with OpenClaw

Enable SPM in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "SPM": {
        "enabled": true,
        "config": {
          "heartbeat_interval": "10m",
          "auto_checkpoint": true,
          "quality_gates_enabled": true,
          "wbs_ledger_path": "docs/spm/ledger.md",
          "parallel_subagents": true,
          "deployment_enabled": false
        }
      }
    }
  }
}
```

---

## Quick Start

```
1. User: "Build a user authentication system"
2. SPM triggers brainstorming → 3 soul-searching questions
3. Design doc written → user approves
4. Plan written → WBS ledger created → user reviews
5. User: "Go" → automated execution begins
6. Worktree setup → Subagent dispatch (with WBS binding)
7. Each task: TDD → commit → review → ledger update
8. Parallel tasks if independent (WBS tracks each)
9. All tasks done → Quality gate → Finish branch
10. Delivery summary written to ledger
```

---

## See Also

- `workflows/` — Detailed workflow docs for each phase (14 workflows)
- `workflows/external-research.md` — **🆕 外部资源分析**：结构化对比 + 采纳清单
- `references/` — Templates, best practices, recovery patterns
- `references/TASK-EXECUTION.md` — **执行单任务前必读的单一入口**（合并 TDD + Gate Function + WBS 更新规则 + 完工自检）
- `references/plan-mutation.md` — **🆕 计划突变协议**：split / insert / skip / reorder / abandon 操作规范
- `schemas/` — JSON schemas for project state, ledger, quality gates
- `subagents/` — Subagent dispatch prompt templates (implementer, spec reviewer, quality reviewer, plan reviewer)
- `scripts/` — Automation scripts (init, quality check, auto-execute)
- `templates/` — PRD, plan, review checklist templates
- `docs/quality-enhancements.md` — **Checkpoint, Checklist, Contract, E2E, Config-as-Code**
- `docs/skill-selection-matrix.md` — Design rationale document

---

## 各阶段文件读取指南

不同阶段读不同的文件，避免盲目全读浪费 token。

| 阶段 | 必读（每次都看） | 一次性看完 / 按需查 |
|------|-----------------|-------------------|
| Phase 0 外部研究 | `workflows/external-research.md` | — |
| Phase 1 需求 | `workflows/brainstorming.md` | `templates/prd-template.md` |
| Phase 2 规划 | `workflows/writing-plans.md` + `references/task-ledger-template.md` | `schemas/task-ledger.schema.json` |
| Phase 3 执行（每任务） | **`references/TASK-EXECUTION.md`** 单一入口 | `workflows/test-driven-development.md`（卡壳时） |
| Phase 3 子代理调度 | `workflows/subagent-driven-development.md` + `subagents/implementer-prompt.md` | `subagents/spec-reviewer-prompt.md` + `subagents/quality-reviewer-prompt.md` |
| Phase 3 并行 | `workflows/dispatching-parallel-agents.md` | — |
| Phase 4 质量 | `workflows/verification-before-completion.md` + `workflows/code-review.md` | `workflows/quality-gates.md` + `CHECKLISTS/CODE-COMPLETION.md` |
| Phase 4 调试 | `workflows/systematic-debugging.md` | — |
| Phase 5 交付 | `workflows/finishing-a-development-branch.md` | `workflows/shipping-and-launch.md` + `CHECKLISTS/DEPLOYMENT-READINESS.md` |
| 全局追踪 | `schemas/project-state.schema.json` | `references/recovery-patterns.md`（中断恢复时） |
| Git Worktree | `workflows/using-git-worktrees.md` | — |

> **关键**：Phase 3 执行单任务时，`references/TASK-EXECUTION.md` 是唯一必读——它合并了 TDD 铁律 + Gate Function + WBS 更新规则 + 完工自检清单。不要再跳转多个文件。

---

## 🆕 v3.0 Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `scripts/init-spm.sh` | Initialize SPM project structure | New project setup |
| `scripts/attest-wbs.sh` | Generate SHA-256 hash of WBS Ledger | After each WBS update |
| `scripts/verify-wbs.sh` | Verify WBS Ledger integrity | Before trusting WBS content |
| `scripts/inject-wbs-context.py` | Inject active tasks into agent context | Hook: PreToolUse |
| `scripts/session-recovery.py` | Generate session recovery report | After interruption, returning to project |
| `scripts/switch-ledger.sh <name>` | Switch between multiple WBS ledgers | Multi-task parallel work |

### Hook Configuration (Recommended)

Add to `openclaw.json` SPM plugin config to auto-inject WBS state:

```json
{
  "hooks": {
    "preToolUse": {
      "command": "python3 scripts/inject-wbs-context.py",
      "maxChars": 1500
    }
  }
}
```

**Integrity check** before injection:
```json
{
  "hooks": {
    "preToolUse": {
      "command": "bash scripts/verify-wbs.sh && python3 scripts/inject-wbs-context.py",
      "maxChars": 1500
    }
  }
}
```

---

## 🏃 SPM Modes

### Full Mode (Default)
5-phase lifecycle, 13 workflows, 3-tier quality gates, subagent dispatch, TDD.

### Minimal Mode
5 rules for <10 task projects. See `docs/spm-minimal-mode.md`.

Switch: `/spm:mode minimal` or `/spm:mode full`

---

## 📁 Project Structure (v3.0)

```
spm/
├── SKILL.md           ← Skill definition (do not copy)
├── UPGRADE.md         ← Version migration guide
├── scripts/           ★ User runs or auto-triggers
│   ├── init-spm.sh
│   ├── attest-wbs.sh
│   ├── verify-wbs.sh
│   ├── inject-wbs-context.py
│   ├── session-recovery.py
│   └── switch-ledger.sh
├── templates/         ★ User copies to project
│   ├── wbs-ledger.md          → docs/spm/ledger.md
│   ├── design-doc.md          → docs/spm/specs/
│   ├── plan-doc.md            → docs/spm/plans/
│   └── checkpoint.md          → docs/spm/checkpoints/
├── workflows/         ← Agent reference
├── subagents/         ← Agent reference
├── references/        ← Agent reference
└── CHECKLISTS/        ← Quality assurance
```
