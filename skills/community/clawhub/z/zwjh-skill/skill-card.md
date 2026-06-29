## Description: <br>
Zwjh Skill helps an agent read local memory, analyze conversation history, repair or optimize behavior, predict issues, and generate evolution reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to run a local self-improvement workflow that reviews conversation memory, records lessons, and produces repair guidance or automation steps. It is intended for dedicated workspaces where local memory and command execution can be reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may retain sensitive conversation content. <br>
Mitigation: Use a dedicated workspace and avoid storing secrets or sensitive conversations in ~/.workbuddy/memory. <br>
Risk: Automatic repair and prevention steps may run package, ClawHub CLI, deletion, or scheduling commands. <br>
Mitigation: Require manual confirmation before pip, clawhub, deletion, or scheduling commands run, and inspect generated commands before execution. <br>
Risk: Scheduled self-improvement may continue running outside an active review session. <br>
Mitigation: Disable or narrowly scope scheduled-task sections unless recurring execution is explicitly needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/zwjh-skill) <br>
- [Publisher profile](https://clawhub.ai/user/fyniujin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, PowerShell, and shell command examples plus generated local report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run local file, package, CLI, deletion, and scheduling actions; require manual confirmation in sensitive workspaces.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and artifact heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
