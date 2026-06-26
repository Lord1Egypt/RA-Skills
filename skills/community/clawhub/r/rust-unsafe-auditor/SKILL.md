---
name: rust-unsafe-auditor
description: Audit Rust code for unsafe block usage — verify safety invariants, check FFI boundaries, review raw pointer operations, validate Send/Sync implementations, and detect unsound abstractions. Use when reviewing Rust codebases for memory safety, preparing security audits, or enforcing unsafe usage policies.
metadata:
  tags: ["rust", "unsafe", "memory-safety", "security", "ffi", "code-quality"]
---

# Rust Unsafe Auditor

Deep audit of `unsafe` code in Rust projects. Analyzes every unsafe block, function, trait impl, and FFI boundary for soundness. Verifies safety invariants are documented, raw pointer operations are bounded, and Send/Sync implementations are correct.

Use when: reviewing a Rust crate before publishing, auditing dependencies, preparing for security review, or establishing unsafe policies.

## Analysis Steps

### 1. Project Discovery & Unsafe Census

```bash
cat Cargo.toml 2>/dev/null | head -20
grep -i "libc\|winapi\|bindgen\|cc\|ffi\|sys\b" Cargo.toml 2>/dev/null | head -10
find . -name "*.rs" -not -path '*/target/*' | wc -l

# Project-level unsafe policy
grep -rn 'forbid(unsafe_code)\|deny(unsafe_code)' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -5

# Census
echo "=== Unsafe Census ==="
echo -n "Blocks: "; grep -rn 'unsafe\s*{' --include="*.rs" . 2>/dev/null | grep -v 'target/' | wc -l
echo -n "Functions: "; grep -rn 'unsafe\s\+fn' --include="*.rs" . 2>/dev/null | grep -v 'target/' | wc -l
echo -n "Trait impls: "; grep -rn 'unsafe\s\+impl' --include="*.rs" . 2>/dev/null | grep -v 'target/' | wc -l
```

### 2. Safety Invariant Documentation

```bash
# SAFETY comments (Rust convention)
grep -B1 -A3 'unsafe' --include="*.rs" . 2>/dev/null | grep -i 'SAFETY' | head -20

# Unsafe blocks WITHOUT safety comments
for f in $(grep -rl 'unsafe\s*{' --include="*.rs" . 2>/dev/null | grep -v 'target/'); do
  grep -n 'unsafe\s*{' "$f" | while read match; do
    line=$(echo "$match" | cut -d: -f1); prev=$((line - 1))
    if ! sed -n "${prev}p" "$f" | grep -qi 'safety'; then echo "UNDOCUMENTED: $f:$line"; fi
  done
done | head -20

# Unsafe functions without safety docs
for f in $(grep -rl 'unsafe\s\+fn' --include="*.rs" . 2>/dev/null | grep -v 'target/'); do
  grep -n 'unsafe\s\+fn' "$f" | while read match; do
    line=$(echo "$match" | cut -d: -f1); prev=$((line - 1))
    if ! sed -n "${prev}p" "$f" | grep -q '///\|//!'; then echo "UNDOC_FN: $f:$line"; fi
  done
done | head -15
```

Flag:
- **Missing `// SAFETY:` comment**: every unsafe block must explain why invariants hold (Clippy lint: `undocumented_unsafe_blocks`)
- **Vague safety comments**: "this is safe" is invalid — must state the specific invariant
- **Missing `# Safety` section on pub unsafe fn**: callers need to know the contract

### 3. Raw Pointer Analysis

```bash
grep -rn 'as \*const\|as \*mut' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -20
grep -rn '\.offset(\|\.add(\|\.sub(' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15
grep -rn 'from_raw\|into_raw\|from_raw_parts' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15
grep -rn 'ManuallyDrop\|MaybeUninit\|mem::forget\|mem::transmute' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15
```

For each raw pointer operation, verify:
- **Non-null**: pointer was checked or came from a reference
- **Aligned**: alignment matches target type (especially after casts)
- **Valid for reads/writes**: memory is initialized and within allocation bounds
- **No aliasing violations**: no `&T` and `&mut T` to same data simultaneously
- **Lifetime correctness**: data outlives the pointer (no dangling pointers)
- **Ownership clarity**: `from_raw`/`into_raw` pairs must be 1:1 (double-free or leak otherwise)

### 4. FFI Boundary Review

```bash
grep -rn 'extern\s*"C"' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15
grep -rn '#\[no_mangle\]' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -10
grep -rn 'CString\|CStr\|c_char\|c_int\|c_void' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15
find . -name "bindings.rs" -o -name "*_ffi.rs" -not -path '*/target/*' 2>/dev/null | head -5
```

Check each FFI boundary for:
- **Panic across FFI**: Rust panics across `extern "C"` are UB — must use `catch_unwind`
- **String handling**: C strings are null-terminated; use `CString`/`CStr`, check for interior nulls
- **Memory ownership**: Rust allocator and C allocator are different — who frees?
- **Struct layout**: `#[repr(C)]` required for structs passed to/from C
- **Integer sizes**: C `int` is platform-dependent — use `c_int`, not `i32`
- **Thread safety**: C functions may not be thread-safe; document constraints

### 5. Send/Sync & Transmute

```bash
# Manual Send/Sync implementations
grep -rn 'unsafe impl.*Send\|unsafe impl.*Sync' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -15

# Atomic operations
grep -rn 'AtomicBool\|AtomicUsize\|AtomicPtr\|Ordering::' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -10

# Transmute (most dangerous operation)
grep -rn 'mem::transmute\|transmute(' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -10

# mem::zeroed / mem::uninitialized (UB for many types)
grep -rn 'mem::zeroed\|mem::uninitialized' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -10

# Union types
grep -rn 'union\s\+[A-Z]' --include="*.rs" . 2>/dev/null | grep -v 'target/' | head -5
```

For Send/Sync, verify:
- **Send**: no thread-local state, no thread-affine OS handles
- **Sync**: no interior mutability without synchronization (`UnsafeCell` makes type `!Sync` by default)
- **Ordering correctness**: atomic operations must use correct `Ordering` (common: `Relaxed` where `Acquire/Release` needed)

For transmute, flag:
- **Transmute to create invalid values**: `0u8` to `bool`, invalid enum discriminants — instant UB
- **mem::zeroed on non-zero types**: zeroed `NonNull`, `bool`, `&T`, enum is UB
- **mem::uninitialized**: deprecated since 1.38, always UB — use `MaybeUninit`

## Output Template

```markdown
# Rust Unsafe Audit — [Crate Name]

## Summary
- Files: N | Edition: 2021 | Unsafe blocks: N | Functions: N | Trait impls: N
- Undocumented unsafe: N (target: 0)
- Audit verdict: PASS / CONDITIONAL / FAIL

## Unsafe Inventory
| # | File:Line | Category | Documented | Verdict |
|---|-----------|----------|-----------|---------|
| 1 | src/lib.rs:45 | Raw pointer deref | Yes | Sound |
| 2 | src/ffi.rs:23 | extern "C" call | No | REVIEW |
| 3 | src/pool.rs:89 | Send impl | Yes | Sound |
| 4 | src/convert.rs:12 | transmute | No | UNSOUND |

## Critical Findings (Potential UB)
### [C1] Transmute Creates Invalid Enum Value
- **File**: src/convert.rs:12
- **Code**: `unsafe { mem::transmute::<u8, MyEnum>(byte) }` — unchecked byte
- **Fix**: Match on byte value, return `Result<MyEnum, InvalidValue>`

### [C2] Panic in extern "C" Callback
- **File**: src/ffi.rs:67
- **Code**: `.unwrap()` in extern "C" fn
- **Fix**: Replace with match + error code, or wrap in `catch_unwind`

## Documentation Gaps
| File | Line | Type | Missing |
|------|------|------|---------|
| src/lib.rs:45 | unsafe block | `// SAFETY:` comment |
| src/ffi.rs:23 | unsafe fn | `# Safety` doc section |

## Recommendations
1. Add `// SAFETY:` comments to N undocumented unsafe blocks
2. Fix N instances of potential UB
3. Add `catch_unwind` to N extern "C" callbacks
4. Run `cargo +nightly miri test` to detect UB dynamically
5. Add `#![deny(unsafe_op_in_unsafe_fn)]` to require scoped unsafe in unsafe fns
6. Consider `#![forbid(unsafe_code)]` for crates that don't need unsafe
```

## Unsafe Reduction Opportunities

| Current Unsafe | Safe Alternative |
|---------------|-----------------|
| `mem::transmute` for enum conversion | `TryFrom<u8>` implementation |
| Raw pointer array indexing | `slice::get_unchecked` (still unsafe but bounds-checkable) |
| `from_raw_parts` for buffer views | `bytemuck::cast_slice` (safe, zero-cost) |
| Manual `Send/Sync` impl | Wrap inner type in `Arc<Mutex<T>>` |

## Tips

- Run `cargo +nightly miri test` to dynamically detect undefined behavior
- Run `cargo clippy -- -W clippy::undocumented_unsafe_blocks` to enforce safety comments
- Use `cargo geiger` to count unsafe across the dependency tree
- Use `cargo audit` to check for known vulnerabilities
- Prefer `NonNull<T>` over `*mut T` to encode non-null invariant in the type system
- Consider `bytemuck` for safe type punning of POD types
- Enable `#![deny(unsafe_op_in_unsafe_fn)]` (Rust 2024 default)
