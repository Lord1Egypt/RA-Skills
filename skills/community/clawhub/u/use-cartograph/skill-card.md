## Description:

Use when Cartograph CLI or MCP is available and you need repository orientation, task-scoped context, or doc inputs with minimal token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthony-maio](https://clawhub.ai/user/anthony-maio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to orient in a repository with Cartograph, gather task-scoped context, and prepare documentation inputs while minimizing token use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository inspection may expose private code or documentation to provider-backed documentation generation if that mode is chosen.

Mitigation: Prefer static Cartograph commands for private repositories unless provider-backed documentation generation is intentional.

Risk: Guidance depends on Cartograph or its MCP server being available in the agent environment.

Mitigation: Check for Cartograph availability first and switch to repo-surveyor when it is unavailable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Cartograph run IDs and artifacts instead of long prose.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
