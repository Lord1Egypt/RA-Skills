## Description: <br>
Schedules Tesla charging on specified dates with target battery percentages and times while managing charge limits during and after sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thibautrey](https://clawhub.ai/user/thibautrey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Tesla owners and automation users use this skill to maintain a schedule file, calculate charge start times, and manage vehicle charge limits through recurring cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls Tesla account behavior on a recurring schedule. <br>
Mitigation: Review the schedule file, credential handling, timezone assumptions, and cron disable procedure before enabling automation. <br>
Risk: The security evidence reports a shell-based charge-start path and advises against using --auto-start until it is fixed or contained. <br>
Mitigation: Avoid --auto-start and use review-gated manual or contained execution for charge-start behavior until that path is corrected. <br>


## Reference(s): <br>
- [API Reference - Tesla Smart Charge](references/api_reference.md) <br>
- [Cron Integration - Tesla Smart Charge](references/cron_setup.md) <br>
- [Tesla charge schedule example](references/tesla-charge-schedule-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON schedule or plan files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local schedule, session-state, and charge-plan JSON files during operation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
