# Encoded circuits: [[7,1,3]] Steane + partial fault-tolerance

Recipe for running non-Clifford logical rotations on H2-class hardware without paying full magic-state-distillation cost. This is the "partial fault-tolerant" (pFT) middle path between raw physical circuits and full FT + Clifford+T synthesis.

Source: Quantinuum/SoftBank "Quantum Computing Frontiers" white paper, July 2026, §3.6.

## The [[7,1,3]] Steane color code

- 7 physical qubits → 1 logical qubit, distance 3, corrects any single-qubit error.
- Cell-based stabilizers: each cell's 4 vertex qubits define one X-type and one Z-type generator.
- **All Clifford operations transverse** (bit-parallel physical gates realize the logical action). No overhead for `H̄, S̄, CNOT̄, Ȳ, Z̄, X̄`.
- The non-Clifford burden is entirely on `R̄_z(θ)` for arbitrary θ.

## Recursive Gate Teleportation (RGT) for logical R_z

Standard non-Clifford gadget:

```
|ψ⟩ ---●--- R_z(2θ) ---   →   R_z(θ)|ψ⟩   (on measurement outcome 0)
|θ⟩ ---⊕----- [measure Z] --      apply R_z(2θ) with sign-flipped angle on outcome 1
```

Pre-measurement state:

```
(R_z(θ)|ψ⟩ ⊗ |0⟩ + R_z(−θ)|ψ⟩ ⊗ |1⟩) / √2
```

- Outcome 0 (prob ½) → done, `R_z(θ)` applied.
- Outcome 1 → recursively apply the same protocol with `2θ` to fix the sign.

**Termination.** For an angle stored as an `n_b`-bit binary fraction `θ/π = b₀ + b₁/2 + … + b_{n_b}/2^{n_b−1}`, the recursion halts after **at most `n_b − 2` rounds**, because `R_z(2^{n_b−2}·θ)` reduces to a Clifford rotation which is transversal (no gadget needed).

Practical implication: choose rotation angles with as few binary-fraction bits as tolerable. 5-bit rounding of `h·t/π` is a good default when the raw Hamiltonian coefficients are only known to ~1e-4 accuracy anyway (see `references/qpde.md`).

## QEC-gadget insertion cadence

The white paper's pFT ethylene circuit uses this rule of thumb:

- Insert an **X-type Steane QEC gadget after every two applications of `u`** (the non-diagonal, single-qubit-rotation-bearing sub-block).
- Diagonal Clifford sub-blocks (`v = R_{Z₁Z₂}(3kπ/2)`) do not need a gadget after each application; batch them.

Rationale: memory-noise errors accumulate during the long idling periods created by nested RGT / QEC gadgets. Denser QEC hurts because it lengthens idle time; sparser QEC hurts because errors compound. Two-`u` cadence is the empirical sweet spot for H2-2 noise.

## Where the errors actually live

Under representative H2-2 emulator noise (see `references/selene-runtime.md` §Realistic H2 noise parameters), the pFT circuit budget breaks down as:

| Noise source | Decoherence parameter q (k=3, k=5) |
| --- | --- |
| Gate + readout error | 0.136, 0.224 |
| Coherent memory (with DD) | 0.120, 0.116 |
| Incoherent memory | 0.104, 0.160 |

Take-aways for future encoded-circuit design:

1. **Incoherent memory + gate/readout dominate** — order any noise-channel activation sweep to hit these first.
2. **Dynamical decoupling neutralizes coherent memory noise** even at `f = 4.3e-2 rad/s`. Always enable DD when transporting or idling encoded qubits.
3. Break-even against the physical baseline was **not** reached in this specific pFT setting — logical > NoQEC, but physical > logical. QEC helped over no-QEC, but the RGT + gadget-insertion overhead pushed the total budget above the raw physical circuit. Report this honestly when comparing pFT to physical baselines.

## When pFT is the right choice

- The circuit is mostly Clifford with a handful of small-angle rotations (e.g. QPDE with the evolution-time trick).
- Rotation angles admit a short binary-fraction representation (few RGT rounds).
- You want to avoid `T`-count blow-ups from Solovay–Kitaev / Ross–Selinger synthesis.

## When to skip pFT and use full FT

- Non-Clifford operations dominate the circuit (arbitrary-angle rotations in every layer).
- Rotation angles are irrational / high-precision (RGT recursion depth explodes).
- Target logical error rate `p_L ≲ 10⁻⁶` — full FT with magic-state distillation scales better past that budget (see `references/hardware-roadmap.md`, Apollo/Lumos generations).

## Read the encoding back out of the compiled circuit

Do not trust that the parity/detection rounds you wrote survived compilation. Run the
structural audit (`references/agent-native-evidence.md`, §Structural audit): the per-qubit
idle windows should show the parity cadence you intended, and any long ancilla idle band is
the dynamical-decoupling insertion point. A missing or merged cadence is a compiler
regression that otherwise only shows up as a quietly worse fidelity.
