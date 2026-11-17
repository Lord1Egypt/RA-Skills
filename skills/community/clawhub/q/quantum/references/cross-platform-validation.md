# Cross-platform validation and error mitigation hierarchies

Reading note from Leviatan et al. 2026 (arXiv:2607.24937), the 74-qubit heavy-hex Floquet Ising magnet executed on IBM Heron r3 and corroborated on Quantinuum H2 and Helios. This file captures the validation hierarchy so future Guppy/Selene experiments can reuse the same structure at smaller scale.

## QESEM in one line

QESEM (Quantum Error Spectrum Extrapolation Method) is a unified software framework that characterizes the noise once with a quasiprobability model and then runs two conceptually different estimators from the same data:

- **QESEM-Unbiased** — Probabilistic Error Cancellation (PEC). Gives an unbiased ideal expectation value at higher sampling cost.
- **QESEM-Extrapolated** — Zero-Noise Extrapolation (ZNE). Noise-amplified circuits are extrapolated back to zero noise; usually lower cost but more heuristic.

When the two estimators overlap in time and agree, the result is protected against a single mitigation failure mode.

## Validation hierarchy

A single number from a noisy QPU is not enough. The paper builds reliability in four layers, from weakest to strongest:

1. **Noise model is validated on the device itself.**
   The characterized model is checked against independent calibration data, so the mitigation does not rest on a fit that was never tested.

2. **Two independent mitigation estimators agree.**
   PEC and ZNE are different mathematics and different assumptions. Agreement where they both have signal is a strong internal consistency check.

3. **Classical comparison where converged.**
   Exact state-vector, small tensor-network, PEPS-BP, or sparse Pauli-path checks are used wherever they converge. In the Floquet paper, both PEPS-BP and sparse Pauli-path fail to converge at the 74-qubit, late-cycle regime, so the quantum data stands alone there.

4. **Cross-platform corroboration.**
   Selected circuits are re-run on a different hardware platform with a different noise model and a different compiler. Agreement on the extrapolated observable is the strongest reliability layer because it rules out platform-specific artefacts.

## Mapping to the Nadarasa G16–G18 experiments

The same hierarchy is already present in the repo, just at smaller scale:

| Hierarchy layer | Leviatan et al. | Nadarasa equivalent |
|---|---|---|
| Ideal benchmark | Exact state-vector / small TN | G16 noiseless QPDE gap fit (`quantum/qpde/sweep.py`) |
| Noise model | QESEM characterized noise model | G17 depolarizing ladder anchored on H2 rates (`quantum/qpde/noise.py`) |
| Extrapolation | QESEM-Extrapolated (ZNE) | G17 Richardson ZNE on the noise ladder |
| Independent estimator | QESEM-Unbiased (PEC) | G18 model-free curve χ² vs Taylor-fit moments (`quantum/tda/sweep.py`) |
| Cross-platform | IBM Heron ↔ Quantinuum H2/Helios | Open — Selene only, no hardware cross-check yet |

## Practical takeaways for Guppy/Selene work

- **Budget for at least two independent checks.** A noise ladder plus a model-free curve check (G17 + G18) is already stronger than either alone. If you can add a second mitigation estimator (e.g. PEC alongside ZNE), do it.
- **Cross-platform is the strongest layer.** If a result is meant to be believed beyond classical reach, re-run the core circuit on a different emulator or, ideally, a different hardware family. The compiler and noise model should be independent.
- **Selene limits.** Selene currently ships `IdealErrorModel`, `DepolarizingErrorModel`, and `SimpleLeakageErrorModel`. It does not expose the full QESEM stack, but the G17 ladder + ZNE is the closest available analog.

## Worked shape: a five-engine agreement table

The concrete form a corroboration claim should take — one metric, five
independent engines, every cell inside its own envelope:

| Engine | Kind | Value |
| --- | --- | --- |
| Exact oracle | NumPy statevector, no sampling | 0.3643 |
| Selene | local emulator, Quest | 0.395 (±0.125 at 512 shots) |
| H2-1LE | Nexus noiseless local emulator | 0.3867 |
| Helios-1E-lite | Nexus Helios emulator | 0.3447 |
| Aer | third-party simulator, independent codebase | 0.3540 |

What makes this table load-bearing rather than decorative:

- The **oracle row is not sampled**, so it fixes the target the other four are
  scored against; the sampled rows carry the `4*sqrt(0.5/shots)` envelope.
- **Aer is a different codebase entirely** — it shares no compiler, no noise
  model, and no vendor with the Quantinuum lanes. Two Quantinuum emulators
  agreeing is much weaker evidence than one Quantinuum lane agreeing with Aer.
- Every sampled row carries its **job id and seed**, so the table is a receipt
  chain and not a screenshot.
- **Device reachability is account-scoped.** A lane another project fills
  routinely can still return `You do not have access to this machine (code: 14)`
  on your account. Report the unreachable lane with its real error rather than
  quietly shipping a four-engine table as a five-engine one.

## Shot noise vs genuine classical equivalence

When a quantum metric fails to beat a classical baseline, there are two very
different explanations, and the shot-scaling ladder separates them: run the
identical comparison at 128, 512 and 2048 shots.

- Metric **improves monotonically** with shots → shot-noise-limited; more shots
  is the honest ask.
- Metric is **flat** across the ladder and the paired-bootstrap CIs cross zero →
  **classically equivalent**. No shot budget recovers an advantage, and saying
  "needs more shots" is wishful.

Pair the ladder with **matched splits**: both the quantum and the classical
model see identical folds/features, and the comparison is a paired bootstrap on
the difference, not two independently quoted numbers. Full discipline in
`evidence-integrity.md`.

- **Heavy-hex vs all-to-all.** IBM's heavy-hex geometry lets ZZ layers run in parallel in one native gate layer. Quantinuum's trapped-ion architecture is all-to-all but has different gate times and crosstalk. A future cross-platform Floquet test on Guppy/Selene would need to check that the schedule does not blow up in depth after routing.


## Worked example: Gate 0.5.1b, one circuit set, three submission paths

Five circuits (QPDE, Simon raw/reduced, Floquet, discharge QUBO) scored against a fixed
Selene baseline on three Nexus lanes, 15/15 cells populated, 0.0000 HQC billed:

| Lane | Config | Submission path | Result type |
| --- | --- | --- | --- |
| Selene (local) | — | Guppy program → emulator builder | `entries` per shot |
| `H2-1LE` | `QuantinuumConfig`, noiseless | **HUGR upload**, no compile job | tagged entries |
| `H2-Emulator` | `QuantinuumConfig(noisy_simulation=True)` | pytket circuit → `start_compile_job` → execute | `BackendResult` distribution |
| `Helios-1E-lite` | `HeliosConfig(system_name=…, emulator_config=…)` | HUGR upload, no compile job | `QsysResult` |

The lesson is not the pass table — it is that **the same circuit needed three different
submission paths and two different result decoders**. A cross-platform harness that assumes
one path per vendor will report a config failure as an unreachable device; here that
misdiagnosis cost a whole lane until `system_name` was traced. Keep the decode step behind a
per-lane adapter, and make an unpopulated cell carry its real error string into the dump.


## References

- Leviatan et al., "Resolving Structure in Prethermal Floquet Dynamics with Precision Quantum Computation", arXiv:2607.24937 (2026).
- Nadarasa G17 route: `/nadarasa/g17` — QPDE under depolarizing noise + ZNE.
- Nadarasa G18 route: `/nadarasa/g18` — Laplacian moments with model-free curve check.
- Nadarasa G19 route: `/nadarasa/g19` — this reading note in the app.
