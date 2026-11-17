## Description:

Pick the best AI model for any task using the Smart Spawn API. No plugin needed - just HTTP requests to ss.deeflect.com/api.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deeflect](https://clawhub.ai/user/deeflect)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to select model IDs for task-specific sub-agent spawning, compare models, request multiple recommendations, or decompose complex work into model-assigned subtasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions are sent to a third-party API.

Mitigation: Use broad categories or sanitized summaries, and do not send secrets, private customer data, or full confidential prompts.

Risk: Returned model IDs, subtasks, or swarm plans may drive follow-on agent spawning and cost.

Mitigation: Review the returned model choices and plans before spawning agents or starting paid work.

Risk: The API can be unavailable, rate limited, or return unsuitable recommendations.

Mitigation: Use the documented fallback behavior, retry only when appropriate, and check the status endpoint when reliability matters.

## Reference(s):

- [Smart Spawn on ClawHub](https://clawhub.ai/deeflect/skills/smart-spawn)
- [deeflect publisher profile](https://clawhub.ai/user/deeflect)
- [Smart Spawn API status](https://ss.deeflect.com/api/status)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce model IDs, pricing and score context, model comparisons, recommended subtasks, or parallel task graphs depending on the endpoint used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
