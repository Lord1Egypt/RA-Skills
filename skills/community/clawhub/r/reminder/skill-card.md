## Description: <br>
Reminder captures natural-language events, saves them to a workspace reminders file, schedules Telegram cron notifications, and summarizes upcoming plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to turn meetings, birthdays, deadlines, and schedule requests into stored reminders and Telegram notifications. They can also ask for upcoming plans and receive a concise schedule summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder details are stored in a local workspace file and may contain personal information. <br>
Mitigation: Keep synced workspaces private, restrict access to the reminders file, and review reminder contents before syncing or sharing the workspace. <br>
Risk: Natural-language dates, lunar birthdays, or time zones may resolve to the wrong reminder time. <br>
Mitigation: Review the resolved date, time, and REMINDER_TZ value after scheduling, and ask clarifying questions when key timing details are ambiguous. <br>
Risk: Telegram cron notifications may send reminder content externally at scheduled offsets. <br>
Mitigation: Confirm reminder offsets before scheduling and remove or replace cron jobs when reminders are changed or canceled. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown or plain-text responses with YAML reminder records and cron scheduling actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reminder events to ~/.openclaw/workspace/reminders/events.yml and schedules Telegram reminders through OpenClaw cron.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
