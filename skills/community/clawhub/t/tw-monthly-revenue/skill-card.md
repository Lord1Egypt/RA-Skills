## Description:

Fetches Taiwan stock monthly revenue data with the included FinMind API script, calculates YoY and MoM growth, and emits BEAT/MISS/NEUTRAL JSON signals for a fixed watchlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyy7263](https://clawhub.ai/user/andyy7263)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and investment workflow operators use this skill to run monthly Taiwan stock revenue checks, classify YoY performance, and consume the resulting JSON in monitoring or decision-support pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation states MOPS as the data source while the script calls FinMind, which can confuse users about data origin and reliability.

Mitigation: Review the FinMind endpoint, data fields, and any MOPS dependency assumptions before relying on generated revenue signals.

Risk: The skill text overstates downstream behavior by referencing investment pipeline triggers and ANALYSIS_INDEX updates that the artifact does not perform by itself.

Mitigation: Treat the JSON output as decision-support data only, and require separate reviewed integration code before connecting it to trading, monitoring, or index-update workflows.

Risk: External data requests can fail or return incomplete monthly data, resulting in DATA_UNAVAILABLE or NO_DATA outputs.

Mitigation: Handle missing-data states explicitly and avoid automated financial decisions from a single script run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyy7263/skills/tw-monthly-revenue)
- [FinMind TaiwanStockMonthRevenue API](https://api.finmindtrade.com/api/v4/data?dataset=TaiwanStockMonthRevenue)
- [MOPS](https://mops.twse.com.tw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON plus Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script targets a fixed watchlist unless WATCHLIST is edited and may return DATA_UNAVAILABLE or NO_DATA when source data is missing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
