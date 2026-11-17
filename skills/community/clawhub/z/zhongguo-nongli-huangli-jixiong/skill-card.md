## Description:

查询中国农历与黄历信息，包括公历转农历、每日宜忌、吉凶详情和按活动筛选择日。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leocdchina](https://clawhub.ai/user/leocdchina)

### License/Terms of Use:

MIT-0

## Use Case:

用户可查询指定日期的中国农历、黄历宜忌与吉凶信息，也可按搬家、结婚或开业等活动筛选日期。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication code does not enforce the advertised secure destination for passwords and access tokens.

Mitigation: Require HTTPS and origin checks with safe redirect handling before supplying credentials; use a unique service password and keep tokens and passwords out of shared logs.

## Reference(s):

- [Huangli Toolkit Reference](artifact/references/reference.md)
- [Service homepage](https://nongli.skill.4glz.com)
- [ClawHub release](https://clawhub.ai/leocdchina/skills/zhongguo-nongli-huangli-jixiong)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Readable JSON query results with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-date, date-range, and keyword queries; results depend on available service data and account quota.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
