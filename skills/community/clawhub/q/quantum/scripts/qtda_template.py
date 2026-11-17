"""
Minimal Guppy + Selene smoke test.

Prepares two amplitude-encoded 2-qubit states, runs a 5-qubit SWAP test on
Selene, and prints the estimated fidelity. If this prints a number in [0, 1],
your Guppy + Selene install is working.

Run:
    pip install "guppylang>=1.0"
    python qtda_template.py
"""
from __future__ import annotations
import math

from guppylang import guppy
from guppylang.std.builtins import output
from guppylang.std.quantum import qubit, h, cx, ry, rz, measure, discard, t as tgate, tdg
from guppylang.std.angles import angle
from selene_sim import Quest


@guppy
def prep(q0: qubit, q1: qubit, a0: float, a1: float, a2: float) -> None:
    ry(q0, angle(a0))
    ry(q1, angle(a1))
    cx(q0, q1)
    rz(q1, angle(a2))


@guppy
def toffoli(c1: qubit, c2: qubit, t: qubit) -> None:
    h(t)
    cx(c2, t); tdg(t)
    cx(c1, t); tgate(t)
    cx(c2, t); tdg(t)
    cx(c1, t); tgate(c2); tgate(t)
    h(t)
    cx(c1, c2); tgate(c1); tdg(c2)
    cx(c1, c2)


@guppy
def cswap(c: qubit, a: qubit, b: qubit) -> None:
    cx(b, a); toffoli(c, a, b); cx(b, a)


# Two patients hard-coded — to parameterize, use the driver pattern
# (see references/driver-pattern.md).
A = [0.10 * math.pi, 0.15 * math.pi, 0.20 * math.pi]
B = [0.55 * math.pi, 0.48 * math.pi, 0.40 * math.pi]


@guppy
def program() -> None:
    anc = qubit()
    a0, a1 = qubit(), qubit()
    b0, b1 = qubit(), qubit()
    prep(a0, a1, 0.10 * 3.14159, 0.15 * 3.14159, 0.20 * 3.14159)
    prep(b0, b1, 0.55 * 3.14159, 0.48 * 3.14159, 0.40 * 3.14159)
    h(anc)
    cswap(anc, a0, b0)
    cswap(anc, a1, b1)
    h(anc)
    output("anc", measure(anc).read())
    discard(a0); discard(a1); discard(b0); discard(b1)


def main() -> None:
    shots = 2000
    res = (
        program.emulator(n_qubits=5)
        .with_shots(shots)
        .with_simulator(Quest())
        .run()
    )
    zeros = total = 0
    for shot in res:
        for _, val in shot.entries:
            total += 1
            if int(val) == 0:
                zeros += 1
    p0 = zeros / total
    fidelity = max(0.0, min(1.0, 2.0 * p0 - 1.0))
    print(f"shots={total}  P(0)={p0:.3f}  estimated fidelity={fidelity:.3f}")


if __name__ == "__main__":
    main()