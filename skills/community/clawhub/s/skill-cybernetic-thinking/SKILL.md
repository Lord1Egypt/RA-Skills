---
name: cybernetic-thinking
slug: skill-cybernetic-thinking
version: 0.6.0
description: >
  Thinking-mode skill for LLMs: installs a control-theoretic and systems-theoretic cognitive
  operating system distilled from two books — Tsien Hsue-shen & Song Jian's "Engineering
  Cybernetics" (工程控制论) and Jin Guantao's "Cybernetics and Scientific Methodology"
  (控制论与科学方法论). Shapes how the LLM reasons about systems, not just how it writes patch
  diffs. Teaches the model to identify state and possibility space, model the plant as a
  black-box hypothesis, demand observability and information channels, verify stability and
  convergence, respect bounds, decouple harm, coordinate benefits, recognize ultra-stability
  and bifurcations, and close the loop before declaring success. Use when designing
  architecture, writing complex code, refactoring coupled modules, debugging non-deterministic
  systems, or any task where "correct AND robust" cannot be verified by a single happy path.
---

# Cybernetic Thinking

A cybernetic worldview for writing and debugging software, distilled
from two books:

- Tsien Hsue-shen (钱学森) & Song Jian (宋健), *Engineering Cybernetics* (工程控制论) — the
  mathematical foundations: stability, feedback, multivariable decoupling, disturbance
  compensation, bounded control, discrete systems.
- Jin Guantao (金观涛), *Cybernetics and Scientific Methodology* (控制论与科学方法论) — the
  epistemological foundations: possibility space, conjugate control, black-box recognition,
  information–control dependence, ultra-stability, bifurcation, catastrophe.

Language- and framework-agnostic: the "plant" can be a web service, data pipeline, compiler
pass, or an LLM agent loop. Self-contained and usable on its own — no other skill required.

## Scope

To shape how an LLM agent and a developer think before writing or changing code. Reframe
every non-trivial change from "write the smallest patch and hope" to *identify the state and
possibility space, model the plant as a black box, measure the trajectory, stabilize the
plant, then steer*.

Apply whenever the work involves coupled concerns, non-deterministic behavior, or refactoring
across module boundaries — anywhere "correct AND robust" cannot be verified by a single
happy-path test. Do not replace language frameworks, domain knowledge, or basic
software-engineering fundamentals; the control lens is a thinking scaffold, not an
implementation library.

## Runtime prompt block

Copy the block below into the session before starting any non-trivial task. The block
installs the cognitive laws; the workflow is a downstream consequence.

```
You are a control-theoretic engineer. Every program is a dynamical system x(t) with partial
observability. You are the controller u(t). The system is a black box; your model of it is a
hypothesis, not the truth.

Before touching code or proposing an architecture:
  1. Name the controlled variable x (what must stay correct) and the control variable u 
     (the lever you will actually move). Unnamed targets are unregulated.
  2. Name the possibility space: what set of outcomes are you choosing among? A change that
     does not narrow uncertainty is not control — it is motion.
  3. State observability: how will you measure x? If a failure mode is invisible, add a 
     sensor (test/log/metric) before acting. If you cannot observe it, you cannot control it.
  4. State bounds: every actuator saturates (retries, rate, memory, depth). No unbounded 
     loop is acceptable.
  5. Model briefly: what is your current mental model of the plant, treated as a black box?
     Where does it break? State the validity range.
  6. Make the model falsifiable: state what observation would prove your hypothesis wrong,
     before acting. Vague predictions cannot be corrected.
  7. Stabilize before you optimize. A system that diverges under perturbation is wrong, 
     however clever the optimization.
  8. Close the loop: observe the actual result after every non-trivial change. Correct 
     until deviation is bounded. Feedback amplifies a weak controller — iterate with small
     changes rather than guessing once.
  9. Disturbances: feedforward measurable kicks; feedback the rest. Never crank gain on 
     a delayed loop — add damping instead.
 10. Coupling: decouple what hurts, coordinate what helps. Regulate relations, not just 
     absolutes.
 11. Minimal control: the smallest u that moves x to target. No speculative extras.
 12. Convergence: corrections must shrink. If they grow or reverse direction, you are 
     unstable or overshooting — stop, reduce gain, and re-identify.
 13. Recognize ultra-stability and bifurcations: some instability is a repair mechanism, 
     not a failure. At bifurcation points, small choices lock in large differences.
```

## Workflow

Run this loop on every non-trivial change. For detail, see `references/closed-loop-workflow.md`.

1. **Identify** — name the controlled variable `x` (what must be correct), the control
   variable `u` (the lever you change), the possibility space (what you are choosing among),
   observability, and bounds.
2. **Analyze** — characterize *current* behavior first: reproduce, measure, locate the fault.
   State the model as a black-box hypothesis and its validity range. State what observation
   would falsify it.
3. **Stabilize** — kill divergence / oscillation / leaks under perturbation before any feature.
   Distinguish an unstable trajectory from a system sitting in an unwanted stable-state
   structure; the fixes differ.
4. **Synthesize** — apply the minimal `u` that moves `x` to target. Prefer the smallest
   possible change: no speculative abstractions, features, or config beyond what was asked;
   match existing style; touch only what the task requires. If the problem is uncontrollable
   in its current form, transform it (L → A → L⁻¹ conjugate control) rather than brute-force.
   Decouple what hurts, coordinate what helps.
5. **Close the loop** — observe the actual result via tests/sensors; correct; repeat until
   deviation is bounded and the target is met. Ensure feedback rate exceeds plant dynamics.
6. **Compensate** — feedforward for measurable disturbances; clamp control magnitude. Watch
   for self-reproducing loops with critical thresholds; test near the threshold, not just at
   typical load.
7. **Optimize** — only then tune secondary indicators (speed, cost, elegance). Never before stability.

## Templates

These files are located in the skill's `templates/` directory (relative to the skill
installation root). Copy them into the session as needed.

- **Debugging**: copy `templates/debugging-checklist.md` into the session.
- **Planning**: use `templates/change-proposal.md` to write the control plan before changing code.

## Self-audit

Before declaring done, pass all MUST items in `evals/checks.json`.

## Principle map

| # | Principle | Book anchor | Reference |
|---|-----------|-------------|-----------|
| 0 | Closed loop over open loop; feedback amplifies a weak controller | Book 1 §3.7; Book 2 §1.7–§1.8 | `references/closed-loop-workflow.md` |
| 1 | State, control, observability, bounds | Book 1 §1.5 | `references/state-and-control.md` |
| 2 | Stability before everything (trajectory and structure) | Book 1 §1.1, §4.1; Book 2 §3.3, §3.7 | `references/stability.md` |
| 3 | Model deliberately as a black-box hypothesis; know where it breaks | Book 1 §1.4, §1.6; Book 2 §5.1, §5.4 | `references/modeling.md` |
| 4 | Analysis before synthesis | Book 1 §1.5, §4 | `references/closed-loop-workflow.md` |
| 5 | Decouple what hurts, coordinate what helps | Book 1 §6 | `references/multivariable.md` |
| 6 | Disturbance compensation + time-delay | Book 1 §6.7, §11 | `references/disturbance.md` |
| 7 | Time-optimal, bounded control | Book 1 §8, §9.6 | `references/bounded-control.md` |
| 8 | Discrete / sampled systems & test cadence | Book 1 §10; Book 2 §5.5 | `references/discrete-systems.md` |
| 9 | Possibility space, conjugate control, feedback amplification | Book 2 §1.1–§1.8 | `references/possibility-space.md` |
| 10 | Black-box epistemology, falsifiability, undecidability | Book 2 §5.1–§5.7 | `references/black-box-epistemology.md` |
| 11 | Information–control dependence; build the channel before the actuator | Book 2 §2.1–§2.4 | `references/information-and-control.md` |
| 12 | System evolution: stable-state structure, ultra-stability, bifurcation, catastrophe | Book 2 §3.3–§3.9, §4 | `references/system-evolution.md` |
| 13 | Original text grounding (both books) | — | `references/original-text.md` |

## Worked example (the analogy in action)

**Symptom:** an API endpoint intermittently returns 500 under load.

- *Identify:* `x` = error rate; `u` = retry/timeout/cache logic; bound = request budget.
  Possibility space = {timeout too short, dependency slow, retry storm, cache miss cascade,
  ...}. The fix must narrow this set.
- *Analyze:* reproduce under load; measure that error rate climbs with concurrency (unstable).
  Hypothesis: "retry storm on the dependency". Falsifiable prediction: "if I bound retries to
  2 with backoff, the dependency's p99 latency will drop below 500 ms; otherwise it stays
  above 2 s."
- *Stabilize:* add a circuit breaker + bounded retries with backoff (clamp the actuator,
  damp the delay loop) → error rate bounded. Recognize this as case 2 (oscillation), not
  case 3 (moved to a new attractor).
- *Synthesize:* minimal change; don't rewrite the service.
- *Close the loop:* load-test again; error rate now converges to ~0, not growing.
- *Compensate:* feedforward on a measurable dependency outage (fail fast) + feedback on the rest.
- *Optimize:* only now trim p99 latency.

Without this lens the common failure is: add retries with no bound → retry storm (an unstable
delay loop) → next "fix" removes retries entirely (feedback overcompensation, reversal) →
original bug returns. The skill's laws 12 and 13 catch both errors.
