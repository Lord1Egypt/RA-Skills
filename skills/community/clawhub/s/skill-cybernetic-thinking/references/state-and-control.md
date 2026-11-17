# Reference: State, Control, Observability & Bounds

Book anchor: §1.5 (controlled vs control quantities; constraints on both).

## Two kinds of variables

In every system you touch, separate:

- **Controlled variables x** — the things that must be correct: output values, internal
  state, invariants, latencies, error rates. You cannot set them directly; you can only
  *influence* them through the equations of motion.
- **Control variables u** — the levers you actually manipulate: function arguments, config
  values, the code you write, the inputs you feed. Only on u do you have freedom to act.

## LLM behavior pattern: Name x before u

> "Name the controlled variable x before proposing any change. Unnamed targets are unregulated."

An LLM using this skill **must** name the controlled variable and the control variable before
any proposal. This is not optional framing—it is the first cognitive law. If you cannot name
x, you cannot verify success; you are operating open-loop.

- "Make it work" is not a control problem; "reduce error rate below 1%" is.
- Before generating a patch, the LLM must internally resolve: what is x, what is u, and how
  will I measure x after u moves?

## LLM behavior pattern: Demand observability before acting

> "A failure mode you cannot observe will drift until it bites. Add the sensor first."

If the LLM identifies a plausible failure mode that is invisible to existing tests/logs, it
must **propose instrumentation before proposing the fix**. Acting without observability is
guessing; guessing is not control theory.

- If observability is impossible in the current environment, state that explicitly as a risk.
- Prefer mechanisms that *measure* outcomes over mechanisms that *assert* they happened.

## Bounds are physical, not optional (§1.5)

Linear regulation theory silently assumes variables are unbounded. Reality is not:

- Control quantities are bounded: thrust limits, voltage/power limits, **API rate limits**,
  **context-window size**, **stack depth**.
- Controlled quantities are bounded: integer ranges, buffer sizes, **memory**, **deadlines**.

Near a bound, linear intuition fails (saturation, overflow, OOM, token cutoff). Design for the
bound, not the asymptote. The book notes that ignoring limits makes "transition time
independent of step size" — which is simply false in practice. Same trap: assuming a function
behaves the same at n=10 and n=10^7.

## Observability vs controllability (§5.5)

- A state you can measure → you can close a loop on it (observable).
- A quantity you can change → you can steer it (controllable).
- Some states are neither easily measured nor directly changed — they must be *estimated*
  from observables. When debugging "impossible" faults, suspect a state that is observable
  only indirectly. Build the estimator (instrumentation) before concluding the bug is
  untraceable.

## When control fails, suspect a missing information channel (Book 2 §2.4)

Book 2 anchor: §2.4 (信息与控制的依存关系). See `references/information-and-control.md` for the
full treatment.

The shallow form of the observability law says "add a test before you fix". The deep form,
from Book 2, says: **control and information are mutually dependent. You cannot control what
you cannot observe, and adding force to an actuator that lacks feedback is open-loop
control — it diverges.**

The book's example: trying to control the position of your own intestines by thought alone
fails — not because the actuator (breathing, relaxation) is weak, but because there is no
information channel from the intestines to consciousness. Biofeedback works *only* by first
building a new channel (a screen showing heart rate), at which point the existing actuator
becomes effective.

Practical rule: if a fix didn't converge after several attempts, the missing piece is usually
a **sensor**, not a bigger lever. Default to adding an information channel before adding more
actuator. Symptoms:
- You've tried several fixes, none converged, and you can't tell which was closest.
- The bug "goes away" when you add logging, then "comes back" when you remove it (the logging
  *was* the fix — it gave you the channel).
- Reproduction is intermittent and you can't correlate occurrences with any input.

## Worked example: unregulated target → open-loop patch

**Before (no x, no u, no observability):**
```python
# "Make it better" — what is x? what is u? how will we know?
def process(data):
    return data  # placeholder; "fix" the symptom later
```
Without naming x and u, every subsequent change is a guess.

**After (closed-loop from the start):**
```python
def process(data, max_size=1000):
    # x = queue depth / error rate; u = max_size
    # observability: raise if exceeded, count in tests
    if len(data) > max_size:
        raise ValueError(f"x exceeded bound: {len(data)} > {max_size}")
    return data
```

- x = `len(data)` (controlled variable, must stay ≤ `max_size`)
- u = `max_size` (the lever we adjust)
- observability = exception raised, testable
- bound = `max_size` (actuator saturation respected)

