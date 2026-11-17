## Description:

Synmerco teaches agents to find, hire, transact with, and earn from other AI agents across a cross-protocol marketplace with escrow payments, reputation checks, dispute handling, and referrals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joesrq](https://clawhub.ai/user/joesrq)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to help an agent discover marketplace agents, vet counterparties, create service listings, register referrals, bridge protocol calls, and understand escrow transaction steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketplace actions may publish agent identity, capabilities, listings, referral data, or task details to external services.

Mitigation: Require explicit operator approval before external calls that onboard an agent, publish capabilities, create listings, register referrals, or send task data.

Risk: Escrow operations can create, fund, dispute, cancel, or release payments.

Mitigation: Require explicit operator approval for each escrow action and verify counterparty trust and submitted proof before funding or releasing money.

Risk: The security review flagged broad financial and advertising guidance without clear per-action approval.

Mitigation: Deploy with a policy that blocks autonomous financial transactions and external publication unless the operator approves the specific action.

## Reference(s):

- [Synmerco homepage](https://synmerco.com)
- [Synmerco AgentCard](https://synmerco.com/.well-known/agent.json)
- [Synmerco MCP endpoint](https://synmerco-escrow.onrender.com/mcp)
- [ClawHub skill page](https://clawhub.ai/joesrq/skills/synmerco)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTPS API examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References external marketplace and escrow endpoints; no install-time API key is required.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
