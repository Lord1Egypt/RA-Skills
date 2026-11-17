## Description:

根据项目名称、公告链接或编号查询招投标公告，整理带来源和待核实事项的项目进度时间线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

采购团队和业务分析人员可查询指定项目的招标、候选人、中标及合同公告，核对阶段、关键日期和原始来源；结果不构成持续监控或完整投标决策。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vendor account setup can collect a hashed device identifier and save an API key locally.

Mitigation: Require informed consent before auto-registration; use a manually configured ZLBX_API_KEY to avoid device collection and local key storage.

Risk: Paid queries and broader contact or competitor lookups can exceed the intended project-tracking scope.

Mitigation: Limit calls to the requested project, confirm before expanding paid searches, and avoid unnecessary contact or competitor queries.

Risk: Incomplete or outdated announcements can misstate a project's current stage or deadlines.

Mitigation: Show source links and distinguish confirmed dates and final awards from candidates and unverified status.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bailianai/skills/tender-bid-tracker)
- [知了标讯平台](https://ai.zhiliaobiaoxun.com/)
- [标讯搜索与项目进度接口说明](artifact/references/api-search.md)
- [账号开通与设备信息说明](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown project timeline and announcement table with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time results; distinguishes confirmed stages from missing or unverified dates.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
