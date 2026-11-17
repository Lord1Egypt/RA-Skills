## Description:

Autonomous vault-based prediction market bot for Torch Market on Solana that creates binary prediction markets, seeds liquidity through a vault, monitors market state, and resolves outcomes through price-feed or manual oracles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run autonomous Torch Market prediction-market workflows on Solana while keeping market capital in a human-controlled vault. It supports market creation, liquidity seeding, monitoring, and resolution from local configuration and market definition files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot can create markets and spend vault funds for seed liquidity once its controller wallet is linked.

Mitigation: Run it against a low-funded dedicated vault, set operator budgets or manual approvals for batches, and keep authority withdrawal and unlink controls outside the agent.

Risk: Package provenance is not server-resolved for this version.

Mitigation: Install with an exact pinned package and lockfile, and confirm the runtime imports the reviewed SDK and bundled source before use.

Risk: A modified markets.json can cause unintended market creation or vault-funded seed buys.

Mitigation: Restrict write access to markets.json, review pending market definitions before the bot runs, and keep the per-market liquidity cap in place.

Risk: An optional SOLANA_PRIVATE_KEY could expose a valuable key if misused.

Mitigation: Prefer generated in-process controller keys, or provide only a fresh low-value controller key that can be revoked from the vault.

Risk: Price-feed or RPC failures can delay or distort market resolution.

Mitigation: Use a trusted HTTPS Solana RPC endpoint, monitor unresolved markets, and manually review or correct outcomes when external data is unavailable or suspect.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrsirg97-rgb/skills/torchpredictionmarketkit)
- [ClawHub Distribution Metadata](https://clawhub.ai/mrsirg97-rgb/torch-prediction-market-kit)
- [Torch Market Website](https://torch.market)
- [Torch Prediction Market Kit Source Link](https://github.com/mrsirg97-rgb/torch-prediction-market-kit)
- [Torch Prediction Market Kit npm Package](https://www.npmjs.com/package/torch-prediction-market-kit)
- [Torch SDK npm Package](https://www.npmjs.com/package/torchsdk)
- [Torch Market Whitepaper](https://torch.market/whitepaper.md)
- [Bundled Security Audit](artifact/audit.md)
- [Bundled Verification Notes](artifact/verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with bash, JSON, and TypeScript snippets plus runtime market-state file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLANA_RPC_URL and VAULT_CREATOR; SOLANA_PRIVATE_KEY is optional and should be a low-value disposable controller key if provided.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
