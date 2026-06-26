## Description: <br>
Create and manage USDC escrows for agent-to-agent payments on Base Sepolia. 30% gas savings, batch operations, dispute resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droppingbeans](https://clawhub.ai/user/droppingbeans) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Trust Escrow to create, monitor, release, cancel, dispute, and batch USDC escrow payments for agent-to-agent work on Base Sepolia. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-signing and USDC approval examples can authorize token movement or allowances if used without review. <br>
Mitigation: Approve each transaction only after checking the receiver, amount, deadline, escrow ID, and allowance. <br>
Risk: The skill is tied to a specific Base Sepolia escrow contract and USDC token address. <br>
Mitigation: Independently verify the escrow contract and USDC addresses before interacting with them. <br>
Risk: Private key examples may lead users to expose sensitive wallet credentials. <br>
Mitigation: Use a dedicated test wallet and never paste a real or reused private key into chat or source files. <br>


## Reference(s): <br>
- [Trust Escrow ClawHub Page](https://clawhub.ai/droppingbeans/trust-escrow) <br>
- [Trust Escrow Platform](https://trust-escrow-web.vercel.app) <br>
- [Agent Docs](https://trust-escrow-web.vercel.app/agent-info) <br>
- [Integration Guide](https://trust-escrow-web.vercel.app/skill.md) <br>
- [Base Sepolia Contract](https://sepolia.basescan.org/address/0x6354869F9B79B2Ca0820E171dc489217fC22AD64) <br>
- [llms.txt](https://trust-escrow-web.vercel.app/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript examples, contract addresses, and transaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Base Sepolia network, USDC token, escrow contract, and wallet transaction guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
