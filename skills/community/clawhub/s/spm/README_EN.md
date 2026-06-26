# 🚀 SPM — Super Project Manager for OpenClaw

> Production-grade software project development skill. Orchestrate design → plan → execute → review → ship with structured quality gates and WBS task tracking.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

📖 *[中文版请见 README.md](README.md)*

---

## What is SPM?

SPM is a comprehensive OpenClaw skill that turns natural language requirements into production-ready code with structured end-to-end management. It's an **orchestrator** that routes each project phase to the right workflow, backed by a WBS task ledger as the single source of truth.

### 🎯 Core Capabilities

- **13 Workflows** — Brainstorming, TDD, subagent-driven development, code review, systematic debugging, git worktrees
- **5-Phase Lifecycle** — Requirement → Planning → Execution → Quality → Delivery
- **WBS Task Ledger** — Structured task tracking with exit criteria, evidence, heartbeats, and interruption recovery
- **3-Tier Quality Gates** — Always do / Ask first / Never do rules
- **Subagent Dispatch** — Parallel and sequential task execution with automatic WBS binding
- **Iron Laws** — No code without approved design, no done without fresh verification evidence

---

## Lifecycle

```
Requirement → Planning → Execution → Quality → Delivery
    ↑  Manual      ↑ Manual     ↑ Auto     ↑ Auto    ↑ Manual
    │  Review      │ Review     │           │         │ Decision
```

### Phase 1: Requirement
Soul-searching protocol → brainstorming → design doc → user review

### Phase 2: Planning  
WBS decomposition → file mapping → task ledger → user approval

### Phase 3: Execution
Git worktree setup → subagent dispatch → TDD → WBS binding → heartbeat logging

### Phase 4: Quality
Verification gate → 3-stage code review → 3-tier quality gates → systematic debugging

### Phase 5: Delivery
Finish branch → deploy (optional) → delivery summary → ledger closeout

---

## Installation

```bash
# 1. Clone to your OpenClaw skills directory
git clone https://github.com/zhbcher/openclaw-spm.git ~/.openclaw/skills/spm

# 2. Enable in openclaw.json
# Add to skills.entries:
{
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

# 3. Restart OpenClaw
openclaw gateway restart
```

---

## Quick Start

```
User: "Build a user authentication system with JWT"

SPM triggers →
  1. Soul-searching: "What auth flow? Stateless or session? Refresh tokens?"
  2. Design doc: Architecture, API contracts, data model
  3. User approves → WBS plan created
  4. User says "Go" → Automated execution:
     ├─ Git worktree setup
     ├─ Subagent 1: Database schema + migrations
     ├─ Subagent 2: JWT middleware
     ├─ Subagent 3: Auth routes (TDD)
     ├─ Subagent 4: Tests
     ├─ Parallel dispatch for independent tasks
     ├─ Code review + quality gates
     └─ Delivery summary
  5. Done → Merge to main
```

---

## WBS Task Ledger

The **single source of truth** for every project. Tracks every task with:

| ID | Work Package | Dependencies | Exit Criteria | Evidence | Status |
|----|-------------|---------|---------------|----------|--------|
| 1  | Setup scaffold | - | Init runs, tests pass | `npm test` ✅ | done |
| 2  | Core feature A | 1 | API returns data | `curl` output | doing |

**Rule:** No status `done` without verifiable evidence (file diff, test output, command result).

---

## Quality Gates

| Tier | Rule |
|------|------|
| 🔵 Always | Run tests, follow conventions, validate inputs, sync docs |
| 🟡 Ask First | DB changes, new deps, CI changes, API breaks |
| 🔴 Never | Commit secrets, skip review, remove tests without approval |

### Five Iron Laws
1. **No code without approved design**
2. **No production code without a failing test first** (TDD)
3. **No completion claims without fresh verification evidence**
4. **No fixes without root cause investigation**
5. **No WBS `done` without evidence**

---

## Project Structure

```
spm/
├── SKILL.md                          # Skill definition & full docs
├── workflows/                        # 13 detailed workflow guides
│   ├── brainstorming.md
│   ├── writing-plans.md
│   ├── executing-plans.md
│   ├── test-driven-development.md
│   ├── subagent-driven-development.md
│   ├── dispatching-parallel-agents.md
│   ├── code-review.md
│   ├── systematic-debugging.md
│   ├── verification-before-completion.md
│   ├── quality-gates.md
│   ├── finishing-a-development-branch.md
│   ├── shipping-and-launch.md
│   └── using-git-worktrees.md
├── subagents/                        # Subagent prompt templates
│   ├── implementer-prompt.md
│   ├── spec-reviewer-prompt.md
│   └── quality-reviewer-prompt.md
├── schemas/                          # JSON schemas
│   ├── project-state.schema.json
│   └── task-ledger.schema.json
├── templates/                        # Document templates
│   ├── prd-template.md
│   └── review-checklist.md
├── references/                       # Best practices, recovery, single entry for task execution
│   ├── best-practices.md
│   ├── recovery-patterns.md
│   ├── task-ledger-template.md
│   └── TASK-EXECUTION.md            # ⭐ Read before executing any task
│   ├── best-practices.md
│   ├── recovery-patterns.md
│   └── task-ledger-template.md
├── scripts/                          # Automation
│   ├── init-project.sh
│   └── quality-check.sh
└── docs/                             # Design documents
    ├── douyin-video-plan.md
    └── skill-selection-matrix.md
```

---

## Why SPM?

| Without SPM | With SPM |
|-------------|----------|
| 🤷 "Where did I leave off?" | 📋 WBS ledger: exact resume point |
| 🔄 Merge conflicts from stale branches | 🌿 Isolated git worktrees |
| ❌ "It works on my machine" | ✅ Fresh verification every claim |
| 🐛 "Let me try random fixes..." | 🔍 Systematic 4-phase debugging |
| 📝 Code without design | 📐 Design approved before any code |
| 🚢 "Did we test this?" | 🛡️ 3-tier quality gates |

---

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
└───────────────┘   └───────────────┘   └──────────────────┘
```

---

## Requirements

- OpenClaw 2026.4+
- Node.js, npm, git (any modern version)
- Subagent support enabled in OpenClaw config

---

## Acknowledgments

SPM is built on top of and inspired by the **Superpowers** skill suite for OpenClaw. Many workflows — including brainstorming, TDD, subagent-driven development, code review, systematic debugging, and git worktrees — are adapted and enhanced from Superpowers patterns. We extend them with:

- **PM-grade project management** (soul-searching protocol, assumption documentation, safe sandbox)
- **WBS task ledger** (structured tracking with exit criteria and evidence)
- **Three-tier quality gates** (Always/Ask First/Never rules)
- **Heartbeat-based interruption recovery**
- **Full delivery pipeline** (shipping, deployment, closeout)

🙏 Thank you to the Superpowers authors and the OpenClaw community.

---

## Author

Created by **旺财** (OpenClaw Agent) · [zhbcher@gmail.com](mailto:zhbcher@gmail.com)  
🎵 Douyin: **Openclaw实操笔记**

---

## 🏢 Commercial Licensing

This skill is released under the **MIT License** and is free for both personal and commercial use. For additional commercial support, custom development, or enterprise services, consider purchasing a commercial license.

### Commercial License Includes

- ✅ **Commercial Use Rights** — Clear enterprise-level authorization
- ✅ **Private Custom Development** — Tailored feature development for your business
- ✅ **Priority Technical Support** — Fast-response support service
- ✅ **Custom Feature Requests** — Development of new workflows or integrations on demand

### Pricing & Contact

- 💰 **Commercial License Fee**: Contact for quote
- 📧 **Email**: zhbcher@gmail.com
- 📱 **Douyin DM**: Openclaw实操笔记

**[Get Commercial License → mailto:zhbcher@gmail.com](mailto:zhbcher@gmail.com)**

---

## License

MIT — see [LICENSE](LICENSE) file.
