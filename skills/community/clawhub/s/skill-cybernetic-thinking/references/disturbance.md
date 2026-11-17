# Reference: Disturbance Compensation & Time-Delay

Book anchors: §6.7 (third method: disturbance compensation / invariance), §11 (systems with
time lag / delay).

## Two ways to reject a disturbance

Outside forces push your system off-target: flaky networks, load spikes, other teams'
services, GC pauses, clock drift.

1. **Feedback (reactive).** Observe the deviation `ε = x* − x` and correct. Robust, but *lags*
   — by the time you measure and act, the disturbance has already moved you.
2. **Feedforward / disturbance compensation (proactive, §6.7).** If the disturbance is
   *measurable*, compensate for it directly so the **relationship** stays invariant. Combine
   both → *composite control*: accuracy from feedforward, stability from feedback.

## LLM behavior pattern: Feedforward when measurable, never crank gain on delay

> "For measurable disturbances, compensate proactively. For delayed loops, add damping, not gain. Never crank gain on a delayed loop — it drives the system unstable."

The LLM must explicitly evaluate whether disturbances are measurable and whether the feedback
loop involves delay. If it proposes increasing retries/logic frequency without addressing the
delay, it is an unstable control action.

- Apply invariance to the **coordination relation**, not just one variable (§6.7): compensate
  so the *relation* holds under the measurable kick.
- For *unmeasurable* disturbances, you can only fall back to feedback — so maximize
  observability of likely kicks.

## Time-delay systems (§11)

Many software loops have intrinsic delay: network round-trips, async pipelines, batch jobs,
human-in-the-loop. Delay is the enemy of stability.

- Expect **reduced stability margin** and **oscillation** when loop delay is large relative to
  the dynamics (§11: delay systems need special stability criteria).
- **Do not crank up gain** to compensate for a slow/delayed loop — that pushes it unstable
  (cf. §4/§5 phase margin). Instead:
  - reduce effective loop gain or add damping;
  - shorten the loop (tighter sampling, §10);
  - predict/delay-compensate if the delay is known and measurable.
- Watch for limit cycles that appear *only* because of the delay (e.g. a retry that fires
  exactly when the late response arrives).

## Worked example: flaky dependency → feedforward + feedback

**Before (feedback only):**
```python
def call_external():
    for attempt in range(5):
        try:
            return requests.get(EXTERNAL_URL, timeout=2)
        except Exception:
            time.sleep(1)     # fixed backoff — no knowledge of cause
```
If the dependency is down for 30 seconds, every call burns 5×2 seconds and still fails.
The disturbance (dependency outage) is *measurable* — we have a health endpoint — but we
do not use it. Pure feedback on a delayed, unmeasured disturbance: unstable under load.

**After (composite control):**
```python
_healthy = None

def call_external():
    global _healthy
    if _healthy is False:
        raise CircuitBreakerOpen()    # feedforward: fail fast on known outage
    try:
        resp = requests.get(EXTERNAL_URL, timeout=2)
        _healthy = True
        return resp
    except Exception:
        _healthy = False
        time.sleep(2 ** attempt + random.uniform(0, 0.1))
        raise
```

- Feedforward: health check measured at startup and on every failure; known outage → open
  loop immediately (invariance from the disturbance).
- Feedback: backoff on transient errors still corrects the trajectory.
- Composite control: accuracy from invariant relation, stability from feedback.

---

## Retry storms are unstable delay loops

A retry-without-backoff is a high-gain, zero-damping controller on a delayed plant →
oscillation that grows. Fix: bounded retries + backoff (damping) + jitter (break sync) +
circuit breaker (open the loop before it diverges).

## LLM anti-pattern detection

When a system has a delay, the LLM must not propose:
- More retries (increasing gain)
- Shorter timeouts without backoff (reducing delay margin)
- Any change that amplifies the loop before reducing the delay or adding damping

These are textbook unstable trajectories. The skill must prevent them.
