## Description:

Stock Info Explorer uses Yahoo Finance data through yfinance to fetch quotes, generate charts with technical indicators, summarize fundamentals, and create one-shot stock reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kys42](https://clawhub.ai/user/kys42)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to inspect ticker-level market information, compare recent price trends, generate technical-analysis charts, and produce concise stock reports from Yahoo Finance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs Python dependencies through uv.

Mitigation: Run it in a normal user account or isolated environment and install only when the configured package index is trusted.

Risk: Chart output uses predictable /tmp filenames and may overwrite an existing chart for the same ticker on shared machines.

Mitigation: Review or move generated chart files after creation, and avoid relying on /tmp chart names for durable storage.

Risk: Market data quality and coverage can vary by ticker, market, and Yahoo Finance availability.

Mitigation: Treat outputs as analysis aids and verify important financial decisions against authoritative market data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kys42/skills/stock-info-explorer)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Terminal text and rich tables, ASCII trend charts, PNG chart files, and CHART_PATH lines for generated charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart files are written under /tmp using ticker-derived filenames.]

## Skill Version(s):

1.2.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
