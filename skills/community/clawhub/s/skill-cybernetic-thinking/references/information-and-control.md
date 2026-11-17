# Reference: Information and Control — The Mutual Dependence

Book anchor: 金观涛《控制论与科学方法论》第二章 §2.1–§2.4 (信息、思维和组织).

## Information is narrowing of the possibility space

(§2.1) Information is not a thing and not a substance; it is a *change in the shape of a
possibility space*. To receive information is to have your uncertainty about a thing reduced.

- Before: "the user's id could be any of 1000 values" — uncertainty = 1000.
- After: "the user's id is in the first 100" — uncertainty = 100, information gained =
  log₂(1000/100) ≈ 3.3 bits.

This is consistent with `references/possibility-space.md`: control narrows the possibility
space of the *plant*, and information narrows the possibility space in the *controller's model
of the plant*. They are two directions of the same arrow.

The book's hard claim (§2.4):

> **Control requires information, and information requires control.** You cannot control what
> you cannot observe; you cannot gain information without acting on the world. The two are
> coupled through a feedback loop.

## Why "just add more control" fails when information is missing

(§2.4) A controller that cannot observe the variable it needs to control will not converge, no
matter how aggressive its actuator is. The book's example: trying to control the position of
your own intestines by thought alone — there is no information channel from the intestines to
consciousness, so voluntary control fails. Biofeedback works *only* by first building a new
information channel (a screen showing heart rate or skin temperature), at which point the
existing actuator (breathing, relaxation) becomes effective.

The pattern: **the missing piece is the sensor, not the actuator.** Adding more force to an
actuator that lacks feedback is open-loop control — it diverges.

## LLM behavior pattern: When control fails, suspect a missing information channel

> "If you cannot steer a variable, your first instinct should be 'I am missing a sensor', not
> 'I need a bigger lever'. Adding force without feedback is open-loop control."

This is the deep form of the observability law in `references/state-and-control.md`. The
shallow form says "add a test before you fix". The deep form says: **if the variable you need
to steer is not observable, no amount of fixing will converge — you must build a new
information channel first, then the existing fix becomes effective.**

Concrete symptoms that you're missing a channel, not missing force:
- You've tried several fixes, each "felt right", none converged, and you cannot tell which one
  was closest. → You have no observable for the variable you're trying to steer.
- The bug "goes away" when you add logging, then "comes back" when you remove it. → The
  logging *was* the fix; it gave you the channel. The real bug is still there.
- Reproduction is intermittent and you cannot correlate occurrences with any input. → You're
  observing the wrong variables; the causal variable is in your blind spot.
- Your mental model fits every observation equally well (and there are many). → Your
  observations carry no information about which model is correct; you need a *different*
  observable, not more of the same one.

## Information channels are the unit of observability

(§2.2) Information flow has three parts: a source, a channel, and a receiver. The channel is
*lossy and bounded* — it has a capacity (Shannon), and signals below the noise floor are
irrecoverable.

- Source: the actual state of the plant (memory layout, thread interleaving, queue depth,
  network conditions).
- Channel: logs, metrics, tests, traces, assertions, exceptions, return codes.
- Receiver: the LLM (or the developer) reading the channel output.

If the source produces information at a rate the channel cannot carry, the receiver's model
will lag the plant. This is the same condition as §5.5 (convergence speed vs. plant dynamics,
in `references/black-box-epistemology.md`): the channel capacity must exceed the plant's
information production rate, or the model falls behind.

## LLM behavior pattern: Match channel capacity to plant dynamics

> "Your test/log/metric cadence is an information channel with a capacity. If the plant's
> dynamics exceed that capacity, your model is always stale and you will oscillate. Tighten
> the channel before tightening the fix."

- A daily test suite is a low-capacity channel. It cannot carry information about
  sub-second dynamics. For a fast-moving bug, it is the wrong channel.
- A single log line per request is a low-capacity channel for a system that handles 100k QPS.
  You will miss the rare interleaving that triggers the bug.
- A single end-to-end test is a low-capacity channel for a system with many internal states.
  It tells you "something failed", not "which subsystem failed first".

Adding capacity means: finer-grained tests, structured logs with correlation IDs, metrics at
the subsystem boundary, traces that span the request, assertions in hot paths.

## When to add a channel vs. when to add an actuator

The book's asymmetry (§2.4) is the practical rule:

- **If the actuator is sufficient but the channel is missing**: adding more actuator
  (retries, force, code) will not help and usually harms. Add the channel.
- **If the channel is sufficient but the actuator is missing**: more observation will not
  help — you already know what's wrong, you just can't reach it. Add the actuator.
- **If both are missing**: add the channel *first*. An actuator without a channel is
  open-loop and may destabilize the system; a channel without an actuator at least tells you
  what's happening.

LLM failure mode: defaulting to "add an actuator" (write more code, add more retries, add
more validation) when the actual bottleneck is "I have no way to see the variable I'm trying
to fix". The result is a more complex system with the same unobservable bug.

## Worked example: the missing channel, not the missing retry

**Bug:** a queue worker occasionally processes the same job twice under load.

**Actuator-only attempts (wrong diagnosis):**
```python
# Attempt 1: add a lock
lock = threading.Lock()
def process(job):
    with lock:
        if already_processed(job.id):
            return
        do_work(job)
        mark_processed(job.id)
```
Still fails. Why? Because the lock is per-process, and there are 4 workers.

```python
# Attempt 2: add a database-level unique constraint
ALTER TABLE processed_jobs ADD UNIQUE (job_id);
```
Still fails intermittently with `IntegrityError` — and now the worker crashes on the duplicate.

**Channel-first diagnosis (right diagnosis):**
The variable you need to steer is "did another worker already pick up this job?". That
variable is not observable from inside a worker. Add the channel:

```python
# Channel: a visibility log that records who picked up what, when, on which worker
def pickup(job_id, worker_id):
    db.execute(
        "INSERT INTO job_pickups (job_id, worker_id, picked_at) VALUES (?, ?, ?)",
        (job_id, worker_id, time.time()))
    # This is the information channel, not the actuator

# Now observe: do two workers ever pick up the same job within 100 ms?
```
The log shows that the same job_id is picked up by two workers within 50 ms of each other,
because the visibility-timeout extension races with the consumer poll. *Now* the actuator is
obvious: extend the visibility timeout *before* the poll, not after. The fix is one line; but
it could not be found without the channel.

---

## Decision rule

- If a fix didn't converge, ask first: "Am I missing force, or missing information?"
- Default to adding a channel before adding an actuator.
- Match the channel's capacity to the plant's dynamics — a slow channel on a fast plant
  produces an oscillating model.
- The bug that "goes away when I add logging" is the bug that *needed* the logging. Don't
  remove the logging.
