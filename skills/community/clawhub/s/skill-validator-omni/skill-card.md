## Description:

Validates skills against seven authoring standards across all agents for audit and certification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelpro](https://clawhub.ai/user/adelpro)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill publishers use this validator to audit agent skills, plugins, or repositories against multiple authoring and installability standards before publishing or using them as a CI gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented workflow uses unpinned npm CLI commands that can change after review.

Mitigation: Prefer running node scripts/validate.js from the reviewed artifact, or pin every npm CLI invocation to an exact trusted version and run it away from broad filesystem access, repository tokens, deployment credentials, and other secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adelpro/skills/skill-validator-omni)
- [Frontmatter Template](references/frontmatter-template.md)
- [Agent Plugins 1.0.0 plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
- [Agent Plugins 1.0.0 MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)
- [agentskills.io discovery schema](https://schemas.agentskills.io/discovery/0.2.0/schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish passing checks, failed checks, and usage errors.]

## Skill Version(s):

2.5.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
