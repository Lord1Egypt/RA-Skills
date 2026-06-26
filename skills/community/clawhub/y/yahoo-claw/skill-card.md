## Description: <br>
YahooClaw integrates Yahoo Finance market data into OpenClaw for stock quotes, financial data, dividends, news, and market analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use YahooClaw to retrieve stock quotes, historical prices, financial statements, dividends, news sentiment, and technical indicators for market-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and news searches are sent to Yahoo Finance through the package dependency. <br>
Mitigation: Use the skill only for symbols and searches appropriate to share with the upstream market-data provider. <br>
Risk: BUY, SELL, confidence, and sentiment labels may be mistaken for financial advice. <br>
Mitigation: Present generated analysis as informational market data and require human review before any investment decision. <br>
Risk: API keys or secrets can be exposed if stored in tracked files or copied into logs. <br>
Mitigation: Store optional API keys in environment variables or a secret manager, and avoid committing .env files or sharing logs that contain secrets. <br>


## Reference(s): <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-like JavaScript objects with human-readable status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market data, quote and history arrays, news metadata, sentiment labels, and technical indicator recommendations.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
