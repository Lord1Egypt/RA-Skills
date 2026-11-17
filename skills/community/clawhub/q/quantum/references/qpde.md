# Quantum Phase Difference Estimation (QPDE)

QPDE is a cousin to QPE that recovers only the **difference** of two eigenphases, `Δφ_ij = φ_i − φ_j`. Prefer QPDE over full QPE when the observable is an energy *gap* (excited-state chemistry, spectroscopy, level splittings) — the sampling overhead is constant in the target precision while the circuit depth grows as `O(1/ε)`.

Source: Quantinuum/SoftBank "Quantum Computing Frontiers" white paper, July 2026, §3.5.

## Circuit shape

```
|+⟩         --●------●------●-------- R_z(β) ---- X ---- measure(X-basis)
|Φ_g⟩       --  U_ex --  U^k --  U_ex† --
```

Steps per shot:

1. Prepare `|Φ_g⟩` and ancilla `|+⟩`.
2. Controlled `U_ex` maps `|Φ_g⟩ → |Φ_e⟩` when the ancilla is `|1⟩`.
3. Apply `U^k` on the system register (`U = e^{-iHt}`).
4. Uncontrolled `U_ex†`.
5. Ancilla phase-shift `R_z(β) = e^{-i(β/2)Z}`.
6. Measure ancilla in the X-basis (H then Z-basis) → outcome `m ∈ {0,1}`.

## Sampling protocol

Draw `(k_l, β_l)` uniformly at random with `k ∈ {1, ..., k_max}` and `β ∈ {0, π/2}`. `k_max` controls precision and sets the deepest circuit depth. Collect `{m_l}` over `N_s` shots (the white paper used `N_s = 1400` for ~2σ = 24 μHa precision on ethylene).

Reconstruct the phase by maximum likelihood over `φ̃ ∈ [−π, π)`:

```
Q(φ̃ | {m_l}; {k_l, β_l}) = Π_l  (1 + cos(k_l·φ̃ + β_l − m_l·π)) / 2
Δφ_est = argmax_φ̃  Q(φ̃)
```

Bootstrap over shot subsets to get a statistical uncertainty on Δφ.

## Ethylene minimal photochemical benchmark

Reusable 2-qubit test problem for any QPDE / partial-FT / noise-sweep harness. C₂H₄ at 90° torsion (conical-intersection geometry), (2e, 2o) active space, STO-3G basis, Jordan–Wigner + particle-number + spin tapering:

```
H = h₁·Z₁ + h₂·Z₂ + h₃·Y₁Y₂ + h₄·Z₁Z₂ + h₅·I
(h₁, h₂, h₃, h₄, h₅) = (-3.02e-4, -3.02e-4, -0.122188, 1.28e-3, -76.856020) a.u.
```

- Ground-state reference: `|Φ_g⟩ = (|01⟩ + |10⟩)/√2`.
- Excitation: `U_ex = X₂·Z₁`, giving `|Φ_e⟩ = (|00⟩ − |11⟩)/√2`.
- Target: `ΔE ≈ −2.559 mHa` at the CI geometry. The full paper reports `−0.0025561(24) Ha` from `R = 1000` bootstrap × `N_s = 1400`.

## The evolution-time trick (why this benchmark is Clifford-mostly)

Choose `t = π / (16·h₁)`. Then:

- `e^{-i h₁ Z₁ t} = e^{-i(π/16)Z₁} = √T₁`, and likewise `√T₂` (single-qubit `T^{1/2}` phase gates).
- `e^{-i h₃ Y₁Y₂ t}` after 5-bit binary rounding of `h₃·t/π` reduces to `R_{Y₁Y₂}(π/2)` — **Clifford**.
- `e^{-i h₄ Z₁Z₂ k t}` similarly rounds to `R_{Z₁Z₂}(3kπ/2)` ∈ {π/2, π, 3π/2, 2π} — **Clifford** for the k-values used.

Net effect: only the `√T` factors sit outside Clifford, so on the [[7,1,3]] Steane code the whole `U^k` needs just a handful of RGT gadgets. See `references/encoded-circuits.md` for the RGT + partial-FT recipe.

## Guppy angle-hygiene warning

The evolution-time trick puts `t = π/(16 h₁)` in radians, but `angle()` in Guppy is in HALFTURNS (multiples of π). Write:

```python
# Correct — halfturns, not radians
u_1q = rz(qA, angle(1/16))   # √T on qubit A
```

NOT `angle(math.pi / 16)`, which is the S gate. See `references/guppy-language.md` §Angles.

## When NOT to use QPDE

- You need the absolute eigenvalue (not a gap) — use QPE.
- Only one eigenstate is accessible — the two-state weighting `|c_i|²|d_j|²` in `P(m|...)` collapses.
- `k_max` circuits blow past your coherence budget — QPE's iterative variants may amortize better.

## Worked Selene implementation (G16, this repo)

`quantum/qpde/{model,kernel,sweep,validate}.py` is the end-to-end reference:

| File | Role |
| --- | --- |
| `model.py` | Closed-form 2-qubit ethylene Hamiltonian + `eigenpairs()`; unit-checked at import. |
| `kernel.py` | `render_qpde_source(k, beta)` string factory → temp `.py` → `importlib` (see `driver-pattern.md`). Guppy needs source on disk, so the factory writes a file per cell. |
| `sweep.py` | 20-cell grid `k ∈ {1,2,4,8} × β ∈ {0, 0.25, 0.5, 0.75, 1.0}` halfturns, resumable per-cell cache under `_cache_qpde/`. |
| `validate.py` | Predicted-vs-measured check, gap fit, static JSON dump to `src/data/demos/qpde_ethylene_selene.json`. |

### Closed form for a one-ancilla QPDE cell

    p(ancilla = 1) = (1 - sin(2*phi) * sin(beta)) / 2,   phi = off * t

Verdict per cell uses the standard `4*sqrt(0.5/shots)` binomial threshold — not
a p-dependent 3σ form. Observed: 20/20 PASS, worst Δ = 0.0217 at 2048 shots,
51 s total.

### k = 8 is an aliasing control, not a data point

At `k = 8` the ethylene parameters put `2*phi` at π, where `p` is stationary in
`phi` and the arcsine branch is degenerate — the QPDE mod-1 wrap. Fit the gap
from `k ∈ {1,2,4}` at `β = π/2` only and **report k = 8 separately as the
aliasing control**. Including it silently biases the gap. Recovered gap with
this exclusion: 0.8099 Ha vs 0.8000 Ha reference (1.2% error).

### Gap-fit recipe

Use only the `β = π/2` column (maximum slope, `p = (1 - sin(2*phi))/2`):

    phi_k = 0.5 * asin(1 - 2*p_k)   # principal branch
    gap_k = phi_k / (k * t)

then average over the non-aliased k. Bootstrap over shots if you need an error bar.
