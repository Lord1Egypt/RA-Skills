## Description:

Torch Domain Auction Bot helps agents operate a Solana domain lending keeper that discovers domain opportunities, launches domain-backed tokens, monitors loans, and submits vault-routed liquidations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run or inspect a Torch Market keeper for domain-backed lending workflows on Solana, including domain discovery, token launch, lending-market monitoring, risk scoring, and liquidation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review flags unpinned npm execution as review-worthy.

Mitigation: Install an exact pinned package version or use a verified local audited build before running the skill.

Risk: The server security review flags automatic fund-moving actions as review-worthy.

Mitigation: Run the bot in a restricted container or account, omit SOLANA_PRIVATE_KEY unless a stable controller wallet is required, and fund the vault minimally.

Risk: The server security review flags unvalidated metadata URL fetching as review-worthy.

Mitigation: Restrict outbound network access so untrusted token metadata cannot reach localhost, private networks, or cloud metadata services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrsirg97-rgb/skills/torchdomainauctionbot)
- [ClawHub Listing](https://clawhub.ai/mrsirg97-rgb/torch-domain-auction-bot)
- [Kit Source](https://github.com/mrsirg97-rgb/torch-domain-auction-bot)
- [Torch Market](https://torch.market)
- [Torch Market Documentation](https://torch-market-docs.vercel.app)
- [Torch SDK npm Package](https://www.npmjs.com/package/torchsdk)
- [Skill Source](artifact/SKILL.md)
- [Security Audit](artifact/audit.md)
- [Formal Verification Report](artifact/verification.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript or TypeScript code snippets, and JSON configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction-building guidance and runtime CLI commands for Solana vault and keeper workflows.]

## Skill Version(s):

2.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
