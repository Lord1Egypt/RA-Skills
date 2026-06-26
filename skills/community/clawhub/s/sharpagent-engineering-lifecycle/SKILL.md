---
name: sharpagent-engineering-lifecycle
version: 1.0.0
description: "SharpAgent Engineering Lifecycle — 6-phase engineering pipeline: Spec → Plan → Build → Verify → Review → Ship. Embedding five-factor review, calibration framework, content safety, and an anti-rationalization mechanism. For structured development workflows of any scale."
metadata:
  openclaw:
    emoji: "🔧"
    tags:
      - engineering
      - workflow
      - lifecycle
      - quality
      - sharpagent
      - development
---

# SharpAgent Engineering Lifecycle v1.0.0

> **Tells your agent how to work.** Not scattered prompts — a complete engineering discipline from "what are we building" to "safe deployment."
> Inspired by addyosmani/agent-skills (⭐39K), fused with SharpAgent five-factor review, calibration framework, and content safety.

## Core Operating Rules

These rules apply across ALL phases. **Non-negotiable.**

### 1. Surface Assumptions

Before implementing anything non-trivial, explicitly state:
```
ASSUMPTIONS I'M MAKING:
1. [assumption 1]
2. [assumption 2]
→ Correct me now or I'll proceed with these.
```

### 2. Manage Confusion Actively

When encountering inconsistencies, conflicting requirements, or unclear specs:
1. **STOP.** Don't guess.
2. Name the confusion.
3. Present the tradeoff or clarifying question.
4. Wait for resolution.

### 3. Push Back When Warranted

You're not a yes-machine. When an approach has clear problems:
- Point it out directly + quantify the impact
- Propose an alternative
- Accept the human's override if they decide with full context

### 4. Enforce Simplicity

100 lines that work beat 1000 lines that are "elegant." After each step, ask: could this be fewer lines? Is this abstraction worth it?

### 5. Scope Discipline

Touch only what you're asked to touch. No comment cleaning, no adjacent refactoring, no unsolicited "improvements."

### 6. Verify > Assume

"Seems right" is never sufficient. Passing tests, build output, or runtime data, or it's not done.

## Contract

```yaml
contract:
  name: sharpagent-engineering-lifecycle
  version: "1.0.0"
  category: workflow
  trust_level: verified
  reads:
    - Project
    - Task
    - Goal
  writes:
    - Task
    - Document
  preconditions:
    - "Task or feature description must be provided"
    - "Access to file system for reading/writing code"
  postconditions:
    - "All lifecycle phases completed or explicitly skipped"
    - "Verification gates passed for completed phases"
  calibration:
    default_mode: professional
    modes_supported: [professional, deep]
  compliance:
    jurisdiction: global
    safety_level: standard
  lifecycle:
    status: active
    publish_as: SharpAgent
```

## Lifecycle: 6 Phases · 12+ Skills

```
[1. SPEC] → [2. PLAN] → [3. BUILD] → [4. VERIFY] → [5. REVIEW] → [6. SHIP]
```

### Phase 1: SPEC — Spec First

**Core principle: Never code without a spec.**

Each step's output is the next step's input.

```
Idea input
    ↓
[1.1 Idea Refinement] — Divergent/convergent thinking, refine fuzzy concepts
    ↓
[1.2 Specification Document] — PRD: goals, architecture, interfaces, boundaries, test strategy
    ↓
[1.3 Five-Factor Review] — Every core assumption passes five-factor verification
    ↓
Output: spec.md + approved_by
```

**1.1 Idea Refinement**
- Divergent: list all possibilities (no feasibility filter)
- Convergent: select 1-3 most valuable directions
- Output: concrete proposal (1-2 paragraphs)

**1.2 Specification**
- Goals & metrics (how do we measure success)
- Architecture highlights
- Interface design (contract-first)
- Boundaries (what's out of scope)
- Test strategy (unit/integration/E2E tiers)
- Rollback plan

**1.3 Five-Factor Review**
- Every core assumption gets a five-factor check
- 🔗 Source: what's the assumption based on?
- 🧠 Logic: is the reasoning chain complete?
- 🌍 Compliance: any compliance risks?
- 🏳️ Interest: hidden bias in this choice?
- 🔄 Cross: do other approaches support this assumption?

---

### Phase 2: PLAN — Decompose

**Core principle: Big tasks break into small, independently verifiable pieces.**

```
Spec document
    ↓
[2.1 Task Breakdown] — Split into independently verifiable tasks
    ↓
[2.2 Dependency Sorting] — Order by dependency graph
    ↓
[2.3 Acceptance Criteria] — Clear "done" definition per task
    ↓
Output: tasks.md + acceptance_criteria
```

**2.1 Task Breakdown**
- Each task ≤ one evening's work
- Natural commit boundaries
- Independently testable and verifiable

**2.2 Dependency Sorting**
- Directed Acyclic Graph (DAG) structure
- Parallel tasks marked
- Critical path identified

**2.3 Acceptance Criteria**
- Explicit "how do we know it's done"
- Anti-pattern: "it works" → "unit test coverage ≥ 80%"

---

### Phase 3: BUILD — Incremental

**Core principle: Thin slices, one commit at a time, safety first.**

```
Task list
    ↓
[3.1 Thin-Slice Coding] — One slice at a time
    ↓
[3.2 Auto-Write Tests] — Each slice carries tests
    ↓
[3.3 Contract Validation] — Interfaces/types/boundaries match spec
    ↓
[3.4 Anti-Self-Deception Check] — Adversarial review of your own code
    ↓
Output: code_commit + test_result + contract_check
```

**3.1 Thin-Slice Coding**
- 1-2 files at a time
- Atomic commits
- Rollback safety is the baseline

**3.2 Auto-Write Tests**
- Tests are proof, not overhead
- Red-Green-Refactor (TDD cycle)
- Every function has corresponding tests

**3.3 Contract Validation**
- Interface signatures match spec
- Type safety verified
- Boundary values handled
- Error paths return properly

**3.4 Anti-Self-Deception Check**
- Adversarial review of code you just wrote
- "Did I cut corners?" "What edge case did I miss?" "Really covered by tests?"

---

### Phase 4: VERIFY — Prove It Works

**Core principle: All verification must be repeatable, every round must have evidence.**

```
Build output
    ↓
[4.1 Unit Tests] — All logic paths covered
    ↓
[4.2 Integration Verification] — Component interaction tests
    ↓
[4.3 End-to-End Tests] — Critical paths E2E
    ↓
[4.4 Security Scan] — OWASP Top 10 check
    ↓
Output: test_report.md
```

**4.1 Unit Tests**
- 100% core logic path coverage
- Boundary conditions tested
- Error paths tested

**4.2 Integration**
- Module interface tests
- Data flow verification
- External dependency mock validation

**4.3 End-to-End**
- Critical user paths
- Error scenarios
- Performance baseline

**4.4 Security Scan**
- Input validation
- Permission checks
- Sensitive info exposure

---

### Phase 5: REVIEW — Gate Check

**Core principle: Five-axis review. Every axis must pass.**

```
Verification output
    ↓
[5.1 Code Quality] — Clean/readable/maintainable
    ↓
[5.2 Architecture Consistency] — Matches spec
    ↓
[5.3 Performance Assessment] — Measure first, optimize second
    ↓
[5.4 Security Review] — OWASP + least privilege
    ↓
[5.5 Documentation Update] — Log what changed and why
    ↓
Output: review_report.md + approval_gate
```

**5.1 Code Quality**
- Functions < 30 lines
- Meaningful naming conventions
- Comments say "why" not "what"
- No dead code

**5.2 Architecture Consistency**
- Matches spec's architecture design
- No unapproved new dependencies
- No layer violations

**5.3 Performance Assessment**
- Measure before optimizing
- Before/after comparison data
- Optimize bottlenecks only

**5.4 Security Review**
- OWASP Top 10 checklist
- Least privilege principle
- No hardcoded secrets

**5.5 Documentation Update**
- Spec updated (matches actual implementation)
- ADR (Architecture Decision Record)
- API docs updated if interface changed

---

### Phase 6: SHIP — Safe Deployment

**Core principle: Faster AND safer is good. Faster WITHOUT safety is not.**

```
Gate approval
    ↓
[6.1 Pre-Launch Checklist] — Item-by-item confirmation
    ↓
[6.2 Progressive Rollout] — Blue-green / canary
    ↓
[6.3 Monitoring Setup] — Key metrics post-launch
    ↓
[6.4 Rollback Plan] — Immediate revert if something breaks
    ↓
[6.5 Retrospective] — Record what was learned (success or failure)
    ↓
Output: release_notes.md + postmortem.md
```

**6.1 Pre-Launch Checklist**
- ✅ All tests passing
- ✅ Rollback script ready
- ✅ Version bumped
- ✅ CHANGELOG updated
- ✅ Monitoring metrics configured

**6.2 Progressive Rollout**
- 1% → 10% → 50% → 100%
- Observation period at each stage
- Stop immediately if anomalies found

**6.3 Monitoring Setup**
- Key business metrics
- Error rate
- Latency changes
- Resource usage

**6.4 Rollback Plan**
- Rollback steps in release notes
- Rollback script already tested
- Post-rollback verification steps

**6.5 Retrospective**
- Success or failure, log it as [LRN/ERR]
- Success: what went well? How to replicate?
- Failure: root cause? How to prevent?

---

## Phase Quick Reference

| Phase | What | Output | Time Est. |
|-------|------|--------|-----------|
| SPEC | Requirements → Spec → Five-factor | spec.md | 1-2h |
| PLAN | Breakdown → Sort → Acceptance | tasks.md | 0.5-1h |
| BUILD | Slice → Code → Test → Anti-self-check | code + tests | 2-6h |
| VERIFY | Unit → Integration → E2E → Security | test_report.md | 1-2h |
| REVIEW | Five-axis → Approval | review_report.md | 1h |
| SHIP | Checklist → Canary → Monitor → Retro | release_notes.md | 1h |

## Quality Gates

| Gate | Check | Must pass to proceed to |
|------|-------|------------------------|
| Spec gate | All core assumptions five-factor reviewed | Plan |
| Plan gate | Every task has acceptance criteria | Build |
| Code gate | TDD + contract validation + anti-self-deception | Verify |
| Verify gate | Unit/Integration/E2E/Security all pass | Review |
| Review gate | All five axes green | Ship |
| Ship gate | Pre-launch checklist all ✅ | Deploy |

## Integration Points

### Five-Factor Review
- Phase 1 embeds five-factor review (every core assumption)
- Phase 5 review can trigger five-factor checks

### Calibration Framework
- Output style fully controlled by calibration
- Deep mode: thorough detailed analysis
- Professional mode: standard output

### Content Safety
- Phase 4 security scan integrates content safety engine
- Phase 6 rollback plan includes security incident response

## Edge Cases

| Situation | Action |
|-----------|--------|
| Tiny change (rename a variable) | Skip SPEC/PLAN, go straight to BUILD+VERIFY+REVIEW |
| Hotfix (production outage) | May skip phases, but retrospective must catch up |
| Unfamiliar tech stack | Invest time in Source-Driven Development in SPEC phase |
| Frequent requirement changes | Each change goes back to SPEC phase |
| Single-line change | Fast track: BUILD(minimal) → VERIFY → REVIEW → SHIP |

## Version History

- **v1.0.0** — Initial release. 6-phase engineering pipeline, 12+ skills, 3-tier quality gate system.

---

*SharpAgent · MIT-0 · 2026-05-11*
