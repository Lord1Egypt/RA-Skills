---
name: team-loop
description: >
  Autonomous task loop engine — self-verifying, goal-driven, human-out-of-loop.
  Triggered by: loop, team-loop, 迭代研发, 迭代.
  Human sets a quantifiable goal (e.g., coverage ≥ 50%), agent team autonomously
  executes plan→execute→verify→memorize→replan cycles with zero human intervention.
  Suitable for: coverage improvement, code migration, refactoring, test completion,
  token-budget tasks.
  Unlike team-dev (waterfall: spec→design→code→test), team-loop is a goal-driven
  loop engine that self-iterates until the target is met.
intent: >
  autonomous-loop, self-verifying, goal-driven, quantifiable-target,
  TDD, adversarial-validation, breakpoint-resume, token-budget,
  coverage-gate, snapshot, interaction-id, health-score,
  exception-capture, three-tier-KR, 2/3-voting, RSF, watchdog,
  budget-guard, test-death-penalty, separation-of-concerns
metadata:
  author: iClaw & iFeel
  version: "2.4.1"
  openclaw:
    emoji: "🔄"
    disable-model-invocation: true
    user-invocable: true
---

# team-loop
- Autonomous Task Loop Engine

## ⚠️ Important — Read Before Use

team-loop is a **fully autonomous** task loop engine. Once a quantifiable goal is set,
it will **modify your repository** without further human approval. Be aware:

- **File modification:** Can create, edit, delete source files and tests autonomously
- **Git operations:** May commit, revert, and branch without confirmation
- **Test execution:** Runs project code and tests in subprocesses — untrusted code paths may execute
- **State persistence:** Stores prompts, code context, file paths, and debug logs in `.team-loop/` on disk
- **Broad triggers:** `loop` and `迭代` are common terms — accidental invocation is possible; always review the goal before confirming
- **Safeguards:** Set `budget≤¥N` and `max_rounds=N`. Create `.team-loop/STOP` to halt. Use a disposable branch or clone for untrusted work.

**Install only on repositories where autonomous edits, commits, and test execution are acceptable.**

## Overview

Upgrades the MA agent team from human-driven waterfall delivery to goal-driven autonomous looping.

- **Input:** `team-loop <quantifiable goal>` or `迭代研发 <quantifiable goal>`
- **Flow:** Initialize → Decompose KRs → Dispatch agents → Adversarial verification → Memorize → Next round
- **Output:** Incremental deliverables + State snapshots + Audit reports + Token bills
- **Human involvement only:** Goal setting, abnormal termination, budget confirmation

**Acceptance condition:** The goal must be quantifiable. "Improve code quality" → rejected. "Branch coverage ≥ 50%" → accepted.

**Core principles:**
1. Humans only define the goal and never enter the loop
2. Different agents / different models / different verification methods
3. State on disk, fresh context every round
4. Infrastructure first — logging, IDs, exception capture in place before business code

---

## Trigger

loop, team-loop, 迭代研发, 迭代

Usage:
```
team-loop <quantifiable goal> [budget≤¥N] [max_rounds=N]
迭代研发 <quantifiable goal> [budget≤¥N] [max_rounds=N]
```

Examples:
```
team-loop handler-layer branch coverage 0%→≥50%, budget≤¥20
迭代研发 old-pkg → new-pkg migration, all tests pass
loop src/handlers/ complete tests, coverage≥80%
```

---

## Skill Configuration

This skill is configured with the following safety-first settings:

### `disable-model-invocation: true`

The AI model will **never** automatically invoke this skill on its own. team-loop requires **explicit user invocation** — you must type `team-loop`, `loop`, `迭代研发`, or `迭代` to trigger it. This prevents the model from accidentally launching an autonomous code-modifying loop without your awareness.

### `user-invocable: true`

You (the user) **can** explicitly invoke this skill at any time by typing one of the trigger keywords listed above.

**Why these settings matter:** team-loop is a fully autonomous engine that modifies your repository without further human approval. Requiring explicit user invocation ensures there is always a conscious human decision before the loop begins.

---

## Role System

6 agents, reusing existing MA roles, zero new additions.

| Agent | Role | Responsibility | Deliverables | Red Line |
|-------|------|---------------|--------------|----------|
| **main** | GoalAgent + PlannerAgent + LoopController + Monitor | Parse goal, decompose KRs, schedule & adjudicate, termination judgement, progress aggregation, token billing | StandardGoal, TaskDAG, StateSnapshot, RoundSummary, TokenReport | GoalAgent does NOT read project files; PlannerAgent MUST read rdf/; LoopController/Monitor are purely programmatic and do not call LLM |
| **coder** | ExecutorAgent | Execute KR with TDD three-step, produce code/tests | TaskResult + commit | Does NOT review own code |
| **reviewer** | CriticAgent (correctness) | Static review of code correctness, does NOT run code | Verdict | Does NOT run code |
| **tester** | CriticAgent (completeness) | Dynamic execution of tests, measure coverage, flaky detection | Verdict + CoverageReport | Does NOT review code logic |
| **auditor** | CriticAgent (robustness) | Audit reviewer quality, go through checklist | Verdict | Never executes code, never modifies files |
| **publicist** | MemoryAgent | Distill experience into RDF memory store | MemoryEntry | Read-only, no execution |

### Independence Red Lines

| Agent | Cannot Do | Reason |
|-------|-----------|--------|
| coder | Review own code | Self-review bias |
| reviewer | Run code | Running = participating = loss of independence |
| tester | Review code logic | Reviewer's responsibility |
| auditor | Execute code, modify files | Execution = participation = reviewing oneself |

---

## Knowledge Management: RDF

Project knowledge lives in the managed project's `rdf/` directory. Agents use `read`/`write` tools to directly read and write Turtle (.ttl) format. RDF only stores indexes; agents use indexes to locate and `read` source code directly. If the project has no `rdf/`, the PlannerAgent scans the source code on first run to generate it.

### Directory Layout

```
{project root}/
├── src/                          ← Source code [coder modifies]
├── tests/                        ← Tests [coder modifies]
├── rdf/
│   ├── ast/                      ← Source code index (auto-scanned)
│   │   ├── index.ttl             ← Files → functions → classes → line numbers
│   │   ├── runtime-ctx.ttl       ← Context structure, fixtures, imports
│   │   └── examples.ttl          ← Test examples
│   └── business/                 ← Business knowledge + execution memory (agent distilled)
│       ├── patterns.ttl          ← Verified recurring patterns
│       ├── anti-patterns.ttl     ← Failure pattern library
│       └── memory.ttl            ← KR execution results + experience
├── .team-loop/                   ← Process state (not committed to git)
│   ├── STATE.md
│   ├── config.json
│   ├── HEARTBEAT
│   ├── CRASH.log
│   ├── adr/                      ← ADR-{N}.md
│   ├── cr/                       ← CR-{N}.json
│   ├── patches/                  ← {interaction_id}.patch
│   ├── state-snapshots/          ← {round}.json
│   └── reports/
├── logs/                         ← Logs (not committed to git)
│   └── {loop_id}/R{round}/
│       ├── {agent}.jsonl
│       ├── {agent}.log
│       ├── metrics.json
│       └── round-summary.md
├── docs/ reference/ examples/ scripts/
├── Makefile README.md .gitignore
└── .team-loop/STOP               ← Empty file triggers safe stop
```

### Read/Write Rules

| Role | When | Reads | When | Writes |
|------|------|-------|------|--------|
| **PlannerAgent** (main) | seq 2 before decomposing KRs | rdf/ast/* + rdf/business/* | — | — |
| **coder** | seq 5 when executing KRs | rdf/ast/* + rdf/business/anti-patterns.ttl | — | Source code, tests |
| **publicist** | — | — | seq 11 recording memories | rdf/business/memory.ttl; new patterns/anti-patterns → patterns.ttl/anti-patterns.ttl |

### Predicate Summary

Prefix convention: `{project-name}-ast:` / `{project-name}-business:`

| Domain | Predicate | Description |
|--------|-----------|-------------|
| ast | hasFunction, hasClass, hasImport, hasFixture | Files → symbols |
| ast | name, signature, source, scope | Symbol properties |
| ast | fields, exampleFile | Runtime context |
| ast | module, function, approach, file | Test examples |
| business | memoryOf, round, vetoBy | KR memory |
| business | outcome → Passed \| Failed \| Skipped | Execution result |
| business | lessons, description, example, solution | Experience explanation |
| business | verifiedIn, seenIn → blank node `{round N}` | Verification/appearance round |

**MemoryEntry example (publicist writing reference):**
```turtle
<kr:K2.1_R3>
    pyov-business:memoryOf "ontology_handler.py coverage test" ;
    pyov-business:outcome pyov-business:Passed ;
    pyov-business:lessons "handle_tree's ctx must include the children field" ;
    pyov-business:round 3 .
```

---

## Git Collaboration (lightweight checkout)

Does not use worktree. Each round, coder develops and commits directly on the current branch.

**Commit convention:** coder commit message format:
```
[KR-{id}] {brief description} | round={N} | interaction_id={id}
```

**auditor review:** The review entry point is `git diff HEAD~1` for the current round's commit.

**Rollback:** KR fails → `git revert` the current round's commit. Patch is backed up by main upon revert into `.team-loop/patches/{interaction_id}.patch`.

| Agent | Git capability |
|-------|----------------|
| main | init, commit, tag (tag: `R{round}-{passed\|failed}`), generate patch |
| coder | Develop and commit on current branch |
| reviewer | Read-only diff |
| tester | Checkout to target commit then pytest |
| auditor | `git diff HEAD~1` to review current round changes (if coder made multiple commits, `git diff HEAD~N..HEAD`) |
| publicist | None |

---

## SOP Main Loop (11-step RSF)

### Initialization (seq 0)

main (LoopController) performs one-time initialization on first launch:
1. Generate `loop_id`: `manual-{timestamp}-{nonce}-L`
2. Generate root `interaction_id`: `manual-{timestamp}-{nonce}`
3. Create directories: `.team-loop/` and subdirectories, `logs/{loop_id}/`
4. Write `config.json`, `STATE.md`
5. Start watchdog process (independent process, heartbeat interval 30s, timeout threshold 60s)
6. If project has no `rdf/`: PlannerAgent scans src/ tests/ to generate `rdf/ast/` index
7. Call `/status` to record baseline balance

### RSF

```json
{
  "format": "roles-steps-flows",
  "version": "2.3",
  "description": "Standard single-round KR execution flow. One ready KR per round.",
  "roles": {
    "items": [
      {"id": "main", "description": "GoalAgent(LLM)+PlannerAgent(LLM)+LoopController(programmatic)+Monitor(programmatic)"},
      {"id": "coder", "description": "ExecutorAgent, TDD three-step"},
      {"id": "reviewer", "description": "correctness critic, static review, does NOT run code"},
      {"id": "tester", "description": "completeness critic, dynamic verification, isolated environment (independent subprocess)"},
      {"id": "auditor", "description": "robustness critic, audits reviewers, 13-item checklist, never executes, never modifies"},
      {"id": "publicist", "description": "memory agent, distills RDF memory"}
    ]
  },
  "steps": {
    "items": [
      {"seq": 1, "description": "Parse goal → StandardGoal", "cells": {"main": {"task": "Parse goal", "description": "GoalAgent(LLM): natural language → StandardGoal. Does NOT read project files", "in": [], "out": ["StandardGoal"]}}},
      {"seq": 2, "description": "Read knowledge base → decompose three-tier KRs", "cells": {"main": {"task": "Plan", "description": "PlannerAgent(LLM): read rdf/ → decompose KRs → generate TaskDAG + TokenEstimate. If technology decision needed → write ADR", "in": ["StandardGoal","MemoryEntry"], "out": ["TaskDAG","TokenEstimate"]}}},
      {"seq": 3, "description": "Fetch ready KR + budget check", "cells": {"main": {"task": "Prepare dispatch", "description": "LoopController(programmatic): fetch highest-priority ready KR → assemble TaskUnit. Call /status + budget guard → produce StateSnapshot(t0)", "in": ["TaskDAG","TokenEstimate","retry|next_kr"], "out": ["TaskUnit","StateSnapshot(t0)"]}}},
      {"seq": 4, "description": "Dispatch coder [timeout 300s]", "cells": {"main": {"task": "Dispatch", "description": "sessions_spawn dispatch TaskUnit to coder", "in": ["TaskUnit"], "out": ["TaskUnit"]}}},
      {"seq": 5, "description": "coder TDD execute", "cells": {"coder": {"task": "Execute KR", "description": "Step1: write test → verify it runs. Step2: if KR requires implementation write minimal code (skip if completing tests for existing code). Step3: full regression → produce TaskResult", "in": ["TaskUnit"], "out": ["TaskResult"]}}},
      {"seq": 6, "description": "Collect → parallel dispatch critics [timeout 120s]", "cells": {"main": {"task": "Dispatch", "description": "Monitor(programmatic): receive TaskResult → sessions_spawn parallel dispatch reviewer + tester", "in": ["TaskResult"], "out": ["TaskResult"]}}},
      {"seq": 7, "description": "Parallel verification", "cells": {
        "reviewer": {"task": "Correctness review", "description": "Static diff read: spec consistency / logical boundaries / API misuse / import hallucination / compatibility / test death penalty → produce Verdict", "in": ["TaskResult"], "out": ["Verdict"]},
        "tester": {"task": "Completeness verification", "description": "Isolated environment (independent subprocess): pytest collect + execute → coverage diff against baseline → full regression → flaky detection (new test run 3 consecutive times for consistent results) → produce Verdict + CoverageReport", "in": ["TaskResult"], "out": ["Verdict","CoverageReport"]}
      }},
      {"seq": 8, "description": "Collect verdicts → dispatch auditor [timeout 120s]", "cells": {"main": {"task": "Collect + dispatch auditor", "description": "Monitor(programmatic): receive reviewer.Verdict + tester.Verdict + CoverageReport → sessions_spawn dispatch auditor (attached with TaskResult + dual Verdict + CoverageReport)", "in": ["Verdict","Verdict","CoverageReport","TaskResult"], "out": ["TaskResult","Verdict","Verdict","CoverageReport"]}}},
      {"seq": 9, "description": "auditor audit", "cells": {"auditor": {"task": "Robustness audit", "description": "Go through 13-item checklist → produce Verdict. If ADR omission found, can interrupt current KR and notify main", "in": ["TaskResult","Verdict","Verdict","CoverageReport"], "out": ["Verdict"]}}},
      {"seq": 10, "description": "Collect auditor → adjudication + termination check", "cells": {"main": {"task": "Adjudication", "description": "LoopController(programmatic): receive auditor.Verdict. Aggregate 3 votes: ≥2 passed → pass; 1 passed → fail (retry ≤3 times, go back to seq3); 0 → skip. Check stop conditions. Produce Decision + TokenReport + StateSnapshot(t1) + RoundSummary", "in": ["Verdict"], "out": ["Decision","TokenReport","StateSnapshot(t1)","RoundSummary","TaskResult","retry|next_kr"]}}},
      {"seq": 11, "description": "Memory distillation", "cells": {"publicist": {"task": "Record memory", "description": "Distill results into rdf/business/: if passed → record success pattern; if failed → record veto reason + improvement suggestions", "in": ["TaskResult","Decision"], "out": ["MemoryEntry"]}}}
    ]
  },
  "flows": {
    "items": [
      {"id":"f1","type":"sync","from":{"role":"main","seq":1},"to":{"role":"main","seq":2},"what":"StandardGoal"},
      {"id":"f2","type":"sync","from":{"role":"main","seq":2},"to":{"role":"main","seq":3},"what":"TaskDAG+TokenEstimate"},
      {"id":"f3","type":"sync","from":{"role":"main","seq":3},"to":{"role":"main","seq":4},"what":"TaskUnit"},
      {"id":"f4","type":"async","from":{"role":"main","seq":4},"to":{"role":"coder","seq":5},"what":"TaskUnit","description":"[timeout 300s]"},
      {"id":"f5","type":"async","from":{"role":"coder","seq":5},"to":{"role":"main","seq":6},"what":"TaskResult"},
      {"id":"f6","type":"async","from":{"role":"main","seq":6},"to":{"role":"reviewer","seq":7},"what":"TaskResult","description":"[timeout 120s]"},
      {"id":"f7","type":"async","from":{"role":"main","seq":6},"to":{"role":"tester","seq":7},"what":"TaskResult","description":"[timeout 120s]"},
      {"id":"f8","type":"async","from":{"role":"reviewer","seq":7},"to":{"role":"main","seq":8},"what":"Verdict"},
      {"id":"f9","type":"async","from":{"role":"tester","seq":7},"to":{"role":"main","seq":8},"what":"Verdict+CoverageReport"},
      {"id":"f10","type":"async","from":{"role":"main","seq":8},"to":{"role":"auditor","seq":9},"what":"TaskResult+Verdict(×2)+CoverageReport","description":"[timeout 120s]"},
      {"id":"f11","type":"async","from":{"role":"auditor","seq":9},"to":{"role":"main","seq":10},"what":"Verdict"},
      {"id":"f12","type":"async","from":{"role":"main","seq":10},"to":{"role":"publicist","seq":11},"what":"TaskResult+Decision"},
      {"id":"f13","type":"async","from":{"role":"publicist","seq":11},"to":{"role":"main","seq":2},"what":"MemoryEntry","description":"[feedback flow, queried by PlannerAgent next round]"},
      {"id":"fR","type":"sync","from":{"role":"main","seq":10},"to":{"role":"main","seq":3},"what":"retry|next_kr","description":"[loop: next_kr or retry → go back to seq3 for next KR or retry]"}
    ]
  }
}
```

### RSF Semantic Rules

- **Parallel:** Multiple cells in the same seq → parallel
- **Sequential:** Different seqs are sequential by default; `from.seq > to.seq` = feedback flow
- **sync:** Within the same role, blocking wait
- **async:** Cross-role (sessions_spawn), fire-and-forget
- **Validation:** flow `(A→B, what=X)` must satisfy `X ∈ A.out ∩ B.in`
- **Annotations:** `[timeout Ns]` `[condition]`

---

## KR Three-Tier Progression

| Tier | Goal | Verification | Failure Handling |
|------|------|--------------|------------------|
| 🔴 K1 Foundation | Prove test infra works | 1 minimal viable test passes | 3 consecutive failures → FATAL |
| 🟡 K2 Coverage | Increase coverage per-file | pytest + cov delta | Retryable ≤3 times → still fail → skip |
| 🟢 K3 Quality | No regression | Full test suite 100% pass | Rollback, record root cause |

**Example:**
```
O: handler-layer branch coverage 0%→≥50%
K1.1: 1 HTTP test is runnable
K2.1-2.3: Per-file coverage ≥50%
K3.1: Full regression passes, no flaky tests
```

### Retry Rules

- A failed KR may be retried up to max 3 times
- On retry, the planner MUST re-read rdf/ for the failure memory from this attempt
- Same KR retried more than 3 times → marked skipped, root cause recorded in memory.ttl
- K1 layer failures are not retried — 3 consecutive failures trigger FATAL directly
- Retry does not change interaction_id, only increments round

---

## Three-Perspective Adversarial Verification

### reviewer — Correctness Review (does NOT run code)

Review items: spec consistency / logical boundaries / API misuse / import hallucination / compatibility / "test death penalty" check

### tester — Completeness Verification (dynamic execution, isolated environment)

Verification items: pytest collect + execute (independent subprocess) / coverage delta / assertion validity / full regression / flaky detection (new test run 3 consecutive times for consistent results)

### auditor — Robustness Audit (never executes code, never modifies files)

13-item checklist:
1. Error handling completeness 2. Resource management 3. Injection safety 4. Reviewer review completeness 5. Tester verification completeness 6. Handover schema compliance (including interaction_id) 7. CR record completeness 8. Log traceability 9. interaction_id consistency 10. Process compliance 11. Model compliance (critic differs from coder model) 12. Patch completeness 13. Self-check (no execution, no modification)

### 2/3 Adjudication

| Votes | Result | Follow-up |
|-------|--------|-----------|
| 3 passed | Pass | Continue to next KR |
| 2 passed | Pass | Record + dissenting opinion |
| 1 passed | Fail | Retryable (≤3 times) → go back to seq3, otherwise → skip |
| 0 passed | Fail | Record root cause, skip |

---

## Stop Conditions (by priority)

| # | Condition | Result |
|---|-----------|--------|
| 1 | All KRs completed | SUCCESS |
| 2 | K1 layer 3 consecutive failures | FATAL |
| 3 | Agent timeout retries exhausted | FATAL |
| 4 | All remaining KR dependencies permanently unsatisfiable | FATAL |
| 5 | Critic spawn fails 3 consecutive times | FATAL |
| 6 | Disk full (ENOSPC) | FATAL |
| 7 | Estimated next round cost > remaining budget | BUDGET |
| 8 | Rounds ≥ max_rounds | MAX_ROUNDS |
| 9 | 3 consecutive rounds with no coverage improvement | STAGNATION |
| 10 | `.team-loop/STOP` exists | MANUAL_STOP |
| 11 | Log escape (M < N) | FATAL |
| 12 | Watchdog detects main controller crash | FATAL |

---

## Configuration & Initialization

### config.json

```json
{
  "budget_yuan": 20,
  "token_rate": {"yuan_per_1k_tokens": 0.002},
  "max_rounds": 50,
  "max_retries": 3,
  "timeouts": {"coder": 300, "critic": 120, "auditor": 120},
  "watchdog": {"heartbeat_interval_s": 30, "timeout_s": 60},
  "models": {
    "coder": "deepseek-v4-pro",
    "reviewer": "glm-5.2",
    "tester": "glm-5.2",
    "auditor": "glm-5.2",
    "publicist": "glm-5.2",
    "main_llm": "deepseek-v4-pro"
  },
  "coverage_thresholds": {"line": 0.80, "branch": 0.70}
}
```

### STATE.md

```markdown
# STATE.md
## Status
running | terminated

## Current loop
- loop_id: {id}
- interaction_id: {id}
- Start time: {ISO8601}
- round: {N}
- KR status: [{"kr_id":"K1.1","status":"completed|failed|skipped|pending"}]

## Accumulated
- Total rounds: {N} | Total duration: {hours}
- Total tokens: in={N}/out={N} | Total cost: ¥{N}

## Stop reason (when loop ends)
{SUCCESS|FATAL|BUDGET|...}
```

### Token ⇔ ¥ Conversion

- `token_rate.yuan_per_1k_tokens` defines the conversion rate
- Every round after /status: `estimated next round cost(tokens) × rate ≤ remaining budget(¥)`
- TokenReport includes the `cost_yuan` field

---

## Deliverable Templates

### Per-Round Loop Output Checklist

| Deliverable | Responsible | Format | Storage Location |
|-------------|-------------|--------|------------------|
| StateSnapshot (t0/t1) | main | JSON | `.team-loop/state-snapshots/{round}.json` |
| TokenReport | main | JSON | `.team-loop/reports/token-R{round}.json` |
| RoundSummary | main | Markdown | `.team-loop/reports/R{round}-summary.md` |
| TaskUnit | main | JSON | sessions_spawn parameter |
| TaskResult | coder | JSON | sessions_spawn return value |
| Verdict×3 | reviewer,tester,auditor | JSON | sessions_spawn return value |
| CoverageReport | tester | JSON | `logs/{loop_id}/R{round}/metrics.json` |
| CR | main | JSON | `.team-loop/cr/CR-{N}.json` |
| Patch | main | unified diff | `.team-loop/patches/{interaction_id}.patch` |
| MemoryEntry | publicist | Turtle | `rdf/business/memory.ttl` append |
| ADR | main | Markdown | `.team-loop/adr/ADR-{N}.md` |
| SessionSummary | main | Markdown | `.team-loop/reports/session-summary.md` |

### Handover Templates

**StandardGoal** (main seq1 output):
```json
{"objective": "handler-layer coverage 0%→≥50%", "budget_yuan": 20, "max_rounds": 50, "constraints": ["do not modify source code"], "accept": "branch coverage ≥50%"}
```

**TaskDAG** (main seq2 output):
```json
{"krs": [
  {"kr_id":"K1.1","layer":1,"priority":1,"spec":"1 HTTP test is runnable","status":"pending","depends":[],"max_retries":3,"retry_count":0},
  {"kr_id":"K2.1","layer":2,"priority":2,"spec":"ontology_handler.py coverage ≥50%","status":"pending","depends":["K1.1"],"max_retries":3,"retry_count":0}
]}
```

**TokenEstimate** (main seq2 output):
```json
{"per_round": {"coder":50000, "reviewer":15000, "tester":12000, "auditor":10000, "publicist":5000, "main_llm":10000}, "total_rounds_estimate": 8, "total_tokens_estimate": 816000, "cost_yuan_estimate": 1.63}
```

**TaskUnit** (main→coder):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"priority":2,"retry_count":0,"max_retries":3,"spec":"ontology_handler.py coverage → ≥50%","context":{"target_file":"src/ontology_handler.py"},"type":"test|code|both"}
```

**TaskResult** (coder→main):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"status":"done|failed","reasoning":"Tested: handle_get(), covered: 4 branches, issue: fixture needs update","files_changed":["src/...","tests/..."],"commit_sha":"abc1234","token":{"in":25000,"out":8000},"self_test":{"total":257,"passed":257,"failed":0}}
```

**Verdict** (reviewer/tester/auditor→main, MUST include interaction_id):
```json
// reviewer:
{"interaction_id":"{id}","passed":true,"issues":[],"suggestions":[]}
// tester:
{"interaction_id":"{id}","passed":true,"all_tests":257,"passed_tests":257,"failed_tests":0,"flaky_tests":[]}
// auditor:
{"interaction_id":"{id}","passed":true,"checklist":[{"#":1,"item":"Error handling","result":"✓|✗|N/A"}],"issues":[]}
```

**CoverageReport** (tester→main):
```json
{"interaction_id":"{id}","baseline":{"line":0.12,"branch":0.08},"current":{"line":0.54,"branch":0.51},"target_file":"src/ontology_handler.py","changed_files":["..."],"br_part":["line:42"]}  // br_part=partially covered branch line numbers
```

**Decision** (main seq10 output):
```json
{"kr_id":"K2.1","interaction_id":"{id}","round":3,"result":"passed|failed|skipped","votes":{"reviewer":true,"tester":true,"auditor":true},"retry_count":0,"next_action":"next_kr|retry|skip|terminate","terminate_reason":"null|<stop condition #N>"}
```

### Document Templates

**StateSnapshot** (one for t0 and one for t1 per round):
```json
{
  "loop_id":"manual-20260628T140000-a3f2-L",
  "interaction_id":"manual-20260628T140000-a3f2",
  "kr_id":"K2.1","round":5,"phase":"start|end",
  "timestamp":"2026-06-28T14:35:00Z",
  "intent":"ontology_handler.py→≥50%",
  "result":"passed|failed|skipped|in_progress",
  "confidence":0.85,"debt_flags":[],
  "next_intent":"mapping_handler.py→≥50%|null",
  "coverage":{"baseline_line":0.12,"current_line":0.54,"baseline_branch":0.08,"current_branch":0.51},
  "tokens":{"round_consumed":45000,"total_consumed":234000,"budget_remaining_yuan":15.32}
}
```

**TokenReport** (mandatory every round):
```json
{
  "loop_id":"manual-20260628T140000-a3f2-L",
  "interaction_id":"manual-20260628T140000-a3f2","round":5,
  "consumption":{
    "coder":{"in":25000,"out":8000,"model":"deepseek-v4-pro"},
    "reviewer":{"in":8000,"out":2000,"model":"glm-5.2"},
    "tester":{"in":6000,"out":1500,"model":"glm-5.2"},
    "auditor":{"in":4000,"out":1000,"model":"glm-5.2"},
    "publicist":{"in":3000,"out":500,"model":"glm-5.2"},
    "main_llm":{"in":5000,"out":2000,"model":"deepseek-v4-pro"},
    "main_prog":{"cost":0}
  },
  "round_total":{"in":51000,"out":15000,"cost_yuan":0.13},
  "cumulative":{"in":234000,"out":68000,"cost_yuan":0.60},
  "budget":{"total_yuan":20,"remaining_yuan":19.40,"used_pct":3.0},
  "guard_triggers":[]
}
```

**RoundSummary** (mandatory every round):
```markdown
# Round {N} Summary
- interaction_id: {id} | round: {N} | KR: {kr_id} {description}
- result: passed/failed | retry: {N}/{max} | duration: {minutes}
- votes: reviewer={✓/✗}, tester={✓/✗}, auditor={✓/✗}
- cost: ¥{amount} ({in}/{out} tokens) | remaining: ¥{amount}
- files: {list} | coverage: {baseline}→{current}
- notes: {issues/experience/debt}
```

**SessionSummary** (loop end):
```markdown
# Session Summary — {loop_id}
- Status: SUCCESS|FATAL|BUDGET|...
- Total rounds: {N} | KR pass rate: {X}/{Y}
- Total duration: {hours} | Total cost: ¥{amount}
- Coverage: {baseline}→{final}
- ADR: {N} | CR: {N}
- Exception aggregation: {ERROR by type + agent distribution}
- Recovery rate: {recovered/total_failures}
- Health score: {0-100}
```

**CR (Change Record)**:
```json
{"cr_id":42,"interaction_id":"{id}","round":5,"commit_sha":"abc1234","files_changed":["src/...","tests/..."],"timestamp":"ISO8601","coder":"{agent}","patch_path":".team-loop/patches/{interaction_id}.patch"}
```

### Health Score

```
health_score = 100 - ERROR_count×5 - WARNING_count×2 - risk_flags_count×3 - no_improvement_3_rounds(-20) - same_KR_retry>2(-10)
```
≥80 healthy / 50-79 warning / <50 triggers manual intervention.

### Budget Guard

| Consumption % | Action |
|---------------|--------|
| ≥80% | Degrade critic model |
| ≥90% | Do not retry failed KRs |
| ≥95% | Pause and wait for manual top-up (stop condition #7 is not yet triggered, giving humans a decision window) |
| Estimated next round > remaining | BUDGET termination (#7) |

### /status Call Timing

| Timing | Step | Purpose |
|--------|------|---------|
| seq 0 initialization | First launch | Record baseline balance |
| seq 3 start of each round | Before dispatching KR | Check remaining balance, budget guard decision |
| seq 10 end of each round | After adjudication | Record consumption, update cumulative |
| On exception | Agent timeout / spawn failure | Record exception, write failure snapshot |

### Escape Detection

Each round should produce 7 agent confirmation logs (coder + reviewer + tester + auditor + publicist + main_seq3 + main_seq10). Expected N=7×round, actual M=log lines matching the interaction_id. M<N → triggers stop condition #11.

---

## Infrastructure

### Interaction Identifier System

Format: `{source}-{timestamp}-{nonce}` (e.g., `manual-20260629T143012-a3f2b1`)

Source: `manual` (manual) | `batch` (sessions_spawn) | `test-{N}` (use case)

Propagation: root ID is immutable → downstream appends context segment → chain trace: `{root ID}/{agent}-R{round}`

**Carriers (absence = escape):**

| Carrier | Location | Purpose |
|---------|----------|---------|
| Log JSONL | `.interaction_id` | Filter full chain by entry point |
| StateSnapshot | `.interaction_id` | State tied to entry point |
| TaskUnit/TaskResult | `.interaction_id` | Task source |
| Verdict(×3) | `.interaction_id` | Review traceability |
| CR | `.interaction_id` | Change traceability |
| ADR | `.interaction_id` | Decision traceability |
| Patch | filename = interaction_id | Patch association |
| STATE.md | interaction_id line | Runtime state association |
| TokenReport | `.interaction_id` | Consumption traceability |

### Logging System (Separation of Concerns)

**Collection side:** Agent calls unified Logger (auto-injects interaction_id/agent/round/timestamp), provides message+level+tools_used. Levels: DEBUG/INFO/WARNING/ERROR.

**Processing side:** Independent analysis module, supports filtering by interaction_id/agent/level, exception aggregation, escape detection, health scoring.

**Perspective side:** main → state+token / auditor → WARNING+ERROR / developer → DEBUG / human → INFO summary.

**Output:** `{agent}.log` (human-readable) + `{agent}.jsonl` (structured, 15 fields: interaction_id, session_id, round, timestamp, level, agent, intent, message, tools_used, tool_calls, failures, latency_ms, tokens_in, tokens_out, risk_flags)

### Exception Capture (Three-Layer Full Coverage)

| Layer | Scope | Mechanism | Escape Prevention |
|-------|-------|-----------|------------------|
| L1 Tool-level | Single tool call | failures field | Must be recorded |
| L2 Session-level | Agent timeout / spawn failure | Monitor detects → ERROR | Fallback log |
| L3 Loop-level | Main controller crash / disk full | Watchdog independent process | Heartbeat timeout 60s → write CRASH.log |

**Watchdog:** Independent process that checks `.team-loop/HEARTBEAT` interval (written every 30s, timeout 60s) → triggers #12. **Fallback log:** Flush `.team-loop/CRASH.log` before process exit.

---

## Architecture Decision Records (ADR)

**Trigger:** Write ADR (with interaction_id) in seq2 when making technology choices. Auditor checks for omissions in seq9 — if found, can interrupt current KR and notify main to supplement.

**Format:** `.team-loop/adr/ADR-{N}.md`
```markdown
# ADR-{N}: {title}
Date: YYYY-MM-DD | Status: proposed|accepted|deprecated|superseded
interaction_id: {id}
## Context
{why, constraints}
## Decision
{what was chosen}
## Consequences
{positive + negative}
## Alternatives
{rejected options + reasons}
```

---

## Coverage Verification

L1 syntax (pytest collection succeeds) → L2 functional (pass + line > 80% + branch > 70%) → L3 semantic (auditor + human). Per-round iteration: baseline → increment → verify improvement → CoverageReport.

---

## TDD Execution Rules (coder)

1. **Write test → verify it runs:** Read TaskUnit → AAA pattern → pytest verify collection success, no import errors → fix on failure → proceed to Step2
2. **Write minimal code to pass:** Execute only when KR requires implementation; skip when completing tests for existing code
3. **Self-check + produce TaskResult:** Full regression → produce reasoning (tested module/function/covered branches/issues) + token stats + commit_sha

---

## Verification Checklist

- [ ] 迭代研发 and team-loop recognize and reject non-quantifiable goals
- [ ] seq0 initialization complete (loop_id/interaction_id/directories/watchdog/config.json)
- [ ] Three-tier KRs correctly decomposed
- [ ] coder TDD three-step, does not self-review
- [ ] reviewer read-only, does not run, includes "test death penalty"
- [ ] tester isolated subprocess + flaky detection (3 consecutive runs with consistent results)
- [ ] auditor post-audit, 13-item checklist includes self-check
- [ ] 2/3 adjudication correct, retry ≤3 times
- [ ] Stop conditions triggered by priority
- [ ] publicist distills to RDF
- [ ] STOP file safe interruption
- [ ] interaction_id fully propagated (9 carriers)
- [ ] StateSnapshot(t0/t1) includes interaction_id + kr_id
- [ ] TokenReport includes cost_yuan + per-agent model
- [ ] RoundSummary + SessionSummary includes health score
- [ ] Budget guard triggers at 80/90/95, estimated overage → #7
- [ ] CR numbered consecutively includes interaction_id
- [ ] JSONL logs include 15 fields
- [ ] Escape detection (expected 7×round vs actual)
- [ ] Watchdog heartbeat 30s / timeout 60s
- [ ] ADR written in seq2 includes interaction_id
- [ ] Commit message includes interaction_id
- [ ] Coverage L1 → L2 → L3
- [ ] Resume after crash from StateSnapshot(t1)

---

## FAQ

**Q: team-loop vs team dev mode?**
`迭代研发` or `team-loop` → team-loop autonomous loop; `团队研发` → 12-stage waterfall. Same main.

**Q: What goals are unsuitable?**
Non-quantifiable ("improve quality"), exploratory ("try optimizing"), requiring frequent human judgment.

**Q: How to stop safely?**
Create `.team-loop/STOP` → complete current KR and exit safely.

**Q: Why is auditor post-positioned?**
Needs to see reviewer + tester Verdicts to evaluate review quality.

**Q: What is the test death penalty?**
On refactoring: wrong test → delete + rewrite, do not patch the wrong test.

**Q: Where to see token/cost?**
TokenReport per round includes cost_yuan, RoundSummary consolidates, SessionSummary shows total ledger.

**Q: How is escape detection calculated?**
Expected 7 records/round × round; actual count log lines by interaction_id; less is escape → #11.

**Q: How to recover after a crash?**
1. Watchdog detects → restart main controller 2. Read STATE.md → find last completed KR 3. Read corresponding StateSnapshot(t1) → resume from next round seq1 4. In-flight KR if already committed, revert then retry.
