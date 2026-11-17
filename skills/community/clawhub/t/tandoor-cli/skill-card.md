## Description:

Manage recipes, meal plans, and shopping lists on a Tandoor Recipe Manager instance via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcenatiempo](https://clawhub.ai/user/dcenatiempo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate tandoor-cli against a configured Tandoor Recipe Manager instance for recipe lookup, meal planning, shopping list management, cook logs, and approved write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can modify or delete Tandoor data when granted write-capable credentials.

Mitigation: Use read-only tokens for lookup workflows and require explicit user approval before write, destructive, bulk, household, or invite commands.

Risk: An unpinned npm installation path could run a different tandoor-cli version than the reviewed skill release.

Mitigation: Pin the CLI to version 1.5.0 before installing or running it, and review the package and repository before granting credentials.

Risk: Admin or space-owner tokens can grant broader access than normal recipe and shopping-list tasks require.

Mitigation: Use short-lived, least-privileged tokens and avoid admin or space-owner credentials unless the specific task requires them.

## Reference(s):

- [Tandoor Recipe CLI on ClawHub](https://clawhub.ai/dcenatiempo/skills/tandoor-cli)
- [tandoor-cli repository](https://github.com/dcenatiempo/tandoor-cli)
- [tandoor-cli npm package](https://www.npmjs.com/package/tandoor-cli)
- [Tandoor Recipe Manager](https://tandoor.dev)
- [Setup Guide](references/SETUP.md)
- [Security Guidelines](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output may be text, slim JSON, or raw Tandoor API JSON depending on the selected format flag.]

## Skill Version(s):

1.5.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
