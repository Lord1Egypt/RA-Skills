## Description: <br>
自动化工作流引擎。定时执行任务链：数据采集、处理、通知和存档，支持 cron 定时、webhook 触发和文件监控。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjstate](https://clawhub.ai/user/cjstate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to define and run automated workflow chains for scheduled data collection, processing, notification, archival, file monitoring, webhook-triggered work, and queue-triggered work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes broad file, network, email, database, webhook, queue, and daemon-style automation capabilities with limited safety scope detail. <br>
Mitigation: Review workflows before installing or running them, restrict file paths, use trusted webhook and queue sources, limit email and database credentials, and avoid daemon mode until trigger scope and shutdown behavior are understood. <br>
Risk: Workflow dependencies and external services may introduce security or reliability exposure. <br>
Mitigation: Use pinned patched dependencies and only run known, reviewed workflow code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjstate/xh-auto-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON workflow examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe daemon execution, workflow configuration, trigger setup, and operational commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
