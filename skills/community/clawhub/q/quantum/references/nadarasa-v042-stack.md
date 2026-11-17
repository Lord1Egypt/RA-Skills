# Nadarasa v0.4.2 reference stack (G16–G19)

Four white-paper tracks reproduced or mapped in the Nadarasa notebook, arranged as a validation hierarchy. Use this as a template for structuring a multi-experiment Guppy/Selene release.

## The stack

| Gate | Track | What it is | Artifact |
|---|---|---|---|
| G16 | Ethylene QPDE | Ideal noiseless gap fit on the 2-qubit ethylene π/π* active space | `quantum/qpde/{model,kernel,sweep,validate}.py` → `src/data/demos/qpde_ethylene_selene.json` → `/nadarasa/g16` |
| G17 | QPDE under noise + ZNE | H2-class depolarizing ladder + Richardson extrapolation | `quantum/qpde/noise.py`, `quantum/qpde/zne.py` → `src/data/demos/qpde_ethylene_noise.json`, `qpde_ethylene_zne.json` → `/nadarasa/g17` |
| G18 | Laplacian-moment TDA | Propagator trace estimator separates C6 vs 2C3, a 1-WL-indistinguishable pair | `quantum/tda/{dataset,moments,sweep}.py` → `src/data/demos/tda_laplacian_moments.json` → `/nadarasa/g18` |
| G19 | Prethermal Floquet reading note | Cross-platform validation hierarchy from Leviatan et al. 2026 | `/nadarasa/g19` + `src/data/nadarasa/quantinuum-2026.ts` |

## Validation hierarchy mapping

The same four layers appear in both the Leviatan et al. Floquet paper and the G16–G18 experiments:

1. **Ideal benchmark / noise-model validation** → G16 noiseless QPDE + closed-form predictor.
2. **Noise + mitigation** → G17 depolarizing ladder + Richardson ZNE.
3. **Independent estimator** → G18 model-free curve χ² vs Taylor-fit moments.
4. **Cross-platform corroboration** → Open. Selene is the only platform currently in the wind tunnel.

## Operational lessons

- **Resumable caches are mandatory.** G18 is 384 circuits × 4096 shots ≈ 30 minutes of emulator time; `quantum/tda/sweep.py` writes one JSON per circuit under `_cache_tda/` so a sandbox reset only loses the in-flight circuit.
- **Angle hygiene in Guppy.** The QPDE evolution-time trick uses radians on paper but `angle()` in Guppy is halfturns; `t = π/(16 h₁)` becomes `rz(q, angle(1/16))`, not `angle(math.pi/16)` (which is the S gate). See `references/qpde.md` §Guppy angle-hygiene warning.
- **Aliasing controls are not fit data.** k = 8 in the ethylene QPDE puts `2φ` at π, where the signal is stationary and the arcsine branch is degenerate. Hold it out of the gap fit and report it separately. See `references/qpde.md` §k = 8 is an aliasing control.
- **Moment fits are conditioning-limited.** For Laplacian-moment TDA, the τ grid and truncation order move σ(T_k) by ~4×; quadrupling shots only halves it. Report a model-free curve verdict alongside the fitted moments. See `references/laplacian-moments-tda.md` §Fit conditioning is the whole game.
- **Ship static JSON, not live server functions.** The Lovable Cloudflare Worker stubs `child_process` and blocks arbitrary filesystem reads. Run Python in the sandbox, commit the JSON, and render a static view. See `references/selene-runtime.md` §Shipping results to the frontend.

## Next gates

- **Step C-2q:** ✅ completed in v0.4.4 — 90/90 cells PASS across 9 depolarizing/leakage levels including H2-2 rates; see `quantum/pqp_frontier/noise_2q.py` and `/nadarasa/proofs/noise-2q`.
- **Floquet native port:** heavy-hex Floquet cycle on Guppy/Selene, testing topology mapping to all-to-all.
- **ADAPT-GQE composition:** feed generated transformer/RL circuits into the rule-(N/M/P) canonicalisation pipeline.

## v0.4.4 addendum

Step C-2q used the same H2-2 noise parameters as G17 (`p_2q = 1.29e-3`, `p_1q = 1.29e-4`, `p_meas = 1.35e-3`) and extended them to 5× and 20× stress levels plus a leakage level. The 100% PASS rate at depol_h2 confirms rule (M) is sound under realistic H2-class gate and readout noise, not just ideal shots.


## References

- `references/qpde.md` — QPDE theory + worked G16 implementation.
- `references/laplacian-moments-tda.md` — quantum TDA + worked G18 implementation.
- `references/cross-platform-validation.md` — QESEM + four-layer validation hierarchy from G19.
- `references/sweep-runner.md` — resumable-cache pattern.
- `references/lovable-orchestration.md` — atomic gates and rollback protocol.
