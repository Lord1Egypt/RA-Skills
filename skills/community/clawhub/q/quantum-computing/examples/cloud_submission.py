#!/usr/bin/env python3
"""Programmatic cloud-task examples for UnifiedQuantum.

By default this script runs a dummy submission so it is safe for local
testing. Real backend examples are included as callable functions but are
not executed automatically.
"""

from __future__ import annotations

import argparse
from pprint import pprint

from uniqc import Circuit, query_task, submit_task, wait_for_result


def build_bell_circuit() -> Circuit:
    circuit = Circuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)
    circuit.measure(0, 1)
    return circuit


def print_result(result: dict | None) -> None:
    if not result:
        print("No result returned.")
        return

    print("Normalized result payload:")
    pprint(result)

    if "counts" in result:
        print("\nCounts:")
        pprint(result["counts"])

    if "probabilities" in result:
        print("\nProbabilities:")
        pprint(result["probabilities"])


def run_dummy_demo(shots: int) -> None:
    try:
        from uniqc.task.optional_deps import check_simulation
    except ImportError:
        check_simulation = lambda: False

    if not check_simulation():
        raise RuntimeError(
            "Dummy mode uses the local simulator. Install unified-quantum[simulation] first."
        )

    circuit = build_bell_circuit()
    task_id = submit_task(
        circuit,
        backend="originq",
        shots=shots,
        dummy=True,
        metadata={"example": "cloud_submission.py"},
    )

    print(f"Dummy task submitted: {task_id}")

    task_info = query_task(task_id)
    print(f"Cached task status: {task_info.status}")
    print(f"Cached backend tag: {task_info.backend}")

    result = wait_for_result(task_id, timeout=60)
    print_result(result)


def real_originq_example(shots: int) -> str:
    """Skeleton for a real OriginQ submission.

    Requires:
      1. pip install "unified-quantum[originq]"
      2. uniqc config set originq.token YOUR_TOKEN
    """

    circuit = build_bell_circuit()
    return submit_task(
        circuit,
        backend="originq",
        shots=shots,
        backend_name="origin:wuyuan:d5",
        metadata={"example": "real-originq"},
    )


def real_quafu_example(shots: int) -> str:
    """Skeleton for a real Quafu submission.

    Requires:
      1. pip install "unified-quantum[quafu]"
      2. uniqc config set quafu.token YOUR_TOKEN
    """

    circuit = build_bell_circuit()
    return submit_task(
        circuit,
        backend="quafu",
        shots=shots,
        chip_id="ScQ-P10",
        metadata={"example": "real-quafu"},
    )


def real_ibm_example(shots: int) -> str:
    """Skeleton for a real IBM submission.

    Requires:
      1. pip install "unified-quantum[qiskit]"
      2. uniqc config set ibm.token YOUR_TOKEN
    """

    circuit = build_bell_circuit()
    return submit_task(
        circuit,
        backend="ibm",
        shots=shots,
        metadata={"example": "real-ibm"},
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="UnifiedQuantum cloud submission demo")
    parser.add_argument("--shots", type=int, default=1000)
    args = parser.parse_args()

    run_dummy_demo(args.shots)

    print("\nReal backend entry points are available as helper functions:")
    print("  - real_originq_example(shots)")
    print("  - real_quafu_example(shots)")
    print("  - real_ibm_example(shots)")


if __name__ == "__main__":
    main()
