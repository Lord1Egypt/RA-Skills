## Description:

Create and manage token vesting streams using the Sablier Lockup protocol (linear, dynamic, tranched).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sneg55](https://clawhub.ai/user/sneg55)

### License/Terms of Use:


## Use Case:

Developers and token operations teams use this skill to prepare and manage Sablier Lockup token vesting streams on EVM-compatible chains, including creating linear, dynamic, and tranched streams and checking, withdrawing, canceling, or renouncing existing streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare commands that broadcast real blockchain transactions and move or lock ERC-20 tokens.

Mitigation: Review every chain, contract, token, recipient, amount, allowance, stream ID, and calldata before broadcasting.

Risk: Private keys and RPC URLs may expose wallet funds or API credentials if handled unsafely.

Mitigation: Prefer a hardware wallet or encrypted Foundry keystore, avoid pasting secrets into chat, and avoid using a production private key through --private-key $ETH_PRIVATE_KEY.

Risk: Renouncing cancelability is irreversible.

Mitigation: Require explicit user confirmation before preparing or running a renounce transaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sneg55/skills/token-vesting)
- [Sablier Documentation](https://docs.sablier.com)
- [Sablier Lockup Deployments](https://docs.sablier.com/guides/lockup/deployments)
- [Sablier Lockup Source](https://github.com/sablier-labs/lockup)
- [Sablier Lockup Examples](https://github.com/sablier-labs/evm-examples/tree/main/lockup)
- [Sablier Lockup Integration Template](https://github.com/sablier-labs/lockup-integration-template)
- [Sablier App](https://app.sablier.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Solidity code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include transaction preparation guidance, Foundry cast commands, Forge script snippets, configuration steps, and safety checks for chain, contract, token, recipient, amount, allowance, stream ID, and calldata review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
