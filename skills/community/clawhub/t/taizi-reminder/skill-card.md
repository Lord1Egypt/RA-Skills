## Description: <br>
Capture natural-language events in Chinese or English, save them to your workspace, and schedule Telegram reminders with default 24h, 1h, and 10m notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal reminder secretary to capture meetings, birthdays, deadlines, and schedule queries in natural language. It stores reminder data in an OpenClaw workspace file and schedules Telegram notifications through OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder titles, times, and notes may be saved in the OpenClaw workspace and delivered through Telegram. <br>
Mitigation: Avoid highly sensitive reminder text, review events.yml periodically, and install only when this storage and delivery path is acceptable. <br>
Risk: Natural-language dates, lunar birthdays, missing times, or timezone assumptions can result in incorrect reminder timing. <br>
Mitigation: Use explicit reminder commands, ask minimal clarifying questions for ambiguous details, confirm the resolved datetime after scheduling, and set REMINDER_TZ when the default Asia/Shanghai timezone is not appropriate. <br>
Risk: Stale or unwanted cron jobs can continue sending notifications after reminder changes. <br>
Mitigation: Review cron jobs periodically and confirm that cancellations or changes remove or replace the affected reminder jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fresh3/taizi-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown responses with YAML workspace updates and cron scheduling commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores reminder entries in reminders/events.yml and uses configurable timezone and reminder-offset environment variables.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
