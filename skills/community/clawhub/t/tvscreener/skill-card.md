## Description:

Queries TradingView screener data for HK, A-share, A-share ETF, and US symbols using deepentropy/tvscreener for stock lookup, technical indicators, symbol filtering, and custom market queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subway-chenyan](https://clawhub.ai/user/subway-chenyan)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve TradingView screener snapshots, technical indicators, and filtered market data for Hong Kong, China A-share, A-share ETF, and US equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell wrappers can silently install or upgrade an unpinned Python package at runtime.

Mitigation: Run the skill in an isolated virtual environment, review or remove auto-install lines before use, and prefer a pinned requirements file for tvscreener.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subway-chenyan/skills/tvscreener)
- [README_USAGE](references/README_USAGE.md)
- [Screeners API Reference](references/api/screeners.md)
- [Fields API Reference](references/api/fields.md)
- [Filters API Reference](references/api/filters.md)
- [Enums API Reference](references/api/enums.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON or CSV market-data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Python scripts that query TradingView screener data and optionally write CSV files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
