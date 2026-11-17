## Description:

Task Analyzer helps agents understand complex user tasks, identify hidden needs, surface risks and information gaps, recommend a suitable AI role, and decide whether the task should be decomposed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a structured task-analysis stage before execution. It is intended to produce task insight, risk notes, a recommended specialist role, and a suggested next action rather than directly completing the user's task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may return Chinese-language structured output, which can be unsuitable for workflows expecting another language.

Mitigation: Adapt the prompt or downstream parser expectations before deployment in non-Chinese-language workflows.

Risk: The skill provides analysis and next-action recommendations, not final execution decisions.

Mitigation: Keep a review or orchestration step in place before acting on recommended roles, decomposition decisions, or next actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/smallkeyboy-task-analyzer)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON with concise text fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Chinese-language structured output unless adapted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
