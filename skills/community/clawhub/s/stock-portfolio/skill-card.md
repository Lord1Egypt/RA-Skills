## Description:

Stock Portfolio helps agents query A-share, Hong Kong, and U.S. stock quotes, track holdings and returns, configure price alerts, and generate daily stock picks using free market-data APIs with local JSON storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinshengf](https://clawhub.ai/user/yinshengf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local stock portfolio workflow: query market quotes, record positions, calculate gains and losses, set alerts, and generate daily candidate lists. Outputs are informational and should not be treated as trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio positions and alert thresholds are stored in local JSON files.

Mitigation: Use local filesystem protections, avoid sharing the data directory, and back up or delete portfolio files according to the user's privacy needs.

Risk: Stock symbols are sent to third-party finance APIs, including unauthenticated market-data endpoints.

Mitigation: Review the configured data sources before use and avoid submitting symbols that reveal sensitive trading intent.

Risk: Free market data and daily picks may be delayed, incomplete, or unsuitable as the sole basis for trades.

Mitigation: Cross-check quotes and recommendations with authoritative sources and keep human review in the investment decision loop.

Risk: Optional scheduled jobs can send recommendations or alert summaries through configured messaging channels.

Mitigation: Enable cron or message examples only after reviewing the exact command, schedule, destination, and data being sent.

## Reference(s):

- [Stock Data API Documentation](references/api_docs.md)
- [Cron Setup](references/cron_setup.md)
- [Daily Recommendation Strategy](references/recommendation_strategy.md)
- [ClawHub Skill Page](https://clawhub.ai/yinshengf/skills/stock-portfolio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown tables, JSON output, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local portfolio and alert JSON files, and may call third-party finance APIs for quote data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
