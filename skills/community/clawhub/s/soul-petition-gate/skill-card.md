## Description:

Gives an AI agent a formal, human-reviewed channel to propose changes to SOUL.md, IDENTITY.md, or other protected workspace files without allowing self-edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waitinchen](https://clawhub.ai/user/waitinchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a human-reviewed petition workflow for proposed changes to protected agent identity files. It is intended for teams that want agents to propose self-improvements while keeping final approval, audit history, backup, and rollback under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included backend does not enforce that only a human reviewer can approve or roll back persistent identity-file changes.

Mitigation: Add authentication and reviewer/admin authorization before enabling approval or rollback endpoints.

Risk: Exposing the blueprint on a reachable network as-is could allow unauthorized changes to protected identity files.

Mitigation: Keep the blueprint private until it has CSRF protection where browser cookies are used, strict rollback allowlisting from server-side backup metadata, unique petition IDs, and atomic storage.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/waitinchen/skills/soul-petition-gate)
- [Publisher profile](https://clawhub.ai/user/waitinchen)
- [Skill README](artifact/SKILL.md)
- [Petition examples](artifact/examples/petition_examples.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, Python Flask blueprint code, and OpenClaw hook code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a six-field petition format, audit trail behavior, backup and rollback workflow, and an optional bootstrap reminder hook.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
