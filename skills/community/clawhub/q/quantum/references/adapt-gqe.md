# ADAPT-GQE: generative circuit synthesis for molecular ground states

Source: Koziell-Pipe et al., *Learning to Prepare Molecular Ground States with Transformer Models*, arXiv:2607.22468 (July 2026). Quantinuum, NVIDIA, Pfizer.

## What it is

ADAPT-GQE is a generative-AI pipeline for quantum chemistry circuit synthesis:

1. **Curriculum generation** — run ADAPT-VQE on a set of molecular geometries to produce high-quality, compact reference circuits.
2. **Supervised pre-training** — train a transformer model to predict the operator sequence and parameters of those reference circuits.
3. **RL refinement** — use a reinforcement-learning objective (circuit fidelity / energy) to improve the generated circuits beyond the accuracy of the ADAPT-VQE training data.
4. **Hardware execution** — run the generated circuits on a quantum device. The paper reports execution on Quantinuum Helios-1.

The headline result is that the trained model generates circuits **an order of magnitude faster** than ADAPT-VQE while matching or improving state-preparation accuracy, and it transfers across related molecular geometries (e.g., different conformations of imipramine).

## Why it matters for this repo

- **Chemistry-on-hardware is the same envelope we target.** The QPDE ethylene benchmark (`references/qpde.md`) is a small-molecule warm-up; ADAPT-GQE is the drug-scale next step.
- **Data-driven + symbolic composition.** ADAPT-GQE generates circuits; the Nadarasa PQP rewriter (`references/tomographic-equivalence.md`) canonicalises and proves them. The two can be stacked: a generated subcircuit can be reduced by rule-(N/M/P), then physically verified on Selene.
- **Template reuse across geometries.** The transfer-learning insight suggests caching circuit templates and parameterising them with `SweepRunner` (`references/sweep-runner.md`) rather than generating from scratch per geometry.

## Critical angle hygiene

If you ever reproduce a Hamiltonian-evolution kernel from the chemistry literature, remember that papers write angles in **radians**, but Guppy's `angle()` is in **halfturns** (multiples of π).

```python
# Correct: 0.5 halfturns = π/2 radians
rz(q, angle(0.5))

# Wrong: angle(math.pi / 2) is ~1.57 halfturns, i.e. 3.14 radians
rz(q, angle(math.pi / 2))   # ❌
```

See `references/qpde.md` (§Guppy angle-hygiene warning) for the full worked example with the ethylene Hamiltonian.

## Practical workflow if we pursue this

1. Generate or import ADAPT-VQE reference circuits for a small active space (e.g., the same 2-qubit ethylene model in `quantum/qpde/model.py`).
2. Train a tiny surrogate model (or hand-craft a few template sequences) over the geometry parameters.
3. Emit the generated circuit as a Guppy `@guppy` kernel in a real `.py` file.
4. Canonicalise with the PQP rewriter or hand-apply rule-(N/M/P).
5. Run tomography on Selene and dump the result to `src/data/demos/<experiment>.json` (`references/selene-runtime.md` §Shipping results to the frontend).
6. Render the result through the `selene_run` v1 schema (`references/selene-run-schema.md`).

## Caution

- ADAPT-GQE is a **training pipeline**, not a single-shot kernel. The expensive part is classical. Do not attempt to run the full training loop inside a Lovable turn; pre-train or stub the model, then only ship the generated circuit + Selene execution in the repo.
- The paper does not publish the exact trained weights or the full operator vocabulary. Any reproduction will be a small-scale surrogate, not a claim of reproducing the imipramine result.

## Relation to other references

- `references/qpde.md` — small-molecule chemistry benchmark (ethylene), angle-hygiene example.
- `references/sweep-runner.md` — parameterised templates across geometries.
- `references/tomographic-equivalence.md` — verifying generated circuits on Selene.
- `references/selene-runtime.md` — running the final kernels and shipping JSON.
