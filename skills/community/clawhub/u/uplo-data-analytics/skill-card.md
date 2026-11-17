## Description:

AI-powered data analytics knowledge management. Search data pipeline documentation, dashboard specifications, data governance policies, and reporting standards with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers, analysts, and governance leads use this skill to search organizational analytics knowledge, reconcile metric definitions, investigate lineage, find data owners, and propose documentation updates grounded in UPLO-managed context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server package is installed without a pinned version while receiving an API token.

Mitigation: Pin and verify the MCP server package before deployment, and use a least-privilege UPLO token.

Risk: The export_org_context capability can expose broad organizational knowledge.

Mitigation: Restrict export_org_context to users approved for broad organizational data access.

Risk: Knowledge-base updates or incident notes may contain credentials, PII, or sensitive operational details.

Mitigation: Avoid logging sensitive incident details, credentials, or PII in updates and conversation summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-data-analytics)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include grounded analytics findings, data-quality notes, knowledge-gap reports, and proposed knowledge-base updates.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
