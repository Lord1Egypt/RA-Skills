## Description:

Autonomous vault-based liquidation keeper for Torch Market lending on Solana. Scans all migrated tokens for underwater loan positions using the SDK's bulk loan scanner (getAllLoanPositions), builds and executes liquidation transactions through a Torch Vault, and collects a 10% collateral bonus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to run a Solana liquidation keeper that scans Torch Market lending positions, builds liquidation transactions, and routes capital and proceeds through a Torch Vault controlled by the human principal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run live financial transactions and the bundled SDK exposes broader Torch Market capabilities than liquidation alone.

Mitigation: Review before installing, prefer the bundled reviewed source or an exact pinned package version, and run it under a dedicated low-privilege account.

Risk: Supplying a valuable wallet key could expose funds beyond the intended controller role.

Mitigation: Use a fresh disposable controller key only, never provide a vault authority key, and revoke the linked controller wallet when the bot is not in use.

Risk: Liquidation activity depends on Solana RPC availability and external read-only market data calls.

Mitigation: Use a secure HTTPS RPC endpoint, keep the agent gas balance bounded, and monitor logs for failed scans or transaction submissions.

## Reference(s):

- [Torch Liquidation Bot on ClawHub](https://clawhub.ai/mrsirg97-rgb/skills/torchliquidationbot)
- [Torch Market](https://torch.market)
- [Torch Market Whitepaper](https://torch.market/whitepaper)
- [Torch Market Risk Model](https://torch.market/risk.md)
- [Torch Liquidation Bot npm Package](https://www.npmjs.com/package/torch-liquidation-bot)
- [Torch SDK npm Package](https://www.npmjs.com/package/torchsdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live Solana transactions when configured with RPC, vault, and controller credentials.]

## Skill Version(s):

10.7.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
