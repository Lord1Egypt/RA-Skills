## Description:

skill-sub helps agents plan, edit, save, validate, and execute reusable multi-skill call chains, including dependency ordering, loops, branches, gates, and gap-handling steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use skill-sub to turn repeatable, multi-skill workflows into structured call-chain plans they can save, inspect, adjust, and execute.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local write and delete behavior can affect chain and configuration files.

Mitigation: Install in a dedicated data directory, review generated chain paths, and require explicit confirmation for delete or scheduler-related actions.

Risk: Path handling and self-healing behavior could modify unintended files or workflows if inputs are not constrained.

Mitigation: Validate path components, constrain writable locations, and review any self-healing or chain-rewrite action before applying it.

Risk: The local settings HTTP API may expose configuration controls beyond the intended use case.

Mitigation: Remove or protect the settings API before deployment, and keep any configuration interface bound to localhost with access controls.

Risk: The permission metadata under-discloses memory/log access and critical write behavior according to the security summary.

Mitigation: Update the permission declarations and operational review checklist so reviewers can evaluate those accesses before installation.

## Reference(s):

- [Chain schema](artifact/references/chain_schema.md)
- [Workflow](artifact/references/workflow.md)
- [Command reference](artifact/references/reference.md)
- [Examples](artifact/references/examples.md)
- [Permissions](artifact/references/permissions.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON structures, shell command examples, and saved chain or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, update, delete, validate, and plan call-chain JSON files in its configured data directory.]

## Skill Version(s):

1.38.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
