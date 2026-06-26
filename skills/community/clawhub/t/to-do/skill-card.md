## Description: <br>
Give your AI the power to act in the future by scheduling delayed prompts and one-off reminders that automatically wake the agent at an exact moment to execute workflows, check systems, or send notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevLumuz](https://clawhub.ai/user/DevLumuz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to schedule precise future reminders or one-off autonomous agent actions with self-contained instructions, routing details, and timezone-aware execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delayed autonomous execution can cause future agent actions to run without the original session context. <br>
Mitigation: Install only when delayed execution is acceptable, and schedule only explicit, self-contained instructions that avoid sensitive operational content. <br>
Risk: The security summary reports command-injection and scheduler-control risks from shell-based scheduling. <br>
Mitigation: Avoid secrets, tokens, shell-like text, and highly sensitive instructions in reminders; prefer a version that uses safer process APIs, input validation, and scoped scheduler deletion. <br>
Risk: Scheduled task bodies or logs may expose sensitive reminder content if stored in broadly readable locations. <br>
Mitigation: Keep reminder text non-sensitive and prefer storage in restricted user-owned locations. <br>


## Reference(s): <br>
- [ClawHub To-Do skill page](https://clawhub.ai/DevLumuz/to-do) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Schedules one-off future agent instructions through the local operating-system scheduler and can list or delete pending tasks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
