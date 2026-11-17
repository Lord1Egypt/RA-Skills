# Reference: Black-Box Epistemology

Book anchor: 金观涛《控制论与科学方法论》第五章 §5.1–§5.8 (黑箱认识论).

## Every system you touch is a black box

(§5.1) For any object you study or change, the relationship between you and the object splits
into exactly two channels:

- **Observable variables** — what the object tells you (its outputs: logs, test results, metrics,
  behavior under input). You can read them; you cannot set them.
- **Controllable variables** — what you can do to the object (its inputs: code you write, config
  you set, requests you send). You can set them; you cannot guarantee their effect.

Everything else about the object — its internal structure, hidden state, uninstrumented
behavior — is **unknown**. That unknown is the *black box*. The name is honest: at any stage of
your knowledge, part of the object is not observable and not controllable by you.

A system and a black box are the same concept. There is no point at which the box becomes
transparent; opening one layer always reveals another black box behind it (§5.1: 摩尔根 opened
the heredity black box, only to find chromosomes as a new black box; chromosomes opened to DNA;
DNA opened to the genetic code; each layer spawned new questions).

## Two ways to know a black box (§5.1)

1. **Don't open the box.** Vary inputs, observe outputs, infer a model of the internal
   structure. Cheap, non-destructive, the only option for systems you cannot or should not
   dissect (living organisms, production traffic, large distributed systems).
2. **Open the box.** Add new observability or controllability — read the source, attach a
   debugger, add a metric, expose an internal state. This *changes* the system: variables that
   were unknown become observable or controllable, and a *new* black box forms at a deeper
   layer.

These are not competing methods; they alternate. You form a model by not opening (hypothesis),
then open a layer to test the model (experiment), which spawns a new model and a new box.

## LLM behavior pattern: Treat your model as a hypothesis, not as the system

> "The model you use to decide is not the plant that runs. The gap between them is where every
> bug lives. Open one layer at a time; recognize that a new black box appears behind the one
> you opened."

An LLM must distinguish three things, always:

1. The **plant** — the code as it actually executes, including state and timing you cannot see.
2. The **model** — the LLM's mental model of how the plant behaves. Stated explicitly, with a
   validity range (see `references/modeling.md`).
3. The **gap** — the difference between 1 and 2. Every bug that surprises you was hiding in this
   gap. A surprise is not bad luck; it is a measurement of how wrong your model was.

When a bug contradicts the model, **the model was wrong, not the bug**. Update the model before
touching code.

## The five failure modes of "practice → theory → practice" (§5.3–§5.7)

The book analyzes when iterating (run code, observe, update theory, repeat) fails to converge
to truth. Five failure modes — each maps to a documented LLM failure pattern.

### 1. Limits of observable and controllable variables (§5.3)

> No matter how many times you iterate, if the variables you can observe and control are bounded,
> you cannot converge to a model that uses variables outside that bound.

The book's example (§5.3): 范·赫耳蒙特 weighed a willow tree, soil, and water over 5 years,
concluded the tree's mass came from water. He was wrong (it came from CO₂ in air), but CO₂ was
not an observable variable for him. **No amount of repetition would have fixed this** — only a
new instrument (a way to observe CO₂ uptake) could.

LLM equivalent: a test suite that exercises only the happy path. Iterating against it cannot
reveal a concurrency bug, because concurrency is not an observable in that suite. The fix is not
more iteration; it is a **new information channel** (see `references/information-and-control.md`)
— add a concurrency test, a race detector, a log line at the critical section.

> "If iteration isn't converging, the problem is usually insufficient observability, not
> insufficient effort. Add a new variable before another iteration."

### 2. Lack of clarity / falsifiability (§5.4)

> A theory that does not narrow the possibility space cannot be tested. "Tomorrow it will rain
> or not rain" carries zero information and is unfalsifiable.

The book invokes Popper: a hypothesis is scientific only if some observation could prove it
wrong. A model that fits every observation explains none of them.

LLM equivalent: "this should fix it", "probably a race condition", "the issue is likely in the
cache". These statements are unfalsifiable — they predict no specific observation, so no
observation can refute them. The LLM cannot tell whether the fix worked or whether it coincided
with luck.

> "Make your hypothesis falsifiable before acting. State the observation that would prove it
> wrong. A prediction that cannot be wrong cannot be right either."

Concretely: before applying a fix, state *what you expect to see after* (a specific log line, a
specific metric value, a specific test outcome) and *what would prove the hypothesis wrong*. If
you cannot state either, you do not yet have a hypothesis — you have a guess.

### 3. Convergence speed vs. plant dynamics (§5.5)

> If feedback speed is slower than the rate at which the plant changes, the loop oscillates
> instead of converging.

The book's example (§5.5): Richardson's 1922 weather forecast took 6 weeks to compute for 6
hours ahead — slower than the weather changed, so the prediction was always wrong by the time
it arrived. Modern NWP works because compute is faster than weather.

LLM equivalent: a flaky test that you can only reproduce by running the full suite (10 minutes
per cycle), but the failure depends on a state that mutates every few seconds. Each iteration's
observation is stale before you can act on it. The fix is to **tighten the loop** (unit test,
faster reproduction) before refining the model.

This reinforces `references/discrete-systems.md` with a sharper criterion: feedback rate must
exceed plant dynamics rate. If your test cycle is slower than the bug's evolution, you will
oscillate.

### 4. Feedback overcompensation (§5.6)

> Negative feedback with too-aggressive correction oscillates around the target instead of
> converging. The book's medical name: 目的性震颤 (intention tremor) — a patient reaches for a
> cup, hand overshoots left, overcorrects right, overshoots left, never lands.

The book's example (§5.6): the history of light. Particle theory failed at diffraction →
physics swung to wave theory → wave theory failed at photoelectric effect → physics swung back
to particle theory → finally resolved by quantum field theory. Three centuries of oscillation
because each correction *reversed* the model instead of *reducing* its error.

LLM equivalent: a test fails because of a missing timeout → LLM adds a 30-second timeout →
test now hangs on a different case → LLM removes all timeouts → original bug returns. The LLM
is reversing direction each iteration instead of reducing the error magnitude.

> "If corrections are reversing direction each iteration, you are overshooting. Reduce the gain
> (smaller, more targeted changes), do not flip the strategy. Reversal is not convergence — it
> is oscillation."

The fix is *gain reduction*: make smaller changes. If the bug is "missing timeout", the
hypothesis-driven fix is "add a 2-second timeout with a clear error", not "add a 30-second
timeout" (overshoot) and not "remove timeouts" (reversal).

### 5. Undecidability condition (§5.7)

> Sometimes the error between theory and practice does *not* reflect distance from truth. A
> correct theory may fail experiments; a wrong theory may pass them.

The book's example (§5.7): Schrödinger's first (relativistic) wave equation disagreed with
experiments on hydrogen — not because the equation was wrong, but because electron spin was
unknown and unobservable. Decades later the same equation was rediscovered as the
Klein–Gordon equation, correct for spin-0 particles. **The experiments were right; the theory
was right; the gap was a missing variable.**

The book invokes Kuhn's paradigms: when decidability fails, scientists use **intermediate
standards** (invariants, symmetry, conservation laws, simplicity) to keep direction while
experiments catch up.

LLM equivalent: the test suite passes, but production still breaks. Or the test suite fails,
but the production code is correct. The LLM cannot use "tests pass" as a proxy for truth when
the tests do not observe the variable that matters. The intermediate standards are the cognitive
laws in this skill: stability under perturbation, bounded control, closed-loop convergence,
model validity range.

> "Passing tests is not proof of truth. When tests and reality disagree, suspect a missing
> variable, not a bad test or a bad theory. Use invariants (stability, bounds, convergence)
> as intermediate standards when decidability fails."

## Worked example: the five failure modes in one bug

**Bug:** a job queue occasionally drops tasks under load. Tests pass. Production complains.

| Failure mode | How it shows up | Fix |
|---|---|---|
| Observable limit (§5.3) | Tests only enqueue + dequeue; drop rate is not observed | Add a `dropped` counter and a test that asserts it stays 0 under load |
| Unfalsifiable hypothesis (§5.4) | "Probably a race" — predicts nothing | "If the race is on `pop`, then serializing `pop` will reduce `dropped` to 0; otherwise it stays > 0" |
| Convergence too slow (§5.5) | Full suite takes 10 min; the drop only reproduces at >1000 qps | Add a focused load test that runs in 5 sec |
| Feedback overshoot (§5.6) | First fix: add a global lock → throughput collapses → second fix: remove all locking → drops return | Reduce gain: lock only the critical section, measure, narrow further |
| Undecidability (§5.7) | Tests pass but production still drops; you blame the test | Recognize the test does not observe the load variable. Add a load test as a new information channel. |

## LLM behavior pattern: Open one layer at a time

> "When the model fails, open one layer of the black box — add one new observable or one new
> controllable. Do not attempt to open every layer at once; each layer you open reveals a new
> black box."

Concretely:
- The model says "race on `pop`". Open the box: add a log line at `pop` showing the
  interleaving.
- The log confirms the race. Now `pop` is no longer black; the new black box is *why* the
  race happens (locking? visibility? reentrancy?).
- Open that box: add a metric on lock hold time and contention count.
- And so on. Each layer is one new variable, not a rewrite.

---

## Decision rule

- Distinguish plant / model / gap explicitly. Bugs live in the gap.
- If iteration isn't converging, add an observable before another iteration.
- State a falsifiable prediction before each fix. State what would prove it wrong.
- If corrections reverse direction, reduce gain — do not flip the strategy.
- When tests and reality disagree, suspect a missing variable, not a bad test.
