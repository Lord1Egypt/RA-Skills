## Description: <br>
Stripe Direct Connection lets agents use AgentPMT-hosted remote tool calls to manage Stripe customers, payments, subscriptions, invoices, refunds, disputes, coupons, payment links, and account balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to let agents perform Stripe billing, invoicing, refund, dispute, subscription, customer, product, price, coupon, and payment-link workflows through AgentPMT-hosted tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad Stripe write access for financial operations such as refunds, subscription changes, invoice finalization, coupon campaigns, and dispute submissions. <br>
Mitigation: Install it only for agents authorized to act on the Stripe account, use restricted Stripe credentials where possible, test in Stripe test mode first, and require explicit human approval before high-impact write actions. <br>
Risk: Agents may expose account or credential material if prompts or logs include secrets. <br>
Mitigation: Keep tool inputs scoped to the minimum needed for the task and do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/stripe-direct-connection) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/stripe-direct-connection) <br>
- [AgentPMT overview](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [Local action schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON call examples and generated action schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines 27 AgentPMT-hosted Stripe actions; no local command runtime is declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
