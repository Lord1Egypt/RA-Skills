# The QIR lane (Guppy → HUGR → QIR)

QIR is the LLVM-bitcode interchange format some Quantinuum submission paths accept. It is a
*third* lane next to Selene and TKET, useful when a target only takes bitcode or when you
want a compiler-independent artifact of the kernel.

## It needs its own pinned environment

The QIR toolchain lags the Guppy v1 line. Keep it in a separate venv; do **not** try to make
one environment serve both.

```bash
# certified execution env: system python3 + guppylang >= 1.0 + selene (see SKILL.md)

# QIR env, pinned and disposable
python3.12 -m venv /tmp/qir021_venv
/tmp/qir021_venv/bin/pip install \
  guppylang==0.21.16 hugr-qir pytket-qir qnexus selene-sim qir-qis
```

Consequence: kernels destined for the QIR lane must be written so they compile under **both**
0.21 and 1.0, or kept in a clearly-marked module that only the pinned venv imports. Under
0.21, parameterized functions go through `compile_function()`; under 1.0 the emulator builder
replaces it. See `references/guppy-v1-migration.md`.

## Emit and validate locally

```bash
/tmp/qir021_venv/bin/python -m quantum.<pkg>.qir_<kernel>   # Guppy → HUGR → QIR bitcode
```

Validate with `qircheck` (ships with `hugr-qir`) **before** attempting any upload. Local
validation is free; a rejected upload is not.

## `qircheck` constraints that bite

1. **Static kernels only.** Runtime-parameterized angles break emission — bake literals into
   the generated source instead (the temp-module driver pattern already does this; see
   `references/driver-pattern.md`). A sweep becomes N emitted modules, not one parameterized
   module.
2. **`discard()` after `measure` aborts.** Use measure-all semantics: measure every qubit and
   ignore the bits you do not need, rather than measuring some and discarding the rest.
3. Anything the classical-control surface cannot lower statically (host-side Python
   arithmetic sneaking into the kernel) fails at emission, not at run time.

## The execution gap

Local `qircheck` passing does **not** imply the job will run. QIR execution targets are
restricted (H2-1SC / H2-1E class) and often unavailable on a standard account; direct QIR
execute against a normal backend fails with `entry not found in database`. Document the gap
explicitly in the write-up — "QIR emitted and qircheck-validated; Nexus execution blocked by
backend access" is a legitimate, citable status. Do not imply the bitcode ran.

## When to bother

- The submission target only accepts bitcode.
- You want an artifact that is independent of both Selene and TKET for a provenance claim.
- Otherwise: stay on Selene for evidence and TKET for the independent compile check
  (`references/pytket.md`). The QIR lane costs a second environment for little extra signal.
