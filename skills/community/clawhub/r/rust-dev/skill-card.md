## Description:

Day-1 guide to building well in Rust - ownership, errors as values, String vs &str, Box/Rc/Arc, anyhow vs thiserror, and a crate shortlist (tokio, serde, axum, sqlx). Use when starting a Rust project, fighting the borrow checker, or picking crates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers starting Rust CLI, service, or library projects use this guide to understand ownership, borrowing, error handling, crate choices, and day-one project setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An example exposes API tokens.

Mitigation: Remove or redact the token-printing example before using the guide to make changes.

Risk: Some performance advice weakens system security.

Mitigation: Retain host security protections and explicitly scope any profiling-policy change.

Risk: Optional cache setup can affect daemon behavior, cleanup, and remote sharing.

Mitigation: Preview the cache setup and review its daemon, cleanup, and remote-sharing effects before enabling it.

## Reference(s):

- [Ownership and types](references/ownership-and-types.md)
- [Error handling](references/error-handling.md)
- [Crate shortlist](references/crate-shortlist.md)
- [Development environment](references/dev-environment.md)
- [Testing](references/testing.md)
- [Publisher project homepage](https://github.com/tenequm/skills/tree/main/skills/rust-dev)
- [ClawHub skill release](https://clawhub.ai/tenequm/skills/rust-dev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Rust code examples, shell commands, and Cargo configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.9.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
