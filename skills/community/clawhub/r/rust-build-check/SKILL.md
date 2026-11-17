---
name: rust-build-check
description: Run cargo check on the agent-browser CLI to catch compile errors and warnings before committing
disable-model-invocation: true
---

## rust-build-check

Run a fast compile check on the agent-browser Rust CLI without building binaries.

### Steps

1. Change to the agent-browser project root:
   ```
   cd C:/Users/eohmig/agent-browser
   ```

2. Run the check:
   ```
   cargo check --manifest-path cli/Cargo.toml
   ```

3. If there are errors or warnings, report them to the user with:
   - The file and line number
   - The error/warning message
   - A suggested fix if obvious

4. If the check passes cleanly, confirm with:
   ```
   ✓ cli/ compiles cleanly — no errors or warnings.
   ```

### Notes

- This only runs `cargo check`, not `cargo build` (much faster).
- Do NOT run `cargo fmt` here — that's a separate concern.
- If `cargo` is not in PATH, tell the user to install Rust via `rustup`.
