# Real controlled `pow_const_mod` for small-N Shor

Pattern from `quantum/nadarasa_g11_real.py`. Implements

    |x⟩_ctrl  |1⟩_work   →   |x⟩_ctrl  |a^x mod N⟩_work

for `a = 2, N = 15` on a 4-qubit work register, controlled by a 4-qubit QPE register. Period `r = ord_15(2) = 4`, so QPE peaks land at `{0, 4, 8, 12}` and continued fractions recover `r = 4`.

## The CSWAP-chain trick

For `a = 2` and `N = 2^k − 1` (here `15 = 2^4 − 1`), controlled mul-by-2 mod N coincides with a **controlled left cyclic shift** on the work register, on the entire orbit of `|1⟩` (`{1, 2, 4, 8}` plus `|0⟩`). It only diverges on `|15⟩ = |1111⟩`, which is unreachable from `|1⟩` under repeated mul-by-2 and therefore never appears.

```python
@guppy
def cswap(c: qubit, a: qubit, b: qubit) -> None:
    cx(b, a); toffoli(c, a, b); cx(b, a)

@guppy
def cmul2_mod15(c, w0, w1, w2, w3) -> None:
    # left cyclic shift by 1: (w0,w1,w2,w3) -> (w3,w0,w1,w2)
    cswap(c, w3, w2)
    cswap(c, w2, w1)
    cswap(c, w1, w0)

@guppy
def cmul4_mod15(c, w0, w1, w2, w3) -> None:
    # left cyclic shift by 2
    cswap(c, w0, w2); cswap(c, w1, w3)
```

For `pow_const_mod(a=2)`, the powers `2^(2^i) mod 15` are `{2, 4, 1, 1}` — so the four QPE-controlled multiplies become `cmul2`, `cmul4`, identity, identity.

## QPE layout

- 4 control qubits `c0..c3`, all Hadamarded.
- 4 work qubits, initialised to `|0001⟩` via `x(w0)`.
- Controlled multiplies in increasing `i`.
- **Inverse QFT with no final swap** on the controls — then measure in increasing bit order. The "no final swap" matters: omit it and you measure in reversed order, which flips the histogram between `msb_first` and `lsb_first`.

```python
# IQFT on (c0, c1, c2, c3), no final swap
h(c3)
cphase_h(c3, c2, -0.5)
h(c2)
cphase_h(c3, c1, -0.25); cphase_h(c2, c1, -0.5)
h(c1)
cphase_h(c3, c0, -0.125); cphase_h(c2, c0, -0.25); cphase_h(c1, c0, -0.5)
h(c0)
```

The driver tries both bit orders (`msb_first` / `lsb_first`) and picks whichever gives the largest overlap with the expected peak set — cheap robustness against convention mismatch.

## Acceptance gates

Three numbers, all checked host-side:

1. `recovered_period == 4` — continued-fractions decode of the histogram peaks. Use `Fraction(k, 2**M).limit_denominator(N)`, take `denominator`, then `lcm` across the top peaks.
2. `peak_share on {0,4,8,12} > 0.90` — the four expected QPE bins should hold >90% of shots at 2048 shots.
3. `work_register_orbit_fraction > 0.99` — work-register measurements must stay inside `{1, 2, 4, 8}` (the orbit of `|1⟩`). This is the integrity check that the permutation circuit is correct; ancilla entanglement can broaden the QPE peaks but the work register is permutation-only and must be exact.

## Where this generalises

- **Other `a` for `N = 15`.** Powers of 2 give shifts; other `a` need a small precomputed permutation table per `a^(2^i) mod 15`. Compile each as a CSWAP/CX permutation by hand.
- **Other `N = 2^k − 1`.** Same shift trick works; pick `a` whose powers are all shifts.
- **General `N`.** No shortcut — falls back to real adder-based `mul_const_mod`. That's a much larger lift; the CSWAP-chain trick is what makes the small-N case fit in ~250 LOC.
