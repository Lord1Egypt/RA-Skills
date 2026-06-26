# Claims + Verifications Infrastructure

Claims and verifications are the structural addition that turns plain multi-agent debate into evaluable deliberation. Without this infrastructure:

- Disagreements are unresolvable narratives
- Decisions can't be traced back to evidence
- Sycophancy looks identical to genuine convergence

With it, every disagreement becomes a *testable claim* with an explicit lifecycle: proposed → verified or refuted → cited in subsequent decisions.

---

## File layout

```
state/
├── claims.jsonl          # one claim per line, append-only
├── verifications.jsonl   # one verification per line, append-only
└── decisions.jsonl       # one decision per line, append-only (cites claims/verifications)
```

All three are append-only JSONL. Never edit prior entries; append corrections as new entries with reference to the prior entry's ID.

---

## Claim entry schema

```json
{
  "id": "C-{round}-{sequence}",
  "round": N,
  "raised_by": "action | guardian | observer | critic",
  "text": "The claim itself, 1-3 sentences.",
  "testable_as": "Single observable outcome that would confirm/refute this claim.",
  "status": "pending | tested_confirmed | tested_refuted | partially_refuted | tested_unclear | superseded",
  "supersedes": null,
  "raised_at_artifact": "artifacts/round_N/{role}.md#claim-section"
}
```

**Required fields**:

- `id` — global unique, format `C-{round}-{sequence}`
- `round` — integer, must match prefix in id
- `raised_by` — one of the 4 roles
- `text` — 1-3 sentences, the claim itself
- `testable_as` — **single observable outcome** that would confirm/refute. Vague claims without `testable_as` are rejected.
- `status` — initially `pending`; transitions via verifications

**Optional**:

- `supersedes` — claim ID this one replaces (when a later claim is more precise)
- `raised_at_artifact` — pointer to the artifact section where the claim was raised

---

## Status state machine

```
       pending
       /  |  \
      /   |   \
   tested_ tested_ tested_
  confirmed refuted unclear
                |
                v
           superseded (optional)
```

**Transition rules**:

- `pending → tested_confirmed`: verification with result=ROBUST and evidence_refs ≥2 supporting the claim
- `pending → tested_refuted`: verification with result=BROKEN and evidence_refs ≥2 contradicting the claim
- `pending → partially_refuted`: verification finds some preconditions break the claim but others hold
- `pending → tested_unclear`: verification produces ambiguous result; documented for later
- `tested_* → superseded`: a later claim with stricter/more-precise wording replaces this one
- `tested_* → tested_*` (re-testing): allowed if a stress test or new evidence emerges; record both the old and new transitions

**Disallowed**:

- Direct `pending → superseded` (must be tested first)
- Editing prior entries to change status (always append a new entry citing the prior)

---

## Verification entry schema

(see [verification-protocol.md](verification-protocol.md) for the full protocol; this is the data shape)

```json
{
  "id": "V-{round}-{check_id}",
  "round": N,
  "check": "critic_attack_on_action_trace | guardian_vs_observer_walkthrough | observer_friction_vs_critic_attack | all_vs_prior_decisions",
  "result": "BROKEN | ROBUST | UNCLEAR | NOT_APPLICABLE",
  "evidence_refs": [
    "artifacts/round_N/action.md#trace-1",
    "artifacts/round_M/critic.md#attack"
  ],
  "notes": "1-3 sentences explaining the result",
  "claims_affected": ["C-N-2"],
  "claim_status_changes": [
    {"claim_id": "C-N-2", "from": "pending", "to": "tested_refuted"}
  ]
}
```

**Required**:

- `id` — globally unique, `V-{round}-{check_id}`
- `evidence_refs` — **at least 2** artifact section pointers (this is the most enforced rule — single-evidence verifications are rejected)
- `result` — one of BROKEN / ROBUST / UNCLEAR / NOT_APPLICABLE
- `claims_affected` and `claim_status_changes` — required when the verification confirms or refutes a claim

---

## Decision entry schema

```json
{
  "id": "D-{round}-{sequence}",
  "round": N,
  "text": "The decision, in actionable language.",
  "cites": [
    {"type": "claim", "id": "C-3-2", "relation": "based-on"},
    {"type": "verification", "id": "V-5-1", "relation": "supported-by"},
    {"type": "decision", "id": "D-2-1", "relation": "supersedes"}
  ],
  "made_by": "consensus | round_lead | adversary_concession",
  "round_artifact_refs": ["artifacts/round_N/lead-proposal.md"]
}
```

**Required**:

- `cites` — at least 1 citation. Decisions without grounding citations are flagged in the continuity check (Check 4 in verification-protocol).
- `made_by` — who/what process produced the decision (consensus / round-lead unilateral / adversary conceded)

**Why decisions need citations**: without them, decisions are floating consensus. The MADEF A1 (Claim Groundedness) measures the fraction of decisions that cite specific evidence. Below ~0.5 indicates sycophancy risk.

---

## Per-round budget

Calibration across multi-round deliberation suggests:

- **Claims raised**: 5-7 per round (1-2 per agent per round, plus 1-2 cross-agent)
- **Verifications**: 4 per non-stress round, 2-3 per stress round
- **Decisions**: 1-3 per round (most rounds make 1-2 decisions; some are pure exploration)

Over 13 rounds, a healthy run produces ~70-90 claims, ~36-50 verifications, ~20-35 decisions.

If your run produces dramatically more (e.g., 200 claims) or fewer (e.g., 15 claims) at 13 rounds, audit:

- Too many claims: claim-raising threshold too low (everything becomes a claim) → tighten `testable_as` requirement
- Too few claims: claim-raising disincentivized or roles aren't producing tensions → check role schemas

---

## Cross-references — how the three files link

```
decisions.jsonl
    cites
       │
       ├──→ claims.jsonl
       │       status updated by
       │           │
       │           v
       │       verifications.jsonl
       │           evidence_refs
       │              │
       │              v
       │       artifacts/round_N/{role}.md
       │
       └──→ verifications.jsonl (direct)
       └──→ decisions.jsonl (supersedes/builds-on)
```

This linkage is what makes the deliberation *evaluable*. Without it, decisions float, claims accumulate without resolution, and verifications are decoration.

---

## Validator

A simple validator script reads the three jsonl files and checks:

1. Every `claim_id` referenced in verifications exists in claims.jsonl
2. Every `evidence_ref` in verifications points to a real artifact section
3. Every claim with status `tested_*` has at least one verification linking to it
4. No claim is in status `superseded` without a later claim citing it as `supersedes`
5. Every decision has at least 1 citation

See `scripts/claims-validator.py` for the reference implementation.

Validation runs after each round (typically as part of phase E). Errors block proceeding to phase F.

---

## Why JSONL not JSON or YAML

- **Append-only**: each round adds entries to the end without rewriting the file
- **Diff-friendly**: git diffs cleanly per-line
- **Streamable**: a long-running process can write entries one at a time without holding state
- **Recoverable**: if a write fails, only the last line is corrupt; everything prior is intact

These properties matter for multi-round runs where the deliberation may span hours/days and the writer is a multi-agent system, not a single human.

---

## Adapting to your domain

The three jsonl files plus the validation pattern transfer to most deliberation-style work. Adaptations to consider:

- **Different claim structure**: if your domain has formal claims (e.g., legal arguments with precedent citations), extend the claim schema with domain-specific fields. Don't change the core fields.
- **Different decision authority**: if your domain has decision-makers other than "consensus / round-lead / adversary", extend the `made_by` enum.
- **Multi-stakeholder verifications**: if multiple parties verify (e.g., red team + compliance + customer support), add a `verifier` field to verifications.

The principle (claims-with-status, verifications-with-evidence, decisions-with-citations) generalizes; the specific fields are domain-tuned.
