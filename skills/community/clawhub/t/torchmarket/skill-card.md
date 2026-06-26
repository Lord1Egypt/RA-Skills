## Description: <br>
Every token is its own margin market. Depth-adaptive risk engine, treasury-backed lending, real-token short selling. No oracles. No stored baselines. No keepers. The pool is the source of truth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect Torch Market state, build Solana token trading and margin transactions, and work with vault-based controller flows. It supports read-only operation and optional transaction signing for users who provide the required Solana configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support Solana DeFi trading, vault actions, purchases, borrowing, and transaction signing. <br>
Mitigation: Prefer read-only mode unless transaction execution is required, and inspect wallet prompts for buys, sells, borrows, withdrawals, and authority transfers. <br>
Risk: Providing a private key creates sensitive credential exposure and could let a controller submit transactions. <br>
Mitigation: Use only a fresh low-balance controller key for automation, never provide a vault authority private key, and revoke controller access from the vault authority when no longer needed. <br>
Risk: Token-detail and reputation features may contact external services or token metadata URLs. <br>
Mitigation: Expect network calls to SAID, CoinGecko, or metadata URLs and review those integrations for the deployment environment. <br>
Risk: Margin and short positions can be liquidated, and bad debt is possible in extreme market conditions. <br>
Mitigation: Review the risk model before use, keep positions conservatively sized, and treat liquidations as an expected protocol behavior. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/mrsirg97-rgb/torchmarket) <br>
- [Publisher Profile](https://clawhub.ai/user/mrsirg97-rgb) <br>
- [Torch Market Website](https://torch.market) <br>
- [Whitepaper](https://torch.market/whitepaper) <br>
- [Risk Model](https://torch.market/risk.md) <br>
- [Verification](https://torch.market/verification.md) <br>
- [Program Source](https://github.com/mrsirg97-rgb/torch_market) <br>
- [SDK Source](https://github.com/mrsirg97-rgb/torchsdk) <br>
- [Torch SDK npm Package](https://www.npmjs.com/package/torchsdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured transaction or query guidance, with TypeScript examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can operate in read-only mode or build Solana transactions when wallet configuration is supplied.] <br>

## Skill Version(s): <br>
11.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
