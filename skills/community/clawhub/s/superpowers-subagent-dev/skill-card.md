## Description: <br>
Coordinates implementation-plan execution by dispatching independent subagents for tasks and applying verification checkpoints, adapted for OpenClaw's isolated session model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to execute implementation plans with mostly independent tasks by coordinating subagent work, review checkpoints, tests, commits, and final review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated coding subagents may modify repository files or create commits that do not fully match the intended plan. <br>
Mitigation: Use the skill on the intended branch, run the specified tests, and review generated commits before relying on them. <br>
Risk: Plans passed to subagents may include unrelated private context or secrets. <br>
Mitigation: Provide only the task context needed for each subagent and avoid including unrelated secrets or private material. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown guidance with inline command examples and task-status conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide subagent coordination, testing, commits, and review loops.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
