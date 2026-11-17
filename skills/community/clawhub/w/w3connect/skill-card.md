## Description:

Gets an ETH-compatible wallet address and triggers ETH or USDC transfers on Base through a local wallet service with one-time authenticator-code verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernel1983](https://clawhub.ai/user/kernel1983)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent retrieve a wallet address, prepare local wallet-service calls, and initiate ETH or USDC transfers when the user supplies and verifies the required payment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-triggered payment commands can transfer real ETH or USDC.

Mitigation: Require manual review before every payment and personally verify the destination address or email, token, chain, amount, and fees.

Risk: Authenticator codes are sensitive and may be exposed through URLs, command lines, or shared logs.

Mitigation: Avoid placing authenticator codes in shared logs or transcripts and only provide them when ready to execute a reviewed transaction.

Risk: The skill depends on a trusted local wallet service to perform address lookup and transfers.

Mitigation: Install and use the skill only when the local wallet service is trusted and under the user's control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kernel1983/skills/w3connect)
- [GET_ADDRESS.md](artifact/GET_ADDRESS.md)
- [SEND.md](artifact/SEND.md)
- [PAY_TO_EMAIL.md](artifact/PAY_TO_EMAIL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands for local wallet-service endpoints.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
