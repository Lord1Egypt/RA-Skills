## Description:

Autonomous Solana token sniper and trading bot that monitors new Raydium and Jupiter launches, evaluates rugpull risk with LLM analysis, and can auto-buy selected tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanthbellary](https://clawhub.ai/user/srikanthbellary)

### License/Terms of Use:


## Use Case:

External developers and advanced traders use this skill to configure and operate a Solana pool-monitoring bot that evaluates new token launches and can submit Jupiter swap transactions. It is intended for users who understand the financial and wallet-custody risks of automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for live wallet authority and can automatically buy tokens, so funded assets can be lost.

Mitigation: Use a dedicated low-balance wallet, start with tiny trade amounts, and never provide a main wallet private key.

Risk: Advertised stop-loss, take-profit, and auto-sell behavior may be missing or unsafe.

Mitigation: Do not rely on unattended exits; monitor positions actively and verify exit logic before running with real funds.

Risk: Transaction signing and validation require review before live use.

Mitigation: Review and fix signing, transaction validation, and preflight behavior before allowing the bot to submit real swaps.

Risk: Server-resolved GitHub import provenance is unavailable for this release.

Mitigation: Treat the packaged artifact as the source of record and do not infer repository provenance from skill text or metadata links.

## Reference(s):

- [Jupiter Aggregator API](artifact/references/jupiter-api.md)
- [Raydium Pool Monitoring](artifact/references/raydium-pools.md)
- [ClawHub Skill Page](https://clawhub.ai/srikanthbellary/skills/solana-sniper-bot)
- [ClawHub Metadata Homepage](https://github.com/srikanthbellary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, environment configuration, and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY and LLM_API_KEY; may also use RPC_URL and HELIUS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
