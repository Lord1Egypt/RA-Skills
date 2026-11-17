## Description:

新帆线索池运营技能：查看私海/公海线索列表与统计、查看线索详情，认领/释放线索、更新跟进状态/备注/采纳优先级，并生成、定时推送私海线索日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiqingqiu23187](https://clawhub.ai/user/yiqingqiu23187)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and internal operations agents use this skill to inspect private and public Xinfan lead pools, review lead details and statistics, perform confirmed lead-management updates, and produce weekday private-lead reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a logged-in browser session to perform production lead-management actions.

Mitigation: Install only in a controlled internal Xinfan environment, review browser target validation, and require explicit user confirmation before write actions or plaintext contact lookup.

Risk: Daily reports can include fixed mock conversion metrics that may be mistaken for real business performance.

Mitigation: Clearly label, disable, or replace mock conversion metrics with verified data before production reporting.

Risk: The fallback token path can persist manually supplied credentials.

Mitigation: Keep browser-session authentication as the normal path and remove or harden the token fallback before production use.

Risk: Browser-context requests can depend on page behavior and origin matching.

Mitigation: Validate CDP targets against exact trusted origins and avoid page-overridable fetch where a safer request path is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiqingqiu23187/skills/xinfan-lead-skill)
- [Publisher profile](https://clawhub.ai/user/yiqingqiu23187)
- [Xinfan lead pool application](https://newark.devops.xiaohongshu.com/seller/investClue)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and report text, with CLI JSON for agent-side processing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require explicit confirmation; daily report placeholders must be filled from the generated facts block before sending.]

## Skill Version(s):

0.1.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
