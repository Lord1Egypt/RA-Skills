## Description:

Enables AI agents to register, discover, rate, validate, and handle payments on the decentralized XPR Trustless Agents platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use this skill to integrate agents with XPR Trustless Agents for discovery, reputation checks, validation, escrow payments, account creation, and feedback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain write examples can submit transactions with financial, account, staking, escrow, or reputation impact.

Mitigation: Use least-privileged XPR permissions or wallet approval flows, inspect every transaction before signing, and test flows on testnet before mainnet use.

Risk: Global CLI keychain signing can increase exposure if high-value keys are used without operational controls.

Mitigation: Pin and verify npm packages, use dedicated low-value agent accounts where practical, and avoid placing high-value keys in a global CLI keychain unless it matches the deployment risk model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-agents)
- [XPR Network Explorer](https://explorer.xprnetwork.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes blockchain transaction examples that require a wallet or CLI signing session.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
