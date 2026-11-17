## Description:

AI-powered defense knowledge management. Search mission documentation, logistics records, personnel data, and ITAR-controlled information with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Defense program managers, logistics officers, export-control staff, security officers, and other authorized users use this skill to search controlled mission, logistics, personnel, contract, and technical documentation through UPLO while respecting clearance, program access, and need-to-know constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive defense and export-controlled information.

Mitigation: Install only in an authorized defense environment and confirm server-side clearance, need-to-know, and export-control enforcement before use.

Risk: The MCP configuration runs an unpinned npm server with a user API token.

Mitigation: Use a narrowly scoped, revocable UPLO token and prefer a pinned or locally reviewed MCP server package instead of unpinned npx execution.

Risk: Organizational context export can expose sensitive program structure, personnel, subcontractor, or systems-of-record information.

Mitigation: Restrict export_org_context to approved users and log controlled-data sessions for auditability.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-defense)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline MCP tool calls, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPLO instance URL and secret API key; outputs may include search results, organizational context, directives, guidance, and audit-log actions subject to the connected knowledge base and access controls.]

## Skill Version(s):

1.0.0 (source: evidence release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
