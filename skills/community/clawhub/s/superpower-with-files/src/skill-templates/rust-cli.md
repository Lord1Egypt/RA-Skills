# Rust CLI Template

When planning a Rust CLI tool, ensure the following standards are met:

## Project Structure
- `Cargo.toml` with descriptive metadata.
- `src/main.rs` for binary entry point.
- `src/lib.rs` if logic should be reusable.

## Recommended Crates
- **`clap`**: With `derive` feature for argument parsing.
- **`anyhow`**: For flexible error handling.
- **`tokio`**: If async execution is required.
- **`serde`**: If JSON/YAML parsing is needed.

## Patterns
- Explicitly define an `Error` enum or use `anyhow::Result`.
- Use `tracing` or `log` for instrumentation.
- Optimize for binary size if requested.
