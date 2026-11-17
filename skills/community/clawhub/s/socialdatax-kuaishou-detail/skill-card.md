## Description:

帮助用户查询快手作品详情，包括作品内容、作者信息和可用的互动指标。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要快手内容调研的用户，获取单条作品详情，并查看来源返回的作者、发布时间和互动数据，以支持内容分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because its instructions repeatedly run an unpinned, changeable CLI package, creating a risk that a future version could access the API key or local files.

Mitigation: Review and pin the CLI package version before running it with an API key or access to personal files; limit the credentials and local access available during execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou-detail)

## Skill Output:

**Output Type(s):** [Structured data, JSON]

**Output Format:** [JSON containing Kuaishou work details and available engagement metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only detail data; returned fields depend on the source response.]

## Skill Version(s):

0.1.23 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
