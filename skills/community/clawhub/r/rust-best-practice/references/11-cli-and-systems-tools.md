# CLI and Systems Tools

## Table of contents
1. Argument parsing with `clap`
2. Terminal output and UX
3. File and process I/O
4. Cross-platform concerns
5. Distributing CLI binaries
6. Anti-patterns checklist

---

## 1. Argument parsing with `clap`

`clap` (via its `derive` feature) is the de facto standard for CLI argument parsing:

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "mytool", version, about = "Does a thing")]
struct Cli {
    #[arg(short, long, global = true)]
    verbose: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Build { #[arg(short, long, default_value = "release")] profile: String },
    Clean,
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Build { profile } => { /* ... */ }
        Commands::Clean => { /* ... */ }
    }
}
```

`clap` gives you `--help`/`--version` generation, shell completion generation (`clap_complete`), and validation for free — avoid hand-rolling `std::env::args()` parsing except for the simplest one-off scripts.

## 2. Terminal output and UX

- Use `anyhow`/`?` in `fn main() -> anyhow::Result<()>` for clean top-level error reporting (see `references/03-error-handling.md`) — avoid `.unwrap()`-induced raw panics with unhelpful backtraces as the user-facing failure mode.
- Respect `NO_COLOR`/`--no-color` and detect non-TTY output (piping to a file/another program) before emitting ANSI color codes — the `owo-colors`/`termcolor`/`console` crates handle this detection; `is-terminal` crate for the raw check.
- Print errors to `stderr`, not `stdout` — keep `stdout` for the program's actual output so it composes correctly in shell pipelines (`mytool | jq`).
- Use exit codes meaningfully (`std::process::exit(1)` on failure, distinct codes for distinct failure classes if scripting consumers need to branch on them) rather than always exiting 0.
- For progress bars/spinners, `indicatif` is the standard choice.

## 3. File and process I/O

- Prefer `std::fs::read_to_string`/`std::fs::write` for whole-file operations; use buffered `BufReader`/`BufWriter` for line-by-line or streaming I/O to avoid excessive syscalls.
- Use `tempfile` crate for scratch files/directories that need reliable cleanup (RAII-based, deletes on drop) rather than hand-rolled temp paths.
- For spawning subprocesses, `std::process::Command` (sync) or `tokio::process::Command` (async) — always check the exit status (`Command::status()`/`.output()` and inspect `.status.success()`); a subprocess that fails silently is a common source of confusing bugs.
- Use `PathBuf`/`Path`, not raw `String`, for filesystem paths — this correctly handles platform path semantics and prevents encoding bugs.

## 4. Cross-platform concerns

- Never hardcode path separators (`/` vs `\`) — always build paths via `Path`/`PathBuf::join`.
- Line endings: be explicit about `\n` vs `\r\n` handling when reading/writing text files meant for cross-platform consumption.
- Use the `dirs` crate for platform-correct config/cache/home directory locations rather than hardcoding `~/.config`.
- If distributing a CLI cross-platform, test in CI on all target OSes (GitHub Actions matrix: `ubuntu-latest`, `macos-latest`, `windows-latest`) — subtle path/permission/signal-handling differences are easy to miss otherwise.

## 5. Distributing CLI binaries

- `cargo install --path .` for local dev; publish to crates.io (`cargo publish`) for `cargo install <name>` distribution.
- For prebuilt binaries, `cargo-dist` automates cross-compiled release artifacts + GitHub Releases + install scripts across platforms — the current standard tool for this in the Rust CLI ecosystem.
- Strip debug symbols (`strip = true` in `[profile.release]`, see `references/09`) to reduce binary size for distributed CLIs.

## 6. Anti-patterns checklist

- [ ] Hand-rolled `std::env::args()` parsing instead of `clap` for anything beyond a single flag
- [ ] Errors/diagnostics printed to `stdout` instead of `stderr`, breaking pipeline composability
- [ ] ANSI color codes emitted unconditionally without checking TTY/`NO_COLOR`
- [ ] `process::Command` output/exit status never checked
- [ ] Hardcoded `/`-separated paths instead of `Path`/`PathBuf`
- [ ] Program always exits 0 regardless of actual success/failure
- [ ] No cross-platform CI matrix for a CLI tool distributed to multiple OSes

---

## Real references

- `clap` official documentation and derive tutorial: https://docs.rs/clap/latest/clap/ , https://github.com/clap-rs/clap/blob/master/examples/tutorial_derive/README.md
- Command Line Applications in Rust (official community book, "CLI Book"): https://rust-cli.github.io/book/
- `indicatif` (progress bars) docs: https://docs.rs/indicatif/latest/indicatif/
- `tempfile` crate docs: https://docs.rs/tempfile/latest/tempfile/
- `dirs` crate docs: https://docs.rs/dirs/latest/dirs/
- `std::process::Command` docs: https://doc.rust-lang.org/std/process/struct.Command.html
- `cargo-dist` project: https://opensource.axo.dev/cargo-dist/
- NO_COLOR informal standard: https://no-color.org/
