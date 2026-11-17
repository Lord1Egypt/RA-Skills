## Description:

Multi-signal trend forecasting for autonomous agents that combines prediction market odds, X/Twitter sentiment, news velocity, and stock market data into confidence-scored trend analysis using AIsa APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to gather multiple market, social, news, and financial signals for a topic and synthesize them into an informational trend forecast with confidence scoring and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast questions, derived search terms, gathered source data, and AISA_API_KEY-authenticated requests are sent to AIsa and relayed providers.

Mitigation: Use the skill only when external processing is acceptable, and avoid confidential or sensitive research topics.

Risk: The skill documentation mentions Twitter/X posting or engagement workflows more broadly than the implementation supports.

Mitigation: Use the skill for research and monitoring outputs only; do not rely on it for Twitter/X posting or engagement automation.

Risk: Trend and market forecasts can be incorrect or misleading if signals are sparse, stale, or in conflict.

Mitigation: Treat outputs as informational analysis, preserve confidence scores and data gaps, and avoid presenting prediction-market or stock signals as certainty or financial advice.

## Reference(s):

- [AIsa API Endpoints - Trend Forecaster](artifact/references/api_endpoints.md)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [AIsa Pricing Guide](https://aisa.one/docs/guides/pricing)
- [Trend Forecast ClawHub Page](https://clawhub.ai/aisadocs/skills/trend-forecast)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown or JSON trend forecast with direction, confidence score, time horizon, analysis, key signals, risks, and data gaps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY for authenticated AIsa API requests; bundled scripts can save forecast reports when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
