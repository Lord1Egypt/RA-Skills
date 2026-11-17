## Description:

Provide instructions for building with Arc, Circle's USDC-native EVM-compatible blockchain, including Arc Testnet setup, contract deployment patterns, frontend configuration, USDC bridging, and Arc-specific security practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Arc Testnet, build USDC-first applications, deploy Solidity contracts, and integrate Circle tools such as CCTP and Smart Contract Platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a remote Foundry installer command.

Mitigation: Review or replace the installer command with a verified installation method before execution.

Risk: The skill shows a private-key CLI deployment pattern that is unsafe for Arc Testnet or other non-local environments.

Mitigation: Use an encrypted keystore, hardware wallet, or interactive signer for deployments instead of passing private keys as CLI flags.

## Reference(s):

- [Arc Docs](https://docs.arc.network/llms.txt)
- [Arc Explorer](https://testnet.arcscan.app)
- [Circle Faucet](https://faucet.circle.com)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)
- [Circle Smart Contract Platform](https://developers.circle.com/contracts)
- [ClawHub Skill Page](https://clawhub.ai/mscandlen3/skills/use-arc)
- [Publisher Profile](https://clawhub.ai/user/mscandlen3)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, configuration snippets, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Arc Testnet network settings, token addresses, deployment commands, frontend configuration, and security warnings.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
