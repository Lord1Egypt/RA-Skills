# Quantinuum Guppy v1.0 & Selene Trapped-Ion Compilation

This reference provides the developer specification for writing, compiling, and simulating Quantum Krump circuits using Quantinuum's Guppy language (v1.0+) and the Selene emulator.

---

## 1. Guppy v1.0 Syntax & Requirements

Guppy is Quantinuum's Python-embedded quantum programming language that compiles directly into HUGR (Hierarchical Unified Generation Representation) control-flow graphs.

### Core Rules
1. **Source File Requirement**: `@guppy`-decorated functions MUST live in a real `.py` file on disk (`inspect.getsource` is required). Functions defined in REPLs or dynamic strings will fail.
2. **Angles are in Halfturns**: `angle(x)` takes values in halfturns ($\pi = 1.0$), NOT radians:
   - $S$ gate ($\pi/2$): `angle(0.5)`
   - $T$ gate ($\pi/4$): `angle(0.25)`
   - Pauli $Z$ ($\pi$): `angle(1.0)`
   - Arbitrary radian $\theta$: `angle(\theta / math.pi)`
3. **v1.0 API Signatures**:
   - `output(...)` replaces legacy `result(...)`.
   - `measure(q).read()` is required to extract classical bits.
   - Run through `program.emulator(n_qubits=N).with_shots(S).with_simulator(Quest()).run()`.

---

## 2. Trapped-Ion Native Gate Set Rebasing

Quantinuum H-series and Helios architectures utilize trapped ytterbium ($^{171}\text{Yb}^+$) or barium ($^{137}\text{Ba}^+$) ions with native laser-driven gates:

- **Single-Qubit Rotations**:
  - `PhasedX(alpha, beta)`: Rotation by $\pi \cdot \alpha$ around an axis in the equatorial plane oriented at angle $\pi \cdot \beta$.
  - `Rz(theta)`: Precise virtual $Z$-rotation performed via software phase shift.
- **Two-Qubit Entangling Gates**:
  - `ZZPhase(theta)`: Fully entangling or fractional phase gate $e^{-i (\pi \theta / 2) Z \otimes Z}$.
  - `ZZMax()`: Maximum entangling gate equivalent to $\theta = 0.5$.

### Translation from Krump Foundations
- `STOMP` (Opening Hadamard): `PhasedX(0.5, 0.5); Rz(1.0)`
- `JAB` (Pauli $X$): `PhasedX(1.0, 0.0)`
- `CHEST POP` (Pauli $Z$): `Rz(1.0)`
- `ARM SWING` ($R_x(\pi/2)$): `PhasedX(0.5, 0.0)`
- `DUET ENTANGLEMENT` (ZZ interaction): `ZZPhase(0.5)`

---

## 3. Selene Emulator Execution Pattern

```python
import math
from guppylang.decorator import guppy
from guppylang.module import GuppyModule
from guppylang.std.angles import angle
from guppylang.std.qsystem import (
    Qubit,
    measure,
    phased_x,
    rz,
    zz_phase,
)
from selene_sim import Quest, IdealErrorModel

module = GuppyModule("quantum_krump_kernel")

@guppy(module)
def krump_duet_circuit() -> tuple[bool, bool]:
    q0 = Qubit()
    q1 = Qubit()
    
    # Lead dancer stomp (Hadamard into kinetic superposition)
    phased_x(q0, angle(0.5), angle(0.5))
    rz(q0, angle(1.0))
    
    # Partner dancer responds (Entangled Duet via ZZ interaction)
    zz_phase(q0, q1, angle(0.5))
    
    # Rhythmic sync pop (Phase adjustment)
    rz(q0, angle(0.5))
    rz(q1, angle(0.5))
    
    # Terminal kill-off measurement
    b0 = measure(q0).read()
    b1 = measure(q1).read()
    return b0, b1

def run_simulation(shots: int = 1000):
    sim = module.emulator(n_qubits=2) \
                .with_shots(shots) \
                .with_simulator(Quest()) \
                .with_error_model(IdealErrorModel())
    results = sim.run()
    return results
```

---

## 4. Bell Control Discipline & Statistical Thresholds

Every simulation or hardware sweep MUST carry an accompanying known-fidelity Bell pair control $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$:

- **Anti-Correlated Shots**: Shots resulting in $|01\rangle$ or $|10\rangle$.
- **Statistical Acceptance Threshold**:
  $$\frac{\text{Anti-Correlated Shots}}{\text{Total Shots}} \le 4\sqrt{\frac{0.5}{\text{Shots}}}$$
- **Batch Rejection Rule**: If the Bell control fails this bound, the **entire batch is rejected and invalid**. Never report noisy, corrupt results as valid experimental evidence.
