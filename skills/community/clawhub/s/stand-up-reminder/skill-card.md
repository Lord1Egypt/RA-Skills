## Description: <br>
Creates recurring workday stand-up reminders with configurable hours, interval, timezone, language, message style, and optional holiday skipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinalucky](https://clawhub.ai/user/tinalucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to create and manage recurring reminders that prompt them to stand up and move during workdays. It is useful for desk-work wellness routines where reminder time, interval, timezone, language, tone, and holiday behavior need to be customized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A short or generic request may create a recurring reminder using default time, interval, language, style, holiday, or timezone settings. <br>
Mitigation: After creation, review the task name, task ID, timezone, interval, schedule, and enabled status; pause, edit, or delete the task if the defaults do not match intent. <br>
Risk: Holiday skipping depends on the agent's ability to determine the current holiday calendar and may be uncertain for future or region-specific schedules. <br>
Mitigation: For holiday-aware reminders, confirm the country or region and review the generated holiday-checking instruction, especially for years or regions outside the agent's reliable knowledge. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tinalucky/stand-up-reminder) <br>
- [Holiday Skip Guide](references/holidays.md) <br>
- [Message Templates](references/messages.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown response with cron task configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task name, task ID, schedule, timezone, reminder count, enabled status, and management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
