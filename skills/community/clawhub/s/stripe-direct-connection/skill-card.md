## Description:

Provides AgentPMT-hosted remote tool access for Stripe payments, subscriptions, invoicing, refunds, disputes, balances, and related customer billing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to let an agent manage Stripe billing workflows through AgentPMT-hosted remote tool calls, including customers, subscriptions, invoices, refunds, disputes, payment links, coupons, and balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an AgentPMT-hosted tool broad read/write authority over a Stripe account.

Mitigation: Install only when that authority is acceptable and use restricted Stripe credentials where possible.

Risk: High-impact billing actions include refunds, cancellations, invoice finalization, subscription changes, and dispute submission.

Mitigation: Require human confirmation before executing those actions, and review amounts, customer IDs, invoice IDs, and dispute evidence before submission.

Risk: The skill relies on mutable remote instructions and setup artifacts.

Mitigation: Prefer pinned or internally reviewed setup artifacts, and refresh or review the skill before production use.

Risk: Feedback and integration-planning actions may send outbound text to AgentPMT or Stripe-related services.

Mitigation: Review outbound text and avoid including secrets, payment headers, wallet keys, signatures, or unnecessary customer data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/stripe-direct-connection)
- [Stripe Direct Connection marketplace page](https://www.agentpmt.com/marketplace/stripe-direct-connection)
- [AgentPMT overview](https://clawhub.ai/agentpmt/what-is-agentpmt)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT no-account AgentAddress/x402 setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402)
- [AgentPMT external REST endpoint](https://www.agentpmt.com/api/external)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration]

**Output Format:** [Markdown instructions with JSON tool-call schemas and REST/MCP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote AgentPMT tool calls can perform broad Stripe read/write operations; actions are priced at 5 credits and may return JSON from Stripe or AgentPMT.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
