#!/usr/bin/env python3
"""Lightweight digit-classification demo using UnifiedQuantum.

This file keeps the historical ``mnist_classifier.py`` name, but the
current example is intentionally smaller and easier to run:

- loads the scikit-learn digits dataset
- keeps only digits 0 and 1
- angle-encodes 4 PCA features into a 4-qubit circuit
- extracts simple quantum features in parallel with ``batch_execute``
- trains a classical logistic regression head

Requirements:
    pip install "unified-quantum[simulation]" scikit-learn
"""

from __future__ import annotations

import argparse

import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from uniqc.analyzer import calculate_expectation
from uniqc.circuit_builder import Circuit
from uniqc.pytorch import batch_execute


def require_simulation() -> None:
    try:
        from uniqc.task.optional_deps import check_simulation
    except ImportError:
        check_simulation = lambda: False

    if not check_simulation():
        raise RuntimeError(
            "This example needs local simulation. Install unified-quantum[simulation] first."
        )


def load_binary_digits(max_samples: int) -> tuple[np.ndarray, np.ndarray]:
    dataset = load_digits()
    mask = np.isin(dataset.target, [0, 1])
    data = dataset.data[mask]
    target = dataset.target[mask]

    if max_samples > 0:
        data = data[:max_samples]
        target = target[:max_samples]

    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    pca = PCA(n_components=4)
    reduced = pca.fit_transform(data)

    min_value = reduced.min()
    max_value = reduced.max()
    encoded = (reduced - min_value) / (max_value - min_value + 1e-12) * np.pi

    return encoded, target


def build_encoding_circuit(sample: np.ndarray) -> Circuit:
    circuit = Circuit(4)

    for qubit, angle in enumerate(sample[:4]):
        circuit.ry(qubit, float(angle))

    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)
    circuit.measure(0, 1, 2, 3)
    return circuit


def extract_quantum_features(samples: np.ndarray) -> np.ndarray:
    from uniqc.simulator import OriginIR_Simulator

    simulator = OriginIR_Simulator(backend_type="statevector")
    circuits = [build_encoding_circuit(sample) for sample in samples]

    def executor(circuit: Circuit) -> np.ndarray:
        probabilities = simulator.simulate_pmeasure(circuit.originir)
        probs = {
            format(index, "04b"): float(value)
            for index, value in enumerate(probabilities)
            if float(value) > 1e-12
        }
        return np.array(
            [
                calculate_expectation(probs, "ZIII"),
                calculate_expectation(probs, "IZII"),
                calculate_expectation(probs, "IIZI"),
                calculate_expectation(probs, "IIIZ"),
            ]
        )

    features = batch_execute(circuits, executor, n_workers=4)
    return np.vstack(features)


def main() -> None:
    parser = argparse.ArgumentParser(description="Binary digit classification with quantum features")
    parser.add_argument("--max-samples", type=int, default=200)
    parser.add_argument("--test-size", type=float, default=0.25)
    args = parser.parse_args()

    require_simulation()

    x, y = load_binary_digits(args.max_samples)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=args.test_size, random_state=42, stratify=y
    )

    train_features = extract_quantum_features(x_train)
    test_features = extract_quantum_features(x_test)

    model = LogisticRegression(max_iter=500)
    model.fit(train_features, y_train)
    predictions = model.predict(test_features)

    print("Quantum feature extraction completed.")
    print(f"Train samples: {len(x_train)}")
    print(f"Test samples: {len(x_test)}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    main()
