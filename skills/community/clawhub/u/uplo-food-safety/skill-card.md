## Description:

AI-powered food safety knowledge management. Search HACCP plans, FDA compliance records, traceability documentation, and quality control data with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Food safety, quality, compliance, and operations teams use this skill to search HACCP plans, FDA/USDA compliance records, traceability documentation, supplier audits, sanitation records, and quality control data. It supports audit response, recall tracing, knowledge-gap reporting, and food-safety decision support grounded in an organization's UPLO knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server while using an API token.

Mitigation: Install only from a trusted package source, pin or otherwise control the MCP server version where possible, and issue a least-privilege API token.

Risk: The skill exposes broad organizational export capability for sensitive food-safety records.

Mitigation: Disable or restrict full organizational export unless required, and rely on server-side access controls, auditing, and redaction.

Risk: Food-safety records can include confidential HACCP, compliance, supplier, traceability, and recall information.

Mitigation: Verify user access before querying and respect classification tiers for confidential or restricted records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-food-safety)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline tool calls, query examples, and JSON or shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted UPLO instance and API token; outputs may reference confidential food-safety, supplier, traceability, compliance, and recall records according to server-side access controls.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
