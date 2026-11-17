# Debugging Checklist (closed-loop thinking mode)

This checklist is a **prompt scaffold for the LLM's internal loop** during debugging.
Work top to bottom; do not skip steps. If you find yourself on step 4 without a clear x
and u, return to step 1.

## 1. Identify (state, possibility space, control)
- [ ] **Controlled variable x**: what must stay correct? Name it concretely, with a target/units.
- [ ] **Possibility space**: what set of states could the system be in? Enumerate at least 2
      candidates. Your fix must narrow this set.
- [ ] **Control variable u**: what lever will I actually change? (Not "rewrite"; the smallest
      editable thing.)
- [ ] **Observability**: do I have a sensor (log/test/metric) that reveals x? If not → add it
      first. If you cannot observe it, you cannot control it.
- [ ] **Bounds**: what are the limits on u and x? Size, rate, time, memory, retries, context.

## 2. Analyze (current behavior, model as hypothesis)
- [ ] Reproduced the fault deterministically? (Not "sometimes".)
- [ ] Measured the deviation ε = x* − x? Stated the mental model of the plant, **treated as a
      black-box hypothesis**, and where it breaks.
- [ ] Stated a falsifiable prediction: what observation would prove the hypothesis wrong?
- [ ] Located the fault to a subsystem (not guessed).
- [ ] If the fix didn't converge after attempts: is the missing piece a sensor (information
      channel) rather than a bigger actuator?

## 3. Stabilize (before any feature)
- [ ] Tested with perturbations: empty / huge / null / concurrent / dependency-down / load spike.
- [ ] No unbounded growth, oscillation, or limit cycle?
- [ ] If unstable → fixed stability before adding anything.
- [ ] Distinguished an unstable trajectory (case 2) from a system sitting in an unwanted
      stable-state structure (case 3). The fixes differ.
- [ ] If the instability is a repair mechanism (cache eviction, GC, circuit breaker), did not
      patch over it.

## 4. Synthesize (minimal control action)
- [ ] Change is the smallest u that moves x to target. No speculative extras.
- [ ] If the problem is uncontrollable in its current form, transformed it (L → A → L⁻¹
      conjugate control) rather than brute-forcing.
- [ ] Decoupled harmful coupling; kept beneficial coupling (coordination, not over-decoupling).

## 5. Close the loop (observe & correct)
- [ ] Ran the actual code; read the actual sensor output — did NOT assume u worked.
- [ ] Verified the falsifiable prediction: did the predicted observation occur? If not, the
      hypothesis was wrong — update the model, don't force the fix.
- [ ] Corrections are getting smaller, not larger. Direction is not reversing each iteration.
- [ ] Reached target within stated bounds.
- [ ] Feedback rate exceeded plant dynamics (no stale observations on a fast-moving bug).

## 6. Compensate & clamp
- [ ] Measurable disturbances handled by feedforward where possible; feedback the rest.
- [ ] Control magnitude clamped (max retries/depth/rate). Graceful degradation at the bound.
- [ ] For positive-feedback loops (retries, cache misses, autoscaling): tested near the
      critical threshold, not just at typical load.

## 7. Optimize (last)
- [ ] Only now tuning speed/cost/elegance. Stability and correctness already proven.

---
Anti-patterns (stop if you catch yourself):
- Adding retries without a bound → retry storm (unstable delay loop)
- Cranking gain on a delayed system → oscillation
- Optimizing before stabilizing → divergence on perturbation
- Guessing cause without reproduction → open-loop patch
- Removing a repair mechanism because it looked unstable → brittle system
- Reversing direction each iteration (overshoot) instead of reducing gain → oscillation
- Adding force to an actuator that lacks feedback → open-loop divergence
- Treating "tests pass" as proof of truth when the test doesn't observe the causal variable
