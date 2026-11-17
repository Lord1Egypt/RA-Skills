# Error-detected inner products (repetition-encoded SWAP test)

A cheap, near-term alternative to full QEC for the one primitive that dominates quantum
kernel methods: the state overlap `|⟨ψ|φ⟩|²`. Detection only — no correction — which is
exactly the right trade when you are allowed to throw shots away.

## Construction

1. **Encode each data qubit into a repetition pair**: `|0_L⟩ = |00⟩`, `|1_L⟩ = |11⟩`.
   Prepare with a rotation on the first physical qubit followed by a CNOT onto the second:

   ```python
   ry(a, angle(theta_halfturns))   # theta in HALFTURNS, as always
   cx(a, b)                        # now (a, b) hold the encoded logical amplitude
   ```

2. **Run the SWAP test at the logical level** — the ancilla-controlled swap acts on logical
   pairs, so each logical CSWAP becomes two physical CSWAPs (see
   `references/circuit-patterns.md` for the CSWAP decomposition).

3. **Measure every physical qubit**, not just the ancilla.

4. **Post-select**: keep only shots where each encoded pair measured **equal**
   (`00` or `11`). A single bit-flip inside a pair breaks the parity and is discarded.

5. Estimate the overlap from the accepted subset only, and report the accept rate alongside
   it.

## Accounting — report all three numbers

| Quantity | Meaning |
| --- | --- |
| `F_raw` | estimate over all shots, no post-selection |
| `F_det` | estimate over accepted shots |
| `F_ideal` | noiseless oracle value (NumPy statevector) |
| `accept` | accepted / total shots |

**Hard invariant: `F_det ≤ F_ideal`.** If a post-selected estimate exceeds the ideal value,
the accept mask or the bit ordering is wrong — see `references/nexus-jobs.md` (§Bit order).
Fix it before reporting; this is the cheapest available self-check.

## Observed behaviour

Recovery grows with circuit depth, because deeper circuits accumulate more detectable single
errors:

- shallow (~9 physical qubits): `F_det − F_raw ≈ +0.03`, accept ≈ 95%
- deep (~17 physical qubits, 4 encoded features): `F_det − F_raw ≈ +0.06`, accept ≈ 91%

Under a plain depolarizing model at device-scale `p ≈ 5e-3`, the recovery is larger still
(+0.19 at ~58% accept) — the density-matrix simulation is optimistic relative to a full
vendor error model, so use it for design, not for the headline.

The cost is shots: budget `n_shots / accept` to hold the same statistical envelope, and keep
the `4·√(0.5/shots_accepted)` threshold computed on the **accepted** count.

## Sizing

Encoding doubles the qubit count, and the SWAP test already doubles it. A 4-feature encoded
comparison lands around 17 physical qubits — which is exactly the noisy-emulator ceiling in
`references/nexus-jobs.md`. Plan the feature count backwards from that limit.

## When not to use it

- If you need an expectation value rather than an inner product, ZNE / PEC give more per shot
  (`references/cross-platform-validation.md`).
- If the dominant error is coherent memory rather than discrete flips, parity post-selection
  detects little; dynamical decoupling is the better lever
  (`references/selene-runtime.md`).
