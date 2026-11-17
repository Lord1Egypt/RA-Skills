## Description:

Solana token launchpad with prediction markets, AI logo generation, website building, earnings checks, and API-driven token launch workflows that use a wallet address as identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicre8dev](https://clawhub.ai/user/aicre8dev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to launch Solana tokens, generate token logos, create or participate in prediction markets, build token landing pages, and check activity or earnings through Vybes.fun API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an undisclosed administrative reserve-changing page with wallet-signing code.

Mitigation: Do not use the admin page or approve wallet prompts unless you control the named authority wallet and have independently verified the transaction details.

Risk: The documented workflows rely on wallet-address identity, external website handoff, and irreversible SOL payment flows.

Mitigation: Review wallet identity, destination wallets, memo requirements, payment amounts, and transaction signatures before submitting or approving any on-chain action.

Risk: The security verdict is suspicious because safeguards around wallet identity and payments are weaker than expected.

Mitigation: Review the skill carefully before installation and limit use to workflows whose API calls, wallet prompts, and payment flows have been independently validated.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aicre8dev/skills/vybes-fun)
- [Publisher profile](https://clawhub.ai/user/aicre8dev)
- [Vybes.fun](https://vybes.fun)
- [aicre8.dev website builder](https://aicre8.dev)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples, wallet-address identity guidance, payment flow instructions, and response examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
