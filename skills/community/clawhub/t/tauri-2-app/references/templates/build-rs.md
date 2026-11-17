# `src-tauri/build.rs`

Tauri's standard build script plus platform-specific framework links. Use `CARGO_CFG_TARGET_OS` (the **target** OS — survives cross-compilation), never the host OS.

```rust
fn main() {
    tauri_build::build();

    let target_os = std::env::var("CARGO_CFG_TARGET_OS").unwrap_or_default();

    match target_os.as_str() {
        "macos" => {
            // Frameworks commonly needed for system integration:
            //   - Accelerate, Metal: GPU/ML acceleration
            //   - CoreGraphics, ApplicationServices: window placement, accessibility
            //   - Foundation: NS* types
            println!("cargo:rustc-link-lib=framework=Foundation");
            println!("cargo:rustc-link-lib=framework=ApplicationServices");
            // Enable the others on demand — keep build.rs to what the code uses:
            // println!("cargo:rustc-link-lib=framework=Accelerate");
            // println!("cargo:rustc-link-lib=framework=Metal");
            // println!("cargo:rustc-link-lib=framework=CoreGraphics");
        }
        "windows" => {
            // Most Windows APIs come in via `windows-sys` features. Only declare libs
            // here for low-level needs not covered by a `windows-sys` feature.
            // println!("cargo:rustc-link-lib=user32");
        }
        "linux" => {
            // pthread + libm are usually pulled in by the system, but be explicit.
            println!("cargo:rustc-link-lib=pthread");
            println!("cargo:rustc-link-lib=m");
        }
        _ => {}
    }
}
```

## Why `CARGO_CFG_TARGET_OS` (not `cfg!`)

`cfg!(target_os = "...")` evaluates at compile time of `build.rs` against the **host** OS. When cross-compiling (macOS host → Linux target, Windows host → ARM target), `cfg!(target_os = "linux")` is `false` on a macOS host even though the actual build target is Linux.

`CARGO_CFG_TARGET_OS` is the environment variable Cargo sets to the target. Always use it in `build.rs`.

## Don't over-link

Every `cargo:rustc-link-lib=framework=*` line adds a framework dependency to the binary, even if the code doesn't actually use it. This bloats binaries and can cause notarization warnings. Start with the minimum (`Foundation`, `ApplicationServices` on macOS; `pthread`, `m` on Linux) and add more only when a linker error proves you need them.

## Don't run external commands

`build.rs` runs on every developer's machine. Calling out to `make`, `cmake`, `python` etc. introduces dependencies that may not be installed. If a Rust crate needs C dependencies (`whisper.cpp`, `opencv`), check whether the crate already handles the build — almost all do. Only add custom build logic when you're authoring a crate from scratch.
