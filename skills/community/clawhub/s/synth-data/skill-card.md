## Description:

Query volatility forecasts from Synthdata.co for crypto, commodities, and stocks, compare assets, and run Monte Carlo simulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emsin44](https://clawhub.ai/user/emsin44)

### License/Terms of Use:

MIT

## Use Case:

Developers, traders, and market analysts use this skill to query Synthdata volatility forecasts, compare supported assets, and generate market-risk summaries or simulations for analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Synthdata API key and requested asset tickers are shared with a third-party volatility API.

Mitigation: Install only if you trust Synthdata.co with those values, keep SYNTHDATA_API_KEY in a secret environment variable, and avoid sending sensitive ticker-watch lists.

Risk: Trading, options, Polymarket, alerting, and simulation examples could be mistaken for financial advice or wired into real transactions.

Mitigation: Treat outputs as informational market analysis, review workflows separately, and avoid connecting the examples to live trades or public alerts without clear financial-risk disclaimers.

Risk: Scheduled reports and notification examples can publish market signals to Slack, Telegram, or similar channels.

Mitigation: Review channels, recipients, thresholds, and message text before enabling cron jobs or webhook-based alerts.

## Reference(s):

- [Synthdata API Reference](references/api.md)
- [Synthdata Use Cases](examples/use-cases.md)
- [Synthdata](https://synthdata.co)
- [ClawHub Skill Page](https://clawhub.ai/emsin44/skills/synth-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and SYNTHDATA_API_KEY for live Synthdata API queries.]

## Skill Version(s):

1.1.5 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
