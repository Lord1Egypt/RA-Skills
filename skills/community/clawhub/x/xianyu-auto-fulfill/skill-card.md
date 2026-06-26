## Description: <br>
闲鱼自动发货监控。使用 agent-browser 自动检查闲鱼新消息，检测付款订单并自动发货。触发词：闲鱼发货、闲鱼监控、闲鱼自动化、xianyu、自动发货。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sellers and operators on Xianyu use this skill to monitor paid order messages in a logged-in browser session and send the configured fulfillment text, link, key, or other delivery content after the user specifies the fulfillment workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Xianyu marketplace browser session and automatically send fulfillment messages. <br>
Mitigation: Use a dedicated browser profile or account where possible, begin with manual approval or dry-run checks, and monitor early runs before relying on automation. <br>
Risk: Scheduled instructions could expose fulfillment secrets or continue running after they are no longer needed. <br>
Mitigation: Avoid placing secrets directly in cron instructions, store credentials in an appropriate external workflow, and remove the cron job when monitoring is no longer required. <br>
Risk: Incorrect order detection or fulfillment source failures could send wrong or incomplete delivery content. <br>
Mitigation: Require the user to specify the fulfillment method, only act on paid-order signals, and surface API or inventory failures instead of sending error content. <br>


## Reference(s): <br>
- [Xianyu chat page](https://www.goofish.com/im) <br>
- [ClawHub skill page](https://clawhub.ai/sliverp/xianyu-auto-fulfill) <br>
- [Publisher profile](https://clawhub.ai/user/sliverp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and browser automation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure recurring OpenClaw cron checks and browser-session actions; fulfillment content must be supplied by the user.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
