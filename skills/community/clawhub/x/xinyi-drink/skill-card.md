## Description:

Use when users ask to 领取Skill用户大礼包, 查询及分析个人历史订单, 查询菜单及饮品热量, or 查询门店及等候时长 for 新一好喝/新一咖啡.

This skill is ready for commercial/non-commercial use.

## Publisher:

[domilin](https://clawhub.ai/user/domilin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to interact with 新一好喝/新一咖啡 for reward claiming, personal order lookup and analysis, menu and nutrition questions, drink recommendations, and store wait-time checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone-number-linked reward and order-history data may be exposed or misused if the skill is run for another person or on a shared machine.

Mitigation: Use only the user's own mini-program-bound phone number, trigger reward and order flows only on explicit user intent, and clear the local cache after shared-machine use.

Risk: The skill relies on the Xinyi backend and a configurable API base URL for phone-number and order-history features.

Mitigation: Install only when the backend is trusted and confirm any API base URL override before using real phone numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/domilin/skills/xinyi-drink)
- [Project homepage](https://github.com/xinyi-drink/xinyi-drink)
- [Activity flow](references/activity-flow.md)
- [Capability map](references/capability-map.md)
- [Privacy boundaries](references/privacy-boundaries.md)
- [Platform install](references/platform-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style user responses with shell command invocations and script-produced text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reward and order-history flows can require network access and a user-provided mini-program-bound phone number.]

## Skill Version(s):

1.2.5 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
