## Description: <br>
Helps users clarify, break down, and schedule long-term goals into manageable tasks with automated reminders and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyxin-del](https://clawhub.ai/user/joeyxin-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn vague long-term goals into clarified goal statements, milestones, atomic tasks, local plan files, cron-style reminder payloads, and progress reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save personal goal, milestone, and task details as local markdown files. <br>
Mitigation: Install only if local plan persistence is acceptable, and use output paths only for folders the user intends the skill to modify. <br>
Risk: Cron-style reminder JSON may be copied into an external automation system and trigger repeated reminders. <br>
Mitigation: Review generated cron expressions and payload contents before placing them into any automation system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeyxin-del/secretaryskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plan files, plain text CLI guidance, and JSON cron reminder payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save goal and task details to local markdown files when the user chooses to persist a plan.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
