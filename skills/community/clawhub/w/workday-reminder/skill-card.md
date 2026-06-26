## Description: <br>
Workday Reminder helps users create weekday off-work reminders, check countdowns to a configured off-work time, and manage reminder schedules for QQ delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artwebs](https://clawhub.ai/user/artwebs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to schedule recurring weekday QQ reminders for off-work time, view countdowns, and list, cancel, or update existing reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring weekday reminders may continue after the user no longer needs them. <br>
Mitigation: Cancel the cron job when reminders are no longer wanted. <br>
Risk: A reminder could be scheduled for the wrong time or QQ recipient if configured incorrectly. <br>
Mitigation: Check the scheduled time and recipient whenever creating or changing a reminder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artwebs/workday-reminder) <br>
- [Publisher profile](https://clawhub.ai/user/artwebs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON cron job configuration and optional JSON countdown output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QQ bot channel configuration and recurring weekday cron schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
