## Description:

Reviews Rust code for ownership, borrowing, lifetimes, error handling, trait design, unsafe usage, common mistakes, and Rust 2024 idioms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Rust projects for ownership and borrowing issues, lifetime design, error handling, trait and interface design, unsafe code, and concurrency risks before changes are merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend standard Rust checks or shell commands against code that is not trusted.

Mitigation: Review proposed commands before execution and run them in a trusted sandbox or disposable checkout when code is untrusted.

Risk: Review guidance can be incorrect or incomplete for complex ownership, unsafe, or concurrency cases.

Mitigation: Treat findings as review assistance and verify material issues against the relevant Rust source, tests, and project constraints before making changes.

## Reference(s):

- [Rust Code Review](SKILL.md)
- [Ownership and Borrowing](references/ownership-borrowing.md)
- [Lifetime Variance](references/lifetime-variance.md)
- [Error Handling](references/error-handling.md)
- [Async and Concurrency](references/async-concurrency.md)
- [Concurrency Primitives](references/concurrency-primitives.md)
- [Memory Ordering](references/memory-ordering.md)
- [Lock-Free Patterns: Hand-Rolled Concurrency Review](references/lock-free-patterns.md)
- [Concurrency Models](references/concurrency-models.md)
- [Types and Layout](references/types-layout.md)
- [Interface Design](references/interface-design.md)
- [Patterns in the Wild](references/patterns-in-the-wild.md)
- [Unsafe Code, API Design, and Derive Patterns](references/common-mistakes.md)
- [Unsafe Code: Deep Review](references/unsafe-deep.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown review report with file-line findings, severity labels, concise explanations, and optional suggested Rust checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No generated files are required.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
