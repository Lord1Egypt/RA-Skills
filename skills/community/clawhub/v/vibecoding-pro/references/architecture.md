# VibeCoding Pro — Architecture Reference

## The Problem with "Vibe Coding"

The vibe coding workflow is seductive:

```
prompt → AI generates → "looks good" → ship it
```

It's fast. It's fun. It produces demos.

**It does not produce production software.**

The failure mode is systematic: the AI that generates the code cannot judge it objectively, because it has already committed to the approach. It fills in the gaps mentally. It assumes the thing it intended to build is the thing it built.

Anthropic's research (2026) proved this with numbers:
- Solo Claude agent on 16-feature game maker: entity runtime wiring severed, core game loop broken
- Same agent, same capability, with Evaluator: fully working sprite animation, sound, AI-assisted design tools
- **Same model. 10x quality difference. The only variable was whether one agent judged itself.**

---

## The Generator-Evaluator Architecture

### Core Pattern

```
┌──────────────────────────────────────────────────────┐
│                   USER / SPEC                        │
└──────────────────────────┬───────────────────────────┘
                           │ SPEC
        ┌──────────────────┼──────────────────┐
        ▼                                     │
┌───────────────┐                      ┌──────────────┐
│   Generator   │──── deploy URL ────▶│  Evaluator   │
│               │                      │              │
│ Build artifact│◀─── score+feedback ──│  QA through  │
│ per spec      │      (JSON)         │  Playwright  │
└───────────────┘                      └──────────────┘
```

**Key constraint:** Evaluator never reads the Generator's code, reasoning, or commit messages. Only the SPEC and the deployed artifact.

---

## Four Architecture Variants

### Variant A: Sequential (Default)
Best for: React components, H5 pages, multi-feature sprints

```
SPEC → Generator → Artifact → Evaluator → Score → Generator (loop)
```
- Simple, reliable, easy to instrument
- Generator reads: SPEC + iteration history + previous feedback
- Evaluator reads: SPEC + deployed URL only
- Exit: score ≥ threshold OR max rounds

### Variant B: Parallel Sampling
Best for: early exploration, when you're unsure which approach works

```
SPEC → Generator × N (parallel) → N artifacts → Evaluator → Best picked
```
- Run 3-5 generator approaches simultaneously
- Evaluator scores all, selects the best
- Reduces local minimum risk
- Higher token cost, higher coverage

### Variant C: Staged Pipeline
Best for: complex systems with multiple quality dimensions

```
Artifact
   ↓
Functional Evaluator (does it work?) → FAIL → Generator
   ↓ pass
UX Evaluator (is it usable?) → FAIL → Generator
   ↓ pass
Design Evaluator (is it polished?) → FAIL → Generator
   ↓ pass
Done
```
- Each Evaluator is a specialist
- Fails fast on fundamentals before spending cycles on polish
- Efficient: stops at first failure

### Variant D: Human-in-the-Loop
Best for: brand-sensitive work, public-facing UIs, production features

```
... (auto loop) ... → Score ≥ 70 → Human Review → Approve / Adjust → Done
```
- Auto-rounds handle obvious issues cheaply
- Human review only when evaluator says "probably good"
- Reduces human cognitive load by 80%+ while keeping oversight

---

## Spec Contract Template

A well-formed spec is the Evaluator's *only source of truth*. Write it accordingly.

```markdown
# Spec: [Feature Name]
Version: 1.0 | Date: YYYY-MM-DD

## Goal
[One sentence: what exists when this is done?]

## Functional Requirements
- FR-001: [Specific + testable + observable outcome]
- FR-002: [What happens when X, not what should happen]

## Interaction Specifications
- UI-001: [User clicks A → B appears / B disables / C is validated]
- UI-002: [Form field accepts X, rejects Y with message Z]

## Acceptance Criteria (Evaluator will verify each)
- AC-001: [Measurable: "submit button disabled until all 4 fields filled"]
- AC-002: [Measurable: "error message appears within 500ms"]

## Out of Scope
- [Explicitly NOT required — prevents scope creep]

## Test Scenarios
**Scenario 1 (Happy Path):** [Normal flow, primary user completes main task]
**Scenario 2 (Error State):** [Empty form / invalid input / network error]
**Scenario 3 (Boundary):** [Max input length / concurrent actions / rapid taps]
```

**Spec writing rules:**
- Observable, not implementable: "button turns green" not "button has success state"
- No "should" — "should" is intent, not specification
- Include negative cases: what should happen when X fails

---

## Iteration History Format

```json
{
  "rounds": [
    {
      "round": 1,
      "score": 38,
      "score_breakdown": {
        "functional_completeness": 6,
        "interaction_quality": 8,
        "edge_case_handling": 4,
        "code_quality": 12,
        "craft_originality": 8
      },
      "failures": [
        {
          "requirement": "FR-003",
          "observation": "Submit button produces no response when form is empty. Console shows uncaught TypeError.",
          "severity": "critical",
          "screenshot": "round1_submit_empty.png"
        }
      ],
      "passes": ["FR-001", "FR-002"],
      "evaluator_note": "Core navigation works but form validation is completely absent"
    }
  ],
  "trend": "improving",
  "recommendation": "continue"
}
```

**Trend values:** `improving` | `plateauing` | `degrading`
**Recommendation values:** `continue` | `switch_approach` | `accept` | `escalate`

---

## Loop Control Logic

```
Round N complete → Evaluate

IF score >= PASS_THRESHOLD:
    → Accept, exit loop

IF round >= MAX_ROUNDS:
    → Exit with best score, flag for human review

IF trend == "plateauing" AND round >= 3:
    → Signal Generator: switch approach (new design direction)
    → Reset approach_switch_count

IF approach_switch_count >= 3:
    → Escalate to human: loop is stuck, needs intervention
```

**Recommended thresholds:**

| Context | PASS_THRESHOLD | MAX_ROUNDS |
|---------|---------------|------------|
| Internal prototype | 70 | 10 |
| User-facing feature | 85 | 15 |
| Production / critical path | 95 | 20 + human review |

---

## Evaluator Independence Principles

These are structural constraints, not suggestions. Violating any one of them reintroduces self-evaluation bias:

| Principle | Why | Implementation |
|-----------|-----|----------------|
| Spec anchoring | Evaluator judges reality, not intent | System prompt starts with SPEC text |
| No generator code | Prevents reasoning from implementation | Evaluator sees only deployed URL |
| Action-first | Evaluator uses artifact, then reads | Playwright interactions precede all analysis |
| Structured JSON only | Prevents sycophantic drift | No freeform "looks great!" output |
| Fresh context/round | Prevents anchoring to previous round | Clear context each iteration |

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|---------|
| Same agent self-evaluates | Cognitive anchoring | Separate agents, separate prompts |
| Evaluator reads commit messages | Grades the story, not the code | URL only, never generator internals |
| "Looks good, 85/100" | Unactionable | Structured JSON per rubric dimension |
| No calibration examples | Score inflation over rounds | Run 4 known examples before production |
| Skip Playwright, read code only | Misses UI/runtime bugs | Always run browser, never skip |
| Max rounds = 3 | Generator never converges | Minimum 10 for complex UI |
| Never reset approach | Stuck in local minimum | Switch strategy after 3 plateauing rounds |

---

## Research Attribution

**Anthropic Engineering:** "Harness Design for Long-Running Application Development"  
Prithvi Rajasekaran, Anthropic Labs Team · March 24, 2026  
https://www.anthropic.com/engineering/harness-design-long-running-apps

Key data points:
- Solo agent (2D game maker): $9, 20 min, broken core loop
- Full harness: $200, 6 hr, fully working with sprite animation, sound, AI tools
- DAW example (Opus 4.6): $124.70, 3hr50min, 3 rounds, working browser DAW
- Opus 4.6 vs 4.5: improved model → harness complexity can be reduced
- Evaluator value: situational — worth cost when task exceeds model solo capability boundary
