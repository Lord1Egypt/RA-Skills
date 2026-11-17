## Description:

分析A股热门强势股票，筛选当日涨幅>7%且IBS>50的领涨股，按板块分组识别热点题材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to fetch DaxiAPI A-share hot-stock data, identify leading themes from concept frequency and sector breadth, and produce a structured short-term market report. The report is informational financial analysis and must not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party npm CLI command that handles an API token.

Mitigation: Review the DaxiAPI CLI and npm publisher before use; prefer a pinned and reviewed CLI version or run it in a sandbox.

Risk: The token-check command can print an API token in shared terminals, logs, or agent transcripts.

Mitigation: Avoid displaying tokens in shared contexts; prefer environment variables or private terminal sessions and redact tokens from logs.

Risk: Generated hot-stock reports may be mistaken for investment advice.

Mitigation: Keep the report framed as informational analysis, include the required disclaimer, and preserve risk tiers for high-, medium-, and lower-risk observations.

## Reference(s):

- [Skill Page](https://clawhub.ai/ksky521/skills/xiapi-top-stocks)
- [DaxiAPI](https://daxiapi.com)
- [CLI Command Reference](references/cli-commands.md)
- [Token Setup Guide](references/token-setup.md)
- [Field Descriptions](references/field-descriptions.md)
- [Report Template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Financial analysis guidance]

**Output Format:** [Markdown report with tables, risk tiers, disclaimers, and inline shell commands for data retrieval or token setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should state that CLI data may be truncated, separate A/B/C market themes, avoid absolute investment claims, and include a disclaimer.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
