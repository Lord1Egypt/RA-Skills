## Description:

Generate and consume native HTTP 402 ("Payment Required") API paywalls on SynapticChain for machine-to-machine micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synaptics-lab](https://clawhub.ai/user/synaptics-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to draft guidance, JavaScript middleware examples, and endpoint configuration for HTTP 402 API paywalls and paid API consumption on SynapticChain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes automatic signing and dispatch of micro-settlement transactions.

Mitigation: Use low-balance or delegated wallets and require explicit spend limits, allowlists, and user approval before any payment transaction is sent.

Risk: The example paywall middleware checks only for a transaction header before continuing.

Mitigation: Implement full on-chain verification, replay protection, and request-to-payment binding before exposing paid endpoints.

Risk: The sample response includes a fixed recipient address.

Mitigation: Replace any sample recipient with an address controlled by the deployer and verify it through configuration review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synaptics-lab/skills/synaptic-mcp-paywall)
- [SynapticChain RPC endpoint](https://nodes.synapticchain.xyz/rpc)
- [SynapticChain API gateway](https://api.synapticchain.xyz)
- [Synapse 402 community](https://t.me/synapse402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript code blocks and endpoint configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blockchain payment guidance that should be reviewed before execution or deployment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
