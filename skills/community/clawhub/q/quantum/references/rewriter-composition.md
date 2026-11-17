# Composing a generated/variational ansatz with the rewriter pipeline

How to hand an AI-generated or variational circuit (ADAPT-GQE, UCCSD, VQE ansatz)
to a Clifford canonicaliser before spending shots on it. Worked example: Nadarasa
Gate 0.4.6 / G21 — the H2 / STO-3G single-excitation UCCSD operator.

## The pattern

```text
ansatz  ──split──▶  Clifford frame  ──rule (N/M/P) canonicaliser──▶  residue
        │
        └─────────▶  rotation core  ──4x4 / 2^n matrix oracle──────▶  numeric check
                                     │
                         both forms ──▶ Guppy kernels ──▶ Selene shots ──▶ histogram compare
```

Three independent verification layers, in increasing cost:

1. **Matrix oracle (free).** Build the dense unitary for every candidate form in
   NumPy and compare to the exact operator. Tolerance `1e-9`; real agreement lands
   at machine epsilon (`1.1e-16` for G21).
2. **Structural canonicalisation (free).** Run the Clifford segments through
   `normalise2qWithMatrix` (rule M) in `src/lib/zx/conjecture-synth-2q.ts`. Equal
   `matrix_key` ⇒ the frames are the same unitary; the residue is the cheapest
   syntactic form.
3. **Selene shots (expensive).** Compile both forms with Guppy, run 512 shots on
   Quest, compare histograms to the exact probability vector using the standard
   `4·√(0.5/shots)` envelope (0.125 at 512 shots).

## When canonicalisation is safe

- **Safe:** segments drawn from the Clifford alphabet `{H0, H1, CZ, S0, S1}` —
  CNOT sandwiches, basis changes, entangling frames. The rewriter is exact here.
- **Not safe:** parameterised rotations (`Ry(θ)`, `Rz(θ)`) with θ outside the
  fixed angle set the oracle enumerates. Do NOT feed these to the rewriter; keep
  them as opaque cores and verify them with the matrix oracle instead.

So: **split the circuit at the rotation boundaries**, canonicalise the Clifford
segments, leave the rotation cores untouched, and re-verify the whole thing
numerically + on Selene.

## Decomposition trap (cost me a gate)

A conjugated-Rz sandwich is NOT a Givens rotation:

```text
CNOT · Rz(2θ) · CNOT   =  exp(-i θ Z0 Z1)        # phase, not excitation
```

The single-excitation operator `exp(-i θ (X₀Y₁ - Y₀X₁)/2)` needs a controlled-Ry:

```text
original  : CNOT(q1->q0) · CRy(2θ)(q0->q1) · CNOT(q1->q0)
alternate : CNOT(q1->q0) · Ry(θ)q1 · CNOT(q0->q1) · Ry(-θ)q1 · CNOT(q0->q1) · CNOT(q1->q0)
```

Always numerically verify a paper's stated decomposition against
`scipy.linalg.expm` of the Pauli sum before writing the Guppy kernel.

## Angle choice

Pick θ so that any derived Clifford angle lands in the alphabet — θ = π/4 gives
2θ = π/2 so a derived Rz is exactly `S`. That maximises how much of the circuit
the rewriter can absorb.

## Language split

The 2q oracle lives in TypeScript; Selene execution lives in Python. Drive the
canonicalisation from a small `bunx tsx` script that emits JSON, and merge it with
the Python dump in a compose step. Document the split — there is no Python port
of the oracle.

## Reference implementation

- `quantum/adapt/adapt_h2_uccsd.py` — matrix oracle, both forms, `src/data/demos/adapt_gqe_matrix.json`.
- `quantum/adapt/kernel.py` + `smoke.py` — Guppy sources (native CX vs H-CZ-H expansion), 512-shot Quest run, `adapt_gqe_selene.json`.
- `src/data/demos/adapt_gqe_composed.json` + `src/routes/nadarasa.g21.tsx` — merged dump and UI.
