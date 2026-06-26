---
name: structured-deliberation
description: Provides a structured multi-agent deliberation framework with role schemas (action/guardian/observer/critic), verification protocols, and stopping criteria. Activate when designing multi-agent systems for non-trivial deliberation, instrumenting agent debates against sycophancy, or seeking an evaluable alternative to free-form group prompting.
version: 0.1.0
---

# Structured Multi-Agent Deliberation Framework

A protocol for running multi-agent deliberation that produces *evaluable* output — claims with explicit lifecycle, verifications with cross-agent evidence, decisions that cite specific support, and stopping criteria that prevent both premature consensus and infinite loops.

The central premise: **free-form multi-agent prompting produces consensus that looks robust but isn't.** Without structural cross-validation, agents drift toward agreement (sycophancy cascade); without explicit claims, decisions can't be traced to evidence; without stopping criteria, deliberations either stop too early (premature consensus) or run forever (artifact accumulation).

This framework provides:

1. **4 role schemas** (Action / Guardian / Observer / Critic) — each contributing a perspective the others can't substitute
2. **4 cross-validation checks** per round — artifacts are not siloed; they must contact each other
3. **Claims + verifications infrastructure** — disagreements become testable claims with status lifecycles
4. **6 goal-driven stopping criteria** — explicit signals for when the deliberation should end
5. **Stress test protocol** — forced agent absence reveals which roles are load-bearing

## When to use

Activate this skill when:

- Designing a multi-agent system for non-trivial deliberation (not chitchat or task delegation, but actual disagreement-resolving discussion)
- Instrumenting an agent debate to detect sycophancy / convergence quality
- Seeking an evaluable alternative to free-form group prompting (e.g., "5 LLMs discuss X")
- Running architectural / strategic / methodological reviews where cross-perspective rigor matters
- Building a multi-agent system that needs `claims.jsonl` / `verifications.jsonl` / `decisions.jsonl` audit trails

Don't activate when:

- The user wants simple multi-agent task delegation (not deliberation)
- A single LLM with chain-of-thought is sufficient (no real perspective diversity needed)
- The user is asking about LLM ensemble methods for accuracy gains (different problem)

## The 4-role structure

| Role | Question | Artifact |
|---|---|---|
| **Action** | "Where's the verb?" | Behavioral Trace Set |
| **Guardian** | "What's the invariant?" | Identity Invariant Check |
| **Observer** | "Can a real operator navigate this?" | Operator Walkthrough |
| **Critic** | "What's the strongest argument against this?" | Adversarial Test Case |

Full role definitions: [references/role-schemas.md](references/role-schemas.md).

Why these 4: each contributes a perspective the others *can't substitute*. Action grounds in state transitions; Guardian formalizes invariants; Observer tests usability; Critic forces adversarial scrutiny. Without one, the deliberation has a structural blind spot.

## Round structure (8 phases)

Each round runs through:

```
A. Lead Assignment       → who leads this round
B. Lead Proposal         → 600-800 word position
C. Supplements           → other agents' takes (200-400 words each)
D. Task Phase            → 4 structured artifacts
E. Cross-Validation      → 4 verification checks
F. Claims Update         → new claims, status changes, validate
G. Assessment            → decisions, tensions, architecture impact
H. (every K rounds) Drift Check
```

Full template: [templates/round-template.md.tmpl](templates/round-template.md.tmpl).

## Cross-validation: 4 checks

After artifacts are produced (Phase D), 4 verification checks run before claims update:

1. **Critic attack vs Action trace** — does Critic's attack break Action's traces?
2. **Guardian invariant vs Observer walkthrough** — does Operator path violate the invariant?
3. **Observer friction vs Critic attack** — friendly-fire overlap (most valuable signal)
4. **All artifacts vs prior decisions** — continuity / drift detection

Each check produces a `verifications.jsonl` entry with `evidence_refs` ≥2 and a verdict (BROKEN / ROBUST / UNCLEAR / NOT_APPLICABLE).

Full protocol: [references/verification-protocol.md](references/verification-protocol.md).

## Claims infrastructure

Disagreements become testable claims:

```json
{
  "id": "C-{round}-{sequence}",
  "round": N,
  "raised_by": "action | guardian | observer | critic",
  "text": "the claim itself, 1-3 sentences",
  "testable_as": "single observable outcome",
  "status": "pending | tested_confirmed | tested_refuted | partially_refuted | tested_unclear | superseded"
}
```

Status transitions are driven by verification verdicts. Decisions cite claims and verifications.

Full schema and validator: [references/claims-infrastructure.md](references/claims-infrastructure.md), [scripts/claims-validator.py](scripts/claims-validator.py).

## Stopping: 6 signals

The deliberation should consider stopping when **≥4 of 6 signals** are satisfied:

1. Claim refutation rate stabilizes
2. Disagreement slope flat or rising (no sycophancy)
3. All agents have led at least one non-stress round
4. Stress tests have been executed (≥N-1 agents stress-tested)
5. Drift checks pass
6. Pending claim fraction < 30%

Full criteria + detector script: [references/stopping-criteria.md](references/stopping-criteria.md), [scripts/stopping-detector.py](scripts/stopping-detector.py).

## Stress tests

Forced agent absence reveals load-bearing-ness. If a stress round looks identical to a normal round, the absent agent's role is decorative.

Recommended schedule for a 13-round deliberation:

- R5: STRESS-CRITIC (test that adversarial pressure is structural)
- R10: STRESS-GUARDIAN (test that invariant work has unique value)
- R12: STRESS-ACTION (test that behavioral grounding has unique value)
- R13: STRESS-OBSERVER (test that operator perspective has unique value)

In stress rounds, the absent agent's artifact is NOT produced. Verifications involving the absent agent's artifact return `NOT_APPLICABLE` with stress reason in notes.

## Failure modes to watch

8 common failure modes with detection signals:

- FM-1: Sycophancy cascade
- FM-2: All-BROKEN performative adversariality
- FM-3: Drift (silent goal-departure)
- FM-4: Single-agent domination
- FM-5: Claim inflation or starvation
- FM-6: Verification bypass
- FM-7: Stress test avoidance
- FM-8: Round budget overrun

Full catalog with detection signals and responses: [references/failure-modes.md](references/failure-modes.md).

## How to use this skill

When triggered, walk the user through 5 stages:

### Stage 1 — Domain elicitation

Ask:

- What system are you building / evaluating?
- What's the deliberation question? (specific, not "let's discuss X")
- What 4 perspectives make sense for your domain? (See role-schemas.md cross-domain examples)
- What's the round budget? (8 minimum, 13 standard)

### Stage 2 — Role configuration

For each of the 4 roles, instantiate for the user's domain:

- Action: who/what produces behavioral traces? (typically: implementation lead)
- Guardian: who/what specifies invariants? (typically: domain expert / safety / compliance)
- Observer: who/what represents the operator? (typically: user-facing role / customer)
- Critic: who/what attacks? (typically: red team / failure-mode adversary)

Use [templates/role-prompt.md.tmpl](templates/role-prompt.md.tmpl) as starting prompts.

### Stage 3 — Round template configuration

Configure:

- Round budget (typically 13: 10 normal + 2 stress + 1 synthesis)
- Stress test schedule
- Drift check interval (typically every 5 rounds)

Use [templates/round-template.md.tmpl](templates/round-template.md.tmpl) as the per-round structure.

### Stage 4 — Run rounds

For each round:

- Run the 8-phase template (A-H)
- After Phase E, run [scripts/claims-validator.py](scripts/claims-validator.py) to verify integrity
- Every 3-4 rounds, run [scripts/stopping-detector.py](scripts/stopping-detector.py) to evaluate stop signals

Use [scripts/round-controller.py](scripts/round-controller.py) as orchestration skeleton (adapt to your LLM API).

### Stage 5 — Synthesis and retrospective

When stop signals satisfied (≥4/6) OR round budget hit:

- Run a synthesis round (no new claims; resolve pending claims; produce summary)
- Write retrospective using the failure-modes catalog as a checklist
- Document any iteration log entries (what calibration revealed)

## Quick example

User: *"I want to evaluate 3 candidate architectures for our agent system, but free-form discussion keeps converging too fast — I think we're sycophanting."*

Stage 1 reveals:

- System: agent architecture comparison (3 candidates)
- Question: which architecture is most robust under load + adversarial conditions?
- Round budget: 13 (standard)

Stage 2 instantiates 4 roles:

- Action: senior backend engineer (produces behavioral traces of each candidate under load)
- Guardian: SRE lead (invariants around uptime / data integrity / observability)
- Observer: customer support lead (walkthroughs of debugging the system as on-call)
- Critic: security lead (adversarial attack hypotheses)

Stage 3 sets:

- 13-round budget; stress tests at R5/R10/R12/R13
- Drift checks at R5 and R10

Stage 4 runs 13 rounds. After R7, sycophancy detector triggers (Signal 2 negative slope). Response: tighten Critic schema, R8 produces a BROKEN verdict on Action's R3 trace.

Stage 5 synthesis: Architecture B emerges as winner not because of consensus, but because:

- Survived 4 stress tests with signature degradation matching predictions (high C2 in MADEF terms)
- Critic attacks on B reproduced as ROBUST 4 of 5 times (vs A: 1/5, C: 2/5)
- Guardian's invariant ("recovery time < 30s under partial outage") only B passed reliably
- Operator walkthroughs found friction at the same place across 3 different operator personas — meaningful signal, not noise

Full walkthrough: [examples/condensed-deliberation.md](examples/condensed-deliberation.md).

## How the skill behaves at each turn

- **Don't** dump the full 4-role schema at the user upfront. Walk them through Stage 1 elicitation first.
- **Don't** start running rounds (Stage 4) before Stage 2 (role configuration) is settled. Roles improperly cast produce noise.
- **Do** push back if the user wants to skip stress tests "to save rounds". Stress tests are the load-bearing-ness check; without them, the deliberation can't be evaluated.
- **Do** run the validator (`claims-validator.py`) after every Phase F. Errors here cascade.
- **Do** trigger sycophancy alarm if Signal 2 (disagreement slope) goes negative for 2+ rounds. Don't wait for the deliberation to end.

## References

- [references/role-schemas.md](references/role-schemas.md) — full 4-role definitions + cross-domain instantiations
- [references/verification-protocol.md](references/verification-protocol.md) — 4 cross-validation checks
- [references/claims-infrastructure.md](references/claims-infrastructure.md) — jsonl schemas
- [references/stopping-criteria.md](references/stopping-criteria.md) — 6 stop signals
- [references/failure-modes.md](references/failure-modes.md) — 8 failure modes catalog

## Templates

- [templates/role-prompt.md.tmpl](templates/role-prompt.md.tmpl) — parameterized 4-role system prompts
- [templates/round-template.md.tmpl](templates/round-template.md.tmpl) — 8-phase round structure
- [templates/artifact-schemas/](templates/artifact-schemas/) — per-role artifact schemas (action / guardian / observer / critic)

## Scripts

- [scripts/claims-validator.py](scripts/claims-validator.py) — JSONL integrity check (run after Phase F each round)
- [scripts/stopping-detector.py](scripts/stopping-detector.py) — evaluate 6 stop signals (run every 3-4 rounds)
- [scripts/round-controller.py](scripts/round-controller.py) — orchestration skeleton (adapt to your LLM API)

## Examples

- [examples/condensed-deliberation.md](examples/condensed-deliberation.md) — 5-round walkthrough on a fictional architecture comparison
- [examples/stress-test-walkthrough.md](examples/stress-test-walkthrough.md) — what stress rounds reveal (R12/R13 patterns)

## What this skill does NOT do

- It does not run the LLM calls for you — `round-controller.py` is a skeleton; you integrate with your LLM API
- It does not validate that *your* 4 roles are domain-correct — that's a calibration question
- It does not work for single-agent deliberation (use chain-of-thought + self-critique instead)
- It does not produce a single ranking score — outputs are claims, verifications, and decisions with provenance, not a scalar

## Source

This skill captures a methodology developed across multiple multi-agent deliberation experiments, frozen as v1 after running on multiple calibration cases. The 4-role structure, 4 cross-validation checks, 6 stopping signals, and stress test patterns all emerged from calibration findings.

Companion skill: [multi-dim-eval-framework](../multi-dim-eval-framework) — for *evaluating* deliberation quality (MADEF). The two skills compose: this skill produces deliberation; that skill evaluates it.

## License

MIT
