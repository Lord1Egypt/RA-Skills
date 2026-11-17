## Description:

Task Analyzer helps an orchestrated agent workflow understand a user's task, identify hidden needs, risks, and information gaps, generate a task-specific AI role, and decide whether the task should be decomposed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent workflow builders use this skill inside orchestrated systems to analyze a task before execution, including goals, hidden needs, risk areas, missing context, role requirements, and decomposition needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for structured upstream analysis rather than final task execution, so using its output as a final answer could produce incomplete or misleading results.

Mitigation: Use it inside an orchestrated workflow that supplies the expected context fields and routes the analysis to an appropriate executor or reviewer.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured JSON-style analysis with success, retry, and error variants]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns task insight, risk descriptions, a recommended role, a suggested next action, and a confidence note.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
