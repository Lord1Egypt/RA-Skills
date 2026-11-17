## Description:

Comprehensive reference for idiomatic and production-grade Rust engineering across ownership, lifetimes, error handling, trait and API design, async, performance, unsafe Rust, testing, tooling, web and CLI development, project structure, and supply-chain security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when writing, reviewing, debugging, or designing Rust code. It provides task-specific guidance for Rust idioms, APIs, async systems, performance, unsafe code, tests, tooling, and dependency hygiene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad Rust trigger may load the skill in conversations that only briefly mention Rust, increasing context use.

Mitigation: Use the skill when Rust guidance is relevant and keep responses focused on the user's current task.

Risk: The skill may lead an agent to propose cargo commands, dependency changes, or code edits that affect a project.

Mitigation: Review generated commands, code, and dependency changes before execution or application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anjasta-tarigan/skills/rust-best-practice)
- [Rust Best Practice Master Reference](artifact/SKILL.md)
- [Idiomatic Style, Naming, and Control Flow](artifact/references/01-idiomatic-style-and-naming.md)
- [Ownership, Borrowing, and Lifetimes](artifact/references/02-ownership-borrowing-lifetimes.md)
- [Error Handling](artifact/references/03-error-handling.md)
- [Traits, Generics, and Type Design](artifact/references/04-traits-generics-and-type-design.md)
- [Concurrency and Async](artifact/references/05-concurrency-and-async.md)
- [Performance and Memory](artifact/references/06-performance-and-memory.md)
- [Unsafe Rust](artifact/references/07-unsafe-rust.md)
- [Testing and Quality Assurance](artifact/references/08-testing-and-quality.md)
- [Tooling, Cargo, and CI](artifact/references/09-tooling-cargo-and-ci.md)
- [Web Backend and Networking](artifact/references/10-web-backend-and-networking.md)
- [CLI and Systems Tools](artifact/references/11-cli-and-systems-tools.md)
- [Project Structure, Workspaces, and Dependencies](artifact/references/12-project-structure-workspaces-and-dependencies.md)
- [Security and Supply-Chain](artifact/references/13-security-and-supply-chain.md)
- [The Rust Programming Language](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
- [Clippy Documentation](https://doc.rust-lang.org/clippy/)
- [RustSec Advisory Database](https://rustsec.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline Rust code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory guidance; generated code, commands, and dependency changes should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
