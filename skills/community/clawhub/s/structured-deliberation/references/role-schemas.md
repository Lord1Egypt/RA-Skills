# Role Schemas — 4-Agent Deliberation Framework

This document defines the 4 agent roles and the artifact each produces per round. The roles are designed to be **structurally complementary**: each contributes a perspective the others can't substitute for, and the verification protocol cross-checks among them.

The framework is domain-agnostic; the role definitions below use abstract language. Three concrete domain instantiations are given at the end.

---

## The 4-Role Structure

| Role | Question it asks | Artifact produced |
|---|---|---|
| Action | "Where's the verb? What does the system actually DO?" | Behavioral Trace Set |
| Guardian | "What's the invariant? What must hold?" | Identity Invariant Check |
| Observer | "Can a real operator/user navigate this?" | Operator Walkthrough |
| Critic | "What's the strongest argument against this?" | Adversarial Test Case |

Each role's artifact is **structured, not narrative** — small enough to produce in ≤30 minutes of focused work, large enough to be cross-validated.

---

## Action — Behavioral Trace Producer

**Purpose**: Force the deliberation to ground in *concrete state-transition sequences*, not abstract feature descriptions.

**Artifact**: Behavioral Trace Set — 3 traces:

- **Happy Path**: typical/expected execution sequence
- **Edge Case**: boundary or adversarial input sequence
- **Cross-Round Reference**: trace that explicitly invokes a prior-round primitive

Each trace contains 10-15 steps with state deltas (e.g., `{var}={new_value}`), an observable outcome, and a self-assessment (1-5) of whether the trace demonstrates the round's topic.

**Minimum required fields**:

- Initial state (≥3 variables)
- Each step has a state delta
- Outcome is a specific observable, not "satisfaction rose" or "the system responded well"
- Architectural hooks used (which prior-round primitives)

**Anti-patterns**:

- Trace is a story (no state transitions)
- Internal-feeling claims ("X feels Y") without a state variable
- Happy + edge paths use identical trigger (no contrast)

**Why irreducible**: Cross-round reference traces (showing how a prior-round primitive enables current-round behavior) can only be produced by an agent that *is* the implementation perspective. Other roles can talk about behavior, but only Action specifies it as state transitions.

---

## Guardian — Invariant Specifier

**Purpose**: Force a falsifiable, single-sentence invariant the system must satisfy. Without an invariant, "consistency" is rhetoric.

**Artifact**: Identity Invariant Check — single-sentence falsifiable invariant + pass/fail verdict on this round's architecture + confidence (1-5) + failure mode descriptions.

**Structure**:

- **Invariant**: "The system must always X — measured by Y — with tolerance Z"
- **Why this invariant matters in this round**: connecting to round topic
- **Verdict**: PASS / FAIL / CONDITIONAL_PASS / INCONCLUSIVE on the round's specific proposal
- **Evidence**: specific text/element being evaluated (not paraphrase)
- **Confidence**: 1-5
- **If FAIL**: mechanism of failure
- **If CONDITIONAL_PASS**: the condition

**Minimum required fields**:

- Invariant must be **falsifiable** (not "the system should feel real")
- Verdict bound to specific round material, not general principles
- Failure mode is a scenario where the invariant fails to protect

**Anti-patterns**:

- Invariant is a feature wish ("should have memory")
- Verdict is "needs more work"
- Evidence is paraphrase, not quote

**Why irreducible**: Formal-style work (proof-sketch, invariant composition, static verification) can only be produced by an agent treating the system as something with falsifiable structure. Other roles look at behavior; Guardian looks at structure.

**Cross-domain examples of invariants**:

- Multi-agent system: "No agent's decision can override a state field marked `protected: true` in the global state"
- RAG system: "Generated answers must include at least one citation with verifiable source from the retrieval set"
- Code review: "All public APIs must have type signatures stable across minor versions"
- Customer-facing tool: "User-visible names and IDs must remain stable across deploys (no breaking-rename without migration plan)"

---

## Observer — Operator Walkthrough Producer

**Purpose**: Force the design to be tested from a non-implementer perspective. Internal beauty without external usability is technical debt.

**Artifact**: Operator Walkthrough — non-technical operator persona + specific goal + 8-15 step attempt + friction points + completion verdict.

**Structure**:

- **Operator Persona**: name, role, technical skill level (specific: "uses Notion, never opens terminal")
- **Goal for this session**: specific, measurable
- **Starting context**: what exists when operator starts; what's documented
- **Step-by-step attempt (8-15 steps)**: each step records *outcome* (success / confusion / stuck), not just action
- **Friction points**: list each stuck-point with line reference to step number
- **Verdict**: goal achieved (Yes / No / Partially); time to first working output; would operator recommend to a peer?
- **Self-assessment**: 1-5 on whether walkthrough tested the round's topic

**Minimum required fields**:

- Persona must include specific non-implementer context
- Steps must record *outcome per step*, not just actions
- Friction points line-referenced to step numbers, not abstract

**Anti-patterns**:

- Persona is generic ("creator", "user")
- Steps are conditional ("the operator would then ...")
- Friction points are abstract ("this is hard")

**Why irreducible**: Operator-voice + completion verdict + proactive friction scanning. Other roles can talk about usability; only Observer enacts it from a specific persona's perspective with concrete outcomes per step.

**Cross-domain examples of operator personas**:

- Game engine: "Mei, indie designer, no programming, wants to add a shopkeeper NPC with memory"
- Internal tool: "Sam, customer support lead, 5 years tenure, wants to set up a new agent team for refunds"
- API library: "Priya, junior engineer, knows Python, has never used this library before, wants to handle webhooks"
- Healthcare workflow: "Dr. Tao, internal medicine, knows EHR but not the new triage tool, wants to assign a patient to specialist"

---

## Critic — Adversarial Tester

**Purpose**: Force adversarial scrutiny of the round's most consequential claims. Without explicit attack, soft consensus is invisible until production.

**Artifact**: Adversarial Test Case — target + hypothesis-of-weakness + preconditions + attack sequence (5-10 steps) + expected outcomes + verdict + claim raised.

**Structure**:

- **Target**: specific artifact being attacked (e.g., "R5 decision on X", "current round Action trace 2", or "Guardian invariant from current round")
- **Why this target**: 1 sentence on why this is the most consequential attack surface
- **Hypothesis of weakness**: "The target fails when X"
- **Preconditions**: input / state / environmental conditions for the attack
- **Attack sequence (5-10 steps)**: each step has observable
- **Expected outcomes**: BROKEN evidence vs ROBUST evidence
- **Verdict** (uncertainty-forward): BROKEN / ROBUST / UNCLEAR
- **Confidence**: 1-5
- **Load-bearing assumption tested**: which prior-round claim/decision this stresses
- **Claim raised** (required, ≥1 per round): each claim has `testable_as` field

**Minimum required fields**:

- Target references a specific prior artifact or decision
- Attack sequence produces observable evidence
- ≥1 claim raised
- **Critic safety valve**: if attack finds no weakness, explicitly record ROBUST with evidence — NOT a pro-forma BROKEN

**Anti-patterns**:

- "What if users are malicious?" (no specific target)
- Sequence is conditional ("the system might...")
- Verdict is "looks okay to me" (no stress test attempted)
- Pro-forma BROKEN to look productive (sycophancy in adversarial form)

**Why irreducible**: Systematic adversarial persistence over many rounds. ~60-80% of Critic's role can be locally replicated by other roles, but the *systematic adversarial persistence* — pursuing the same kind of attack across rounds, accumulating pressure — has no substitute.

---

## Shared Conventions

### Length budget

Each artifact ≤600 words. The schema enforces structure; depth lives in the state/sequence detail, not the prose. If artifacts consistently exceed 600 words, the schema is over-specified — simplify in your next version.

### Time budget

Each artifact producible in ≤30 minutes of focused work. If consistently taking longer, schema needs simplification.

### Claim ID scheme

`C-{round}-{sequence}` where sequence is per-round global. Example: `C-3-2` = 2nd claim raised in R3.

### Cross-references

Within an artifact, reference prior claims/decisions as `R{N}-{role}-{field}` or `C-{round}-{n}`.

---

## Why these 4 roles, not 3 or 5

The 4-role split emerged from calibration on prior 3-agent deliberation experiments. The minimum structural finding:

- **3 roles** (Action / Guardian / Observer): enough perspective diversity, but adversarial pressure is weak. Failure modes get found late.
- **4 roles** (add Critic): adversarial persistence catches failure modes earlier. Disagreement rate goes up (sycophancy resistance improves).
- **5 roles** (add e.g. Domain Expert): more cross-agent coupling emerges, but contribution balance becomes harder; some roles get squeezed in airtime. The 5th role can produce a unique system-layer finding (e.g., "cross-agent dependency emerges only at 5+ agents") but at the cost of round-time efficiency.

If your system has well-defined external standards (e.g., regulatory compliance, domain expertise), a 5th role may be warranted. For most cases, 4 is the floor for adversarial coverage and the ceiling for round-budget tractability.

---

## Domain-specific instantiations

The 4 roles are abstract; their concrete instantiation depends on domain:

### Multi-agent product/architecture deliberation
- Action: implementation engineer perspective
- Guardian: domain ethicist / character integrity (for content systems)
- Observer: end-user / non-technical operator
- Critic: red team / security perspective

### Software architecture review
- Action: implementation lead, demonstrates feasibility traces
- Guardian: maintainability/long-term invariants
- Observer: developer-experience / documentation completeness
- Critic: failure-mode adversary

### Research methodology review
- Action: experimentalist, traces of intended runs
- Guardian: theoretical-validity invariants (does the experiment test what it claims?)
- Observer: peer reviewer / replicator perspective
- Critic: methodological adversary (confounds, alternative explanations)

### Product launch readiness
- Action: ship trace (specific user journey end-to-end)
- Guardian: brand / safety / compliance invariant
- Observer: customer support / first-time user
- Critic: PR risk / failure-mode adversary

The principle is: each role contributes a perspective the others can't substitute, and the 4 perspectives together force the deliberation to engage *behavior, structure, usability, and adversariality* explicitly.
