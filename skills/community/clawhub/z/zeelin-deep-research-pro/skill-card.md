## Description:

ZeeLin Deep Research 深度研究是一款 AI 驱动的专业研究辅助平台，支持一句话生成与多步骤生成，提供深度、专家两大研究路径，从快速信息梳理、系统分析到超万字专家报告全流程覆盖，帮助完成企业分析、市场洞察、招商研究等复杂任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhushanwei](https://clawhub.ai/user/zhushanwei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research teams use this skill to submit research topics to ZeeLin and receive generated PDF research reports for market, company, policy, product, and investment analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts and topics are sent to ZeeLin's external service.

Mitigation: Use the skill only for content approved for that provider and avoid submitting sensitive prompts unless an appropriate data-sharing review is complete.

Risk: The ZeeLin API key is stored in the local config.json file.

Mitigation: Use a dedicated low-privilege API key and restrict local file permissions for config.json.

Risk: Completed PDF report links are automatically sent through OpenClaw messaging.

Mitigation: Confirm target_user and channel routing before use, or review and disable automatic notification behavior when report recipient control matters.

Risk: Temporary watcher logs may contain task titles, status details, or notification output.

Mitigation: Review temporary logs after use and avoid sensitive task titles where local log retention is not acceptable.

## Reference(s):

- [ClawHub skill listing: ZeeLin Deep Research 深度研究](https://clawhub.ai/zhushanwei/skills/zeelin-deep-research-pro)
- [Publisher profile: zhushanwei](https://clawhub.ai/user/zhushanwei)
- [ZeeLin API key console](https://skills.zeelin.cn/console/apps)
- [ZeeLin recharge console](https://skills.zeelin.cn/console/recharge)
- [ZeeLin Deep Research service endpoint](https://desearch.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style agent guidance with shell command examples and PDF report links sent through OpenClaw messaging]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates ZeeLin research tasks, polls task status, and sends a generated PDF report link when the task completes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
