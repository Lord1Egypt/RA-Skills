## Description:

Builds a stock market dashboard as a single self-contained HTML file with a morning briefing generated from live market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and market researchers use the skill to create a self-contained morning market briefing that brings together sentiment, market activity, company watchlists, and upcoming earnings. The dashboard is a read-only snapshot and does not trade or make purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated dashboard may expose its contents when shared or served from a local machine.

Mitigation: Prefer an attachment or pasted HTML. If serving locally, serve only the generated file, bind to loopback, and stop the server after delivery.

Risk: Requested ticker symbols are sent to SentiSense when market data is fetched.

Mitigation: Choose requested tickers with that data flow in mind. Keep the API key out of the generated HTML.

Risk: A pinned widget can persist across resets and be replaced on later runs.

Mitigation: Pin the widget only when persistence and replacement on later runs are intended.

## Reference(s):

- [SentiSense API reference](https://sentisense.ai/skill.md)
- [SentiSense website](https://sentisense.ai)
- [Stock Market Dashboard on ClawHub](https://clawhub.ai/thesentitrader/skills/stock-market-dashboard)

## Skill Output:

**Output Type(s):** [HTML, Files, Guidance]

**Output Format:** [Single self-contained HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A static market-data snapshot with inline styles and scripts; opens in a browser without a build step or external dependencies.]

## Skill Version(s):

1.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
