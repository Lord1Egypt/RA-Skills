## Description:

Advanced Rust on Windows, macOS, and Linux: ownership and lifetimes, Result/error design, async Tokio, concurrency, serde/clap/tracing, Cargo features and profiles, testing, profiling, cross-compilation, Windows FFI, and PyO3/maturin. Use when the borrow checker, an async Send error, a linker error, a version conflict, or a production binary needs a real diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use this skill to diagnose Rust ownership, lifetime, async, compiler, linker, dependency, and production-build issues. It provides practical guidance and starter examples for Rust applications and libraries across Windows, macOS, and Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI example writes to its configured output path and may overwrite an existing file.

Mitigation: Check the destination path and back up any existing file before running or adapting the example.

Risk: Dependency and toolchain updates, or uncompiled external-crate templates, may behave differently in a target environment.

Mitigation: Review current dependency and toolchain versions, then compile and test the examples in the intended environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/rust-advanced)
- [Rust Book: Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [Rust Book: Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [Rust Book: Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html)
- [Rust Book: Async/Await](https://doc.rust-lang.org/book/ch17-00-async-await.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [PyO3 Guide](https://pyo3.rs/)
- [windows-rs Documentation](https://microsoft.github.io/windows-docs-rs/)
- [Curated Rust references and verification notes](references/SOURCES.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Rust code blocks, shell commands, configuration examples, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes starter templates and diagnostic guidance; external-crate templates are examples and are not all compiled in the documented verification.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
