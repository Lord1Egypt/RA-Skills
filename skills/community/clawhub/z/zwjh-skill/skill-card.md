## Description: <br>
Zwjh Skill helps an agent analyze local WorkBuddy memory, identify root causes and implicit needs, suggest or record fixes, and generate ongoing evolution reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to inspect local conversation memory, identify recurring issues and root causes, generate evolution reports, and optionally configure daily scheduled analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent daily automation that analyzes conversation memory and stores inferred needs or analysis history. <br>
Mitigation: Review the scheduled task or cron command before enabling it, confirm the files it writes, and remove the schedule if ongoing unattended execution is not wanted. <br>
Risk: Suggested repair commands and generated scripts may affect the local environment or scheduled-task configuration. <br>
Mitigation: Review commands before execution, require user confirmation for system-level changes, and verify local logs and generated files after setup. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Python, PowerShell, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local memory, log, scheduled-task, and report files when a user chooses to run the generated snippets.] <br>

## Skill Version(s): <br>
1.6.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
