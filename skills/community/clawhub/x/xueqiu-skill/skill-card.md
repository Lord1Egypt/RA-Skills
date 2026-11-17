## Description:

雪球数据API接口调用工具。当用户需要查询雪球组合、用户、行情、调仓历史等投资数据时调用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongweixp](https://clawhub.ai/user/xiongweixp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Xueqiu users, investment portfolios, posts, quotes, net value history, holdings, and rebalancing history through the wxpub.aibana.art API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billable API credentials may be exposed in chat or transmitted to the remote wxpub.aibana.art service.

Mitigation: Use service-specific credentials, avoid pasting real secure_key values into ordinary chat when possible, and rotate credentials after testing.

Risk: Successful API calls spend account balance.

Mitigation: Use a limited test balance, monitor usage, and set spending controls where the service supports them.

Risk: Search terms, user IDs, portfolio IDs, and credentials are sent to the remote service during use.

Mitigation: Review requests before sending and avoid submitting sensitive or regulated data unless the remote service is approved for that use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiongweixp/skills/xueqiu-skill)
- [Publisher profile](https://clawhub.ai/user/xiongweixp)
- [wxpub.aibana.art API service](https://wxpub.aibana.art)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON request examples and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents billable POST requests that require app_id and secure_key credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
