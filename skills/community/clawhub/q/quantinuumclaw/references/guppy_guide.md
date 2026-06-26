# Guppy Quantum Programming Guide

Complete reference for programming with Quantinuum's Guppy language for quantum computing applications. This guide covers syntax, quantum gates, circuit construction, and best practices for the Selene backend integration.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Concepts](#basic-concepts)
3. [Quantum Gates](#quantum-gates)
4. [Circuit Construction](#circuit-construction)
5. [Measurement](#measurement)
6. [Advanced Patterns](#advanced-patterns)
7. [Examples](#examples)
8. [Integration with Selene](#integration-with-selene)

## Introduction

Guppy is Quantinuum's quantum programming language designed for expressing quantum algorithms in a clear, Pythonic syntax. It provides high-level abstractions for quantum circuit construction while allowing fine-grained control over quantum operations.

**Key characteristics:**
- Python-like syntax for quantum programming
- Native support for quantum gates and measurements
- Circuit composition and reuse
- Integration with classical Python control flow
- Target execution on Quantinuum quantum hardware or emulators

## Basic Concepts

### Quantum Context

All quantum operations must be within a quantum context:

```python
from guppy import quantum

with quantum() as q:
    # Quantum operations here
    q.h(0)  # Hadamard on qubit 0
    q.cx(0, 1)  # CNOT
    q.measure_all()
```

### Qubit Registers

Create named qubit registers for organization:

```python
with quantum() as q:
    # Allocate qubits
    qbits = q.qubits(4)  # Creates qubits[0], qubits[1], qubits[2], qubits[3]

    # Use them
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
```

### Classical Variables

Mix classical and quantum computation:

```python
from guppy import quantum, classical

with quantum() as q:
    n_qubits = 4

    # Classical variable
    shots = classical(1000)

    # Use in quantum context
    qbits = q.qubits(n_qubits)

    # Classical control
    if shots > 500:
        q.h(qbits[0])
```

## Quantum Gates

### Single-Qubit Gates

```python
# Pauli gates
q.x(qubit)     # Pauli-X (NOT)
q.y(qubit)     # Pauli-Y
q.z(qubit)     # Pauli-Z

# Hadamard (creates superposition)
q.h(qubit)

# Phase gates
q.s(qubit)     # S gate (phase π/2)
q.t(qubit)     # T gate (phase π/4)
q.sdg(qubit)   # S† (conjugate)
q.tdg(qubit)   # T†

# Rotation gates
q.rx(angle, qubit)  # Rotation around X axis
q.ry(angle, qubit)  # Rotation around Y axis
q.rz(angle, qubit)  # Rotation around Z axis

# Identity
q.i(qubit)
```

### Multi-Qubit Gates

```python
# CNOT (controlled-X)
q.cx(control, target)

# Controlled-Z
q.cz(control, target)

# Toffoli (CCNOT)
q.ccx(control1, control2, target)

# Swap
q.swap(qubit1, qubit2)

# Controlled rotation
q.crx(angle, control, target)
q.cry(angle, control, target)
q.crz(angle, control, target)
```

### Parameterized Gates

For variational quantum algorithms:

```python
def variational_layer(q, params, qubits):
    """Apply parametrized rotation gates"""
    for i, qubit in enumerate(qubits):
        q.rx(params[i*3], qubit)
        q.ry(params[i*3+1], qubit)
        q.rz(params[i*3+2], qubit)

    # Entangling layer
    for i in range(len(qubits)-1):
        q.cx(qubits[i], qubits[i+1])
```

## Circuit Construction

### Sequential Operations

Operations are applied sequentially:

```python
with quantum() as q:
    qbits = q.qubits(2)

    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
    q.h(qbits[1])
    q.measure(qbits[0], qbits[1])
```

### Reusable Subroutines

Define reusable circuit blocks:

```python
def bell_state(q, q0, q1):
    """Create a Bell state pair"""
    q.h(q0)
    q.cx(q0, q1)

with quantum() as q:
    qbits = q.qubits(4)
    bell_state(q, qbits[0], qbits[1])
    bell_state(q, qbits[2], qbits[3])
```

### Quantum State Preparation

Prepare specific quantum states:

```python
with quantum() as q:
    qbits = q.qubits(3)

    # Initialize in |000>
    # Create W state: (|001> + |010> + |100>)/√3
    q.x(qbits[2])
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
    q.cx(qbits[0], qbits[2])
    q.h(qbits[0])
```

## Measurement

### Measure All Qubits

```python
with quantum() as q:
    qbits = q.qubits(2)
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
    result = q.measure_all()  # Returns bitstring like "01"
```

### Measure Specific Qubits

```python
with quantum() as q:
    qbits = q.qubits(3)
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])
    q.cx(qbits[1], qbits[2])

    # Measure only some qubits
    measurements = q.measure([qbits[0], qbits[2]])
    # Returns dictionary: {qbits[0]: 0, qbits[2]: 1}
```

### Multiple Shots

Run circuit multiple times:

```python
with quantum() as q:
    qbits = q.qubits(2)
    q.h(qbits[0])
    q.cx(qbits[0], qbits[1])

    # Run 1000 shots
    results = q.execute(shots=1000)

    # Results is a histogram
    # {'00': 503, '11': 497}
```

## Advanced Patterns

### Quantum Phase Estimation

```python
def quantum_phase_estimation(q, unitary, precision_qubits):
    """Estimate phase of a unitary operator"""
    # Allocate registers
    phase_qubits = q.qubits(precision_qubits)
    state_qubits = q.qubits(1)

    # Prepare superposition on phase register
    for qubit in phase_qubits:
        q.h(qubit)

    # Apply controlled-unitary operations
    for i, qubit in enumerate(phase_qubits):
        for _ in range(2**(precision_qubits - i - 1)):
            q.cunitary(unitary, qubit, state_qubits)

    # Inverse QFT
    inverse_qft(q, phase_qubits)

    # Measure phase register
    return q.measure(phase_qubits)
```

### Variational Quantum Eigensolver (VQE)

```python
def vqe_circuit(q, hamiltonian, params):
    """VQE for finding ground state energy"""
    ansatz_qubits = q.qubits(hamiltonian.n_qubits)

    # Parameterized ansatz
    variational_layer(q, params, ansatz_qubits)

    # Measure expectation value
    return measure_hamiltonian(q, hamiltonian, ansatz_qubits)
```

### Quantum Fourier Transform

```python
def qft(q, qubits):
    """Quantum Fourier Transform"""
    n = len(qubits)
    for i in range(n):
        q.h(qubits[i])
        for j in range(i+1, n):
            angle = 2 * 3.14159 / (2**(j-i+1))
            q.crz(angle, qubits[j], qubits[i])
    # Swap qubits
    for i in range(n//2):
        q.swap(qubits[i], qubits[n-i-1])
```

## Examples

### Quantum Coin Flip

```python
from guppy import quantum

with quantum() as q:
    qbits = q.qubits(1)
    q.h(qbits[0])  # Create superposition
    result = q.measure_all()
    # result is "0" or "1" with 50% probability each
```

### Bell State (Entanglement)

```python
from guppy import quantum

with quantum() as q:
    qbits = q.qubits(2)
    q.h(qbits[0])     # |+> state
    q.cx(qbits[0], qbits[1])  # Entangle
    result = q.measure_all()
    # result is "00" or "11" (correlated)
```

### Grover's Search

```python
def grover_search(q, oracle, n_qubits, iterations):
    """Grover's algorithm for unstructured search"""
    qbits = q.qubits(n_qubits)

    # Initialize superposition
    q.h(qbits)

    # Grover iterations
    for _ in range(iterations):
        oracle(q, qbits)
        diffusion_operator(q, qbits)

    return q.measure(qbits)
```

### Quantum Random Number Generator

```python
def quantum_random_number(q, n_bits):
    """Generate n-bit random number"""
    qbits = q.qubits(n_bits)
    q.h(qbits)  # Apply Hadamard to all
    result = q.measure_all()
    return int(result, 2)  # Convert bitstring to integer
```

## Integration with Selene

This section explains how to wrap Guppy circuits in Selene services for web API access.

### Basic Selene Service Template

```python
# main.py - Selene service
from fastapi import FastAPI
import guppy as qp

app = FastAPI()

class QuantumService:
    def __init__(self):
        # Initialize quantum hardware/emulator
        pass

    def execute_circuit(self, circuit_builder):
        """Run a Guppy circuit and return results"""
        with qp.quantum() as q:
            circuit_builder(q)
            return q.execute()

@app.post("/api/quantum/compute")
async def compute(request: dict):
    """API endpoint that runs quantum circuit"""
    service = QuantumService()

    def circuit(q):
        # Build circuit from request parameters
        n_qubits = request.get("n_qubits", 2)
        qbits = q.qubits(n_qubits)
        q.h(qbits[0])
        q.cx(qbits[0], qbits[1])
        # ... more operations

    result = service.execute_circuit(circuit)
    return {"result": result}
```

### Serializing Circuits

For complex circuits, accept JSON descriptions:

```python
def build_circuit_from_json(q, circuit_spec):
    """Build quantum circuit from JSON specification"""
    for gate in circuit_spec["gates"]:
        gate_type = gate["type"]
        qubits = [q.qubits()[i] for i in gate["qubits"]]

        if gate_type == "h":
            q.h(*qubits)
        elif gate_type == "cx":
            q.cx(qubits[0], qubits[1])
        elif gate_type == "rx":
            q.rx(gate["angle"], qubits[0])
        # ... other gates
```

### Error Handling

```python
try:
    with qp.quantum() as q:
        # quantum operations
        result = q.execute()
except qp.QuantumError as e:
    # Handle quantum-specific errors
    raise HTTPException(status_code=500, detail=str(e))
except Exception as e:
    # Handle other errors
    raise HTTPException(status_code=500, detail="Unexpected error")
```

### Performance Optimization

```python
# Cache compiled circuits
from functools import lru_cache

@lru_cache(maxsize=128)
def compile_circuit(gates_tuple):
    """Cache compiled quantum circuits"""
    with qp.quantum() as q:
        for gate in gates_tuple:
            apply_gate(q, gate)
        return q.compile()

# Batch execution
def batch_execute(circuit_specs, shots_per_circuit=1000):
    """Execute multiple circuits efficiently"""
    results = []
    for spec in circuit_specs:
        # Reuse hardware connection
        result = execute_circuit(spec, shots=shots_per_circuit)
        results.append(result)
    return results
```

## Best Practices

1. **Qubit Management**: Allocate only the qubits needed. Naming qubit registers improves readability.
2. **Circuit Depth**: Minimize circuit depth for better results on noisy hardware.
3. **Error Mitigation**: Use techniques like zero-noise extrapolation for NISQ devices.
4. **Testing**: Always test with emulator before running on real hardware.
5. **Resource Cleanup**: Release quantum hardware resources properly with context managers.
6. **Observability**: Log circuit specifications, parameters, and results for debugging.
7. **API Design**: Keep quantum execution endpoints stateless for scalability.

## Troubleshooting

**Guppy import failed**: Ensure Guppy is installed: `pip install guppy`. Check version compatibility.

**Quantum compilation error**: Verify gate definitions and qubit indices. Use emulator to debug.

**Hardware connection failed**: Check Quantinuum API credentials and network connectivity.

**Results seem random**: Increase shot count for better statistics. Check circuit logic.

**Slow execution**: Optimize circuit depth. Use emulator for development, only use hardware for final runs.

---

**For Selene API specifications, see [selene_api.md](./selene_api.md)**
**For Fly.io deployment, see [flyio_config.md](./flyio_config.md)**
**For frontend patterns, see [lovable_patterns.md](./lovable_patterns.md)**
