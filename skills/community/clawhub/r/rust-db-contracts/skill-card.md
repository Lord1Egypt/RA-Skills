## Description:

Guides agents working on Rust and SeaORM projects to make Entity files the complete, explicit contract for database schema, typing, transactions, documentation, and CI checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiamu-ssr](https://clawhub.ai/user/xiamu-ssr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when modifying Rust + SeaORM projects to keep database contracts explicit in Entity files and to check for unsafe patterns such as raw SQL, weak JSON typing, missing state-transition checks, and soft-delete query gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled checker may not reliably enforce mandatory state-transition and soft-delete rules as a blocking security gate.

Mitigation: Review the checker before CI-blocking use and add tests or stronger project-specific checks for state transitions and soft-delete filters.

Risk: Database guidance can lead to unsafe or inconsistent changes if generated code is accepted without review.

Mitigation: Review generated entity and data-access changes against the database safety examples before deployment.

## Reference(s):

- [Entity File Complete Example](references/ENTITY_EXAMPLE.md)
- [Database Contract Checker](references/check_db_contracts.sh)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Rust and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional CI shell checker and a SeaORM entity example.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
