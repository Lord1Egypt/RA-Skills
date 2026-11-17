---
name: workflow-guard-rails
slug: workflow-guard-rails
displayName: Workflow Guard Rails
description: >
  Wrap multi-step agent workflows with pre-execution checks, side-effect queues,
  result validation, retry budgets, checkpointing, audit logs, and failure-rule
  accumulation. Prevents false successes, duplicate sends, unrecoverable
  crashes, and silent drift in LLM production systems. Use it when a workflow
  sends, publishes, pays, deletes, or writes to another system, runs unattended
  on a schedule, or must be safe to rerun after a mid-task failure. Trigger
  keywords: workflow safety, workflow guardian, agent guard, guardrails,
  pre-execution check, pre-flight check, retry budget, idempotency, false
  success, duplicate send, checkpoint recovery, rerun safety, audit log, drift
  detection, agent reliability, production guardrails, 工作流守护, Agent 护栏,
  副作用队列, 漂移检测, 幂等, 防重复发送, 假成功, 断点恢复, 生产护栏, 重跑安全.
  Guard #7 (rule accumulation) captures confirmed failures in the same turn
  into a staging file (~/.workbuddy/ERROR-PLAYBOOK.staging.md). Entries reach
  the authoritative ~/.workbuddy/ERROR-PLAYBOOK.md only when the failure
  recurs (count >= 2) or a human confirms the rule — durable global guidance
  is never created by a single unreviewed append.
  中文摘要：为多步骤 Agent 工作流加装七项护栏——执行前检查、检查点、副作用队列、预算
  重试、结果验证、审计记录、规则沉淀，拦截假成功、重复发送与渐进漂移。触发词：工作流
  守护、Agent 护栏、假成功拦截、防重复发送、重试预算、断点恢复、生产护栏、漂移检测.
description_zh: 工作流守护护栏：为多步骤 Agent 工作流加装七项护栏（执行前检查、检查点、副作用队列、预算重试、结果验证、审计记录、规则沉淀），拦截假成功、重复发送与渐进漂移。适用于定时运行、无人值守、含发送/发布/写库等外部副作用、需要失败后安全重跑的工作流。触发词：工作流守护、Agent 护栏、假成功、防重复发送、幂等、断点恢复、生产护栏
description_en: A horizontal safety layer for multi-step agent workflows — pre-execution checks, checkpointing, side-effect queues, retry budgets, result validation, audit logs, and rule accumulation.
version: "1.0.9"
agent_created: true
not_for:
  - Single-shot prompts with no external side effects
  - Pure data transforms already covered by unit tests
  - Workflow authoring or design (use a design guide instead)
  - Judgments requiring human taste or policy decisions (use a review skill)
  - Monitoring external systems the workflow does not own
read_when:
  - "workflow safety"
  - "workflow guardian"
  - "agent guard"
  - "guardrails"
  - "pre-execution check"
  - "pre-flight check"
  - "retry budget"
  - "idempotency"
  - "false success"
  - "duplicate send"
  - "checkpoint recovery"
  - "rerun safety"
  - "audit log"
  - "drift detection"
  - "agent reliability"
  - "工作流守护"
  - "副作用队列"
  - "漂移检测"
  - "幂等"
  - "防重复发送"
  - "断点恢复"
  - "生产护栏"
  - "重跑安全"
tags:
  - workflow
  - reliability
  - agent-safety
  - guardrails
  - idempotency
  - human-in-the-loop
  - llm-ops
  - automation
  - error-handling
  - checkpoints
  - production-readiness
---

# Workflow Guard Rails

A horizontal safety layer for multi-step agent workflows. It does not replace the workflow logic — it wraps it with guards that catch what the workflow itself cannot see: a tool call that returns "success" but produced invalid output, a side effect that fired before validation, a retry that duplicated an external write, and drift that compounds across runs until the system collapses.

## Position in the stack

This skill is the **process host**. It decides *when* to check and *where* a confirmed failure goes. It carries no knowledge of specific errors.

| Layer | What it holds | Who reads it |
|---|---|---|
| Resident | pointer in `~/.workbuddy/MEMORY.md`; gate line inlined into each automation prompt | every session, every unattended run — no trigger needed |
| Process host (this skill) | timing, sequencing, side-effect control, retry budget, rule-accumulation gate | whenever a workflow with external effects starts |
| Knowledge base | `~/.workbuddy/ERROR-PLAYBOOK.md` — concrete errors by operation type + recurrence board | queried at guard #1, #5, #7 |

A skill that is never loaded guards nothing. Do not treat "a skill exists" as "the guard is active" — unattended runs are covered by the resident layer, not by this file.

## Querying the knowledge base

When guard #1 (pre-execution) or #5 (result validation) needs content, open `~/.workbuddy/ERROR-PLAYBOOK.md` and jump by operation type:

| Operation | Section |
|---|---|
| Write JSON / YAML / frontmatter | §2.1 |
| Write files (Edit / Write / scripts) | §2.2 |
| Run shell commands | §2.3 |
| Call APIs / network | §2.4 |
| git | §2.5 |
| Publish / sync skills | §2.6 |
| Data handling / computation | §2.7 |
| Content / layout | §2.8 |
| Facts / images | §2.9 |

Other anchors: **§1** recurrence board — errors seen 2+ times, read this first when tokens are tight; **§3** post-write verification and the six false-success receipts; **§4** attribution discipline.

The playbook lives outside this skill directory on purpose. It is referenced by `~/.workbuddy/MEMORY.md` and by automation prompts that never load a skill, so its path must survive this skill being renamed, removed, or republished.

## When to use

- An LLM or agent workflow runs on a schedule or reacts to events, and a failure means broken output, duplicate messages, or an unrecoverable state.
- You have seen "the task reported done but the result was wrong" at least once.
- External actions (send, publish, pay, delete, write to another system) happen as part of the workflow.
- The same workflow runs repeatedly and you want to detect slow drift, not just hard crashes.

## Do not use

- Single-shot prompts with no external side effects — just validate the output directly.
- Pure data transforms where a unit test already covers correctness.
- Cases needing a human to make the judgment call itself (use a review skill instead).

## The seven guards

| # | Guard | What it does | Signal it catches |
|---|---|---|---|
| 1 | Pre-execution check | Verify input completeness, permissions, success criteria, idempotency key | Missing prerequisites, wrong scope |
| 2 | Checkpointing | Split long tasks into recoverable checkpoints | Unrecoverable mid-task crash |
| 3 | Side-effect queue | Hold external actions until validation passes | Broken output reaching users |
| 4 | Retry budget | Rebirth on failure, capped retries, no local patches | Duplicate sends, partial corruption |
| 5 | Result validation | Independent assertions, not "tool returned OK" | False success |
| 6 | Audit log | Record steps, evidence, human confirmations | Lost context, undetectable drift |
| 7 | Rule accumulation | Capture every confirmed failure **in the same turn** into the staging file `~/.workbuddy/ERROR-PLAYBOOK.staging.md`; promote to the authoritative playbook on recurrence or human confirmation | Recurring, un-codified errors |

> **Detailed patterns**: for per-guard implementation details and example invariants by workflow type, load `references/guardian-patterns.md`.

## Operating procedure

1. **Before execution**: run guard #1. If input, permissions, or success criteria are incomplete, stop and report — do not guess.
2. **During execution**: emit checkpoints (guard #2) at each irreversible boundary.
3. **Before any external action**: push it to the side-effect queue (guard #3). It stays queued until validation passes.
4. **After generation/computation**: run independent assertions (guard #5). Any failure triggers rebirth within the retry budget (guard #4). Local patches are forbidden — rebirth the whole unit.
5. **After success**: write the audit log (guard #6). Confirmed failures are captured into the staging file (guard #7) **in the same turn the failure is confirmed** — staging is immediate and reversible; promotion into the authoritative playbook is gated (recurrence or human confirmation).

## Human in the loop

Require explicit confirmation before:
- First use of a high-privilege tool.
- Any irreversible or external action (send, publish, pay, delete, external write).
- Low-confidence results.
- Retry budget exhausted or validation still failing.
- Overriding or deleting an accumulated rule. Staging appends do not wait for approval — waiting is what kept the rule library empty. **Promotion** of a staged rule into the authoritative playbook does require a gate: either the failure recurs (count >= 2) or a human confirms the rule.

## Result validation pattern (guard #5)

This is the core. Never treat "the tool call returned successfully" as "the task is done."

```
After the workflow produces output:
  1. Force the model to self-check: output verifiable counts + assertions
  2. Code independently verifies the key invariants
  3. Any assertion fails → rebirth the whole unit (no local patch)
  4. Retry budget reached → report failure, stop, wait for human
```

Key invariants to assert depend on the workflow: field completeness, length limits, format contracts, JSON schema, non-empty critical sections, count equality (e.g. items == summaries), and absence of the broken form (unreplaced placeholders, stale markers, duplicate items).

**Boundary trap**: when asserting `A == B`, also assert `A > 0`. Otherwise `A == B == 0` passes but is clearly broken.

**Checkpoint trap**: a checkpoint is state written by the same fallible run. On resume, validate it with guard #5 assertions before continuing — a corrupt checkpoint silently reinstates a broken state, and the retry loop then defends the wrong output.

## Side-effect queue pattern (guard #3)

External actions must never fire directly from a "success" signal. They enter a queue and execute only after validation passes. This is what prevents an empty or broken output from reaching users, customers, or other systems.

## Failure-rule accumulation (guard #7)

This guard is the reason a workflow stops repeating the same mistake. Two parts:

- **Where** — a two-stage store:
  1. `~/.workbuddy/ERROR-PLAYBOOK.staging.md` — the **capture** file. Every confirmed failure is appended here in the same turn. Staging is cheap, reversible, and bounded: a wrong entry here never becomes durable guidance.
  2. `~/.workbuddy/ERROR-PLAYBOOK.md` — the **authoritative** knowledge base, indexed by **operation type** (write JSON/YAML/frontmatter, write files, run shell, call API, git, publish, compute, layout, facts/images). Guards #1/#5 read only this file. Do not create a third location.
- **When** — capture in the same turn the failure is confirmed. Not at the end of the session, and not into a daily log.

### The promotion gate

A pure approval gate never worked: most failures are discovered while the agent runs unattended, where no human is present to approve anything — the rule library stayed empty for two months while the same errors recurred. A pure no-gate append is also wrong: it lets a single unreviewed entry durably shape every future run.

**The gate is therefore two-stage.** On a confirmed failure, append immediately to the staging file:

```
现象 / 根因 / 可执行的正确做法 / 复发计数 / 捕获时间
```

A staged rule is promoted into the authoritative playbook when either:
- the **same failure recurs** (recurrence count >= 2 — the pattern is proven, not hypothetical), or
- a **human confirms** the rule (e.g. while reviewing the staging file, or when the next session opens the playbook and sees the staged entry).

Promotion moves (not copies) the entry out of staging, so the staging file stays small and reviewable. Human review of staging is **promotion or deletion, not post-hoc cleanup of a live rule**.

If an entry for this failure already exists in staging, increment the recurrence count in place; at count >= 2 promote it into the playbook's §1 recurrence board.

### Why the daily log is not the sink

Daily logs are organised by **date**; the retrieval key is **operation type**. The next time a JSON write fails, nothing leads back to a file named after a day in September. Experience organised by date is unretrievable experience.

### Unattended runs

Most errors are found by the agent itself, mid-run, with no human present to trigger anything. Two consequences:

1. Pre-execution check (#1) and result validation (#5) must be **inlined into the automation prompt**. A skill that is never loaded guards nothing.
2. A failure found during an unattended run is still confirmed — capture it into the staging file within that same run, and state that you did so in the run output. If no human is present to promote it, the recurrence rule (count >= 2) is the gate.

## Drift monitoring (guard #6)

Do not judge compliance on a single run. Track the compliance rate across runs. A single deviation in one run is an early warning; a trend across runs is an escalation. Catching drift at the first deviation prevents the "looks fine every day, then suddenly collapses" failure path.

## Output format

After each guarded run, emit:

```
🛡️ Guardian Report
- Pre-check: ✅ / ❌
- Checkpoints: N
- Side-effects queued: N, executed: N
- Validation: ✅ / ❌ (assertions: X/Y passed)
- Retries used: N / budget
- Audit log: written / skipped
- Rule captured: yes/no (staged this run; promoted to the playbook: yes/no)
- Verdict: ✅ released / ❌ held for human
```

## Limitations

- Guards #5/#6 catch machine-checkable problems (format, count, keyword, length drift). They cannot catch style, semantics, or judgment drift — those need a separate review layer.
- Guards add one validation step per run; budget it as <20% overhead.
- The side-effect queue only protects actions routed through it. Actions fired outside the guardian are not covered.

## Failure Handling

| Scenario | Action |
|---|---|
| Pre-check fails (missing input/permissions) | Stop and report missing items; do not guess |
| Checkpoint crash mid-task | Resume from last checkpoint; do not restart from scratch |
| Validation fails (assertion broken) | Rebirth the whole unit within retry budget; no local patches |
| Retry budget exhausted | Stop, report failure, wait for human confirmation |
| Side-effect queue blocked | Hold all queued actions; do not release until validation passes |
| Audit log write fails | Continue the run but flag the missing audit entry; do not mark fully complete |
| New rule captured | Append to the staging file immediately and flag it in the run output; it reaches the authoritative playbook only via the promotion gate (recurrence or human confirmation) |

## Hard Rules

1. Pre-execution check is mandatory; never skip it to save time.
2. External actions must pass through the side-effect queue; no direct fire-on-success.
3. Validation assertions must be independent — never trust "tool returned OK" as success.
4. Rebirth the whole unit on failure; local patches are forbidden.
5. Retry budget is capped; when exhausted, stop and wait for human.
6. Audit log must be written for every run, including failures.
7. Confirmed failures are captured into `~/.workbuddy/ERROR-PLAYBOOK.staging.md` by the agent in the same turn. The authoritative `~/.workbuddy/ERROR-PLAYBOOK.md` only gains an entry via the promotion gate: recurrence (count >= 2) or explicit human confirmation. Never let a single unreviewed append durably shape future runs — and never depend on a human being present to trigger the capture.
8. Drift is tracked across runs, not judged on a single run.

---

> **中文导语**：Workflow Guard Rails 是多步骤 Agent 工作流的安全护栏，形态为"固定工作流 + 守护 Skill"，不是自主 Agent。它通过七项守卫（执行前检查、检查点、副作用队列、预算重试、结果验证、审计记录、规则沉淀）拦截"假成功"、重复副作用、不可恢复崩溃和渐进漂移。当你说"这个自动化跑久了会不会哪天悄悄坏了""发出去的内容是不是真的验证过""重试会不会重复发"时，就应该用它。