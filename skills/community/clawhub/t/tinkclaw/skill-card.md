## Description: <br>
Financial market intelligence from TinkClaw for real-time BUY, SELL, and HOLD trading signals, market regime detection, Signal Market bot competition data, and natural language market analysis across crypto, stocks, forex, and commodities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dieub](https://clawhub.ai/user/dieub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for TinkClaw market signals, regime summaries, Signal Market bot data, proof verification, and multi-symbol scans through the bundled helper script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can send the user's API key and market questions to an environment-selected TinkClaw API server. <br>
Mitigation: Leave TINKCLAW_API_URL unset unless the alternate endpoint is intentionally trusted, use limited-scope keys, and avoid sending private account or portfolio details in prompts. <br>
Risk: The API reference describes account, staking, subscription, webhook, payment, and bot-mutation endpoints. <br>
Mitigation: Require explicit user confirmation before using endpoints that mutate account, bot, staking, subscription, webhook, or payment state. <br>
Risk: Market signals and natural language analysis may be mistaken for financial advice. <br>
Mitigation: Present outputs as TinkClaw AI data, include the not-financial-advice notice, and encourage independent verification before trading decisions. <br>


## Reference(s): <br>
- [TinkClaw API Reference](references/api.md) <br>
- [TinkClaw Documentation](https://tinkclaw.com/docs) <br>
- [TinkClaw Signal Market Challenge](https://tinkclaw.com/signal-market/challenge) <br>
- [ClawHub Skill Page](https://clawhub.ai/dieub/tinkclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include TinkClaw's not-financial-advice notice when presenting market data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
