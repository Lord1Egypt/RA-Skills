## Description:

AI-powered knowledge management intelligence. Search taxonomies, content curation records, expertise directories, and communities of practice with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge management practitioners, content stewards, and organizational leaders use this skill to search UPLO-indexed taxonomies, expertise directories, content lifecycle records, and communities of practice. It supports knowledge audits, taxonomy governance, expertise lookup, content freshness review, and knowledge gap reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can export broad organizational context, which may include sensitive knowledge assets, expertise data, or strategic information.

Mitigation: Use narrowly scoped UPLO tokens, respect classification tiers, and require explicit approval before full organizational context exports.

Risk: The MCP server is launched through an unpinned npm package command.

Mitigation: Pin and review the MCP server package version before deployment, and install only from a trusted package source.

Risk: The skill requires an API token for UPLO access.

Mitigation: Store the token as a secret, rotate it regularly, and grant only the minimum permissions needed for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-knowledge-management)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured MCP tools to retrieve organizational knowledge; outputs can include sensitive internal knowledge-management context when authorized.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
