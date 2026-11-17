## Description:

Manage SOC 2, HIPAA, ISO 27001, and ISO 42001 compliance with Screenata. Use for workspace readiness, failing security tests, evidence collection, policy drafting, risk review, and audit preparation through Screenata's hosted MCP tools. Requires a Screenata account and authorized MCP connection. General framework explanations do not require Screenata tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[screenata](https://clawhub.ai/user/screenata)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance and security teams use the skill to review workspace readiness, failing checks, audit blockers, controls, policies, and risks; collect evidence; and prepare authorized fixes or policy drafts through Screenata. It also answers general framework questions without workspace access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes low-probability findings involving a Screenata URL and user-confirmation wording, which it considers expected for the skill's purpose.

Mitigation: Verify the Screenata endpoint and selected workspace, and review the target and effects before authorizing scans, uploads, or changes.

Risk: Readiness scores and passing checks could be mistaken for an audit report or certification.

Mitigation: Describe scores and checks as readiness or automated results; the user's auditor issues audit reports and certifications.

## Reference(s):

- [Screenata MCP connection guide and tool overview](https://github.com/Screenata/screenata-mcp)
- [Screenata](https://screenata.com)
- [Screenata app](https://app.screenata.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown summaries, recommendations, and draft policy content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workspace-specific; may include compliance findings, next steps, evidence guidance, or drafts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
