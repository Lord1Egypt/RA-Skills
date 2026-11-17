## Description:

Provides guidance for querying A-share limit-up market-data endpoints covering limit-up ladders, filters, premiums, broken boards, limit-down pools, approaching limit-up stocks, statistics, hot sectors, and seal/break event streams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdreamjc](https://clawhub.ai/user/jcdreamjc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to call a third-party A-share market-data API and summarize limit-up board activity. It is intended for informational market-data workflows, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party financial market-data service and bearer API key.

Mitigation: Store the API key in environment variables, avoid exposing it in logs or shared prompts, and rotate it if disclosure is suspected.

Risk: Returned stock analysis or market-data summaries could be mistaken for financial advice.

Mitigation: Present outputs as informational market data and require users to make independent investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcdreamjc/skills/wudao-limitup)
- [Publisher profile](https://clawhub.ai/user/jcdreamjc)
- [QuickTiny stock API](https://stock.quicktiny.cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown with curl examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables; outputs are informational market-data guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
