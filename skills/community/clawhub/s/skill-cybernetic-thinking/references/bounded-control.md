# Reference: Time-Optimal & Bounded Control

Book anchors: §8 (time-optimal / bang-bang control), §9.6 (optimal control under control
constraints).

## Control effort is bounded — always

Real actuators saturate: a thruster cannot exceed max thrust, a valve cannot open past
fully-open. Software analogues are everywhere and just as hard:

- retry budget, recursion depth, loop iterations, allocation size, request rate, context
  window, transaction timeout.

Linear theory ignores these bounds and is wrong at the edge (§1.5). **Unbounded control →
actuator saturation → instability** (e.g. retry storm, stack overflow, OOM, rate-limit ban).

## LLM behavior pattern: Clamp every actuator

> "Every loop must have an explicit bound. No unbounded retry, recursion, or allocation."

The LLM must proactively identify actuators in its proposed changes and clamp them:
- Retry: max attempts, backoff, jitter, circuit breaker
- Recursion: depth limit
- Loop: iteration cap or progress guarantee
- Allocation: size cap
- Rate: throughput limit with graceful degradation at saturation

## Bang-bang where appropriate (§8)

To reach a target *fastest* under a bound, the optimal law is often **bang-bang**: drive the
actuator to its limit in the right direction, then switch. Translated to code:

- Make **decisive, maximal, well-scoped** changes to kill a fault — don't nibble at it with
  timid partial fixes that leave the system near the unstable region.
- Switch decisively when the sign of the error flips (e.g. change strategy, not just magnitude).

But note (§9.6): bang-bang is optimal for *time*; for *energy/integral cost* (§9) a softer
law is better. Pick the criterion to the goal.

## Clamp the actuator

- Bound every control loop: max retries, max recursion, max batch, max rate. Saturation
  without a clamp is how a bounded disturbance becomes a runaway.
- When you hit the bound, *degrade gracefully* (drop to a safe mode, shed load, return a
  partial result) rather than oscillating at the limit.

## Optimize the integral, not just the endpoint (§9)

Often you minimize a **cumulative cost** — total latency, total tokens spent, total energy,
total user-visible glitches — not just final state. Choose the change that minimizes the
integral of cost over the whole trajectory, not the one that looks tidiest at the endpoint.

## Generality notes

These ideas apply identically whether the "plant" is a web service, a data pipeline, a
compiler pass, or an LLM agent loop: every one has bounded actuators and a cost to minimize
over time. The physical vocabulary (thrust, valve) is illustrative only — the invariant is
*bounded, goal-directed control*.

## Worked example: uncontrolled recursion → stack overflow

**Before (no bound on actuator):**
```python
def walk(node):
    for child in node.children:
        walk(child)         # actuator: recursion depth — unbounded!
```
Circular reference in `node.children` → unbounded recursion → `RecursionError` /
stack overflow. The actuator (call stack) has a hard saturation, but the code ignores it.

**After (clamped actuator):**
```python
def walk(node, _depth=0, max_depth=100):
    if _depth >= max_depth:
        raise ValueError(f"Actuator saturated: depth {_depth} >= {max_depth}")
    for child in node.children:
        walk(child, _depth + 1, max_depth)
```
- Bound: `max_depth=100` (explicit actuator clamp).
- Graceful degradation: exception at bound instead of silent crash.
- Cost: O(n) with bounded cost per call; integral cost stays predictable.

