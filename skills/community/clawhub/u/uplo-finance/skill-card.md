## Description:

AI-powered financial knowledge management. Search financial statements, audit findings, tax documents, and treasury records with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, treasury, audit, and FP&A teams use this skill to search organizational financial records, retrieve period-sensitive policies and figures, investigate variances, and locate responsible knowledge owners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is launched from an unpinned third-party npm package while receiving a sensitive finance API token.

Mitigation: Pin and verify the MCP package version, use a dedicated least-privilege UPLO token, protect and rotate the API key, and run the server with limited filesystem and network access.

Risk: The skill can export organizational context and retrieve restricted financial, audit, tax, treasury, M&A, projection, or executive compensation information.

Mitigation: Restrict export_org_context and sensitive search workflows to approved users, enforce classification tiers, and review summaries before sharing privileged or confidential finance information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-finance)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds responses in configured UPLO financial knowledge sources and should preserve reporting period, document type, preparation date, classification tier, and knowledge-owner context when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
