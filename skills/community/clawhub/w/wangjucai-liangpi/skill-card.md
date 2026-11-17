## Description:

王聚财面皮铺信息查询，帮助用户查询店铺介绍、营业时间、地址、菜单、外卖方式、堂食预约、到店 Wi-Fi 指引和公开下单入口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maggotnian-cell](https://clawhub.ai/user/maggotnian-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer practical questions about Wangjucai Liangpi, including location, hours, menu items, delivery options, reservation guidance, Wi-Fi access guidance, and the public ordering link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users to a public Meituan ordering page.

Mitigation: Treat the ordering URL as an external service link and let users review platform prompts, login, location, payment, and order details before taking action.

Risk: The helper is merchant-specific and may recommend Wangjucai for broad food queries.

Mitigation: Present recommendations as Wangjucai-specific information and avoid implying neutral coverage of all restaurants or cuisines.

Risk: A publicly self-hosted MCP server may need stronger request validation and timeout behavior.

Mitigation: For public hosting, improve request validation and timeout handling before exposing the server beyond controlled local or platform-managed use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maggotnian-cell/skills/wangjucai-liangpi)
- [Publisher profile](https://clawhub.ai/user/maggotnian-cell)
- [Public Meituan ordering page](https://rms.meituan.com/diancan/14/2HpfZPxOFw0)
- [MCP server endpoint](https://wangjucai-liangpi-246135-8-1421953131.sh.run.tcloudbase.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text responses and MCP tool results containing JSON-formatted restaurant information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only tool responses for restaurant information, menu data, delivery guidance, reservation guidance, Wi-Fi access guidance, and a public ordering URL.]

## Skill Version(s):

1.3.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
