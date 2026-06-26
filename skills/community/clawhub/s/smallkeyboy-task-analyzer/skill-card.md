## Description: <br>
Task Analyzer（认知理解 + 策略建模）helps an agent analyze complex user tasks by identifying explicit and implicit goals, risks, information gaps, an appropriate AI role, and whether the task should be decomposed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, orchestrator builders, and agent operators use this skill to turn a user task plus prior context and critic insight into structured task understanding, risk analysis, a recommended specialist role, and a suggested next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence how an agent frames complex work and recommends follow-up roles. <br>
Mitigation: Review the task insight, risks, recommended role, and next action before acting on the analysis or handing it to another agent. <br>
Risk: Incomplete or missing context can lead to a retry response or lower-confidence analysis. <br>
Mitigation: Provide the required user_task, context.previous_output, and context.critic_insight fields, and treat confidence_note as a review signal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/smallkeyboy-task-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/smallkeyboy) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance] <br>
**Output Format:** [Structured JSON with task insight, risk entries, recommended role, next action, and confidence note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, need_retry, or error status depending on input completeness and processing outcome] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
