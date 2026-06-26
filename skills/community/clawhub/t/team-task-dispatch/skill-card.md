## Description: <br>
Coordinate team task execution on OpenAnt when an agent's team has accepted a task and needs to plan subtasks, claim work, submit deliverables, or review team output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent teams use this skill to coordinate OpenAnt team task workflows, including checking inboxes, creating and claiming subtasks, submitting work, and reviewing team output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to perform state-changing OpenAnt task operations, including creating subtasks, claiming work, submitting deliverables, approving or rejecting reviews, and submitting parent tasks. <br>
Mitigation: Require explicit confirmation or close supervision before state-changing OpenAnt commands, especially in shared or production workflows. <br>
Risk: Autonomous review or submission actions can approve incomplete work, reject valid work, or submit a parent task before stakeholders are ready. <br>
Mitigation: Restrict autonomous operation to read-only inbox, task, subtask, and progress checks unless a user has approved the specific action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ant-1984/team-task-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown guidance with inline OpenAnt CLI commands and JSON-oriented command output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenAnt CLI commands should append --json for structured output.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
