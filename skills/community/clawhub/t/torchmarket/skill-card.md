## Description:

Torch Market helps agents query and build Solana transactions for a margin-market protocol with treasury-backed lending, real-token short selling, and pool-reserve pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to query Torch Market state, prepare quote-driven trades, and build or submit Solana transactions for token launch, vault, lending, short-selling, liquidation, treasury, and rewards workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build and submit real Solana DeFi transactions.

Mitigation: Prefer read-only or build-only use unless submission is needed, and review transaction details, amounts, slippage, and target accounts before signing.

Risk: A private key supplied through SOLANA_PRIVATE_KEY could expose funds if it controls valuable assets or vault authority.

Mitigation: Use only a fresh disposable controller key with minimal gas funds, never provide a vault authority key or seed phrase, and revoke controller access when it is no longer needed.

Risk: The optional npm install can introduce supply-chain drift from the reviewed bundled SDK.

Mitigation: Use the bundled SDK when possible, or pin the npm package version so deployed code matches the reviewed release.

Risk: Outbound Solana RPC and external API access can expand network and metadata exposure.

Mitigation: Use a trusted HTTPS Solana RPC endpoint and restrict outbound network access where the deployment environment allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrsirg97-rgb/skills/torchmarket)
- [Torch Market website](https://torch.market)
- [Torch Market whitepaper](https://torch.market/whitepaper)
- [Torch Market risk model](https://torch.market/risk.md)
- [Torch Market verification report](https://torch.market/verification.md)
- [Torch Market program source](https://github.com/mrsirg97-rgb/torch_market)
- [Torch SDK source](https://github.com/mrsirg97-rgb/torchsdk)
- [Torch SDK npm package](https://www.npmjs.com/package/torchsdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, configuration notes, and transaction-building instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate in read-only/build-only mode without a private key; transaction submission requires a Solana RPC endpoint and an optional disposable controller key.]

## Skill Version(s):

11.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
