## Description: <br>
Coordinates complex tasks through a Three Departments and Six Ministries multi-agent workflow that separates triage, planning, review, dispatch, execution, and final reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[743834110](https://clawhub.ai/user/743834110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run non-trivial work through a structured workflow with separate planning, review, task dispatch, execution, and final reporting roles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create local .court-session records in the current project, which can capture task details from sensitive repositories. <br>
Mitigation: Use it in a controlled workspace and review generated session records before sharing or committing them. <br>
Risk: The workflow can delegate larger tasks across multiple agents, including background work. <br>
Mitigation: Monitor delegated work, review proposed changes before applying them, and keep sensitive repositories under explicit user control. <br>
Risk: The quick-path command can skip the review step that normally checks plans before execution. <br>
Mitigation: Avoid the quick-path command when independent review is needed for safety, security, or correctness. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/743834110/san-sheng-liu-bu) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/743834110) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown session records and concise agent responses, with code, diffs, shell commands, or configuration changes when the delegated task requires them.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates .court-session/{YYYYMMDD-task}/ records in the current workspace for multi-step task sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
