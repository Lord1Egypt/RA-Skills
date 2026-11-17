## Description:

选股雷达 helps Chinese-speaking agents screen A-share stocks using multi-factor scoring, hot-sector scanning, and Dragon/Tiger List analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and automation builders use this skill to request A-share stock-screening analysis, sector scans, and structured decision-support outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command-execution capability and access to local files or API-key-backed data sources.

Mitigation: Require explicit confirmation before command execution, file writes, or credential-backed API use, and run it with only the minimum files and credentials needed.

Risk: Stock-screening outputs may be mistaken for investment advice.

Mitigation: Treat outputs as informational market analysis and require human review before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stock-radar-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown with structured JSON examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on user-provided A-share data sources or API credentials; outputs should be treated as informational market analysis, not investment advice.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
