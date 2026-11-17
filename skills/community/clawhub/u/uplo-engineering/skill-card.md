## Description:

AI-powered engineering knowledge management. Search architecture docs, API specs, incident reports, runbooks, and infrastructure documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to search organizational architecture docs, API specs, incident reviews, runbooks, repository metadata, and infrastructure records for RFC research, onboarding, code archaeology, incident review, and technical debt investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the skill runs an unpinned external MCP package with a secret API token.

Mitigation: Use a pinned and reviewed MCP server version, store the UPLO token as a dedicated least-privilege secret, and rotate it regularly.

Risk: The release evidence says the skill can expose broad organizational engineering context.

Mitigation: Confirm that organization-wide context export and update/reporting tools are authorized for the data the configured UPLO token can access.

Risk: The release evidence gives a suspicious security verdict.

Mitigation: Install only after reviewing the UPLO publisher, the @agentdocs1 npm package source, and the configured MCP server behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-engineering)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UPLO instance URL and API token; output may include organization-specific engineering context based on configured access.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
