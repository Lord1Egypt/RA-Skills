## Description:

Audit Rust code for unsafe block usage by checking safety invariants, FFI boundaries, raw pointer operations, Send/Sync implementations, and potentially unsound abstractions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit Rust crates, dependencies, and FFI-heavy code for unsafe-code soundness, documentation gaps, and memory-safety risks before publishing or security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest Rust tooling commands such as clippy, miri, cargo audit, or cargo geiger that read or analyze local project source.

Mitigation: Review proposed commands before running them, especially on sensitive or very large repositories.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit summaries with inline shell commands and review tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces unsafe-code inventories, critical findings, documentation-gap tables, and remediation recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
