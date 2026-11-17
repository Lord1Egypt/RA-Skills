# Laplacian moments for quantum-enhanced TDA

Quantum-computed topological features for graph ML. Use this whenever the user asks about quantum + graphs, fraud/anomaly detection, or "quantum TDA beyond Betti numbers".

Source: Quantinuum/SoftBank "Quantum Computing Frontiers" white paper, July 2026, §4.

## The observable

For the `k`-th combinatorial (Hodge) Laplacian `Δ_k = ∂_{k+1}·∂_{k+1}† + ∂_k†·∂_k` on a simplicial complex, the **d-th Laplacian moment** is:

```
T_k^(d) = Tr((I − Δ_k)^d)
```

Interpretation: `(I − Δ_k)^d` is d-hop diffusion on k-simplices; the trace is its total self-correlation. Small `d` emphasizes local structure; large `d` emphasizes global structure. In the limit `d → ∞`, only the zero-eigenvalue subspace survives, so `T_k^(d) → β_k` (the k-th normalized Betti number).

**Why finite-d beats Betti.** Betti numbers are coarse: distinct structures often share identical Betti signatures. Finite-`d` moments interpolate between local and global, capturing **mesoscopic** correlation that fraud/anomaly labels may depend on but WL-hash / vanilla GNN aggregation cannot see.

## The hybrid pipeline

Standard shape (quantum-HPC-AI):

1. For each graph node, extract its `r`-hop ego-graph.
2. Quantum computes the moment sequence `(T_k^(1), T_k^(2), …, T_k^(d))` for that ego-graph.
3. Attach the moment vector as **node features** to the GNN input.
4. Train the GNN classically on HPC infrastructure.

This is a feature-extractor architecture — no direct quantum ML, no barren plateaus, no data-loading bottleneck. The GNN learns per-class weightings across moment orders automatically.

## Executable envelope

Resource estimates from the white paper for 50 blocks of the algorithm on graphs whose complement edges scale as `n²/20` and max complement degree as `n/20`, compiled to Clifford+T via GRIDSYNTH at `1e-10` whole-circuit accuracy:

| Vertices `n` | T-gate count | T-gate depth |
| --- | --- | --- |
| 10² | 5 × 10⁵ | 1 × 10⁵ |
| 10³ | 1 × 10⁷ | 5 × 10⁵ |
| 10⁴ | 3 × 10⁹ | 1 × 10⁸ |

For structured complete-k-partite graphs `K(m, k)`, aggressive optimization brings this down to <4000 two-qubit gates for up to 15 moment steps on `k·m < 90`, which fits on current Helios.

## The canonical synthetic dataset

WL-indistinguishable-but-Laplacian-distinguishable graph pair, useful as a proof-of-concept that Laplacian features carry information vanilla GNNs cannot see:

- **Graph A**: circulant `C(km, {1, …, (m−1)/2})` on `km` nodes.
- **Graph B**: `k` disjoint cliques `K_m`.

Both have identical 1-hop neighborhood structure → WL-indistinguishable → GNNs classify at chance (50%). They differ in Betti-0 (components) and Betti-1 (loops).

To push the topological difference to **arbitrary high moment order** (making the discriminator provably non-classical for large `d`), take the **graph complements**:

- Complement of A: complete k-partite `K(m, k)` (many holes, complex homology).
- Complement of B: still `k` disjoint cliques after complement transform.

Complement keeps them WL-indistinguishable, makes them Laplacian-moment distinguishable, and — via "suspension" — pushes the discriminating information to arbitrary high `k`. The paper reports 100% vs 50% accuracy on this construction.

## Real-world hook: fraud detection

The white paper motivates this pipeline via International Revenue Share Fraud (IRSF) in telecom:

- 2023 global losses: **$38.95B** (CFCA).
- 1% detection improvement ≈ $390M in prevented loss.
- Fraud signatures often modify **intermediate-scale** correlation structure (small groups of accounts) without altering global topological invariants → exactly the regime where finite-`d` Laplacian moments beat Betti summaries.

For real-graph target sizes, the paper observed 2-hop ego-graphs of 10 to 2×10⁴ vertices in telecom data — which maps directly onto the resource-estimate table above and places the crossover into early fault-tolerant hardware (Sol/Apollo generation; see `references/hardware-roadmap.md`).

## Implementation notes for a Guppy/Selene demo

- Start with complete `k`-partite graphs where the ground truth `T_k^(d)` is analytically known (Berry et al.). Any deviation is a bug in the circuit, not a discovery.
- The block-encoding of `(I − Δ_k)` requires a signed incidence oracle for `∂_k`; write it as a controlled sequence of Pauli products in Guppy.
- Cache moment values per `(graph, k, d)` under `_cache_lm/<hash>.json` — sweeps over many graphs benefit from the same resumable-cache pattern used for noise-2q (see `references/sweep-runner.md`).
- Ship results as static JSON, not through a server function (see `references/selene-runtime.md` §Shipping results).

## Worked implementation (G18, this repo)

`quantum/tda/{dataset,moments,sweep}.py` + `/nadarasa/g18`, data at
`src/data/demos/tda_laplacian_moments.json`.

Smallest honest instance: **C6 (6-cycle) vs 2C3 (two triangles)** — same V, E
and all-degree-2 colouring, so 1-WL stabilises immediately. Exact Laplacian
moments agree at `T1 = 12`, `T2 = 36`, diverge at `T3 = 120 vs 108`.

Estimator: instead of block-encoding `(I − Δ)^d`, measure the **propagator
trace** `f(τ) = tr(e^{-iHτ})/N` with `H = Δ / λ_max`, then fit the truncated
Taylor series `f(τ) = Σ (-iτ)^k m_k / k!` for the moments. Cheaper, and the
same data yields every `k` at once.

- Pad Δ to `2^n`, Pauli-decompose (20-22 terms for these graphs), Trotterise
  (3 steps → trace error ~8e-4, well below shot noise).
- Hadamard test on 1 ancilla + n system qubits gives `Re⟨x|U|x⟩`; insert `sdg`
  on the ancilla before the closing `h` for the imaginary part.
- At n ≤ 3, sweep **all** `2^n` basis states deterministically and average —
  cheaper than a purification register and removes state-prep variance.

### Fit conditioning is the whole game

Tune the design offline against simulated binomial noise BEFORE spending
emulator time. Measured on this pair at 4096 shots/circuit:

| τ grid | order | σ(T3) |
| --- | --- | --- |
| 12 pts, 0.5–3.5 | 6 | 2.5 (biased low by ~8) |
| 12 pts, 0.5–3.5 | 8 | 8.2 |
| 12 pts, 0.5–4.5 | 8 | 4.2 |

Truncation order and τ range move σ by ~4x; shot count only moves it as
`1/√shots`. Report BOTH a low-order (low-variance, biased) and a high-order
(near-unbiased, high-variance) fit — a low-order truncation silently
reassigns the discrepancy to the highest fitted moment.

### Report a model-free verdict first

Fitted moments are a lossy summary. Subtract the two measured trace curves
point by point and χ²-test them against the binomial point error
`√2 / √(2^n · shots)`. On this pair that gives χ²/dof ≈ 110 (max point 24σ),
a decisive separation, while the per-moment T3 test at fit order 8 is
inconclusive on the same data.

### Cost budgeting

`n_graphs × n_τ × 2^n × 2 parts` circuits. The G18 grid is 384 circuits at
~4 s each ≈ 30 min — far past one sandbox command. Cache per circuit
(`_cache_tda/<graph>_t<τ>_b<basis>_<part>_s<shots>.json`) and drive it from a
background resume loop; poll the cache-file count rather than blocking.
