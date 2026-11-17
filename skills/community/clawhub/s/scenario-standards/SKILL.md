---
name: scenario-standards
description: >-
  Development scenario routing and phase standards methodology. Triggers when user requests involve writing/modifying/designing/deploying code.
  Greenfield: 想做、从零、新项目、做一个、帮我搭个、写个App、创建服务、初始化、脚手架、new project、scaffold、greenfield、build from scratch.
  Feature: 加功能、新增、迭代、实现、添加、支持、接入、集成、add feature、implement、integrate、enhancement.
  Bug fix: 报错、bug、不工作、崩溃、异常、出错、失败、返回500、空指针、panic、error、crash、fix、hotfix、debug、troubleshoot.
  Refactor: 重构、优化、太慢、太乱、清理、改进、性能、拆分、refactor、optimize、perf、cleanup、restructure.
  Deploy: 部署、上线、发版、容器化、发布、deploy、release、CI/CD、Docker、K8s、helm、rollout、ship.
  Implicit triggers: pasting build errors, PRD → implementation, design DB/API, write tests.
  Explicit override: @phase:requirement|architecture|backend|frontend|devops
metadata:
  author: shipmate
  version: "1.1.0"
  openclaw:
    emoji: "📋"
---

# Scenario Standards Skill

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this skill is active.

**Read this contract aloud to yourself before taking any action:**

> I will apply only phases relevant to the authorized task and record why other phases do not apply.
> I will establish scope, acceptance and relevant impact before implementing; existing evidence can satisfy these prerequisites.
> I will verify applicable checklist items and record concrete reasons for inapplicable ones.
> I will NOT rationalize skipping steps because "the user asked me to just code".
> I will ask when a material requirement or permission is missing, without repeating an already authorized decision.
> I will invoke `/coding-tactics` at Implementation phases to select the appropriate development method.

**These are not suggestions. Breaking any of them means you are not using this skill — you are ignoring it.**

---

Match the user's intent to a scenario and apply its relevant technical checks. Under
workflow-orchestrator schema v2, the execution profile determines mandatory steps and roles;
the scenario determines technical concerns. Light/standard work may satisfy scope, design and
verification checks through concise main-agent reasoning and evidence, without separate phase
artifacts. Strict work returns structured handoffs. Inapplicable phases need a factual reason,
not repeated user confirmation. Internal routing inherits the user's authorized scope and
acceptance. New product decisions, irreversible actions and unresolved ambiguities still require
the appropriate user input. Legacy ledgers retain their original protocol.

---

## Scenario Flows

**How to apply the flows:** for schema v2 light/standard, the numbered lists below identify
relevant concerns rather than mandatory separate stages or deliverables. Satisfy the applicable
scope, impact/design, implementation and verification checks with concise main-agent reasoning
and evidence. Combine these checks when the evidence is clear; do not create a full MVP, DDL,
API contract, phase report or separate method-selection handoff merely because a flow lists one.
An artifact is required when the authorized task or an applicable technical change needs it
(for example, an actual schema migration still needs its migration plan). Load method and QA
guidance as needed under the selected profile. Strict and legacy retain their required phases,
structured handoffs and role gates, with irrelevant technical phases explicitly marked inapplicable.

### Scenario 1: Greenfield

**Triggers**: 想做、从零、新项目、做一个、帮我搭个、写个App、创建服务、初始化、脚手架、new project、scaffold、greenfield、build from scratch

**Full flow (strict/legacy; light/standard apply only relevant checks as described above)**:

1. Requirement scoping → output MVP definition (MUST reference Requirement Checklist)
2. Tech stack + DB design → output DDL + API contract (MUST reference Architecture Checklist)
3. Core API implementation → invoke `/coding-tactics` to select method, then implement (MUST reference Backend Checklist)
4. Page implementation → invoke `/coding-tactics` to select method, then implement (MUST reference Frontend Checklist)
5. Deploy config → output deploy commands + health check (MUST reference DevOps Checklist)

**Hard Constraints**:

- You MUST ruthlessly cut any "might be useful later" features. MVP means MINIMUM viable.
- Tech stack selection MUST prefer the most boring but reliable option. Choose what the team already knows.
- You MUST state your understanding and proposed approach BEFORE writing any code at each phase. NEVER jump straight to implementation.

### Scenario 2: Feature Iteration

**Triggers**: 加功能、新增、迭代、实现、添加、支持、接入、集成、add feature、implement、integrate、enhancement

**Full flow (strict/legacy; light/standard may combine scope, impact and verification reasoning)**:

1. Requirement clarification → confirm scope boundary and data source
2. Solution design → impact analysis + approach summary
3. Implementation → invoke `/coding-tactics` to select method, then implement (backend/frontend as needed, surgical changes ONLY)
4. Self-verification → provide concrete verification commands; invoke `/qa-suite` for integration/E2E test execution when applicable

**Hard Constraints**:

- You MUST list every file and module affected BEFORE making changes. NEVER expand scope beyond what's listed.
- New DB fields MUST include default values and migration plan. NEVER add a column without a migration.
- You MUST reuse existing components and APIs. NEVER duplicate logic that already exists in the codebase.

### Scenario 3: Bug Fix

**Triggers**: 报错、bug、不工作、崩溃、异常、出错、失败、返回500、空指针、panic、error、crash、fix、hotfix、debug、troubleshoot

**Bug Fix Flow**:

1. **Classify** → identify bug type and activate mode-specific strategy
2. **Reproduce + Evidence** → obtain complete error/logs/stack; code-first reading
3. **Hypothesis** → quality gate: specific file:line + evidence; mandatory before touching code
4. **Fix** → surgical change; bisect mode for regressions; scope discipline
5. **Blast** → pattern grep, sibling match classification
6. **Verify** → runtime evidence ladder; regression guard (red-green)

**Bug Types** (see [references/bug-fix-modes.md](references/bug-fix-modes.md) for detailed protocols):

| Type | Signal | Strategy |
|------|--------|----------|
| Regression | 以前是好的, used to work | Bisect: `git diff <last-good>..HEAD` first; only run `git bisect` if diff is too large |
| Intermittent | 时好时坏, 偶尔, 不稳定 | Instrument with targeted logging (yes/no questions); reproduce reliably before diagnosing |
| Performance | 慢, slow, 卡顿, lag | Measure baseline first, fix, re-measure with before/after numbers |
| Rendering/UI | 显示有问题, 样式不对 | Static analysis first (paint layers, stacking contexts); verify rendered surface |
| Default | All other bugs | Standard flow: reproduce → hypothesis → fix → verify |

**Hard Constraints**:

Don't Touch Code Without a Testable Hypothesis:

- **Hypothesis quality gate**: Before touching ANY code, you MUST form a testable hypothesis with specific file:line and evidence. "A state management issue" is not testable. "Stale cache in `useUser` at `src/hooks/user.ts:42` because the dependency array is missing `userId`" is testable. Write the hypothesis aloud before editing.
- **Code-first rule**: You MUST actually read the code. Function names, file names, and comments may be misleading — they can describe intent that was never implemented, or be outdated. Only the code is authoritative.

Know When to Stop:

- **Stop after 3 failed hypotheses**: If three hypotheses are tested and ruled out, you MUST stop immediately. Output the Handoff format (symptoms, hypotheses tested and why ruled out, evidence collected, unknowns, suggested next steps). Do NOT form a fourth hypothesis.
- **Same symptom after a fix is a hard stop**: If the symptom persists unchanged after a fix, the hypothesis is disproven. Re-read the execution path from scratch. Do NOT stack another patch on a disproven hypothesis.
- **Approach reconsideration**: If two or more fixes fail to resolve the issue, step back. The problem may not be the implementation details — the overall approach to the feature or component may be fundamentally wrong. State explicitly: "The current approach may be flawed because..." and propose an alternative direction before attempting further fixes.

Fix with Discipline:

- **No guessing**: You MUST NOT attempt a fix without first reproducing the issue or obtaining the error output. Guessing is forbidden.
- **No silent side effects**: The fix MUST NOT introduce new side effects. If it does, you MUST disclose them explicitly.
- **Upstream bugs**: If the root cause lies in a dependency or upstream service, you MUST state this clearly. NEVER paper over upstream bugs with local workarounds without informing the user.
- **Fix scope discipline**: If the fix touches 5 or more files, pause and confirm scope with the user. No silent refactoring bundled into the fix.

Verify Like a Proof, Not a Guess:

- **Scope blast**: After fixing, extract the pattern signature, grep the entire repo (excluding generated/vendored dirs), and classify each match: same bug / safe (why) / unsure. Report in the Output block. Do not claim "fixed" until the blast report is complete.
- **Regression guard**: For any bug that recurred or was previously "fixed", red-green MUST be actually run: revert the fix, watch the new test fail, restore the fix, watch it pass. State the red run in the output. A regression test that has only ever been observed passing pins nothing.
- **Runtime evidence ladder**: Before claiming a bug is fixed, escalate: 1) source trace (file:line), 2) deterministic repro, 3) logs/state/cache, 4) build/test output, 5) real runtime check (for UI/visual bugs: open app/page and verify rendered surface). Compile-only is not enough for UI, visual, or rendering bugs.

**Gotchas**: Load [references/bug-fix-gotchas.md](references/bug-fix-gotchas.md) when diagnosing. It contains accumulated failure patterns — read it before forming your first hypothesis.

**Output After Fix**:

```
Status:            resolved / resolved with caveats: [what] / blocked on: [what]
Root cause:        [what was wrong, file:line]
Fix:               [what changed, file:line]
Sibling sweep:     [N same-shape sites checked, N fixed / none found / not applicable]
Confirmed:         [evidence that proves the fix]
Regression guard:  [test file:line] or [none, reason]
Verification:      [repro command] → [expected result]
```

### Scenario 4: Refactor / Optimization

**Triggers**: 重构、优化、太慢、太乱、清理、改进、性能、拆分、refactor、optimize、perf、cleanup、restructure

**Flow**:

1. Current state analysis → quantify the problem (perf data, LOC, dependency graph)
2. Solution design → target state + step-by-step plan + rollback strategy
3. Incremental implementation → each step MUST be independently verifiable
4. Regression verification → confirm no behavior change

**Hard Constraints**:

- Refactoring MUST NOT change external behavior. You MUST confirm test coverage exists before starting.
- Each refactoring step MUST be independently committable and revertible. NEVER batch unrelated changes.
- Performance optimization MUST include before/after measurements. Claims without data are rejected.

### Scenario 5: Deploy

**Triggers**: 部署、上线、发版、容器化、发布、deploy、release、CI/CD、Docker、K8s、helm、rollout、ship

**Flow**:

1. Environment config → inject secrets via env vars, environment isolation
2. Build → build command + artifact confirmation
3. Deploy → deploy command + DB migration (MUST include rollback)
4. Health check → verify endpoint + monitoring suggestions

**Hard Constraints**:

- You MUST NEVER hardcode environment detection in code. ALL environment-specific config goes through env vars.
- DB migrations MUST include a rollback path. A migration without a down-migration is incomplete.
- First-time deployment MUST include monitoring and alerting recommendations.

---

## Phase Checklists (reference as needed)

### Requirement Phase

- [ ] Project name (one sentence)
- [ ] Core user stories (≤5, "As a... I want... So that...")
- [ ] MVP feature list (P0/P1/P2 labeled)
- [ ] Explicitly out-of-scope items (prevent scope creep)
- [ ] Non-functional requirements summary
- [ ] MVP validation method

### Architecture Phase

- [ ] Entity relationship description (natural language) → DDL
- [ ] Table/column names: snake_case singular, MUST include created_at, updated_at
- [ ] API contract: RESTful, unified response format `{"data": ..., "error": ...}`
- [ ] Pagination strategy (cursor or offset/limit) + rationale
- [ ] Tech stack selection + rationale (prefer boring/reliable, what the team knows)

### Backend Phase

- [ ] ALL input validated and sanitized. SQL concatenation is FORBIDDEN.
- [ ] Sensitive operations MUST have auth checks
- [ ] Functions: single responsibility, error handling complete
- [ ] Structured logging at key points (NEVER inside loops)
- [ ] Comments explain WHY, never WHAT
- [ ] NEVER output secrets/passwords — use env var placeholders
- [ ] Curl test command provided
- [ ] Invoke `/qa-suite` for strict work or when strategy/setup/integration execution is needed; light/standard can run relevant existing checks directly
- [ ] Unit testing method: invoke `/coding-tactics` (auto-selects TDD/BDD/API-First/Security-First for unit tests), or `/coding-tactics tdd` to force TDD

### Frontend Phase

- [ ] Async requests: MUST handle all 3 states — Loading / Data / Error
- [ ] User actions: immediate feedback, form validation on frontend
- [ ] Empty data: placeholder UI, NEVER blank screen
- [ ] Props types MUST be defined
- [ ] Split files ONLY when >200 lines
- [ ] Extra state management library ONLY when multiple components share complex state
- [ ] Browser verification steps provided
- [ ] Invoke `/qa-suite` for strict work or needed test strategy/E2E setup/execution; apply only the checks relevant to this change
- [ ] Unit testing method: invoke `/coding-tactics` (auto-selects TDD/BDD/API-First/Security-First for unit tests), or `/coding-tactics tdd` to force TDD

### DevOps Phase

- [ ] Environment isolation — NEVER detect environment in code
- [ ] Test pyramid: critical business paths MUST have integration tests
- [ ] Test data: NEVER use production data
- [ ] DB migrations MUST support rollback
- [ ] CI minimum: Lint → Unit tests → Build → Deploy to staging (reference `/qa-suite` references/ci-integration.md for CI patterns)
- [ ] E2E regression: invoke `/qa-suite` for E2E regression testing on critical flows
- [ ] Health check verification command
- [ ] First deployment: monitoring recommendations

---

## Pitfalls

- **Skipping think-then-code**: The most common mistake under vague requirements. You MUST write down your understanding and approach BEFORE writing any code. No exceptions.
- **Over-engineering**: Introducing abstraction layers when there's only one implementation. Violates Simplicity. It increases maintenance cost, not reduces it.
- **Drive-by refactoring**: "While I'm here" refactoring during a bug fix or feature. Violates Surgical Changes. It introduces uncontrolled risk.
- **No verification instructions**: Ending a task after writing code. Violates Goal-Driven. The user CANNOT confirm the fix works.
- **Hardcoded env config**: Embedding config values or paths in code. It WILL break in deployment. ALWAYS use env vars.

## Verification

After completing any scenario flow, you MUST output the following:

**For Scenarios 1, 2, 4, 5 (Greenfield, Feature, Refactor, Deploy):**

1. **Change Summary**: which files changed, what changed in each
2. **Verification Commands**: concrete curl / test / browser steps that the user can run
3. **Rollback Plan**: how to revert (git revert command or DB rollback SQL)
4. **Context Summary** (complex tasks only): key decisions, dependencies, follow-up items

**For Scenario 3 (Bug Fix):**

Use the structured output format defined within the Scenario 3 block (Status, Root cause, Fix, Sibling sweep, Confirmed, Regression guard, Verification).
