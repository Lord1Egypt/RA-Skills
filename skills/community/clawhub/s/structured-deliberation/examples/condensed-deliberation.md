# Example: 5-round condensed deliberation on architecture comparison

This example shows a compressed (5-round) version of the structured deliberation framework applied to a fictional architecture comparison. Real runs typically use 13 rounds; this is a teaching version showing the rhythm and the kinds of artifacts/verifications/decisions produced.

## Setup

**System**: 3 candidate architectures (Architecture A: monolithic agent + RPC; Architecture B: event-driven multi-agent with bus; Architecture C: orchestrator + worker pools)

**Question**: Which architecture is most robust under load + adversarial conditions?

**Round budget**: 5 (compressed for example purposes)

**Roles instantiated**:

- Action: senior backend engineer (behavioral traces under load)
- Guardian: SRE lead (uptime / observability / data integrity invariants)
- Observer: customer support lead (debugging-as-on-call walkthroughs)
- Critic: security engineer (adversarial attack hypotheses)

**Stress test schedule** (compressed):
- R3: STRESS-CRITIC

---

## Round 1 — A. Lead Assignment

**Lead**: Action

**Rationale**: opening round, ground in concrete behavior before opinions form.

## R1 Phase B-C: Lead proposal + supplements

Action proposes: "Let me trace each architecture under a 10x load spike scenario." Behavioral traces produced for all 3.

Supplements:

- Guardian: "I see all 3 traces, but only B includes a backpressure step explicitly. Want to formalize: 'no architecture should accept requests it cannot bound' as the invariant."
- Observer: "From the on-call perspective, A's RPC failure mode is opaque — debugger has to guess which leg of the call failed. B has explicit message IDs. C has orchestrator telemetry."
- Critic: "Trace 3 (Architecture C) has a single point of failure at the orchestrator. Going to attack that next round."

## R1 Phase D — Artifacts produced

`artifacts/round_01/`:

- `action.md` — Behavioral Trace Set: 3 traces of 10x load spike across A/B/C
- `guardian.md` — Identity Invariant Check: "System must reject requests it cannot bound, with explicit error rather than silent retry"
- `observer.md` — Operator Walkthrough: on-call engineer debugging a partial outage in each architecture
- `critic.md` — Adversarial Test Case: target = Architecture A's monolithic agent failure mode

## R1 Phase E — Verifications

| Check | Result | Notes |
|---|---|---|
| 1. Critic attack vs Action trace | UNCLEAR | Attack on A's monolith partially reproduces in trace; some preconditions don't apply at 10x load |
| 2. Guardian invariant vs Observer walkthrough | ROBUST | Operator's debugging path doesn't violate the invariant; consistent across A/B/C |
| 3. Observer friction vs Critic attack | BROKEN | Both surface at "opaque RPC failure" — A/RPC failure is both an operator confusion point AND an adversarial attack vector |
| 4. All vs prior decisions | NOT_APPLICABLE | R1 |

3 verifications written to `state/verifications.jsonl` (Check 4 skipped).

## R1 Phase F — Claims raised

- C-1-1 (action): "Architecture B's backpressure handling tolerates 10x load spikes without dropping requests" — testable_as: synthetic 10x load test, measure dropped-request rate < 0.1%
- C-1-2 (guardian): "Invariant 'reject what cannot be bounded' is preserved by all 3 architectures under load" — testable_as: chaos-test each, verify no silent drops
- C-1-3 (critic): "Architecture A's monolithic agent has 3 single-point failure modes" — testable_as: fault injection at each, count system-wide outage incidents

All status: pending.

## R1 Phase G — Decisions

D-1-1: "Continue with all 3 architectures into R2; no early elimination based on R1 alone." Cites: C-1-2 (all 3 preserved invariant under R1's 10x load test).

---

## Round 2 — Lead: Guardian

Guardian's lead proposal focuses on R1's invariant (`reject what cannot be bounded`). Tests it across each architecture under harder conditions: cascading failure scenarios.

R2 Phase E results:

| Check | Result |
|---|---|
| 1. Critic attack vs Action trace | BROKEN | Critic's cascading failure attack on Architecture A reproduces in Action's trace 3 (10x load → backend dependency timeout → cascade) |
| 2. Guardian invariant vs Observer walkthrough | BROKEN | Operator's debugging path on A reveals the invariant fails: A retries silently when downstream times out |
| 3. Observer friction vs Critic attack | BROKEN | Same surface as R1: A's RPC opacity is both attack vector and friction point |
| 4. All vs prior decisions | ROBUST | All 4 artifacts cite R1 decisions |

Status changes:

- C-1-1 (B's backpressure): pending → tested_confirmed (B's backpressure held under cascading failure)
- C-1-2 (all 3 preserve invariant): pending → partially_refuted (A failed silent-retry test)
- C-1-3 (A has 3 SPOFs): pending → tested_confirmed (cascading failure reproduces)

Decision D-2-1: "Architecture A is excluded from further consideration. Continue with B and C." Cites: C-1-2 (partially refuted on A), C-1-3 (confirmed).

---

## Round 3 — STRESS-CRITIC

**Stress test**: Critic absent. Test whether other roles produce adversarial work.

R3 Phase D — only 3 artifacts (Action / Guardian / Observer); `artifacts/round_03/critic.md` does NOT exist.

What happens without Critic:

- Action's traces continue to be production-typical, no edge-case stress
- Guardian's invariant work proceeds, but doesn't have an adversarial counterpart
- Observer's walkthrough surfaces operator friction at known weak points, but no novel attack vectors
- **No new BROKEN verdicts produced** in R3 (verifications all ROBUST or NOT_APPLICABLE for Critic-dependent checks)

R3 Phase E results:

| Check | Result |
|---|---|
| 1. Critic attack vs Action trace | NOT_APPLICABLE | Critic absent |
| 2. Guardian invariant vs Observer walkthrough | ROBUST | Operator path on B and C respects bounded-rejection invariant |
| 3. Observer friction vs Critic attack | NOT_APPLICABLE | Critic absent |
| 4. All vs prior decisions | ROBUST | All 3 artifacts cite R2 decisions |

**C2 stress signature**: clear. Without Critic:

- Adversarial pressure drops to zero (matches prediction for Critic absence)
- Cascading failure scenarios disappear from this round (only Action sometimes covers, but at 60-70% saturation level)
- Decision D-3-1 reflects this: "Continue with B and C. No new disqualifications. R3 confirmed Critic role is load-bearing — without adversarial pressure, no new failure modes surfaced."

---

## Round 4 — Lead: Observer

Observer's lead: "Operator-walkthrough comparison of B and C under chaos conditions." Recruits operator persona "Sam, on-call SRE, 3 years tenure". Walks Sam through a partial outage in each.

R4 verifications surface a new finding:

- C-4-1 (observer): "Architecture C's orchestrator centralizes operator visibility — Sam can debug 4x faster than in B" — testable_as: time-to-diagnosis benchmark, n=3 operators per arch
- C-4-2 (critic): "But that same orchestrator is a ransomware target — adversary that compromises it gets full system view" — testable_as: red team simulation against orchestrator

Decision D-4-1: "B is the operator-readability winner; C is the operator-visibility winner. They optimize different things." Cites: C-4-1 confirmed, C-4-2 pending (deferred to R5).

---

## Round 5 — Synthesis

**Lead**: Critic (final adversarial pressure round before close)

Critic's lead: "Final attack: ransomware compromise of C's orchestrator. What's recovery time?"

Phase D-E surfaces:

- C-4-2 status: pending → tested_confirmed (red team sim against orchestrator showed 6-hour full-system compromise window)
- New decision D-5-1: "Architecture B is the recommended choice. C's orchestrator concentration is a liability outweighing its observability benefit. Cites: C-4-2 confirmed, prior tradeoff in D-4-1."

Phase G synthesis:

| Architecture | Group A (Grounding) | Group B (Process) | Group C (Architecture) | Recommendation |
|---|---|---|---|---|
| A | 0.42 (excluded R2) | 0.30 | 0.50 | Excluded |
| B | 0.85 | 0.75 | 0.80 | **Recommended** |
| C | 0.78 | 0.70 | 0.65 (orchestrator SPOF) | Strong runner-up |

Stop signal evaluation at end of R5:

- Signal 1 (claim refutation rate): satisfied (declining transitions)
- Signal 2 (disagreement slope): +0.18, satisfied
- Signal 3 (all agents led): 4/4, satisfied
- Signal 4 (stress tests done): 1/4 → NOT satisfied (only Critic stress, missing Guardian/Action/Observer stress)
- Signal 5 (drift checks pass): 0 drift checks ran (compressed example), unable to evaluate
- Signal 6 (pending fraction < 30%): all claims tested, satisfied

4/6 satisfied. Verdict: STOP after one synthesis round.

In a real 13-round run, R10 / R12 / R13 would have stress-tested the other 3 roles, satisfying Signal 4. The compressed 5-round version demonstrates the rhythm but cannot fully satisfy stress-test coverage.

---

## What this example shows

1. **Cross-validation surfaces real findings**: Architecture A excluded by R2 because Critic + Action + Guardian + Observer all converged on the same weakness (silent retry on RPC failure). No single role would have caught it alone.
2. **Stress tests reveal structure**: R3 STRESS-CRITIC produced *no new failure modes* — confirming the Critic role is load-bearing, not decorative.
3. **Tradeoffs are made explicit**: B vs C in R4 isn't "B is better"; it's "B optimizes for operator readability, C for operator visibility — different things." The framework forces this distinction.
4. **Decisions cite evidence**: every decision in D-1 through D-5-1 has explicit citations to claims and verifications. Without claim-citing, "B is the recommended choice" is an opinion; with citations, it's a traceable conclusion.

In a real 13-round version, you'd have ~50-70 claims, ~36-50 verifications, ~20-30 decisions, and full stress-test coverage — producing an audit trail that survives 6 months later when someone asks "wait, why did we pick B?".
