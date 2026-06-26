#!/usr/bin/env python3
"""
quantum-sim: A pure-Python quantum circuit simulator.
Simulates up to ~20 qubits using statevector representation.
No dependencies beyond Python 3 stdlib + numpy (optional, falls back to pure Python).
"""

import sys
import math
import json
import argparse
import random
import cmath
from typing import List, Tuple, Dict, Optional

# ---------------------------------------------------------------------------
# Linear algebra: use numpy if available, else pure Python fallback
# ---------------------------------------------------------------------------
try:
    import numpy as np
    _USE_NUMPY = True
except ImportError:
    _USE_NUMPY = False

def _zeros(n):
    if _USE_NUMPY:
        return np.zeros(n, dtype=complex)
    return [0+0j] * n

def _kron(a, b):
    """Kronecker product of two matrices (lists of lists or np arrays)."""
    if _USE_NUMPY:
        return np.kron(a, b)
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = [[0+0j]*(ca*cb) for _ in range(ra*rb)]
    for i in range(ra):
        for j in range(ca):
            for k in range(rb):
                for l in range(cb):
                    out[i*rb+k][j*cb+l] = a[i][j] * b[k][l]
    return out

def _matmul_vec(mat, vec):
    """Matrix-vector product."""
    if _USE_NUMPY:
        return mat @ vec
    n = len(vec)
    out = [0+0j]*n
    for i in range(n):
        s = 0+0j
        for j in range(n):
            s += mat[i][j] * vec[j]
        out[i] = s
    return out

def _eye(n):
    if _USE_NUMPY:
        return np.eye(n, dtype=complex)
    return [[1+0j if i==j else 0+0j for j in range(n)] for i in range(n)]

def _norm(vec):
    if _USE_NUMPY:
        return float(np.real(np.vdot(vec, vec)**0.5))
    return math.sqrt(sum(abs(v)**2 for v in vec))

# ---------------------------------------------------------------------------
# Gate definitions (2x2 matrices)
# ---------------------------------------------------------------------------
_I2 = [[1+0j, 0+0j], [0+0j, 1+0j]]
_sq2 = 1/math.sqrt(2)

GATES = {
    'I': [[1+0j, 0+0j ], [0+0j, 1+0j ]],
    'X': [[0+0j, 1+0j ], [1+0j, 0+0j ]],
    'Y': [[0+0j, -1j ], [1j, 0+0j ]],
    'Z': [[1+0j, 0+0j ], [0+0j, -1+0j ]],
    'H': [[_sq2+0j, _sq2+0j], [_sq2+0j, -_sq2+0j]],
    'S': [[1+0j, 0+0j ], [0+0j, 0+1j ]],
    'T': [[1+0j, 0+0j ], [0+0j, cmath.exp(1j*math.pi/4)]],
    'Sdg':[[1+0j, 0+0j ], [0+0j, 0-1j ]],
    'Tdg':[[1+0j, 0+0j ], [0+0j, cmath.exp(-1j*math.pi/4)]],
}

def rx_gate(theta):
    c = math.cos(theta/2)
    s = math.sin(theta/2)
    return [[c+0j, -1j*s], [-1j*s, c+0j]]

def ry_gate(theta):
    c = math.cos(theta/2)
    s = math.sin(theta/2)
    return [[c+0j, -s+0j], [s+0j, c+0j]]

def rz_gate(theta):
    return [[cmath.exp(-1j*theta/2), 0+0j], [0+0j, cmath.exp(1j*theta/2)]]

def p_gate(lam):
    return [[1+0j, 0+0j], [0+0j, cmath.exp(1j*lam)]]

# ---------------------------------------------------------------------------
# Statevector circuit
# ---------------------------------------------------------------------------
class QuantumCircuit:
    def __init__(self, n_qubits: int):
        if n_qubits < 1 or n_qubits > 20:
            raise ValueError("Qubit count must be 1-20")
        self.n = n_qubits
        self.dim = 1 << n_qubits  # 2^n
        self.state = _zeros(self.dim)
        self.state[0] = 1+0j
        self.log: List[str] = []

    def _apply_single(self, gate_mat, qubit: int):
        """Apply a single-qubit gate to the statevector."""
        n = self.n
        if _USE_NUMPY:
            op = np.array([[1+0j]])
            for i in range(n-1, -1, -1):
                if i == qubit:
                    op = np.kron(op, np.array(gate_mat, dtype=complex))
                else:
                    op = np.kron(op, np.eye(2, dtype=complex))
            self.state = op @ self.state
        else:
            op = [[1+0j]]
            for i in range(n-1, -1, -1):
                if i == qubit:
                    op = _kron(op, gate_mat)
                else:
                    op = _kron(op, _I2)
            self.state = _matmul_vec(op, self.state)

    def _apply_cnot(self, control: int, target: int):
        new_state = list(self.state) if not _USE_NUMPY else self.state.copy()
        for idx in range(self.dim):
            if (idx >> control) & 1:
                flipped = idx ^ (1 << target)
                if _USE_NUMPY:
                    new_state[idx], new_state[flipped] = self.state[flipped].copy(), self.state[idx].copy()
                else:
                    new_state[idx], new_state[flipped] = self.state[flipped], self.state[idx]
        if _USE_NUMPY:
            self.state = np.array(new_state, dtype=complex)
        else:
            self.state = new_state

    def _apply_cz(self, control: int, target: int):
        for idx in range(self.dim):
            if ((idx >> control) & 1) and ((idx >> target) & 1):
                self.state[idx] *= -1

    def _apply_swap(self, q1: int, q2: int):
        new_state = list(self.state) if not _USE_NUMPY else self.state.copy()
        for idx in range(self.dim):
            b1 = (idx >> q1) & 1
            b2 = (idx >> q2) & 1
            if b1 != b2:
                flipped = idx ^ (1 << q1) ^ (1 << q2)
                new_state[idx] = self.state[flipped]
        if _USE_NUMPY:
            self.state = np.array(new_state, dtype=complex)
        else:
            self.state = new_state

    def h(self, q): self._apply_single(GATES['H'], q); self.log.append(f"H({q})")
    def x(self, q): self._apply_single(GATES['X'], q); self.log.append(f"X({q})")
    def y(self, q): self._apply_single(GATES['Y'], q); self.log.append(f"Y({q})")
    def z(self, q): self._apply_single(GATES['Z'], q); self.log.append(f"Z({q})")
    def s(self, q): self._apply_single(GATES['S'], q); self.log.append(f"S({q})")
    def t(self, q): self._apply_single(GATES['T'], q); self.log.append(f"T({q})")
    def sdg(self, q): self._apply_single(GATES['Sdg'], q); self.log.append(f"Sdg({q})")
    def tdg(self, q): self._apply_single(GATES['Tdg'], q); self.log.append(f"Tdg({q})")
    def rx(self, theta, q): self._apply_single(rx_gate(theta), q); self.log.append(f"Rx({theta:.4f},{q})")
    def ry(self, theta, q): self._apply_single(ry_gate(theta), q); self.log.append(f"Ry({theta:.4f},{q})")
    def rz(self, theta, q): self._apply_single(rz_gate(theta), q); self.log.append(f"Rz({theta:.4f},{q})")
    def p(self, lam, q): self._apply_single(p_gate(lam), q); self.log.append(f"P({lam:.4f},{q})")
    def cx(self, ctrl, tgt): self._apply_cnot(ctrl, tgt); self.log.append(f"CX({ctrl},{tgt})")
    def cnot(self, ctrl, tgt): self.cx(ctrl, tgt)
    def cz(self, ctrl, tgt): self._apply_cz(ctrl, tgt); self.log.append(f"CZ({ctrl},{tgt})")
    def swap(self, q1, q2): self._apply_swap(q1, q2); self.log.append(f"SWAP({q1},{q2})")

    def probabilities(self) -> List[float]:
        if _USE_NUMPY:
            return list(np.real(self.state * self.state.conj()))
        return [abs(v)**2 for v in self.state]

    def statevector(self) -> List[complex]:
        return list(self.state)

    def measure(self, shots: int = 1024) -> Dict[str, int]:
        probs = self.probabilities()
        counts: Dict[str, int] = {}
        for _ in range(shots):
            r = random.random()
            cumulative = 0.0
            chosen = self.dim - 1
            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    chosen = i
                    break
            bitstr = format(chosen, f'0{self.n}b')
            counts[bitstr] = counts.get(bitstr, 0) + 1
        return dict(sorted(counts.items()))

    def draw(self) -> str:
        lines = []
        for q in range(self.n-1, -1, -1):
            ops = []
            for entry in self.log:
                if f'({q})' in entry or f',{q})' in entry or f'({q},' in entry:
                    short = entry.split('(')[0]
                    ops.append(short[:4].center(6))
                else:
                    ops.append('------')
            line = f"q{q}: |0>-" + '-'.join(ops) + '-'
            lines.append(line)
        return '\n'.join(lines)

# Built-in presets
# ---------------------------------------------------------------------------
def bell_state(q0=0, q1=1) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(q0); qc.cx(q0, q1)
    return qc

def ghz_state(n=3) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n-1):
        qc.cx(i, i+1)
    return qc

def qft_circuit(n=3) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    for j in range(n):
        qc.h(j)
        for k in range(j+1, n):
            qc.p(math.pi / (2 ** (k - j)), j)
    for i in range(n//2):
        qc.swap(i, n-1-i)
    return qc

def grover_2qubit() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0); qc.h(1)          # superposition
    qc.cz(0, 1)               # oracle: mark |11>
    qc.h(0); qc.h(1)          # diffusion
    qc.x(0); qc.x(1)
    qc.cz(0, 1)
    qc.x(0); qc.x(1)
    qc.h(0); qc.h(1)
    return qc

def teleportation_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(3)
    qc.x(0)                   # prepare |1> to teleport
    qc.h(1); qc.cx(1, 2)      # Bell pair
    qc.cx(0, 1); qc.h(0)      # Bell measurement
    qc.cx(1, 2); qc.cz(0, 2)  # corrections
    return qc

PRESETS = {
    'bell':          (bell_state,            'Bell state |Phi+>: maximally entangled 2-qubit state'),
    'ghz':           (ghz_state,             'GHZ state: N-qubit maximally entangled state'),
    'qft':           (qft_circuit,           'Quantum Fourier Transform on N qubits'),
    'grover':        (grover_2qubit,         "Grover's search algorithm (2 qubits, marks |11>)"),
    'teleportation': (teleportation_circuit, 'Quantum teleportation protocol (3 qubits)'),
}

# ---------------------------------------------------------------------------
# QASM-like parser
# ---------------------------------------------------------------------------
def parse_and_run(qasm_lines: List[str]) -> QuantumCircuit:
    qc = None
    for raw in qasm_lines:
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.lower().split()
        op = parts[0]
        if op == 'qubits':
            qc = QuantumCircuit(int(parts[1]))
        elif qc is None:
            raise ValueError("First instruction must be: qubits N")
        elif op in ('h','x','y','z','s','t','sdg','tdg'):
            getattr(qc, op)(int(parts[1]))
        elif op in ('rx','ry','rz','p'):
            getattr(qc, op)(float(parts[1]), int(parts[2]))
        elif op in ('cx','cnot'):
            qc.cx(int(parts[1]), int(parts[2]))
        elif op == 'cz':
            qc.cz(int(parts[1]), int(parts[2]))
        elif op == 'swap':
            qc.swap(int(parts[1]), int(parts[2]))
        elif op == 'measure':
            pass
        else:
            raise ValueError(f"Unknown gate: {op}")
    if qc is None:
        raise ValueError("No circuit defined. Use: qubits N")
    return qc

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
ANSI = sys.stdout.isatty()
def bold(s):   return f'\033[1m{s}\033[0m'  if ANSI else s
def cyan(s):   return f'\033[96m{s}\033[0m' if ANSI else s
def green(s):  return f'\033[92m{s}\033[0m' if ANSI else s
def yellow(s): return f'\033[93m{s}\033[0m' if ANSI else s
def dim(s):    return f'\033[2m{s}\033[0m'  if ANSI else s
def bar(prob, width=30):
    filled = int(prob * width)
    return '[' + '#' * filled + ' ' * (width - filled) + ']'

def print_results(qc: QuantumCircuit, shots: int, json_out: bool, label: str = ''):
    probs = qc.probabilities()
    counts = qc.measure(shots)
    sv = qc.statevector()

    if json_out:
        out = {
            'label': label, 'n_qubits': qc.n, 'gates': qc.log,
            'statevector': [{'re': round(v.real,6), 'im': round(v.imag,6)} for v in sv],
            'probabilities': {format(i, f'0{qc.n}b'): round(p,6) for i,p in enumerate(probs) if p > 1e-9},
            'counts': counts, 'shots': shots,
        }
        print(json.dumps(out, indent=2))
        return
    if label:
        print(bold(f'\n=== {label} ==='))
    print(cyan(f'Qubits: {qc.n}   Dim: {qc.dim}   Gates applied: {len(qc.log)}'))
    print(dim(f'Circuit: {" -> ".join(qc.log) if qc.log else "(empty)"}'))
    print(bold('\nStatevector (|amplitude| > 0.001):'))
    for i, v in enumerate(sv):
        if abs(v) > 0.001:
            basis = '|' + format(i, f'0{qc.n}b') + '>'
            amp = f'{v.real:+.4f}{v.imag:+.4f}j'
            prob = abs(v)**2
            print(f'  {basis}  {amp}  p={prob:.4f}  {bar(prob, 20)}')
    print(bold(f'\nMeasurement ({shots} shots):'))
    total = sum(counts.values())
    for bitstr, cnt in sorted(counts.items(), key=lambda x: -x[1])[:16]:
        pct = cnt / total
        print(f'  |{bitstr}>  {green(bar(pct, 24))}  {cnt:5d} ({pct*100:5.1f}%)')
    if len(counts) > 16:
        print(f'  ... ({len(counts)} total outcomes)')
    print()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='Quantum circuit simulator - statevector engine, pure Python',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --preset bell
  %(prog)s --preset ghz --qubits 4
  %(prog)s --preset qft --qubits 3
  %(prog)s --preset grover --shots 2048
  %(prog)s --qasm "qubits 2; h 0; cx 0 1"
  %(prog)s --qasm-file my_circuit.qasm
  %(prog)s --list-presets
  %(prog)s --preset bell --json
        """
    )
    parser.add_argument('--preset', choices=list(PRESETS.keys()))
    parser.add_argument('--qubits', type=int, default=None)
    parser.add_argument('--qasm', type=str, default=None)
    parser.add_argument('--qasm-file', type=str, default=None)
    parser.add_argument('--shots', type=int, default=1024)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--list-presets', action='store_true')
    parser.add_argument('--statevector-only', action='store_true')
    args = parser.parse_args()

    if args.list_presets:
        print(bold('Built-in presets:'))
        for name, (fn, desc) in PRESETS.items():
            print(f'  {yellow(name):<20} {desc}')
        return
    qc = None
    label = ''

    if args.preset:
        fn, desc = PRESETS[args.preset]
        label = desc
        if args.preset == 'ghz' and args.qubits:
            qc = fn(args.qubits)
        elif args.preset == 'qft' and args.qubits:
            qc = fn(args.qubits)
        else:
            qc = fn()
    elif args.qasm:
        lines = args.qasm.replace(';', '\n').split('\n')
        qc = parse_and_run(lines)
        label = 'Custom QASM circuit'
    elif args.qasm_file:
        with open(args.qasm_file) as f:
            lines = f.readlines()
        qc = parse_and_run(lines)
        label = f'Circuit: {args.qasm_file}'
    else:
        parser.print_help()
        print('\nTip: try --preset bell or --list-presets')
        return
    print_results(qc, args.shots, args.json, label)

if __name__ == '__main__':
    main()