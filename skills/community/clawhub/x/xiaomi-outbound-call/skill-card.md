## Description:

触发阿里云晓蜜外呼机器人任务，自动批量拨打电话。适用于批量外呼、客户回访、满意度调查、简历筛查约面试等场景。可从前置工具或节点获取外呼名单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[raven-xia](https://clawhub.ai/user/raven-xia)

### License/Terms of Use:


## Use Case:

External agents and business operators use this skill to prepare, confirm, and launch Alibaba Cloud OutboundBot campaigns for customer callbacks, surveys, promotions, notifications, and candidate interview scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Alibaba Cloud OutboundBot resources and place real outbound calls.

Mitigation: Use credentials scoped to the required OutboundBot permissions and confirm every campaign purpose and call list before execution.

Risk: Phone numbers, CRM records, candidate records, and campaign metadata may appear in inputs or logs.

Mitigation: Pass only the minimum required contact data and run the skill where logs are protected, retained appropriately, and redacted before sharing.

Risk: Credential material may be loaded from environment variables or nearby .env files.

Mitigation: Run from a clean working directory, avoid unrelated .env files, rotate exposed keys, and store Alibaba Cloud AccessKey secrets outside shared artifacts.

## Reference(s):

- [阿里云晓蜜外呼机器人及对话分析配置指南](references/config.md)
- [Alibaba Cloud OutboundBot console](https://outboundbot.console.aliyun.com/)
- [Alibaba Cloud OutboundBot documentation](https://help.aliyun.com/product/outboundbot.html)
- [ClawHub skill page](https://clawhub.ai/raven-xia/skills/xiaomi-outbound-call)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, runtime logs, and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alibaba Cloud OutboundBot credentials and a confirmed list of valid mainland China mobile phone numbers.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
