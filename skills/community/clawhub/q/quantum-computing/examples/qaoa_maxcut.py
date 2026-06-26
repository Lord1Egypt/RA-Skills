#!/usr/bin/env python3
"""QAOA MaxCut demo aligned with the current qaoa_ansatz API."""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import minimize

from uniqc.algorithmics.ansatz import qaoa_ansatz


PRESET_GRAPHS = {
    "triangle": [(0, 1), (1, 2), (0, 2)],
    "square": [(0, 1), (1, 2), (2, 3), (3, 0)],
    "line3": [(0, 1), (1, 2)],
}


def require_simulation() -> None:
    try:
        from uniqc.task.optional_deps import check_simulation
    except ImportError:
        check_simulation = lambda: False

    if not check_simulation():
        raise RuntimeError(
            "This example needs local simulation. Install unified-quantum[simulation] first."
        )


def build_cost_hamiltonian(edges: list[tuple[int, int]]) -> list[tuple[str, float]]:
    return [(f"Z{i}Z{j}", -0.5) for i, j in edges]


def bitstring_cut_value(bitstring: str, edges: list[tuple[int, int]]) -> int:
    return sum(1 for i, j in edges if bitstring[i] != bitstring[j])


def expected_cut(probabilities: dict[str, float], edges: list[tuple[int, int]]) -> float:
    return sum(probability * bitstring_cut_value(bitstring, edges) for bitstring, probability in probabilities.items())


def main() -> None:
    parser = argparse.ArgumentParser(description="QAOA MaxCut demo")
    parser.add_argument("--graph", choices=sorted(PRESET_GRAPHS), default="triangle")
    parser.add_argument("--p", type=int, default=1)
    parser.add_argument("--maxiter", type=int, default=80)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    require_simulation()

    from uniqc.simulator import OriginIR_Simulator

    np.random.seed(args.seed)

    edges = PRESET_GRAPHS[args.graph]
    n_qubits = max(max(edge) for edge in edges) + 1
    cost_hamiltonian = build_cost_hamiltonian(edges)
    simulator = OriginIR_Simulator(backend_type="statevector")

    def objective(parameters: np.ndarray) -> float:
        betas = parameters[: args.p]
        gammas = parameters[args.p :]
        circuit = qaoa_ansatz(cost_hamiltonian, p=args.p, betas=betas, gammas=gammas)
        circuit.measure(*range(n_qubits))
        raw_probabilities = simulator.simulate_pmeasure(circuit.originir)
        probabilities = {
            format(index, f"0{n_qubits}b"): float(value)
            for index, value in enumerate(raw_probabilities)
            if float(value) > 1e-12
        }
        return -expected_cut(probabilities, edges)

    initial = np.random.uniform(0.0, np.pi, size=2 * args.p)
    result = minimize(
        objective,
        x0=initial,
        method="COBYLA",
        options={"maxiter": args.maxiter},
    )

    best_betas = result.x[: args.p]
    best_gammas = result.x[args.p :]
    final_circuit = qaoa_ansatz(cost_hamiltonian, p=args.p, betas=best_betas, gammas=best_gammas)
    final_circuit.measure(*range(n_qubits))
    final_raw_probabilities = simulator.simulate_pmeasure(final_circuit.originir)
    final_probabilities = {
        format(index, f"0{n_qubits}b"): float(value)
        for index, value in enumerate(final_raw_probabilities)
        if float(value) > 1e-12
    }

    print("QAOA MaxCut")
    print("-" * 60)
    print(f"Graph: {args.graph}")
    print(f"Edges: {edges}")
    print(f"Layers p: {args.p}")
    print(f"Best expected cut: {-result.fun:.6f}")
    print(f"Best betas: {best_betas}")
    print(f"Best gammas: {best_gammas}")

    print("\nTop bitstrings:")
    for bitstring, probability in sorted(final_probabilities.items(), key=lambda item: item[1], reverse=True)[:5]:
        print(
            f"  {bitstring}  prob={probability:.4f}  cut={bitstring_cut_value(bitstring, edges)}"
        )


if __name__ == "__main__":
    main()
