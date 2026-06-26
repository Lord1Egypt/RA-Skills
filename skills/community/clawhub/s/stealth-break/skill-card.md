## Description: <br>
Stealth Break gives wellness break suggestions and can help set macOS notification reminders for eye rest, posture breaks, breathing, and other short recovery routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-qianchen](https://clawhub.ai/user/ryan-qianchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual developers use this skill to ask for short work-break ideas and optional macOS reminder setup for wellness pauses during long work sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose persistent user-level cron reminders for macOS notifications. <br>
Mitigation: Ask the agent to show the exact cron command and schedule before enabling reminders, confirm explicitly, and keep instructions for listing and removing cron entries. <br>
Risk: Some break suggestions involve appearing to work while taking a break, which may conflict with workplace expectations. <br>
Mitigation: Use the guidance only where appropriate for the user's role and organization, and prioritize transparent, health-focused breaks that do not affect commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-qianchen/stealth-break) <br>
- [Publisher profile](https://clawhub.ai/user/ryan-qianchen) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, configuration] <br>
**Output Format:** [Markdown with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cron schedules and osascript notification commands for macOS after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
