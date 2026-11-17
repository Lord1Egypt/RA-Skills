## Description:

Provides workflows, schemas, and code patterns for integrating agents with QuickBooks Online APIs, including OAuth, accounting entities, webhooks, reporting, payments, query handling, and MCP server configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build QuickBooks Online integrations and agent workflows for authentication, accounting data access, payments, reporting, webhook processing, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-driven payment, charge, refund, bill, journal, or account-changing operations may create unintended financial changes.

Mitigation: Require explicit human approval and deterministic checks before executing any accounting or payment-changing action.

Risk: QuickBooks OAuth refresh tokens and client secrets can expose accounting data or allow account changes if mishandled.

Mitigation: Protect refresh tokens and secrets, start with sandbox or read-only scopes, and encrypt stored tokens.

Risk: The MCP server installation path includes an unpinned npm dependency workflow.

Mitigation: Pin and audit the MCP server dependency before running npm install or connecting it to production credentials.

## Reference(s):

- [QuickBooks Online API documentation](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api)
- [QuickBooks Online MCP Server](https://github.com/intuit/quickbooks-online-mcp-server.git)
- [Authentication and authorization reference](artifact/authentication.md)
- [Query language and error handling reference](artifact/queries_and_errors.md)
- [Webhooks reference](artifact/webhooks.md)
- [AI and MCP server integration reference](artifact/ai_and_mcp.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON, Python, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QuickBooks OAuth credentials and realm ID for live API use.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
