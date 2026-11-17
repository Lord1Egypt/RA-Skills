## Description:

AI-powered hospitality knowledge management. Search guest service standards, property procedures, F&B operations, and event planning documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Hospitality employees and operators use this skill to retrieve property-specific procedures, guest service standards, event planning details, F&B operations guidance, and organizational directives from a UPLO knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a third-party MCP server package that is not pinned in the provided install example.

Mitigation: Install only from a trusted npm package source and pin or otherwise control the MCP server version before deployment.

Risk: The skill requires an API token for a UPLO knowledge base.

Mitigation: Use a least-privilege, rotatable UPLO token and store it through approved secret-management controls.

Risk: The skill can expose broad organizational context through export capabilities.

Mitigation: Restrict full organizational exports to authorized users and approved business needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-hospitality)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline command examples and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a configured UPLO instance URL and API token to query organization-specific hospitality knowledge.]

## Skill Version(s):

1.0.0 (source: evidence release version and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
