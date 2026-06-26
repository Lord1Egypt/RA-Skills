## Description: <br>
智能任务与排班管理系统，支持多时段工作安排、动态排班和上班时间自适应提醒 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnkennypan](https://clawhub.ai/user/cnkennypan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage multi-shift work schedules, import Excel or CSV rosters, update schedules with natural language, and calculate adaptive reminders for tasks tied to work periods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded schedules and task records may contain sensitive personal or workplace timing information. <br>
Mitigation: Confirm where workspace JSON files will live and treat schedule and task files as sensitive before installation or use. <br>
Risk: The skill uses Feishu application credentials for reminders. <br>
Mitigation: Grant the Feishu app only the permissions needed for reminder delivery and keep FEISHU_APP_ID and FEISHU_APP_SECRET in environment variables. <br>
Risk: Suggested cron jobs can trigger automated reminder checks on a schedule. <br>
Mitigation: Enable the cron jobs only when periodic automated reminder checks are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnkennypan/smart-task-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local workspace schedule and task JSON files, Feishu app credentials, and optional OpenClaw cron commands.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
