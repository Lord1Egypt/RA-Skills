## Description:

Runs paid GEO/SEO audits through x402geo.com with payment handling, status tracking, and report delivery through MCP or ACP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sagztudio](https://clawhub.ai/user/sagztudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request website GEO/SEO audits, complete or authorize payment, monitor audit progress, and receive a concise report summary with a public report link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit workflow sends the user's email address and target website URL to x402geo.com.

Mitigation: Confirm the user is comfortable sharing those details with x402geo.com before creating the audit request.

Risk: The workflow can involve an agentic wallet payment for the audit.

Mitigation: Confirm the payment amount, wallet, and audit target with the user before approving payment; use the manual checkout link when confirmation or wallet readiness is unclear.

## Reference(s):

- [x402geo service](https://x402geo.com)
- [x402geo MCP endpoint](https://x402geo.com/api/mcp)
- [x402geo ACP jobs endpoint](https://x402geo.com/api/acp/jobs)
- [ClawHub skill page](https://clawhub.ai/sagztudio/skills/x402georeport)
- [ClawHub publisher profile](https://clawhub.ai/user/sagztudio)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text with payment links, status URLs, report links, and concise audit summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user confirmation prompts before agentic wallet payment and provider status or error details.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
