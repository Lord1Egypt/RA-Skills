## Description:

Use when work should span one or more detached tasks but still behave like one job with a single owner context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use TaskFlow to coordinate durable multi-step work that can link detached child tasks, persist small resume state, wait on people or external systems, and return one owner-facing result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflows can persist small state or waiting metadata that may include sensitive content if callers place it there.

Mitigation: Store only the minimum state required to resume, and avoid placing sensitive content in stateJson or waitJson unless it is necessary.

Risk: Linked child tasks may continue running as part of durable multi-step work if cancellation is not handled deliberately.

Mitigation: Use requestCancel when scheduling should stop, use cancel when active linked child tasks should also be cancelled, and inspect task summaries during orchestration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/yihui-taskflow)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with TypeScript examples and API usage patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for durable flow identity, child-task linkage, waiting state, revision-checked mutations, and cancellation handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
