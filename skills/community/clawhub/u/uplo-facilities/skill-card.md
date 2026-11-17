## Description:

AI-powered facilities knowledge management for searching building management records, maintenance schedules, space planning data, and vendor service documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Facilities, operations, workplace, and real estate teams use this skill to query organization-specific building records, maintenance history, vendor contracts, space utilization, inspection status, and facilities directives. It helps agents ground facilities answers in connected UPLO knowledge rather than unsourced general guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned remote npm MCP server with a secret token.

Mitigation: Install only after reviewing the UPLO and @agentdocs1 npm supply chain, use a narrowly scoped UPLO token, and prefer a pinned and reviewed MCP server version.

Risk: Broad organizational facilities exports can expose sensitive internal building, vendor, occupancy, or maintenance data.

Mitigation: Restrict endpoint and network access, limit who can run full context exports, and handle exported facilities context as sensitive internal data.

Risk: Facilities records, inspection certificates, vendor contracts, and maintenance schedules may be stale or superseded.

Mitigation: Check effective dates and completion status before acting, and use the provided stale-document flagging workflow when outdated records are found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-facilities)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and MCP tool invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require access to a configured UPLO MCP server and organization-specific facilities data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
