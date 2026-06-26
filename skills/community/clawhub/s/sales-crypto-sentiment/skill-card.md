## Description: <br>
Analyzes crypto sentiment, on-chain data, and technical indicators to provide trading signals and market insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and investors use this skill to request crypto market sentiment, on-chain, and technical-analysis signals for assets and timeframes they specify. The skill frames outputs as market analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be speculative crypto market signals that a user could mistake for investment advice. <br>
Mitigation: Treat outputs as market analysis only, verify market data independently, and review risk factors before acting. <br>
Risk: Wallet or trading-account exposure could occur if a user shares private keys or authorizes trades through related tooling. <br>
Mitigation: Do not share wallet private keys, seed phrases, or trading credentials, and do not authorize trades through this skill. <br>
Risk: The skill declares curl and clawhub dependencies that may be installed by compatible OpenClaw clients. <br>
Mitigation: Check the OpenClaw client install plan and dependency sources before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/fuzzyb33s/sales-crypto-sentiment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response with structured trading-signal fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include asset, direction, confidence, timeframe, entry zone, stop loss, take profit, catalyst, and risk/reward.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
