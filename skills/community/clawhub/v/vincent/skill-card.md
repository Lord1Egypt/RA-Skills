## Description:

Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction. Also supports raw signing and Polymarket betting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give agents controlled wallet capabilities for token transfers, swaps, EVM contract calls, raw signing, and Polymarket activity. Wallet owners use claim links and policies to set spending limits, allowlists, and approval requirements before funding or authorizing the agent wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad financial authority through a hosted wallet service.

Mitigation: Use it only with a trusted wallet service, claim the wallet immediately, and configure approval requirements, spending limits, and allowlists before funding it.

Risk: API keys and re-link tokens can authorize wallet access.

Mitigation: Store API keys in a real secret store, treat re-link tokens like wallet credentials, and rotate or recover access only through the documented owner-controlled flow.

Risk: The security summary notes fail-open policy behavior when no policies are set.

Mitigation: Set explicit address, token, function, and spending policies before allowing an agent to transact.

Risk: The Polymarket balance call can deploy a Safe and approve collateral.

Mitigation: Use Polymarket wallet operations only after the owner understands the Safe deployment and collateral approval behavior.

## Reference(s):

- [Vincent ClawHub skill page](https://clawhub.ai/glitch003/skills/vincent)
- [Vincent service](https://heyvincent.ai)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet setup and operational instructions; API responses may include wallet addresses, claim URLs, balances, order data, transaction status, and signatures.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
