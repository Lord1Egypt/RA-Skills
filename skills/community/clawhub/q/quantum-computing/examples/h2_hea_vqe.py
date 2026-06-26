#!/usr/bin/env python3
"""Minimal H2-style VQE workflow with HEA.

This example uses a reduced two-qubit Hamiltonian to demonstrate the
current UnifiedQuantum variational workflow:

1. build an ansatz with ``hea()``
2. simulate probabilities locally
3. evaluate expectation values with ``calculate_expectation()``
4. optimize with SciPy

It is intentionally lightweight and should be read as a workflow template,
not as a complete quantum-chemistry stack.
"""

from __future__ import annotations

import argparse
from typing import Iterable

import numpy as np
from scipy.optimize import minimize

from uniqc.algorithmics.ansatz import hea
from uniqc.analyzer import calculate_expectation


REDUCED_H2_TERMS: list[tuple[float, str]] = [
    (-1.052373245772859, "II"),
    (0.39793742484318045, "ZI"),
    (-0.39793742484318045, "IZ"),
    (-0.01128010425623538, "ZZ"),
]


def probability_dict(probabilities: Iterable[float], n_qubits: int) -> dict[str, float]:
    return {
        format(index, f"0{n_qubits}b"): float(value)
        for index, value in enumerate(probabilities)
        if float(value) > 1e-12
    }


def build_energy_function(depth: int):
    try:
        from uniqc.task.optional_deps import check_simulation
    except ImportError:
        check_simulation = lambda: False

    if not check_simulation():
        raise RuntimeError(
            "This example needs local simulation. Install unified-quantum[simulation] first."
        )

    from uniqc.simulator import OriginIR_Simulator

    simulator = OriginIR_Simulator(backend_type="statevector")
    n_qubits = 2

    def energy(params: np.ndarray) -> float:
        circuit = hea(n_qubits=n_qubits, depth=depth, params=params)
        probabilities = simulator.simulate_pmeasure(circuit.originir)
        probs = probability_dict(probabilities, n_qubits)

        total = 0.0
        for coefficient, pauli in REDUCED_H2_TERMS:
            if pauli == "II":
                total += coefficient
            else:
                total += coefficient * calculate_expectation(probs, pauli)
        return float(total)

    return energy


def main() -> None:
    parser = argparse.ArgumentParser(description="Reduced H2-style HEA VQE demo")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=100)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    np.random.seed(args.seed)

    energy = build_energy_function(args.depth)
    n_params = 2 * 2 * args.depth
    x0 = np.random.uniform(0.0, 2 * np.pi, size=n_params)

    result = minimize(
        energy,
        x0=x0,
        method="COBYLA",
        options={"maxiter": args.maxiter},
    )

    print("Reduced H2-style VQE")
    print("-" * 60)
    print(f"Depth: {args.depth}")
    print(f"Initial energy: {energy(x0):.8f}")
    print(f"Optimized energy: {result.fun:.8f}")
    print(f"Iterations: {result.nfev}")
    print(f"Best parameters: {result.x}")


if __name__ == "__main__":
    main()
