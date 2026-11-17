# Circuit patterns

Reusable Guppy snippets for the patterns this project actually needs. Copy and adapt.

## Amplitude-encoded feature state (3 features → 2 qubits)

Maps three values in `[0, 1]` to a non-trivial entangled 2-qubit state.

```python
@guppy
def prep_patient(q0: qubit, q1: qubit, a0: float, a1: float, a2: float) -> None:
    ry(q0, angle(a0))
    ry(q1, angle(a1))
    cx(q0, q1)
    rz(q1, angle(a2))
```

Pre-scale features into radians: `angles = [f * math.pi for f in features]`.

## Toffoli (CCX) from H, CX, T, Tdg

Standard 6-T decomposition. Guppy has no native CCX.

```python
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
```

## CSWAP (Fredkin) from CX + Toffoli

```python
@guppy
def cswap(c: qubit, a: qubit, b: qubit) -> None:
    cx(b, a)
    toffoli(c, a, b)
    cx(b, a)
```

## SWAP test (state fidelity)

Measures `F = |<psi_i|psi_j>|^2` between two registers. `P(ancilla=0) = (1 + F) / 2`.

```python
@guppy
def swap_test(ai: float, bi: float, ci: float,
              aj: float, bj: float, cj: float) -> None:
    anc = qubit()
    pi0, pi1 = qubit(), qubit()
    pj0, pj1 = qubit(), qubit()

    prep_patient(pi0, pi1, ai, bi, ci)
    prep_patient(pj0, pj1, aj, bj, cj)

    h(anc)
    cswap(anc, pi0, pj0)
    cswap(anc, pi1, pj1)
    h(anc)

    output("anc", measure(anc).read())
    discard(pi0); discard(pi1); discard(pj0); discard(pj1)
```

Invert measurement: `F = 2 * P(0) - 1`, clamped to `[0, 1]`.

## Controlled phase from `rz` + `cx`

Guppy has no native `cphase` / `crz`. The standard rz/cx identity gives a controlled phase on `d` from control `c`:

```python
@guppy
def cphase_on(c: qubit, d: qubit, theta: float) -> None:
    rz(d, angle(theta / 2.0))
    cx(c, d)
    rz(d, angle(-theta / 2.0))
    cx(c, d)
```

Used in `quantum/nadarasa_g1.py` and `g3.py` to encode dihedral coset structure (label qubit selects `|x⟩` vs `|x+s⟩` branch in the QFT basis).

## Coset-state QFT readout (G1)

Prepare `|+⟩^n` on data, bake the slope `s` as per-qubit phases `2π · s · 2^j / N`, then `H` and measure each data qubit. The marginal of `y` carries the dihedral coset structure:

```python
for j in range(n):
    d[j] = qubit(); h(d[j])
for j in range(n):
    theta = ((2*math.pi*s*(2**j)/N + math.pi) % (2*math.pi)) - math.pi
    phase_on(d[j], theta)         # or cphase_on(label, d[j], theta)
for j in range(n):
    h(d[j]); output(f"y{j}", measure(d[j]).read())
```

Decode `y` host-side (see selene-runtime.md) and bin into `y % p` for the residue histogram.

## Mid-circuit parity window (G2)

H-sandwiched ancilla touching a disjoint subset of data qubits, measured mid-circuit. The ancilla slot is reused across windows:

```python
# per window w with support j in [w*width, (w+1)*width):
a = qubit(); h(a)
for j in support:
    cx(d[j], a)         # probe_one(a, d[j])
h(a); output(f"w{w}", measure(a).read())
```

After `k` windows, measure the data register. Use disjoint round-robin supports so each data qubit is touched at most once per window group.

## Host-side metrics

Pair the above kernels with these post-processors (run on the decoded shot dicts):

- **Residue histogram** — `P(y mod p)` from per-shot integer decode. Refutation knob for G1 (SRP slopes concentrate on residue 0; violating slopes should sit at `1/p`).
- **Collision probability** — `Σ_x p_x²` over final data outcomes. A measurement-basis purity proxy; uniform baseline is `1/N`. Used in G2 to track per-window decay.

## Cross-check classically

Always validate with a NumPy statevector before trusting shot statistics. See `classical_fidelity` in `quantum/qtda.py` for the reference implementation (Kronecker products of RY/RZ + CX matrix).

## Feed-forward / mid-circuit branching (G4)

Guppy supports `if measure(...)` mid-circuit; the measured qubit's classical bit drives subsequent gates. Pattern from `quantum/nadarasa_g4.py`:

```python
@guppy
def kernel(theta: float) -> None:
    a = qubit(); q = qubit()
    h(a)
    cphase_on(a, q, theta)
    h(a)
    b = measure(a).read()
    if b:
        x(q)                # classical-controlled correction
    output("b", b)
    output("y", measure(q).read())
```

The ancilla is consumed by `measure`; it does not need `discard`. Branch only on freshly-measured bits — do not stash them for later (Guppy bit-flow is forward-only).

## Inverse QFT, no final swap (G11)

Standard IQFT but skip the closing bit-reversal swap; instead, measure in increasing qubit order. Decoder picks `msb_first` vs. `lsb_first` host-side based on which gives the larger overlap with the expected peak set — see `references/shor-modexp.md` for the full driver pattern.

## CSWAP-chain cyclic shifts (permutation oracles)

A chain of `cswap(c, w[j+1], w[j])` implements a controlled left cyclic shift on the work register. For modular arithmetic where `a^k mod N` lands inside a closed orbit of states (e.g. `a = 2, N = 15`), the shift IS the controlled mul-mod on that orbit. See `references/shor-modexp.md` for the orbit-coincidence argument and acceptance gates.
