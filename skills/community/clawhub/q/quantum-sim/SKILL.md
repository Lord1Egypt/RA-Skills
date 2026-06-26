SKILL.md:
---
name: quantum-sim
description: Simulate quantum circuits using a statevector engine. Supports up to 20 qubits with gates H, X, Y, Z, S, T, Rx, Ry, Rz, P, CX, CZ, SWAP. Built-in presets for Bell state, GHZ state, QFT, Grover search, and quantum teleportation. Accepts inline QASM-like syntax or a circuit file. Use when the user asks to simulate a quantum circuit, demonstrate quantum entanglement, run Grover search, apply quantum gates, show measurement probabilities, or explore quantum algorithms. Trigger phrases include "simulate quantum", "quantum circuit", "Bell state", "GHZ", "Grover", "QFT", "quantum gates", "qubit", "statevector", "superposition".
metadata: {"openclaw":{"emoji":":atom_symbol:","requires":{"bins":["python3"]}}}
---

# Quantum
 Circuit Simulator

Statevector-based quantum circuit simulator in pure Python 3 stdlib. No Qiskit, no pip install.
Optional: if numpy is installed, matrix ops run faster for larger qubit counts.

Simulates up to 20 qubits. Provides statevector output, measurement probability histograms,
and shot-based measurement sampling.

---

## Quick Start

    python3 {baseDir}/scripts/quantum_sim.py --list-presets
    python3 {baseDir}/scripts/quantum_sim.py --preset bell
    python3 {baseDir}/scripts/quantum_sim.py --preset ghz --qubits 5
    python3 {baseDir}/scripts/quantum_sim.py --preset grover
    python3 {baseDir}/scripts/quantum_sim.py --qasm "qubits 3; h 0; cx 0 1; cx 0 2"
    python3 {baseDir}/scripts/quantum_sim.py --preset bell --json

---

## Built-in Presets

Preset        | Qubits
 | Description
--------------|--------|--------------------------------------------------
bell          | 2      | Bell state (|00>+|11>)/sqrt(2) - max entanglement
ghz           | N      | GHZ state - N-qubit entanglement (use --qubits)
qft           | N      | Quantum Fourier Transform (use --qubits)
grover        | 2      | Grover search, marks |11>, 100% success rate
teleportation | 3      | Full quantum teleportation protocol

---

## Supported Gates

Single-qubit: H, X, Y, Z, S, T, Sdg, Tdg, Rx(theta), Ry(theta), Rz(theta), P(lambda)
Two-qubit:    CX (CNOT), CZ, SWAP

---

## QASM-like Syntax

Write one instruction per line (or semicolon-separated inline):

    qubits 3
    h 0
    cx 0 1
    cx 0 2
    rx 1.5708 0
    rz 3.1416 1
    measure 2048

Rules:
- First line must be: qu
bits N
- Gate names are case-insensitive
- Single-qubit gates: gate_name qubit_index
- Rotation gates: rx/ry/rz/p theta qubit_index  (theta in radians)
- Two-qubit gates: cx/cz/swap qubit1 qubit2
- Comments start with #

Save to a file and run:
    python3 {baseDir}/scripts/quantum_sim.py --qasm-file my_circuit.qasm

---

## All Flags

Flag              | Effect
------------------|-----------------------------------------------------
--preset NAME     | Run a built-in preset circuit
--qubits N        | Override qubit count for ghz/qft presets
--qasm "..."      | Inline QASM (semicolons separate instructions)
--qasm-file PATH  | Load circuit from a .qasm text file
--shots N         | Measurement shots (default 1024)
--json            | Output statevector + counts as JSON
--list-presets 
   | Show all presets with descriptions
--statevector-only| Skip measurement simulation

---

## Output Format

Each run prints:
1. Circuit summary (qubit count, gate sequence)
2. Statevector - complex amplitudes for all basis states with prob > 0.001
3. Measurement histogram - shot counts with ASCII bar chart

Example output for Bell state:
    === Bell state |Phi+>: maximally entangled 2-qubit state ===
    Qubits: 2   Dim: 4   Gates applied: 2
    Circuit: H(0) -> CX(0,1)

    Statevector:
      |00>  +0.7071+0.0000j  p=0.5000  [#########           ]
      |11>  +0.7071+0.0000j  p=0.5000  [#########           ]

    Measurement (1024 shots):
      |11>  [############            ]    532 ( 52.0%)
      |00>  [###########             ]    492 ( 48.0%)

---

## JSON Output

Use --json 
for machine-readable output (safe to pipe, no ANSI):
    python3 {baseDir}/scripts/quantum_sim.py --preset bell --json | python3 -c \
      "import json,sys; d=json.load(sys.stdin); print(d['probabilities'])"

JSON keys: label, n_qubits, gates, statevector (re/im per state), probabilities, counts, shots

---

## Physics Notes

- Qubit ordering: qubit 0 is least significant bit. |01> means q1=0, q0=1.
- Statevector size: 2^n complex numbers. Memory: 16 * 2^n bytes. 20 qubits = 16MB.
- Grover preset: 1 iteration on 2 qubits achieves 100% success for marked state |11>.
- QFT: includes bit-reversal swaps. Output is frequency-domain representation.
- Teleportation: simulates all 3 qubits unitarily (no mid-circuit measurement collapse).
- All rotation angles are in radians. pi/2 = 1.5708, pi
 = 3.1416.
