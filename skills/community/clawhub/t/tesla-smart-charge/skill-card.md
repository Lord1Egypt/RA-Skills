## Description:

Schedules Tesla charging on specified dates with target battery percentages and times, managing charge limits during and after sessions for battery health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thibautrey](https://clawhub.ai/user/thibautrey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to schedule Tesla charging from a JSON plan, calculate charging start times, and manage charge limits before, during, and after planned sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended Tesla account actions that change vehicle charge limits or start charging.

Mitigation: Review the schedule and commands before enabling cron, and use the skill only where unattended Tesla account automation is acceptable.

Risk: Security evidence reports a shell-command injection issue in the auto-start path.

Mitigation: Do not enable --auto-start until the shell=True command path is fixed and reviewed.

Risk: The skill depends on a separate tesla skill and passes account-related environment variables to subprocesses.

Mitigation: Pin and verify the tesla dependency, configure credentials through the documented TESLA_EMAIL environment variable, and pass only required environment variables.

## Reference(s):

- [Tesla Smart Charge on ClawHub](https://clawhub.ai/thibautrey/skills/tesla-smart-charge)
- [API Reference](references/api_reference.md)
- [Cron Integration](references/cron_setup.md)
- [Schedule File Template](references/tesla-charge-schedule-example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read JSON schedule, plan, and session-state files when the provided Python script is executed.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
