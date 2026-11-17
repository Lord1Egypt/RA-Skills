## Description:

A Yahoo Finance (yfinance) powered financial analysis tool that gets real-time quotes, generates high-resolution charts with moving averages and indicators, summarizes fundamentals, and runs one-shot reports with text summaries and chart output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users can use this skill to fetch Yahoo Finance market data, inspect ticker prices and fundamentals, and generate local technical-analysis summaries and charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches ticker data from Yahoo Finance, so outputs may reflect upstream market-data availability, delay, or quality issues.

Mitigation: Review market data against authoritative sources before making financial or operational decisions.

Risk: Python dependencies are resolved at runtime by the script metadata.

Mitigation: Run the skill in an isolated environment and pin or review dependencies before production use.

Risk: Chart output uses predictable /tmp paths based on ticker symbols.

Mitigation: Avoid shared multi-user systems or adjust chart generation to use unique private temporary files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bingze00000/skills/stock-info-explorer-jarvis)
- [Publisher Profile](https://clawhub.ai/user/bingze00000)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown/text with inline shell commands, terminal tables, ASCII charts, and local PNG chart paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit CHART_PATH values for PNG charts written under /tmp.]

## Skill Version(s):

1.2.11 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
