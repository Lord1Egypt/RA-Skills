# Quantinuum hardware roadmap (as of July 2026)

Lookup table for citing hardware-generation capability without re-parsing the SoftBank/Quantinuum white paper each time. Use these numbers to say what a proposed circuit *can* realistically run on today vs. what needs waiting for.

Source: Quantinuum/SoftBank "Quantum Computing Frontiers" white paper, July 2026, §5, Tables 5.1 and 5.2.

## Generations

| Generation | Year (target) | Physical qubits (order of magnitude) | Physical 2Q error `p_phys` | Logical error `p_L` (achievable) | Code distance `d` |
| --- | --- | --- | --- | --- | --- |
| **Helios** | Current (2025–2026) | ~100 (98 on Helios) | ~10⁻³ | ~10⁻³ | 3–5 |
| **Sol** | 2027 | ~few×10² | | ~10⁻⁴ | 5–7 |
| **Apollo** | 2029 | ~10³ | | ~10⁻⁷ | 7–9 |
| **Lumos** | 2030+ | 10⁴+ | | ≤10⁻¹⁰ | Chemical accuracy achievable |

## Executable chemistry envelope (spin orbitals)

| Generation | Physical / QED | Logical (FTQC) | Representative use case |
| --- | --- | --- | --- |
| Helios | ~50 (subspace methods, dynamics) | ~10 (early QPE / T-gate benchmarks, Steane [[7,1,3]]) | Small-molecule excited-state PoC (e.g. ethylene at CI) |
| Sol | ~100 (QED with high rejection) | ~10 (toy QPE, small active space, logical stabilization) | Limited excited-state applications |
| Apollo | ~100 (QED or pFT) | ~100 (excited-state QPE) | Medium-scale materials modeling |
| Lumos | N/A (fully logical era) | 100+ (chemical accuracy, scalable workflows) | Integrated materials discovery |

## Executable TDA envelope (graph size)

| Generation | Graph regime | Notes |
| --- | --- | --- |
| Helios | Complete k-partite `K(m, k)` with `k·m < 90` | Error mitigation on noisy qubits; structured validation only |
| Sol | ~100 nodes, ~30 moment steps | Early advantage demos on generic graphs; integration with QEC codes |
| Apollo | 100–300 nodes | Structured real-world approximations; commercial pilot |
| Lumos | Hundreds to thousands | Production quantum-enhanced graph analytics |

## Non-Clifford gate budgets by generation

Cliff+T synthesis via Ross–Selinger typically costs ~`3 log₂(1/ε_synth) + 9` T gates per arbitrary rotation. For representative circuits:

- **Helios**: T-count budgets in the ~10²–10³ range per shot are realistic under pFT + RGT (see `references/encoded-circuits.md`). Avoid full magic-state distillation.
- **Apollo**: T-count ~10⁷ per shot for medium graphs (see `references/laplacian-moments-tda.md`) becomes feasible with full FT + distillation.
- **Lumos**: T-count ~10⁹+ per shot for real-world data-scale TDA; the crossover to end-to-end quantum-advantage workloads.

## Guidance rules

1. If a proposed circuit needs `p_L ≲ 10⁻⁴` with 100+ logical qubits, it is a **Sol-or-later** proposal — mark it as such rather than promising Helios feasibility.
2. If a proposed chemistry model needs >10 spin orbitals *at the logical level*, it is **Apollo-or-later** for FTQC execution. Physical/QED runs may reach ~50 orbitals today but with `P_succ ~ e^{-p·N}` shot overhead.
3. If a graph-TDA proposal needs `n > 100` on generic (non-k-partite) graphs, it is **Sol-or-later**.
4. Ethylene-scale (2-qubit tapered) chemistry benchmarks are **Helios-today** — the pFT Steane demo already ran there.
5. WL-indistinguishable-but-Laplacian-distinguishable synthetic datasets (see `references/laplacian-moments-tda.md`) are **Helios-today** at the K(m,k) < 90 scale.

## What the roadmap does NOT tell you

- Actual availability slots on H2 / Helios hardware (governed by cloud queue, not the roadmap).
- Connectivity constraints (Quantinuum ions are all-to-all in principle but transport time scales with qubit count — this is where the memory-noise budget lives).
- The mix of managed vs. BYO magic-state factories at each generation.
- Any calendar guarantee — treat the years as targets, not commitments.

## What is actually reachable today (Nexus account, Aug 2026)

The roadmap above is capability planning. For "can I submit this tonight", the live backend
list is narrower:

Verified against a live `qnexus` 0.48.2 session (`qnx.devices.get_all()`), 2026-08-21:

| Target | `backend_name` / `device_name` | Status |
| --- | --- | --- |
| `H1-1LE`, `H2-1LE` (noiseless) | `Quantinuum` / `H1-1LE`, `H2-1LE` | available — the default real-stack sanity leg |
| `H1-Emulator`, `H2-Emulator` | `Quantinuum` / `H1-Emulator`, `H2-Emulator` | available — noise-ladder workhorse with `noisy_simulation=True`, ≤ ~17q and/or ≤ 2048 shots |
| `Helios-1E-lite` | `Helios-1E-lite` / `None` | available, but requires **`HeliosConfig`** (not `QuantinuumConfig`); it is listed as a *backend name*, so there is no `device_name` to pass |
| `Aer`, `AerState`, `AerUnitary` | `aer_simulator*` | available — the independent-simulator leg of a multi-leg proof, hosted by Nexus (no local Qiskit install needed) |
| `Braket` / `sv1`, `Qulacs`, `Selene`, `SelenePlus` | — | available; `Selene`/`SelenePlus` are the same emulator we run locally, submitted through Nexus |
| `H1-1`, `H2-1`, `H2-1SC` (real QPU / cluster) | — | **absent from the device list** on this account — no hardware submission surface, and `H2-1SC` is also the QIR execution target |

Sol / Apollo / Lumos are roadmap generations with no submission surface. Cite them as
capability horizons, never as somewhere a circuit was run. Full submission mechanics in
`references/nexus-jobs.md`.
