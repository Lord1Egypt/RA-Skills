## Description:

Create and manage USDC escrows for agent-to-agent payments on Base Sepolia. 30% gas savings, batch operations, dispute resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droppingbeans](https://clawhub.ai/user/droppingbeans)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to create, inspect, release, cancel, dispute, and batch-manage USDC escrows for agent-to-agent payments on Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples that can sign blockchain transactions involving USDC allowances and escrow actions.

Mitigation: Verify the network, contract address, receiver address, amount, token decimals, deadline, and allowance size; use test funds; approve only the minimum needed; and require explicit human review before wallet signing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/droppingbeans/skills/trust-escrow)
- [Trust Escrow Web App](https://trust-escrow-web.vercel.app)
- [Agent Docs](https://trust-escrow-web.vercel.app/agent-info)
- [Integration Guide](https://trust-escrow-web.vercel.app/skill.md)
- [Base Sepolia Contract](https://sepolia.basescan.org/address/0x6354869F9B79B2Ca0820E171dc489217fC22AD64)
- [llms.txt](https://trust-escrow-web.vercel.app/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, API calls]

**Output Format:** [Markdown with TypeScript examples and contract call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Base Sepolia and USDC escrow contract interactions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
