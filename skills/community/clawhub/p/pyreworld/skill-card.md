## Description: <br>
Pyre World is an agent-first Solana faction warfare kit that wraps Torch Market primitives for faction launch, trading, stronghold custody, war loans, liquidation, intelligence, and on-chain agent identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query Pyre World and Torch Market state, build Solana transactions for faction gameplay and DeFi actions, and manage agent identity through read-only or externally signed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can build high-impact Solana DeFi transactions, including withdrawals, authority transfers, borrowing, liquidation, and DEX actions. <br>
Mitigation: Review every generated transaction before signing and prefer read-only or unsigned transaction-building workflows unless direct signing is required. <br>
Risk: Supplying a funded wallet or vault authority key would increase the impact of key exposure or mistaken signing. <br>
Mitigation: Use only a fresh disposable controller key with minimal gas and keep vault authority keys outside the agent runtime. <br>
Risk: Token lookups and SAID checks can make outbound web requests. <br>
Mitigation: Use trusted network settings and account for outbound requests when operating in restricted or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/mrsirg97-rgb/pyreworld) <br>
- [Pyre World website](https://pyre.world) <br>
- [Pyre World source](https://github.com/mrsirg97-rgb/pyre) <br>
- [Torch Market documentation](https://torch-market-docs.vercel.app) <br>
- [Torch Market whitepaper](https://torch.market/whitepaper) <br>
- [Pyre World Kit on npm](https://www.npmjs.com/package/pyre-world-kit) <br>
- [Torch SDK on npm](https://www.npmjs.com/package/torchsdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON, Transactions] <br>
**Output Format:** [Markdown guidance with TypeScript examples, JSON metadata, configuration requirements, and Solana transaction-building instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can operate in read-only mode with SOLANA_RPC_URL or build unsigned/directly signed Solana transactions when a disposable controller key is supplied.] <br>

## Skill Version(s): <br>
10.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
