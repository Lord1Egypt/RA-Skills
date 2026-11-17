# Tomographic equivalence + conjecture synthesis (PQP Frontier pattern)

The harness that powered Tracks A and B of the v0.3.7–v0.3.8 PQP Frontier
work, and that proved 11 / 105 conjectural gate-identities from shot
statistics alone. Reach for this whenever you need to prove two gate
sequences `A ≡ B` (mod global phase) **without trusting a matrix oracle**
— i.e. when the rewriter says they should be equal and you want Selene
to confirm.

Reference implementations:

- `quantum/pqp_frontier/tomography.py` — 1q 18-cell harness, `prove_equal_1q(...)`.
- `quantum/pqp_frontier/conjectures.py` — driver that runs the harness on every flagged conjecture.
- `quantum/pqp_frontier/dump_conjectures.ts` / `dump_conjectures_2q.ts` — the TS-side matrix oracle + rewriter promotion report.
- `src/lib/zx/conjecture-synth.ts` (1q) / `conjecture-synth-2q.ts` (2q) — sequence enumeration + canonical matrix key.

## When to use it

- Verifying a new rewriter rule produces physically equivalent diagrams.
- Promoting a "conjectured equality" (matrix oracle says equal, structural rewriter cannot prove it) from candidate to physical fact.
- Sanity-checking an angle convention before a long sweep — a tomography PASS at shots=256 takes seconds and catches halfturn-vs-radian bugs immediately.
- Falsifying a TS-side oracle: a FAIL with shot noise well below threshold means the matrix code, not Selene, has a bug.

Do NOT use it for stochastic kernels (G1 cosets, Birthday) — the harness assumes a deterministic unitary; for stochastic kernels compare full distributions, not per-cell `P(1)`.

## The 1q grid (18 cells)

Six tomographically complete inputs × three measurement bases:

| Inputs | Prep gates from `\|0⟩` |
| --- | --- |
| `\|0⟩` | (none) |
| `\|1⟩` | `xgate(q)` |
| `\|+⟩` | `h(q)` |
| `\|−⟩` | `xgate(q); h(q)` |
| `\|+i⟩` | `h(q); rz(q, angle(0.5))` |
| `\|−i⟩` | `h(q); rz(q, angle(-0.5))` |

| Basis | Rotation before `measure` |
| --- | --- |
| Z | (none) |
| X | `h(q)` |
| Y | `rz(q, angle(-0.5)); h(q)` |

For each of the 18 (input, basis) cells, compile two kernels (A-side and B-side), run `shots` shots each, compute `p_A(1)`, `p_B(1)`. The pair PASSes when **every** cell passes the threshold below.

## The 2q grid (324 cells)

Product structure: 6 × 6 = 36 product inputs, 3 × 3 = 9 product measurement bases. Each cell measures both qubits and reports `P(11)` (or any fixed bit-pattern) per side.

Wall-time budget on Selene: ≈ 1 minute per pair at 256 shots/cell. Cap a single run at ~10 pairs to stay under a 15-minute sandbox window. For larger sweeps, drive `prove_equal_2q` in a background job and persist intermediate JSON per pair so the run can resume.

## The threshold — read carefully

```python
import math
threshold = 4.0 * math.sqrt(0.5 / shots)
# pair PASSes when worst_tv := max over cells of |p_A(1) - p_B(1)| < threshold
```

This is a **4σ bound on the standard error of a binomial difference at p = 1/2**, Bonferroni-ish for the 18 / 324 cells. Concrete numbers:

- `shots = 256` → threshold ≈ 0.177
- `shots = 384` → threshold ≈ 0.144
- `shots = 1024` → threshold ≈ 0.088

**Do NOT use the textbook `3σ · √(p(1−p)/n)` form.** It produces false FAILs for any cell where the true `p` sits near 0 or 1 (the variance estimate collapses but the binomial CLT does not), and is the source of the bogus v0.3.4 failure cascade. The constant `√(0.5/shots)` is the worst-case standard error and is always conservative.

## Conjecture synthesis pipeline

The full Tracks A + B loop:

1. **Matrix oracle** — enumerate every gate sequence over a chosen generator set up to `maxLen`. Compute each sequence's unitary in TypeScript using simple complex-matrix multiplication. Canonicalise by rotating the first non-zero entry to `+ℝ` and serialising every entry to N decimals (5 for 2q, 6 for 1q). Group sequences by canonical key — that's the equivalence-class partition.
2. **Structural rewriter** — apply the existing `bastard-rewriter` (1q) or `normalise2q` (2q) to each representative; record a residue string.
3. **Open conjectures** — within each equivalence class, if multiple residues survive, the class is an open conjecture: the matrix oracle says equal, the rewriter cannot prove it.
4. **Matrix-canonical rewriter rule** — rule (N) for 1q (Z(γ)·X(β)·Z(α) Euler decomposition) or rule (M) for 2q (4×4 canonical key as residue). Re-run the residue computation with the matrix rule enabled.
5. **Promotion report** — dual-pass JSON: `{promoted, reduced, unchanged}` counts plus per-conjecture status. Emitted by `dump_conjectures*.ts` to `src/data/demos/pqp_frontier_promotion*.json`.
6. **Selene PASS-verify (optional but recommended for new rules)** — pick the shortest contrasting pair per surviving conjecture, run `prove_equal_1q` / `prove_equal_2q` at 384–512 shots. A FAIL means the matrix oracle has a bug; a PASS confirms the rewriter has a genuine completeness gap.

UI surface: `/nadarasa/proofs/conjectures` (1q) and `/nadarasa/proofs/conjectures-2q` (2q) render the promotion headline, per-card PROMOTED badges, and the residue diff between structural and matrix-canonical passes.
