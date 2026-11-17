## Description:

SurrealDB Surrealism WASM extension development. Write Rust functions, compile to WASM, deploy as database modules. Part of the surreal-skills collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24601](https://clawhub.ai/user/24601)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build SurrealDB 3 WASM extensions in Rust, compile them with the SurrealDB CLI, and register them as database modules callable from SurrealQL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Quick Start uses root/root credentials for an isolated local SurrealDB example.

Mitigation: Do not reuse those credentials outside local testing; avoid real passwords on command lines and create least-privileged database users for shared or production environments.

Risk: Surrealism is described as actively in development and not yet stable.

Mitigation: Confirm API compatibility against the target SurrealDB 3.x release before adopting generated setup or deployment guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/24601/skills/surrealism)
- [SurrealDB Extensions Documentation](https://surrealdb.com/docs/surrealdb/extensions)
- [SurrealDB CLI Module Reference](https://surrealdb.com/docs/surrealdb/cli/module)
- [SurrealDB Repository](https://github.com/surrealdb/surrealdb)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Rust, TOML, and SurrealQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers local project setup, WASM compilation, module registration, use cases, and stability cautions.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata; artifact frontmatter metadata.version is 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
