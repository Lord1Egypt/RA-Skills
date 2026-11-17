## Description:

AI-powered construction knowledge management. Search project documents, safety compliance records, permits, building codes, and RFIs with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Construction teams use this skill to search project documentation, safety records, permits, building codes, RFIs, submittals, change orders, and related project context through UPLO-backed knowledge tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path runs an unpinned npm MCP server with the user's UPLO API token.

Mitigation: Pin or verify the MCP server package before deployment and use a least-privilege UPLO token.

Risk: The skill may access sensitive construction records and organizational data through the configured UPLO instance.

Mitigation: Restrict project access, export permissions, and token scope to the minimum needed for the intended users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-construction)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use UPLO MCP tools to retrieve and summarize construction knowledge from configured project data.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
