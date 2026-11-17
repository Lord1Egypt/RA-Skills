## Description:

Autonomously discovers and trades Solana memecoins by combining smart-wallet copy trading, rule-based market analysis, social narrative detection, and on-chain risk gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance237a-hash](https://clawhub.ai/user/binance237a-hash)

### License/Terms of Use:


## Use Case:

External developers and trading automation operators use this skill to run or adapt a Solana memecoin monitoring and trading agent that evaluates smart-wallet events, market data, social narratives, and risk gates before simulated or live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can automatically sign and submit real Solana trades with weak controls.

Mitigation: Keep the skill in paper mode unless the code has been audited, and use only a dedicated low-balance trading wallet for any live testing.

Risk: Live exit-state bugs and transaction-validation gaps can misreport or mishandle exits.

Mitigation: Fix and test live exit-state handling and transaction validation before allowing autonomous trades with real funds.

Risk: Wallet private keys, API tokens, and custom API base URLs can expose funds or route trading through untrusted services.

Mitigation: Protect wallet and API credentials, and avoid custom API base URLs unless the endpoint is fully trusted and audited.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binance237a-hash/skills/solana-memecoin-trade)
- [README](README.md)
- [OpenClaw Skill Specification](docs/solana_memecoin_guardian_v2.md)
- [Live Setup](docs/live_setup.md)
- [Testing](docs/testing.md)
- [Narrative Engine Setup](docs/narrative_setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, TypeScript code, YAML/JSON configuration, shell commands, and runtime log events.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper mode. Live mode requires wallet and API credentials and can submit signed Solana transactions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
