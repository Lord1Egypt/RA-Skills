## Description: <br>
SIWA (Sign-In With Agent) authentication for ERC-8004 registered agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildersgarden](https://clawhub.ai/user/buildersgarden) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add ERC-8004 agent identity, SIWA sign-in, authenticated request signing, and optional x402 payment flows to agent services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents wallet-signing, transaction, and x402 payment authority without consistently requiring clear approval or spend limits. <br>
Mitigation: Use a dedicated low-value or testnet wallet, require explicit approval for each onchain transaction or x402 payment, and set amount, network, recipient, and resource limits. <br>
Risk: Direct private-key based signing increases exposure if the agent or runtime is compromised. <br>
Mitigation: Prefer the keyring proxy over raw private keys, and review the external SDK or container before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/buildersgarden/siwa) <br>
- [Documentation](https://siwa.id/docs) <br>
- [SIWA Protocol Spec](references/siwa-spec.md) <br>
- [Security Model](references/security-model.md) <br>
- [ERC-8004 Registration Guide](references/registration-guide.md) <br>
- [Contract Addresses](references/contract-addresses.md) <br>
- [SIWA vs SIWX](references/siwa-vs-siwx.md) <br>
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [ERC-8128](https://eips.ethereum.org/EIPS/eip-8128) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet provider setup, server verification patterns, signing flows, registration metadata, and payment guidance.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
