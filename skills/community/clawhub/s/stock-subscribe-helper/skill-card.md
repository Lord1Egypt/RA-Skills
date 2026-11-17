## Description:

基于东方财富和集思录数据接口，筛选A股新股与可转债申购信息，并通过飞书发送申购提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mc82465](https://clawhub.ai/user/mc82465)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users who monitor Mainland China A-share IPO and convertible bond subscription dates use this skill to fetch listings, filter by product and board, and send Feishu reminders.

### Deployment Geography for Use:

Global; content focuses on Mainland China A-share markets.

## Known Risks and Mitigations:

Risk: The artifact asks for Feishu table read/write credentials even though the current code only sends webhook messages.

Mitigation: Use only a narrowly scoped Feishu webhook unless table-writing functionality is added, and avoid granting table read/write tokens for this release.

Risk: The artifact includes .env-style credential configuration.

Mitigation: Keep .env files out of version control and rotate any real credentials if they were committed or shared.

Risk: The artifact makes strong certification and 100% accuracy or safety claims that are not supported by the security evidence.

Mitigation: Treat those claims as marketing, validate market data independently, and review scanner results before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mc82465/skills/stock-subscribe-helper)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [EastMoney data API endpoint](https://datacenter-web.eastmoney.com/api/data/v1/get)
- [Jisilu convertible bond endpoint](https://www.jisilu.cn/data/cbnew/pre_list/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Console text and Feishu text messages, with configuration supplied as environment variables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu webhook for message delivery and uses optional filters for subscription product, stock board, and user identifier.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact package.json and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
