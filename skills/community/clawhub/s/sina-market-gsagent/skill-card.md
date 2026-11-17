## Description:

Fetches and inspects market data from Sina Finance public webpage resources for A-share, Hong Kong stock, and domestic futures workflows, including quote lookup, futures metadata fallback, Chinese futures name normalization, code validation, and batch coverage checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzsec](https://clawhub.ai/user/yzsec)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market-data analysts use this skill to inspect public Sina Finance quote data and symbol availability for A-shares, Hong Kong stocks, and Chinese domestic futures. It is suited for lookup and diagnostics, not for private trading instructions or account-specific workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested symbols are sent to Sina Finance public web endpoints.

Mitigation: Use only public, non-sensitive symbols and do not provide private trading instructions, account information, or confidential portfolio data.

Risk: Sina public webpage fields, endpoint availability, and symbol coverage can change without an official service guarantee.

Mitigation: Validate important market values against authoritative data sources and treat empty or fallback responses as availability signals rather than definitive business records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzsec/skills/sina-market-gsagent)
- [Sina futures normalized fields](references/fields.md)
- [Chinese futures mapping](references/chinese_futures_mapping.json)
- [Sina Finance quote endpoint](https://hq.sinajs.cn)
- [Sina futures quote pages](https://finance.sina.com.cn/futures/quotes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or table command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Sina public webpage availability and may include raw fields for debugging.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
