# Reference: Modeling & Engineering Approximation

Book anchors: §1.4 (almost every real system is nonlinear; linearize deliberately), §1.6
(model identification: analytic, experimental, statistical).

## Deliberate simplification (§1.4)

> Almost any physical system is nonlinear if analyzed precisely enough. We call a system
> "linear" only when, *for the question being asked*, a linear system represents it precisely
> enough that the difference is irrelevant.

- Don't reach for the full-complexity model first. Build the **simplest model that answers the
  current question**, and **state its validity range**.
- **Pick the model to the question:**
  - Near a stable equilibrium → linearize, ignore nonlinearity (§1.4, Lyapunov first
    approximation).
  - Studying oscillation / self-excited vibration / limit cycles → the nonlinearity *is* the
    cause; keep it. Linearizing would delete the very phenomenon you're investigating.
- This is the control-theoretic twin of the simplicity rule: simplify, but **know where
  the simplification breaks** — and say so.

## LLM behavior pattern: State the model and its limits

> "I model the plant as X. This model holds under conditions Y. It breaks when Z."

The LLM must explicitly state its mental model of the system and where it breaks, before
synthesizing a fix. Implicit models lead to implicit breakage.

- If a bug contradicts your model, **the model was wrong, not the bug**. Update the model.
- Distinguish the *model you use to decide* from the *plant that actually runs*. The gap
  between them is where instability hides.

## Model identification: you don't know the plant exactly (§1.6)

You rarely have a perfect model of the system you're editing. Three ways to get one:

1. **Analytic** — decompose into units, model each, compose. Works *only* when decomposition
   is faithful. Beware emergent behavior at the seams: a component's model in isolation can
   differ qualitatively from its behavior inside the system.
2. **Experimental (preferred for code)** — inject a known input `u`, record the output `x`,
   infer the model. *This is exactly running the code and observing.* Let behavior, not
   assumption, teach you the plant.
3. **Statistical** — when the plant is too complex for clean analytic or single-shot
   experimental identification, use frequency/statistical probing (§1.6: sine sweep →
   amplitude/phase → transfer function).

## Treat the model as approximate and updatable

- After a surprise during debugging, **update your mental model** of the plant. A bug that
  contradicts your model means the model was wrong, not the bug.
- Distinguish the *model you use to decide* from the *plant that actually runs*. The gap
  between them is where instability hides.

## Worked example: linear model breaks at scale

**Scenario:** a list-merging function works for n=10 but segfaults at n=10^7.

```python
def merge(a, b):
    return a + b          # model: O(n) concatenation, works for small n
```

**Analysis:**
- Mental model: "concatenation is cheap; I can use it anywhere"
- This model breaks at n=10^7 because `a + b` allocates a new list of size `len(a)+len(b)`.
- Memory spikes → OOM → crash. The model assumed linear cost; reality is linear *coefficient*
  with a fixed allocation overhead that dominates at scale.

**Correct model (stated validity range):**
```
x = memory usage; model = O(n) allocation per merge; valid for n << cache size.
Breaks when n approaches memory limit.
```

**Fix informed by correct model:**
```python
def merge(a, b, out=None):
    if out is None:
        out = []
    out.extend(a)
    out.extend(b)           # in-place; model remains valid at scale
    return out
```

- Model validity range is now explicit.
- Bug informed the model update; model informed the fix.

