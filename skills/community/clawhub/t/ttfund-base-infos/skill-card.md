## Description:

通过天天基金API查询指定基金代码的详细基金信息，包括基金名称、类型、基金公司、当前净值及风险等级等核心数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yemeng831-cloud](https://clawhub.ai/user/yemeng831-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Tiantian Fund base information by fund code through FUND_BASE_INFOS and receive concise explanations of returned JSON fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTFUND_APIKEY may be exposed through logs, shared terminal output, or copied request examples.

Mitigation: Treat TTFUND_APIKEY as a secret and avoid sharing logs or command output that might reveal the key.

Risk: Fund lookup output may be incomplete, unavailable, or misread if request parameters are missing or the remote service returns an error.

Mitigation: Check required parameters, summarize only returned values, and do not fabricate successful results when the service reports an error.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yemeng831-cloud/skills/ttfund-base-infos)
- [Publisher profile](https://clawhub.ai/user/yemeng831-cloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON data summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-configured TTFUND_APIKEY for requests to the disclosed Tiantian Fund service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
