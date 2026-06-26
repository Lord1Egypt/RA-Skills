## Description: <br>
Task Analyzer helps an agent understand a user task, identify hidden needs, surface execution, cognitive, and information risks, recommend a task-specific AI role, and decide whether the task should be decomposed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a planning stage before execution: it analyzes the user task, checks upstream context and critic feedback, identifies risks and missing information, and returns a structured recommendation for role selection and possible task decomposition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent more planning-oriented and less execution-focused. <br>
Mitigation: Use it as an explicit pre-execution analysis stage, then hand off based on the returned next_action instead of letting analysis replace execution. <br>
Risk: Incorrect or incomplete task analysis could lead downstream agents to follow a poorly matched role or strategy. <br>
Mitigation: Review the confidence note, risks, and missing context; retry when required fields are absent or when critic feedback indicates high uncertainty. <br>


## Reference(s): <br>
- [Task Analyzer on ClawHub](https://clawhub.ai/smallkeyboy/task-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON with task insight, risk findings, recommended role, next action, and confidence note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, need_retry, or error status depending on context completeness and analysis outcome.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
