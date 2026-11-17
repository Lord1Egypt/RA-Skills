## Description:

提供基于股票代码从 Tushare 获取 A 股股票基础数据，支持自定义返回条数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghjkkkkkklkk](https://clawhub.ai/user/ghjkkkkkklkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query A-share stock basic data from Tushare by stock code and limit the number of returned records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds and silently uses a real Tushare API token.

Mitigation: Remove and rotate the embedded token, and require users to provide their own token through a secret or environment variable.

Risk: The skill depends on outbound access to Tushare for stock lookup.

Mitigation: Document the external Tushare dependency and review service terms, availability, and failure handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghjkkkkkklkk/skills/tushare-stock-data)

## Skill Output:

**Output Type(s):** [API Calls, Data]

**Output Format:** [JSON-compatible object with status, count, and stock data records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stock_basic records from Tushare up to the requested limit.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
