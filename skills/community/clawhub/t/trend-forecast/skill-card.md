## Description: <br>
Multi-signal trend forecasting for autonomous agents that combines prediction market odds, Twitter/X sentiment, news velocity, and stock market data into confidence-scored trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to gather prediction market, social, news, and market signals through AIsa APIs and synthesize them into trend forecasts. It is suited for research, monitoring, posting, and engagement workflows around emerging trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast topics, tickers, market questions, social and news search terms, and synthesized research data are sent to AIsa services. <br>
Mitigation: Do not use the skill with secrets, confidential strategy, regulated data, private watchlists, or sensitive personal information. <br>
Risk: Trend forecasts and prediction market odds can be mistaken for certainty or financial advice. <br>
Mitigation: Present outputs as informational research, frame odds as current market pricing, include risks and data gaps, and avoid investment recommendations. <br>
Risk: The skill requires an AISA_API_KEY credential. <br>
Mitigation: Provide the key through the environment, limit access to the credential, and avoid exposing it in prompts, reports, logs, or saved outputs. <br>


## Reference(s): <br>
- [ClawHub Trend Forecast release page](https://clawhub.ai/aisadocs/trend-forecast) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API endpoint reference for this skill](references/api_endpoints.md) <br>
- [AIsa API reference](https://aisa.one/docs/api-reference) <br>
- [AIsa pricing guide](https://aisa.one/docs/guides/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON trend forecast with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; forecasts include direction, confidence score, signal agreement, analysis, key signals, risks, and data gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
