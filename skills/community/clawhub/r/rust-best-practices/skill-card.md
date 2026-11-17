## Description:

Development guidance for writing idiomatic Rust functions, modules, ownership patterns, Result-based error handling, performance tuning, Clippy configuration, dispatch choices, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill while building Rust code to choose idiomatic ownership, error handling, API design, performance, linting, documentation, and dispatch patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following generated development commands can modify a Rust project or install Cargo tooling.

Mitigation: Review commands before execution, avoid elevated privileges, and pin cargo-installed tool versions when practical.

Risk: Guidance may be applied to the wrong Rust crate context or used to claim performance improvements without evidence.

Mitigation: Run the documented Clippy, documentation, and before-and-after measurement gates before relying on the result.

## Reference(s):

- [Rust Best Practices](artifact/SKILL.md)
- [API Design](artifact/references/api-design.md)
- [Clippy Configuration](artifact/references/clippy-config.md)
- [Coding Idioms](artifact/references/coding-idioms.md)
- [Documentation](artifact/references/documentation.md)
- [Ecosystem Patterns](artifact/references/ecosystem-patterns.md)
- [Generics and Dispatch](artifact/references/generics-dispatch.md)
- [Performance](artifact/references/performance.md)
- [Pointer Types](artifact/references/pointer-types.md)
- [Type State Pattern](artifact/references/type-state-pattern.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Rust code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No credentials required; commands are ordinary Rust development workflow commands.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
