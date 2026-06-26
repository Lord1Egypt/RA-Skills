# Cross-Validation Protocol

After 4 artifacts are produced in a round (Task Phase), 4 verification checks run before Claims Update phase. Each check produces one `verifications.jsonl` entry with a concrete verdict and evidence_refs ≥2.

This is the load-bearing structural addition over plain multi-agent debate: artifacts are *not siloed* — the 4 verifications enforce cross-perspective contact.

---

## Entry schema (verifications.jsonl)

```json
{
  "id": "V-{round}-{check_id}",
  "round": N,
  "check": "critic_attack_on_action_trace | guardian_vs_observer_walkthrough | observer_friction_vs_critic_attack | all_vs_prior_decisions",
  "result": "BROKEN | ROBUST | UNCLEAR | NOT_APPLICABLE",
  "evidence_refs": ["artifacts/round_N/action.md#trace-1", "artifacts/round_M/critic.md#attack"],
  "notes": "short explanation, 1-3 sentences",
  "claims_affected": ["C-N-2"],
  "claim_status_changes": [
    {"claim_id": "C-N-2", "from": "pending", "to": "tested_refuted"}
  ]
}
```

**Rules**:

- `evidence_refs` must include ≥2 artifact section pointers. Bare "I reviewed both" does not count
- `result=NOT_APPLICABLE` allowed only when the check is structurally impossible this round (e.g., no Critic artifact during STRESS-CRITIC). Note reason.
- `claim_status_changes` required when verification refutes/confirms a prior claim

---

## Check 1 — Critic Attack vs Action Trace

**Question**: Does Critic's attack sequence break any of Action's 3 traces?

**Procedure**:

1. For each Action trace (1, 2, 3), simulate Critic's attack preconditions applied mid-trace.
2. Compare: does the trace's outcome change vs its original? Does an invariant in the trace state get violated?

**Verdict rules**:

- `BROKEN`: attack preconditions are realistic (can arise in normal operation) AND at least one trace outcome flips OR state invariant violated.
- `ROBUST`: attack fires but traces hold; document why (what buffer or guard absorbed it).
- `UNCLEAR`: attack partially affects traces but outcome is narrative-level, not state-level.
- `NOT_APPLICABLE`: STRESS-CRITIC round (no Critic artifact).

**Evidence refs**: at least one Action trace section + Critic attack sequence section.

---

## Check 2 — Guardian Invariant vs Observer Walkthrough

**Question**: Does the operator-facing walkthrough respect or violate Guardian's invariant?

**Procedure**:

1. Take Guardian's invariant statement.
2. Walk through Observer's persona's operator steps. At each friction point or success point, ask: does the result preserve the invariant?

**Verdict rules**:

- `BROKEN`: at least one operator action (supported by docs/API) would *produce* a state violating the invariant. E.g., operator can set a field that contradicts a bedrock constraint.
- `ROBUST`: invariant is structurally enforced — operator cannot violate it through supported paths.
- `UNCLEAR`: invariant could be violated through a path the walkthrough doesn't explicitly test.
- `NOT_APPLICABLE`: STRESS-GUARDIAN or STRESS-OBSERVER round.

**Evidence refs**: Guardian invariant + specific Observer walkthrough step.

---

## Check 3 — Observer Friction vs Critic Attack (friendly-fire overlap)

**Question**: Do Observer's friction points (where operators get stuck) overlap with Critic's attack surfaces (where adversaries break the system)?

**Why this matters**: overlap is a strong signal — it means both legitimate-user confusion AND adversarial exploitation target the same architectural weakness. This is the highest-value failure mode type: legitimate users and bad actors converge on the same brittle point.

**Procedure**:

1. List Observer's friction points (step numbers with friction flags).
2. List Critic's attack preconditions and expected break points.
3. Check each Observer friction against Critic surfaces: is there a semantic match?

**Verdict rules**:

- `BROKEN`: ≥1 Observer friction point coincides with Critic attack surface (e.g., "operator gets stuck setting memory" AND "Critic attacks memory via malformed input").
- `ROBUST`: friction points and attack surfaces are orthogonal — operators confuse in one place, adversaries break in another. This is healthy separation.
- `UNCLEAR`: partial overlap, not verifiable.
- `NOT_APPLICABLE`: STRESS-OBSERVER or STRESS-CRITIC round.

**Evidence refs**: Observer friction enumeration + Critic attack preconditions.

---

## Check 4 — All Artifacts vs Prior-Round Decisions (Continuity)

**Question**: Do this round's 4 artifacts reference, respect, or consciously-break prior rounds' decisions?

**Procedure**:

1. Extract all `decisions.jsonl` entries with round < current_round.
2. For each of the 4 artifacts, check: does it cite ≥1 prior decision by R# or primitive name?
3. If an artifact contradicts a prior decision, is the contradiction explicit (overturn) or silent (drift)?

**Verdict rules**:

- `ROBUST`: all 4 artifacts cite ≥1 prior decision; any contradictions are explicitly named as overturns.
- `BROKEN`: ≥1 artifact silently contradicts a prior decision (drift signal).
- `UNCLEAR`: artifacts are novel enough that continuity isn't testable this round.
- `NOT_APPLICABLE`: R1 only (no prior decisions to cite).

**Evidence refs**: per-artifact citation list + specific `decisions.jsonl` entries referenced.

---

## Phase placement in round template

```
A. Lead Assignment
B. Lead Proposal (600-800 words)
C. Supplements (non-lead agents, 200-400 words each)
D. Task Phase — 4 artifacts produced in artifacts/round_NN/
E. Cross-Validation — 4 verifications.jsonl entries
F. Claims Update — new claims + status transitions
G. Assessment (Decision / Convergence / Tensions / Architecture impact)
H. (every 5 rounds) Drift Check
```

Checks 1-4 run in order; Check 3 depends on Checks 1 and 2 being complete (reuses artifact refs).

---

## Failure modes to watch

### 1. Rubber-stamping

All verdicts come back ROBUST across many rounds → flag sycophancy, audit. A healthy run requires ≥1 BROKEN flip across the experiment. If 100% ROBUST, either:

- The system is genuinely robust (rare, suspect) → audit by counting Critic attack severity (escalate adversarial pressure)
- The Critic is producing pro-forma attacks → tighten Critic schema, require more specific hypotheses-of-weakness

### 2. All BROKEN

Critic attack + Observer friction both find everything broken → either:

- The architecture is genuinely fragile (flag for deep rework)
- Critic/Observer are being performatively harsh

Audit by checking whether BROKENs reproduce across rounds. A BROKEN that reproduces is a real signal; one-off BROKENs without follow-up are noise.

### 3. Skipping Check 3

The friendly-fire check (Observer friction vs Critic attack) is the most valuable cross-agent coupling signal. Skipping it (e.g., always marking NOT_APPLICABLE) drops the most important signal. If Check 3 is repeatedly skipped, refine the verification procedure to force it.

### 4. Evidence-ref bypass

If `evidence_refs` consistently point to section *headers* rather than specific lines, the evidence is shallow. Tighten the citation requirement to specific sub-section anchors or line ranges in the next round.

### 5. Claim status changes missing

If verifications produce verdicts but no `claim_status_changes` are recorded, the claims-vs-verifications link is broken. Each `BROKEN` verdict should typically refute a prior pending claim; each `ROBUST` should confirm one. If neither happens, the claim writing or verification process is decorative.

---

## Round count budget

- Non-stress round: 4 verifications expected (`N=4`).
- Stress round (one agent absent): 2-3 verifications expected (some checks NOT_APPLICABLE).
- Over 10 rounds: ~36 verifications minimum; plan target ≥4/round average.

---

## Adapting to your domain

The 4 checks above are designed around the 4-role schema. If your domain uses the same 4-role split, the checks transfer directly. If you've modified the roles:

- Each pair of roles whose artifacts can be meaningfully cross-validated → 1 check
- Always include "current artifacts vs prior decisions" continuity check (Check 4 equivalent)
- Always include the friendly-fire check (operator friction vs adversary attack) if both perspectives exist
- Aim for 3-5 checks per round; less than 3 is under-validation, more than 5 is over-budget
