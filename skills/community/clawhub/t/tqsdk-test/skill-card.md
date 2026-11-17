## Description:

天勤量化 - 期货实时行情与历史数据接口，提供国内期货、期权的实时报价、K线序列与历史数据查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingyiyl](https://clawhub.ai/user/qingyiyl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading workflow builders use this skill to query Tianqin/TqSdk futures and options market data, including real-time quotes, K-line series, and historical K-line data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may place Tianqin account credentials in prompts, chat messages, README-style JSON examples, or normal skill request parameters.

Mitigation: Configure TQ_USERNAME and TQ_PASSWORD only through protected secrets or environment variables, and remove credential fields from ordinary request examples before deployment.

Risk: Runtime dependencies are specified with lower-bound version ranges.

Mitigation: Review and pin dependency versions before using the skill in a sensitive environment.

## Reference(s):

- [TQSDK homepage](https://www.shinnytech.com/tqsdk/)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing human-readable text and structured market-data results or errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical K-line queries may return many records and require a Tianqin professional account.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
