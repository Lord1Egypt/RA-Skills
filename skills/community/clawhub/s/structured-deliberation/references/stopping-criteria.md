# Stopping Criteria — When the Deliberation Should End

Multi-round deliberation without explicit stopping criteria has two common failure modes: it stops too early (premature consensus) or runs forever (artifact accumulation without convergence). This document defines 6 goal-driven stopping signals.

The deliberation should consider stopping when **≥4 of the 6 criteria are satisfied**. Fewer than 4 means the system is not yet in a stable state, even if individual signals are positive.

---

## Signal 1 — Claim refutation rate stabilizes

**What to measure**: Per-round count of claims with status transitions (`pending → tested_*`). Track 3-round rolling average.

**Stop signal**: rolling average drops below 50% of mid-experiment peak AND remains stable for ≥2 consecutive rounds.

**Why**: claims that aren't being refuted/confirmed have stopped accumulating evidence. Either the claim space is exhausted (good) or the cross-validation is going through motions (bad — cross-check with Signal 5).

**Example**:
- R5-R7 rolling avg: 4.2 status transitions/round
- R8-R10 rolling avg: 3.8/round
- R11-R13 rolling avg: 1.7/round (~40% of peak) → Signal 1 satisfied at R13.

---

## Signal 2 — Disagreement slope flat or rising

**What to measure**: Per-round disagreement count (verifications with result ∈ {BROKEN, UNCLEAR}) regressed over rounds.

**Stop signal**: slope ≥ 0 across the *entire* experiment AND last 3 rounds maintain the trend (no late-phase collapse).

**Why**: a healthy multi-agent system should *not* see disagreement decline over rounds. Sycophancy cascades show declining disagreement; healthy convergence shows stable or rising disagreement (the harder questions emerge as easier ones resolve).

If disagreement slope is negative but B2 (failure mode discovery) also dropped, that's *legitimate convergence* (the easy issues resolved, the hard ones remain). If disagreement slope is negative but B2 is flat, that's *sycophancy*.

**Example**:
- Disagreement count: R1=3, R5=4, R10=5, R13=5 — slope +0.18 (positive) → Signal 2 satisfied.
- Disagreement count: R1=4, R5=5, R10=2, R13=1 — slope -0.30 (negative) AND B2 also dropped → likely sycophancy, do NOT stop, escalate Critic pressure instead.

---

## Signal 3 — All agents have led at least one round

**What to measure**: `lead_history.jsonl` count per agent (excluding system / stress rounds).

**Stop signal**: Shannon entropy of lead distribution ≥ 0.7 × log2(N_agents). All agents have led at least 1 non-stress round.

**Why**: if an agent never leads, their perspective hasn't been tested as the round-shaping voice. Stopping before all agents have led under-uses the structural diversity.

**Note**: adversarial agents (Critic) may legitimately lead less often than non-adversarial agents (their contribution is via tensions/claims, not lead-shaping). Use `C1_note` from MADEF to determine whether under-lead is structural.

---

## Signal 4 — Stress tests have been executed

**What to measure**: Number of agents that have been stress-tested (forcibly absent for ≥1 round).

**Stop signal**: At least N-1 agents stress-tested OR the *most consequential* agent stress-tested.

**Why**: stress tests reveal whether each agent's role is load-bearing. Without them, you don't know if an agent's apparent contribution is structural or decorative. Stress-test signature clarity (C2 in MADEF) is one of the most important quality signals.

**Recommended order**: stress-test the adversarial agent first (typically Critic) — its absence has the strongest signal; then stress-test agents whose roles you're uncertain about.

---

## Signal 5 — Drift checks pass

**What to measure**: Drift check verdicts (PASS / FAIL) at each K-round interval (typically every 5 rounds).

**Stop signal**: All drift checks PASS, OR the most recent drift check PASS and the prior FAIL has been explicitly addressed (drift was identified and corrected).

**Why**: drift checks verify the deliberation hasn't quietly wandered from its anchoring. A failed drift check that's never re-checked is a worse signal than no drift checks.

---

## Signal 6 — Claim status distribution: pending fraction < 30%

**What to measure**: Of all claims raised across the experiment, what fraction is still in `pending` status (never tested).

**Stop signal**: pending fraction < 30%.

**Why**: claims that never get tested are dead weight. They were proposed, but no verification ever attempted to confirm or refute them. If 30%+ of claims are pending, either:

- The cross-validation is too sparse → run more verification rounds
- The claims are being raised but not tied to testable outcomes → tighten claim-raising schema (require `testable_as` field)

---

## Composite stop signal

Don't stop on any single signal. Stop when **≥4 of the 6 are satisfied**.

| Combination | Interpretation |
|---|---|
| 6/6 | Strong stop signal; deliberation has run its course |
| 5/6 | Stop after one more "wrap-up" round (synthesize, no new claims) |
| 4/6 | Borderline; check which signals are unsatisfied — if Signal 4 (stress tests), run them and re-evaluate |
| ≤3/6 | Don't stop. Identify the unsatisfied signals and address them |

---

## Anti-patterns

### Stopping early on consensus

If all 4 verifications come back ROBUST in a single round, that's *not* a stop signal — that's a sycophancy candidate. Real convergence shows ROBUST verdicts gradually displacing UNCLEAR/BROKEN over many rounds, not a sudden all-ROBUST round.

### Running past the budget

If the budget is 10 rounds and you've hit 8 with only 3/6 signals satisfied, the deliberation is not converging. Don't run rounds 9-15 hoping it will. Either:

- Adjust scope (the question may be too broad)
- Restructure (a key role may be under-active)
- Accept the non-convergence and document why in RETROSPECTIVE

A non-converging deliberation is a finding, not a failure. Document and learn.

### Ignoring stress tests

Skipping stress tests "to save rounds" is the most common shortcut. Without stress tests, you don't have C2 (signature clarity), which means you can't verify that any agent's role was load-bearing. The deliberation may be 4-agent in name and 1-agent in effect, and you have no way to tell.

---

## Recommended round budget

Based on calibration across deliberation experiments:

- **Minimum viable**: 8 rounds (5 normal + 2 stress tests + 1 synthesis)
- **Standard**: 13 rounds (10 normal with drift checks at R5/R10 + 2 stress tests + 1 synthesis)
- **Extended**: 16-20 rounds for high-stakes decisions or larger agent populations

The 13-round standard is what calibration of 4-agent deliberation showed produces full coverage on all 6 stop signals if the system is healthy. Shorter runs frequently leave Signal 4 (stress) or Signal 6 (pending fraction) unsatisfied.

---

## Operationalizing the stop check

A simple stopping detector reads state files and returns the satisfied signals:

```python
def evaluate_stop_signals(state_dir, n_agents):
    signals = {}
    signals['claim_refutation_stable'] = check_signal_1(state_dir)
    signals['disagreement_slope_ok'] = check_signal_2(state_dir)
    signals['all_agents_led'] = check_signal_3(state_dir, n_agents)
    signals['stress_tests_done'] = check_signal_4(state_dir, n_agents)
    signals['drift_checks_pass'] = check_signal_5(state_dir)
    signals['pending_fraction_ok'] = check_signal_6(state_dir)
    
    satisfied = sum(1 for v in signals.values() if v)
    should_stop = satisfied >= 4
    return signals, satisfied, should_stop
```

See `scripts/stopping-detector.py` for reference implementation.
