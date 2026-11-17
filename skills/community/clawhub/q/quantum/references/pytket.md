# pytket / TKET compile lane

TKET is Quantinuum's compiler. Use it as a **second, independent optimiser**
next to the Guppy v1 / Selene path — never as a replacement for the emulator
evidence, and never as a source of gate counts that have not been proved
semantics-preserving.

Reference implementation: `quantum/tket/` (G24), route `/nadarasa/g24`,
data `src/data/demos/tket_compile.json`.

## Install

```
pip install --target .pydeps pytket pytket-quantinuum
```

Pure-Python wheels; they coexist with `guppylang>=1.0` in the same `.pydeps`
prefix. Note `.pydeps` is gitignored, so a fresh sandbox has **neither** guppy
nor pytket — reinstall from `quantum/requirements.txt` before any driver run.

## Offline compilation — no credentials, no HQCs

```python
from pytket.extensions.quantinuum import QuantinuumAPIOffline, QuantinuumBackend

be = QuantinuumBackend(device_name="H2-2", api_handler=QuantinuumAPIOffline())
compiled = be.get_compiled_circuit(circuit, optimisation_level=2)
```

- `QuantinuumAPIOffline().get_machine_list()` returns **dicts**, not objects:
  read `m["name"]` (`H1-1`, `H2-1`, `H2-2`). `m.device_name` raises.
- Offline mode compiles and rebases only. Nothing is submitted, so this is safe
  to run in any sandbox and costs nothing.
- Native gate set: `PhasedX`, `Rz`, `ZZPhase`, `ZZMax` (plus `TK2` and the
  classical ops). Level 0 is rebase-only and *already* reduces 2q counts on
  phase-type circuits, because CX–Rz–CX maps onto one `ZZPhase`. Do not report
  that as optimisation.

## Rule: equivalence oracle before any gate count

An optimiser that changes semantics looks like the best optimiser in the table.
Prove equality on the full state space, up to global phase, before scoring:

```python
overlap = np.trace(a.conj().T @ b)
phase = overlap / abs(overlap)
dist = np.linalg.norm(a - phase * b)   # accept at <= 1e-9
```

Build the comparison circuits **without measurement or reset** so
`Circuit.get_unitary()` works. Typical passing distance is ~1e-15.

**TKET drops idle wires.** A compiled circuit can have fewer qubits than its
source, which silently changes bitstring width and makes TVD read 1.0. Pad with
`circuit.add_blank_wires(n - circuit.n_qubits)` before comparing unitaries or
sampling.

## Round-tripping TKET output onto Selene

The native gate set has an exact image in `guppylang.std.qsystem`:

| TKET op   | Guppy call                            |
| --------- | ------------------------------------- |
| `PhasedX` | `phased_x(q, angle(a), angle(b))`     |
| `Rz`      | `rz(q, angle(a))`                     |
| `ZZPhase` | `zz_phase(q0, q1, angle(a))`          |
| `ZZMax`   | `zz_max(q0, q1)`                      |

Both sides use **half-turns**, so pytket `cmd.op.params` go straight into
`angle(...)` with no conversion (Gotcha #2 does not bite here). Render the
compiled circuit to Guppy source, load it, and sample through
`quantum.emulate.build(program).run_shots(Quest(), ...)`. Compare against the
exact distribution of the *source* circuit with a 4σ envelope,
`4*sqrt(0.5/shots)`.

## Scoring the comparison honestly

- Only score families where the reduced form is an **exact** rewrite. An
  approximation (e.g. AQFT band truncation) can never be found by a
  correctness-preserving compiler; scoring it as a win compares a compiler
  against a modelling decision.
- Report agreements as the headline. TKET independently reaching the same 2q
  count as the rewriter is external corroboration; the rewriter beating TKET is
  interesting only when the mechanism is nameable (G24: a non-local involution
  across commuting parity gates that a peephole window cannot see).

## Angles: half-turns on both sides, verifiable in one line

`Ry`, `Rz`, `ZZPhase` and friends take **half-turns** — the physics angle is
`param · π`, exactly Guppy's `angle()` convention. Never multiply by π when
porting a formula between the two stacks. Confirm empirically rather than from
memory:

```python
from pytket import Circuit
Circuit(1).Ry(0.5).get_unitary()      # a π/2 rotation, not a π/2-radian one
```

Any paper formula containing an explicit π: divide the π out before it reaches
either `angle()` or a pytket parameter.

## Online lane

Everything above is offline (`QuantinuumAPIOffline`) — no credentials, no HQCs.
For real emulator/hardware submission through Nexus (compile → execute the
compiled ref → `get_distribution()`, backend matrix, sizing limits, bit-order
calibration) see `references/nexus-jobs.md`.
