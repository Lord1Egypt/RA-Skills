## Description: <br>
Create, inspect, and cancel OpenClaw cron-based chat reminders for one-time reminders, pending reminder review, due-soon or overdue checks, and cancellation of unexecuted reminder jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anghu666](https://clawhub.ai/user/anghu666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage OpenClaw chat reminders through native cron workflows, including creating one-time reminders, inspecting pending or overdue reminders, and canceling unexecuted reminder jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text and delivery routing may remain stored in scheduled cron jobs until they run or are canceled. <br>
Mitigation: Verify the time, message, channel, target, and account before creating reminders, and cancel jobs that should no longer run. <br>
Risk: The optional helper script depends on trusted OPENCLAW_BIN and OPENCLAW_REMINDER_* environment variables. <br>
Mitigation: Use the helper only in trusted local environments, and prefer native OpenClaw cron workflows when portability or environment trust is uncertain. <br>
Risk: Canceling the wrong reminder could remove an intended scheduled message. <br>
Mitigation: Identify the correct reminder job by id or title and confirm ambiguous cancellation requests before removing a job. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with JSON examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose native OpenClaw cron job definitions and optional helper script commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
