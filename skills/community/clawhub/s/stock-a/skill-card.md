## Description:

Provides real-time and historical A-share stock data from multiple free sources including mootdx, Sina, Tencent, Eastmoney, and Tushare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[same1317](https://clawhub.ai/user/same1317)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve A-share real-time quotes, historical K-line data, and related market fields from supported free finance-data providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts contact external finance-data providers and send the requested stock codes when run.

Mitigation: Run the scripts only for stock codes that are appropriate to share with those providers and review provider availability before relying on returned market data.

Risk: Optional Python packages such as mootdx and tushare may be installed to enable additional data sources.

Mitigation: Install optional packages in a virtual environment and pin reviewed versions for repeatable releases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/same1317/skills/stock-a)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces quote and K-line examples; helper scripts print human-readable text and JSON snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
