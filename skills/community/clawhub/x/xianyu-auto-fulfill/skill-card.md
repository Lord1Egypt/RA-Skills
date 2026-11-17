## Description:

闲鱼自动发货监控。使用 agent-browser 自动检查闲鱼新消息，检测付款订单并自动发货。触发词：闲鱼发货、闲鱼监控、闲鱼自动化、xianyu、自动发货。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:


## Use Case:

External sellers and operators use this skill to monitor Xianyu chats for paid orders and send the configured fulfillment message, such as a key, link, or fixed text. The skill requires the user to define the fulfillment method before automation is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation in the main browser session or a personal Chrome profile can expose broader account access than the fulfillment task needs.

Mitigation: Use a dedicated browser profile logged into only the required Xianyu account, and avoid storing unrelated credentials in that profile.

Risk: Cron-based fulfillment can repeatedly send incorrect content if the fulfillment source, message, or schedule is misconfigured.

Mitigation: Start in manual or dry-run mode, confirm the fulfillment source and message content, and enable cron only after validating the schedule and removal command.

Risk: Assuming an API, key pool, or fixed delivery text can cause wrong or unauthorized fulfillment behavior.

Mitigation: Require the user to specify the fulfillment method before setup and do not prefill API endpoints, secrets, or delivery content.

## Reference(s):

- [Xianyu chat page](https://www.goofish.com/im)
- [ClawHub skill page](https://clawhub.ai/sliverp/skills/xianyu-auto-fulfill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and operational instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser automation and cron setup guidance; fulfillment details are supplied by the user.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
