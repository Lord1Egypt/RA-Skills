## Description:

AI-powered banking knowledge management. Search KYC records, regulatory reports, risk assessments, and loan processing documentation with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Banking, compliance, risk, and operations teams use this skill to search institutional knowledge for KYC/AML records, regulatory reports, risk assessments, loan documentation, directives, and responsible knowledge owners. It helps agents answer with sourced banking context while respecting classification limits and reporting unavailable information honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive banking, financial, compliance, and customer records.

Mitigation: Use server-side role and record-level access controls, short-lived narrowly scoped UPLO tokens, masking where appropriate, and strict classification enforcement.

Risk: The skill can export broad organizational context.

Mitigation: Require explicit approval for export_org_context and limit access to roles with a documented business need.

Risk: Conversation logging can capture regulated or confidential information.

Mitigation: Disable logging unless governed by consent, redaction, retention, and audit controls.

Risk: Runtime execution depends on an MCP server package and endpoint that must be trusted.

Mitigation: Use only a pinned and reviewed MCP server connected to an approved UPLO instance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-banking)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured UPLO MCP endpoint and API key; responses should cite source records and respect classification tiers.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
