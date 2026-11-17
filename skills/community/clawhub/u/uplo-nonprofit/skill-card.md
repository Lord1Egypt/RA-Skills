## Description:

AI-powered nonprofit knowledge management. Search grant documentation, donor records, program reports, and compliance data with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Nonprofit staff and their AI agents use this skill to search grant, donor, program, board, and compliance knowledge; extract structured metrics; and prepare grant proposals, board packets, funder reports, audits, and onboarding briefs grounded in the organization's records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server with an API token.

Mitigation: Install only from a trusted UPLO MCP package source, prefer a pinned and reviewed server version, restrict the API token to minimum permissions, and run the server in a constrained environment.

Risk: Searches and organization exports may include donor, board, financial, grant, and compliance records.

Mitigation: Treat all retrieved results and exported organizational context as confidential unless classification tiers and user clearance explicitly allow disclosure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-nonprofit)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)
- [Publisher Profile](https://clawhub.ai/user/roojenkins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool-call examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UPLO instance URL and API key; outputs may include confidential organizational records subject to classification tiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
