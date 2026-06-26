## Description: <br>
Autonomous vault-based prediction market bot for Torch Market on Solana that creates binary markets as Torch tokens, seeds liquidity through a vault, monitors markets, and resolves outcomes through price-feed or manual oracles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and operators use this skill to run a vault-controlled Solana prediction-market bot that creates, monitors, and resolves Torch Market binary markets from a local markets.json file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot can continuously create markets and spend seed liquidity from a local markets.json file through the configured vault. <br>
Mitigation: Use a segregated vault funded only with the amount intended for this bot, protect and review markets.json before startup, and monitor logs and vault balance during operation. <br>
Risk: The bundled financial SDK has a broader transaction surface than the bot's narrow market-creation workflow. <br>
Mitigation: Prefer the reviewed bundled source or pin exact npm versions, and review SDK updates before increasing vault funding. <br>
Risk: A linked controller wallet can initiate vault-routed market operations until it is revoked. <br>
Mitigation: Use a fresh disposable controller key, keep the authority key separate, and unlink the agent wallet when finished or if behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrsirg97-rgb/torchpredictionmarketkit) <br>
- [Torch Market website](https://torch.market) <br>
- [Torch Prediction Market Kit source link from metadata](https://github.com/mrsirg97-rgb/torch-prediction-market-kit) <br>
- [Torch Market whitepaper](https://torch.market/whitepaper.md) <br>
- [Prediction Market Kit npm package](https://www.npmjs.com/package/torch-prediction-market-kit) <br>
- [Torch SDK npm package](https://www.npmjs.com/package/torchsdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime text logs and markets.json state updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLANA_RPC_URL and VAULT_CREATOR; SOLANA_PRIVATE_KEY and MARKETS_PATH are optional.] <br>

## Skill Version(s): <br>
2.0.3 (source: SKILL.md frontmatter, agent.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
