## Description:

Advanced Rust + Python engineering: choose the right language per layer, build typed Python around a Rust core, use subprocess JSON or PyO3/maturin, share errors and tests, profile both, and ship Windows binaries. Use when Python is fast enough to orchestrate but Rust is needed for CPU, memory, concurrency, or distribution — or when a Python/Rust boundary is failing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use this skill to design and troubleshoot Rust–Python integrations, including JSON sidecars and PyO3 extensions. It provides implementation patterns, tests, packaging guidance, and performance practices for choosing the right boundary between the languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an untrusted or unverified sidecar executable, or processing large or untrusted inputs, can create security or resource-exhaustion risks.

Mitigation: Use a project virtual environment and a trusted, locally built sidecar; verify builds and enforce input/output limits and timeouts before processing untrusted or large data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/rust-python-interop)
- [Rust Book: Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)
- [Rust Book: Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
- [Cargo Book](https://doc.rust-lang.org/cargo/)
- [PyO3 User Guide](https://pyo3.rs/)
- [maturin User Guide](https://www.maturin.rs/)
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html)
- [Python packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with explanatory text, code examples, command snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Rust and Python integration examples and testing and packaging guidance]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
