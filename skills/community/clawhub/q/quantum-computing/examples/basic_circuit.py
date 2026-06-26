#!/usr/bin/env python3
"""Basic UnifiedQuantum circuit example.

Builds a Bell circuit, prints both export formats, and tries a local
probability simulation when simulation dependencies are available.
"""

from __future__ import annotations

from pprint import pprint

from uniqc.circuit_builder import Circuit


def build_bell_circuit() -> Circuit:
    circuit = Circuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)
    circuit.measure(0, 1)
    return circuit


def try_local_simulation(circuit: Circuit) -> None:
    try:
        from uniqc.task.optional_deps import check_simulation
    except ImportError:
        check_simulation = lambda: False

    if not check_simulation():
        print("Local simulation skipped: install unified-quantum[simulation] first.")
        return

    from uniqc.simulator import OriginIR_Simulator

    simulator = OriginIR_Simulator(backend_type="statevector")
    probabilities = simulator.simulate_pmeasure(circuit.originir)

    print("\nState probabilities:")
    pprint(
        {
            format(index, f"0{simulator.qubit_num}b"): float(probability)
            for index, probability in enumerate(probabilities)
            if float(probability) > 1e-10
        }
    )


def main() -> None:
    circuit = build_bell_circuit()

    print("OriginIR")
    print("-" * 60)
    print(circuit.originir)

    print("\nOpenQASM 2.0")
    print("-" * 60)
    print(circuit.qasm)

    try_local_simulation(circuit)


if __name__ == "__main__":
    main()
