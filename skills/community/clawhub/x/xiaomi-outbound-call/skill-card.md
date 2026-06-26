## Description: <br>
触发阿里云晓蜜外呼机器人任务，自动批量拨打电话。适用于批量外呼、客户回访、满意度调查、简历筛查约面试等场景。可从前置工具或节点获取外呼名单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Raven-XIA](https://clawhub.ai/user/Raven-XIA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External and internal operators use this skill to prepare and launch Alibaba Cloud Xia蜜 outbound calling tasks for customer callbacks, surveys, product outreach, interview scheduling, notifications, and similar batch phone workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls through the user's Alibaba Cloud account. <br>
Mitigation: Confirm the call purpose, phone list, and call content before execution, and install only when this outbound calling capability is intended. <br>
Risk: Alibaba Cloud credentials and phone-number data are involved in execution. <br>
Mitigation: Use least-privilege RAM credentials and handle recipient phone numbers according to applicable privacy, consent, and retention requirements. <br>
Risk: Outbound calling may create cloud costs or legal compliance obligations. <br>
Mitigation: Check recipient consent, calling rules, and expected Alibaba Cloud charges before starting a task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Raven-XIA/xiaomi-outbound-call) <br>
- [Alibaba Cloud Outbound Bot documentation](https://help.aliyun.com/product/outboundbot.html) <br>
- [Configuration reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON task input, shell command output, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before calls are placed and valid Alibaba Cloud credentials in environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
