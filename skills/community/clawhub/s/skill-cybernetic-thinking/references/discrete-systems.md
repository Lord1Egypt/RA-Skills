# Reference: Discrete / Sampled Systems & Test Cadence

Book anchor: §10 (discrete control systems — difference equations, sampled data).

## Software runs in discrete steps

Continuous control theory assumes you can act and observe at every instant. Software acts and
observes only at **sample instants**: function calls, test runs, deploys, metric scrapes,
human reviews. Between samples the state is *unobserved*.

Consequences:
- **Sample often enough.** A feedback loop sampled too coarsely (tests only at the end,
  manual checks weeks apart) cannot stabilize a fast-moving fault. Tighten the loop:
  unit → integration → typecheck → run, frequently and automatically.
- **Guard the gap.** Between samples, anything can happen: timeout, partial write, concurrent
  mutation, crash. Design for the unobserved interval — idempotency, transactions, rollback,
  heartbeat/lease.
- **Aliasing instability.** A bug that appears only at certain intervals or scales is a
  *sampled-system alias* — the true dynamics are faster than your sampling. Vary the
  sample/scale when testing (small vs large input, fast vs slow clock).

## LLM behavior pattern: Treat cadence as a controlled variable

> "Your feedback cadence is a design variable. Tighten it when you need stability; loosen it only when the system is already robust."

The LLM should recognize that its own test/review cadence is a *sampling rate* that affects
stability margin. It should not propose changes that rely on coarse-grained verification for
systems with fast dynamics.

- Tight cadence (fast tests, CI on every commit) → can use higher gain (more aggressive
  fixes) and still stay stable.
- Loose cadence (nightly, manual) → must use lower gain (conservative, well-reviewed changes)
  or it will overshoot.

## Discrete instability signatures (§10)

- **Limit cycle at the sample period**: a fault that recurs every N runs because the
  correction and the next sample line up badly.
- **Chattering**: a value flips every sample between two states (Zeno-like behavior in
  continuous terms) — add hysteresis / deadband so small errors don't trigger action.
- **Deadbeat vs sluggish**: too much gain overshoots and oscillates; too little never
  converges. Tune the *discrete* gain (e.g. test frequency, retry backoff curve).

## Anti-pattern: Coarse sampling masks instability

> "A system that passes only when tested weekly may be oscillating daily. The LLM must probe at multiple scales before declaring stability."

The LLM must vary test scale and frequency when assessing stability. A single golden-path
test at low frequency is not observability; it is a sample that may miss the true dynamics.

## Worked example: weekly test passes, daily test reveals oscillation

**Symptom:** a data pipeline passes end-to-end test when run manually, but downstream teams
report stale data every morning.

```python
# pipeline runs once a day; test runs manually on demand
def run_pipeline():
    ...
```
- Sampling rate: 1× per day (coarse)
- True dynamics: cache TTL = 1 hour; data freshness degrades within hours → oscillation
  between "fresh" and "stale" every hour
- Weekly manual test catches only one sample point — coincidentally fresh — masking the
  daily limit cycle

**Fix (tighten the loop):**
```python
# Hourly CI job + explicit freshness assertion
def run_pipeline():
    ...
    assert freshness_hours() < 2, f"Data stale: {freshness_hours()}h"

# Hourly cron in CI; alert on assertion failure
```
- Sample rate increased from daily to hourly.
- True limit cycle (1-hour) now falls within the sampling window and is detectable.
- Observability: assertion converts invisible state (freshness) into a measurable signal.

