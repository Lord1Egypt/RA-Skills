## Description: <br>
Autonomously discovers and trades Solana memecoins by combining smart-wallet copy trading, rule-based market analysis, social narrative detection, and on-chain risk gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance237a-hash](https://clawhub.ai/user/binance237a-hash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run or evaluate an automated Solana memecoin trading workflow with paper and live execution modes. It is intended for high-risk trading scenarios where candidate selection, copy-trade behavior, position sizing, and exit logic are mediated by configurable risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can sign irreversible Solana trades using a wallet private key. <br>
Mitigation: Keep the skill in paper mode unless the code has been audited, use a dedicated low-balance wallet for live mode, and store private keys only in a secret manager or tightly controlled environment file. <br>
Risk: Live execution and exit paths require review before capital is exposed. <br>
Mitigation: Verify Jupiter swap execution, sell behavior, emergency exits, and token amount handling before enabling live trading. <br>
Risk: Solana memecoin trading is highly volatile and can include rug pulls, liquidity removal, and manipulative token behavior. <br>
Mitigation: Use conservative risk budgets, daily loss limits, low position sizes, and the built-in risk gate checks; skip trades when required token metadata cannot be verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/binance237a-hash/solana-memecoin-trade) <br>
- [Publisher Profile](https://clawhub.ai/user/binance237a-hash) <br>
- [Solana Memecoin Guardian v2 Specification](artifact/docs/solana_memecoin_guardian_v2.md) <br>
- [Live Setup](artifact/docs/live_setup.md) <br>
- [Testing in Paper Mode](artifact/docs/testing.md) <br>
- [Narrative Engine Setup](artifact/docs/narrative_setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, TypeScript project files, and YAML/JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a runnable TypeScript trading-bot skeleton that defaults to paper mode and can be configured for live Solana execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
