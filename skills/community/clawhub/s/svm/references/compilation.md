# Compilation Pipeline

Solana programs are compiled to sBPF (Solana Berkeley Packet Filter) bytecode — a deterministic, sandboxed instruction set derived from eBPF. Any LLVM-compatible language (Rust, C, C++, Zig) can target Solana because the compilation goes through LLVM's intermediate representation before being lowered to sBPF. Rust is the dominant choice due to its memory safety and ecosystem.

## Key Concepts

- **sBPF** — Solana's fork of eBPF with modifications for determinism: no floating point, bounded loops, strict memory access
- **eBPF** — Linux's "extended Berkeley Packet Filter" — a general-purpose VM originally for kernel networking; Solana adopted its ISA as the program runtime
- **LLVM IR** — LLVM's language-agnostic intermediate representation; the shared target for all LLVM frontends
- **MIR** — Rust's Mid-level Intermediate Representation; sits between HIR and LLVM IR, where borrow checking runs
- **Compilation stages** — Rust source → HIR → MIR → LLVM IR → eBPF object → sBPF binary (ELF)
- **LLVM eBPF backend** — translates LLVM IR to eBPF opcodes; maintained by Anza for the Solana target
- **cargo build-sbf** — the toolchain command that wraps the LLVM pipeline and produces a deployable `.so`
- **Determinism constraints** — sBPF forbids floating point, non-deterministic syscalls, and unbounded iteration

## Blog Posts

Use `fetchHeliusBlog` with these slugs:

- `solana-virtual-machine` — Deep dive into the SVM: covers the full compilation pipeline from Rust → sBPF, why eBPF was chosen, how the LLVM backend works, and what makes sBPF deterministic (most comprehensive source)

## Relevant SIMDs

Use `getSIMD` for:

- SIMD-0161 — sBPF v2 instruction set changes (new opcodes, 32-bit moves)
- SIMD-0178 — sBPF static syscalls (deterministic dispatch IDs)
- SIMD-0174 — sBPF v2 program entrypoint changes

## Source Code Entry Points

**Note**: `sdk/program/src/entrypoint.rs` (program entrypoint macro) and `sdk/program/src/instruction.rs` (Instruction type) live in `solana-labs/solana`, not agave — `readSolanaSourceFile` cannot fetch them. Skip source code fetches for compilation topics and rely on `fetchHeliusBlog` instead.

## Solana Docs

Try `searchSolanaDocs` with: "sbpf", "bpf loader", "program compilation", "cargo build-sbf"

## See Also

- `references/programs.md` — what happens after compilation: deploying the binary to chain
- `references/execution.md` — how the deployed sBPF bytecode is executed at runtime
