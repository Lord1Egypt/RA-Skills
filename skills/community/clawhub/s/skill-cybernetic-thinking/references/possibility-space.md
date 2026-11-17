# Reference: Possibility Space & Conjugate Control

Book anchor: 金观涛《控制论与科学方法论》第一章 §1.1–§1.8 (控制和反馈).

## What control actually means

(§1.1) Control is not "make a thing do X". Control is **narrowing a possibility space**. A thing
that has only one possible future cannot be controlled — there is nothing to choose between. A
thing that has many possible futures, but where you have no way to favor one over another, also
cannot be controlled. Control exists only when there is *both* uncertainty *and* a means to
select.

- The set of futures a thing may take is its **possibility space** M.
- After you act, the space narrows to m.
- Your **control ability** is M/m. A scale accurate to 0.0001 g has a larger control ability
  than one accurate to 1 g, because it narrows the space more per use.

A change that does not narrow the possibility space of the thing you care about is not control.
It is motion.

## LLM behavior pattern: Name the possibility space before the action

> "Before choosing u, name the set of outcomes you are choosing among. A change that doesn't
> reduce uncertainty is not control."

An LLM using this skill must, before proposing a fix, name:
- what set of states the system could be in (the uncertainty),
- which of those it is trying to bring about / rule out,
- how its proposed `u` actually narrows that set.

If the LLM cannot say which alternatives its action rules out, it is not controlling — it is
hoping. "Try this and see" without an explicit hypothesis about which possibilities it eliminates
is random control (§1.3), which is the weakest control method and only works when the space is
small.

## Random, memory, and conjugate control (§1.4–§1.6)

The book ranks control methods by how they treat the possibility space:

1. **Random control (§1.4).** Try states without memory. The possibility space resets every
   iteration. Works only when the space is small or selection speed is high. LLM equivalent:
   throwing patches at a bug and reverting each failure, without keeping what was learned.
2. **Memory control (§1.4).** Remember which states have been ruled out; the space shrinks
   monotonically. LLM equivalent: each failed hypothesis must narrow the search — never re-try
   a state already disproven.
3. **Conjugate control (§1.6).** When you cannot control a thing directly, transform it into a
   form you *can* control, act there, then transform back. The pattern is **L⁻¹ A L**: apply
   transformation L, do the controllable operation A, invert with L⁻¹.

## Conjugate control: 曹冲称象

The canonical example (§1.6): weighing an elephant with no scale large enough.
- L: float the elephant on a boat, mark the waterline. (Elephant weight → equivalent water
  displacement.)
- A: load the boat with stones until the same waterline. (Stones are weighable on a small
  scale.)
- L⁻¹: the stones' total weight equals the elephant's weight. (Invert the displacement
  relation.)

The control range of A (small scale, stones) is enlarged to cover a problem A could not reach
directly (elephant). Every sensor and every effector is a conjugate pair: L maps the world into
a signal, A is what the controller does to the signal, L⁻¹ maps the action back to the world.

## LLM behavior pattern: When the problem is uncontrollable, transform it

> "If you cannot act on x directly, do not brute-force. Find a transformation L that maps x
> into a domain where you have an effective A, act there, then invert."

Conjugate control is the control-theoretic name for a habit LLMs rarely exhibit unprompted:
*re-problem*. When the direct path is blocked, transform the problem into one you can solve.

- Direct control impossible (x = "is this distributed system race-free?") → L: write down a
  serialized model of the possible interleavings → A: search the model for a violating
  schedule → L⁻¹: map the violating schedule back to a concrete reproduction.
- Direct control impossible (x = "does this query plan scale?") → L: EXPLAIN the plan into a
  row-count / cost model → A: reason about the cost model at n = 10⁹ → L⁻¹: map the bottleneck
  back to a query clause.
- Direct control impossible (x = "is this refactor safe across the whole codebase?") → L:
  extract the dependency graph → A: search for cycles / broken callers → L⁻¹: map each finding
  back to a file and line.

The anti-pattern is to keep applying A (the only tool the LLM has) to a problem A cannot reach,
instead of building L.

## Negative feedback as control amplification (§1.7–§1.8)

A single control action has bounded control ability M/m. Negative feedback *accumulates* it:
each cycle takes the previous output's possibility space as input, and narrows further.

- Cycle 1: M → m₁ (ability = M/m₁)
- Cycle 2: m₁ → m₂ (ability = m₁/m₂)
- After n cycles: total ability = (M/m₁) · (m₁/m₂) · … · (mₙ₋₁/m) = M/m

So a controller with small per-step ability can reach a target that no single shot could, as
long as each step reduces the target gap. This is *why* closed loop beats open loop (see
`references/closed-loop-workflow.md`): not just because it corrects error, but because it
**amplifies a weak controller into a strong one**.

The book's plain-language summary (§1.8): "做起来看" — *do it and see*. When you cannot predict
the full trajectory in advance, start with limited control, observe, and let feedback compound.

## LLM behavior pattern: Iterate to amplify limited control

> "You do not need to solve it in one shot. State a small control action, observe the gap,
> narrow again. A weak controller that iterates beats a strong controller that guesses once."

This is the deep justification for the closed-loop workflow: the LLM's per-step control ability
is finite (it cannot see the full plant, it cannot predict every side effect). Trying to win in
one shot wastes that finite ability. Iterating compounds it.

- Do not propose a 200-line patch that "should" fix everything. Propose the smallest u that
  narrows the possibility space measurably, observe, narrow again.
- Do not refuse to act because the model is incomplete. Use feedback to *build* the model
  (§5.2 in `references/black-box-epistemology.md`).

## Worked example: debugging a flaky test by possibility-space narrowing

**Random control (anti-pattern):**
```python
# Re-run the test until it passes, then ship
for _ in range(100):
    if test_passes():
        break
```
The possibility space ("why does this fail?") is not narrowed. If it passes on run 7, you know
no more than on run 1. Tomorrow it fails again.

**Memory control (better):**
```python
# Each failure rules out a hypothesis
# H1: race on startup      → tested with --no-concurrency, still failed → H1 ruled out
# H2: clock skew            → tested with fake clock, still failed → H2 ruled out
# H3: order-dependent init  → tested with shuffled init order, reproduced → H3 supported
```
The space shrinks monotonically. After 3 iterations the hypothesis is anchored.

**Conjugate control (when direct observation is impossible):**
```python
# Directly observing the race is impossible (x = interleaving of two threads).
# L: instrument both threads with a deterministic ordering log
log = []
def thread_a():
    log.append(("a", time.monotonic(), state))
    ...
def thread_b():
    log.append(("b", time.monotonic(), state))
    ...

# A: replay the log offline; search for the interleaving that produces the failure
# L^-1: map the failing interleaving back to a synchronization point in the source
```
The uncontrollable x (live interleaving) is transformed into a controllable A (offline log
search), then mapped back. This is the same structure as 曹冲称象.

---

## Decision rule

- Can you act on x directly? → do so (memory control if iterative).
- Cannot act on x directly? → build L, act on the transformed problem, invert.
- Does your action narrow the possibility space? if not, it is not control — stop and reframe.
