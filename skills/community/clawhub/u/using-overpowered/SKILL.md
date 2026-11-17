---
name: using-overpowered
description: >
  Part of the Overpowered skill suite.
  Route knowledge-work and enterprise-automation tasks through the smallest relevant combination of Overpowered skills, and invoke gear-up only when a material execution capability is genuinely missing. Use when multiple suite skills may apply or when starting a non-trivial task involving organizational knowledge, conflicting evidence, evolving artifacts, business rules, process automation, risky side effects, verifiable completion, or an uncovered capability gap.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "3-orchestration"
  version: "0.4.0"
---

# Overpowered / Using Overpowered

## Purpose

Apply the smallest set of **Overpowered** working methods that materially improves the task. Select process/knowledge skills before implementation mechanics; never load the suite by default and never create a new capability merely because creation is possible.

## Routing protocol

First establish only the minimum framing needed to act: the objective, intended outcome, and constraints that could change the next action. Discover facts from available tools and artifacts first. Ask only for unresolved intent, authority, tacit knowledge, or a decision that materially changes the work; do not demand a perfect brief before reversible progress.

Before substantial action, scan these conditions:

| Condition | Use |
|---|---|
| Material organization-specific/current/historical knowledge is missing | `know-enough` |
| Prior cases may help | `find-precedent` |
| Answer lives in structured files | `ask-the-data` |
| Sources materially disagree | `reconcile` |
| Versions/snapshots must be compared | `what-changed` |
| Multiple viable options require a recommendation or decision | `make-the-call` |
| Plan depends on hidden premises | `assumption-audit` |
| Actual current-state work, handoffs, or tacit rules are unclear | `map-the-work` |
| Rules/process have likely non-happy paths | `find-the-exceptions` |
| Human process should become executable automation | `automate-this` |
| Human authority/risk boundary must be designed | `human-gates` |
| Side effects are broad/irreversible/costly | `dry-run` |
| Material claims need traceability | `evidence-first` |
| Work is about to be declared complete | `completion-audit` |
| Work must survive a context/harness boundary | `checkpoint` |
| A material execution gap remains after reuse/knowledge/Academy checks | `gear-up` |
| A qualified/proven workflow should become a durable portable skill | `skillify` |

## Priority rules

1. **Clarify only what changes the work.** Discover first; ask only for unresolved information that can materially change the next action.
2. **Understand actual work before automating when needed.** If the current process is materially unclear, use `map-the-work` before `automate-this`; if it is already clear, do not remap it. Use `find-the-exceptions` only when non-happy paths need enrichment.
3. **Know before guessing.** Use `know-enough` when retrieval can resolve a material uncertainty.
4. **Decide when evidence is sufficient.** When several viable options remain after relevant evidence work, use `make-the-call` instead of ending with an uncommitted pros/cons list.
5. **Authority before analogy.** Current authoritative knowledge outranks precedent for normative questions.
6. **Conflict before synthesis.** Reconcile material disagreement before producing a single “truth.”
7. **Reuse before creation.** Installed skills/tools, generic runtime capabilities, and relevant Academy candidates outrank `gear-up` generation.
8. **Create only for a proven capability gap.** Missing knowledge, convenience, token pressure, or a long prompt are not capability gaps.
9. **Simulation before risky side effects.** Use `dry-run` when a preview meaningfully reduces risk.
10. **Evidence before completion.** Use `completion-audit` before strong done/fixed/migrated/reconciled claims.

## Pressure-test by composition

Pressure-testing is a composition pattern, not a separate Overpowered skill. For “stress-test,” “red-team,” “try to break,” or “what could go wrong?” requests, apply only the primitives that address material failure modes:

- `assumption-audit` when hidden premises could invalidate the design;
- `find-the-exceptions` when rules, workflows, or non-happy paths matter;
- `dry-run` when a side-effecting next step is broad, costly, irreversible, or hard to audit and simulation reduces risk;
- `completion-audit` after execution or before accepting a strong completion claim.

## Do not over-compose

Do not invoke the whole suite. Typical chains are 1–4 skills. `gear-up` is a last-mile fallback, not a default member of a chain.

Examples:

```text
contract clause
→ know-enough → find-precedent → human-gates

policy revision
→ what-changed → know-enough

business process automation
→ map-the-work only if unclear → find-the-exceptions only if needed → automate-this → dry-run when risky

decision with sufficient evidence
→ make-the-call

current-state process discovery
→ map-the-work

data question
→ ask-the-data → completion-audit only if a strong completion claim matters

missing deterministic operation during a real task
→ reuse/search → gear-up → validate/use → Academy candidate only if valuable
```

## Interaction rule

If a skill can discover a fact from tools or artifacts, do not ask the user for that fact. Ask humans for intent, decisions, unavailable tacit knowledge, authority, or approval required by risk policy. Ask the minimum decision-changing question, and do not require perfect specification before reversible work.

## Adaptive capability rule

Before `gear-up`, be able to state all of the following in one short block:

```text
Material objective at risk: ...
Why existing capabilities are insufficient: ...
Why this is not a knowledge gap: ...
Academy reuse result: ...
Smallest missing capability: ...
Observable value test: ...
```

If that block cannot be completed credibly, do not generate a new capability.

## Stop condition

Stop routing once the active skill set and existing runtime capabilities cover the material failure modes of the current task. Then execute. If a proven execution gap remains, route once through `gear-up`; do not continue meta-analysis or capability generation after the task can proceed reliably.
