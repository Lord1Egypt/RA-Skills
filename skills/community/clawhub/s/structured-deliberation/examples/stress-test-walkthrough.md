# Example: Stress test patterns (R12 / R13)

This example shows what stress test rounds produce — what *signature* each absent agent leaves on the round when forcibly removed. The pattern is calibrated from prior multi-agent deliberation runs; if your stress tests produce similar signatures, your roles are load-bearing. If stress rounds look identical to normal rounds, the absent agent's role is decorative.

The two stress patterns shown here (STRESS-ACTION at R12 and STRESS-OBSERVER at R13) are the most diagnostic — they reveal whether implementation grounding and operator perspective are doing structural work.

---

## STRESS-ACTION at R12

**Setup**: Round 12 of a 13-round deliberation about agent architecture. Action is forcibly absent. Guardian, Observer, and Critic produce artifacts; Action does not.

### What signatures should appear (predicted before reading)

If Action's role is load-bearing:

1. **Cross-round reference traces completely absent.** Only Action produces these (it's the only role that grounds in state-transition sequences spanning multiple rounds). Without Action, the round has no "and here's how this connects to R7's primitive in concrete behavior" content.

2. **Happy-path concreteness drops.** Other roles describe behavior abstractly ("the system would handle X") rather than concretely ("at step 4, state.queue_depth=12, then trigger fires...").

3. **Edge case behavior is present but framed as adversarial concerns**, not as design output. Critic covers it (their attacks include edge cases by nature) but Critic's framing is "this could break", not Action's "here's the design that handles edge cases."

4. **Verifications Check 1 (Critic attack vs Action trace) returns NOT_APPLICABLE.**

### What actually appeared in the R12 round

- Guardian's artifact: invariant about state convergence, verdict CONDITIONAL_PASS on R11 architecture
- Observer's artifact: operator persona "Sam, SRE", walkthrough of debugging the architecture under partial outage
- Critic's artifact: adversarial test on Guardian's R11 invariant — attempted attack via state divergence
- (action.md absent)

Verifications produced (3 instead of 4):

| Check | Result | Notes |
|---|---|---|
| 1. Critic vs Action trace | NOT_APPLICABLE | Action absent |
| 2. Guardian vs Observer | ROBUST | Operator path respects invariant |
| 3. Observer friction vs Critic attack | UNCLEAR | Friction is at observability, attack is at state divergence — semantic similarity but not direct overlap |
| 4. All vs prior decisions | ROBUST (3 artifacts cited prior) |

**Substitution rate**: roughly 5-20% of Action's normal contribution was substituted by other roles. Cross-round trace work was *not* covered (Critic's attacks include sequences but not happy-path designs; Observer's walkthroughs cover operator paths but not architectural state transitions).

**Diagnostic verdict**: Action's role is load-bearing. The absence produces a clear signature (no cross-round traces, no happy-path concreteness, Check 1 NOT_APPLICABLE). C2 (stress signature clarity) score: 5/5.

---

## STRESS-OBSERVER at R13

**Setup**: Round 13. Observer absent. Action, Guardian, Critic produce artifacts.

### What signatures should appear (predicted)

If Observer's role is load-bearing:

1. **Operator-satisfaction verdict completely absent.** Only Observer produces this (Yes/No/Partially on goal achievement, time-to-output, peer-recommend).

2. **Operator-voice perspective absent.** Other roles can talk *about* operators but don't enact a specific persona's session step-by-step.

3. **Friction points only emerge as adversarial findings, not as proactive scans.** Critic covers what's hard *for adversaries*; Observer covers what's hard *for legitimate users*. Without Observer, the friction surface is smaller and skewed toward attack-relevant friction.

4. **Verifications Check 2 (Guardian vs Observer walkthrough) and Check 3 (Observer friction vs Critic attack) return NOT_APPLICABLE.**

### What actually appeared in the R13 round

- Action's artifact: 3 traces of architecture under regression load (no operator persona; pure system behavior)
- Guardian's artifact: invariant verdict on R12's stress findings
- Critic's artifact: attempted to cover operator-friction territory by including "operator-style errors" in attack preconditions, but framed as adversarial inputs not as legitimate user paths
- (observer.md absent)

Verifications produced (2 instead of 4):

| Check | Result | Notes |
|---|---|---|
| 1. Critic vs Action trace | ROBUST | Critic's attack on R12 architecture was absorbed by Action's trace 2 |
| 2. Guardian vs Observer | NOT_APPLICABLE | Observer absent |
| 3. Observer friction vs Critic attack | NOT_APPLICABLE | Observer absent |
| 4. All vs prior decisions | ROBUST | 3 artifacts cite R12 decisions |

**Substitution rate**: roughly 60-70% of Observer's contribution was substituted (Critic covered some friction territory; Action's traces sometimes implied operator paths). The remaining 30-40% was uniquely missing — most importantly, no creator-satisfaction verdict, no proactive friction scanning, no specific persona enactment.

**Diagnostic verdict**: Observer's role is load-bearing but partially substitutable. Some friction-detection work could be approximated by Critic (with framing adjustments) but the operator-perspective verdict is irreducible. C2 score: 4/5 (partial signature, not maximal).

---

## What stress tests reveal more broadly

Stress tests are the single most diagnostic measurement of multi-agent deliberation health. Specifically:

### Stress test produces no signature → role is decorative

If R12 (STRESS-ACTION) looked indistinguishable from a normal round (other roles seamlessly covered Action's work), then Action's role wasn't actually load-bearing. The "multi-agent" deliberation was effectively 3-agent in disguise.

### Stress test produces full signature → role is irreducible

If R12 produced clear absence signatures (no cross-round traces, no happy-path concreteness, Check 1 NOT_APPLICABLE) AND the other agents *could not* substitute the missing work, then Action is irreducibly load-bearing. The deliberation needs all 4 roles for full coverage.

### Stress test produces partial signature → role is partially substitutable

R13 (STRESS-OBSERVER) showed this pattern: ~60% substitutable by Critic with framing adjustments, ~40% uniquely missing. This means Observer's role is load-bearing for the unique 40% (operator-satisfaction verdict, persona enactment) but the remaining 60% could in principle be redistributed if needed.

### Stress test produces unexpected signature → process surprise

If the stress signature doesn't match prediction, that's a finding. For example: STRESS-CRITIC might be expected to drop adversarial pressure, but if Action steps up and produces edge-case-heavy traces, you've discovered that Action was already doing partial Critic work — your role boundaries aren't where you thought.

---

## Stress test scheduling

For a 13-round run, recommended schedule:

| Round | Stress | Why this round |
|---|---|---|
| R5 | STRESS-CRITIC | First stress should test the role most easy to lose (sycophancy if adversary is decorative) |
| R10 | STRESS-GUARDIAN | Mid-late, after invariants have been established |
| R12 | STRESS-ACTION | Late, after behavior patterns are established |
| R13 | STRESS-OBSERVER | Last, often combined with synthesis (since synthesis doesn't need new operator walkthroughs) |

This ordering reflects: most-diagnostic stress first (Critic), then progressively to roles whose absence is harder to detect.

---

## Pre-commitment requirement

Before reading a stress round's artifacts, **write down the predicted signature**. Then read. Match against prediction → score 5 only if match. Without pre-commitment, scoring is biased — you find what you expected.

This is C2's pre-commitment rule from MADEF (see [multi-dim-eval-framework/references/madef-axes.md](../../multi-dim-eval-framework/references/madef-axes.md) C2 section).

---

## What if stress tests are skipped

Don't skip them. If you must (e.g., hard time budget), document:

- Which roles weren't stress-tested
- Why (specific reason, not "we ran out of rounds")
- Caveat in retrospective: "C2 (stress signature clarity) score is partial — only X of N agents stress-tested"

A deliberation without stress tests can't be evaluated for load-bearing-ness. The 6 stop signals (see [references/stopping-criteria.md](../references/stopping-criteria.md)) include "≥N-1 agents stress-tested" as one of the 6 — skipping stress tests means at least one stop signal is unverifiable, lowering confidence in the convergence.
