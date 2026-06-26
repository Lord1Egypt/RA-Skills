## Description: <br>
企业微信智能办公助手，每日自动汇总日程、会议、待办和团队数据，生成可视化早报卡片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers, project leads, and operations teams use this skill to assemble a daily Enterprise WeChat office brief from schedules, meetings, todos, and team smart-sheet data. It supports manual prompts and scheduled morning runs that produce a shareable briefing card. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect sensitive workplace schedule, meeting, todo, and team-data content and package it into a report. <br>
Mitigation: Confirm the exact WeCom data sources and permissions before installation, and use data minimization or redaction for sensitive fields. <br>
Risk: Automatic cron execution and chat delivery could send the briefing to unintended Feishu or WeCom recipients. <br>
Mitigation: Prefer manual runs until recipient allowlists, trigger permissions, approval checks, and audit logging are configured. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Image] <br>
**Output Format:** [Structured office brief with a generated PNG briefing card] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for manual chat triggers or scheduled weekday morning delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and workflow.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
