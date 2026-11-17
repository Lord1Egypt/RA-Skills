## Description:

Advanced techniques for minimizing token consumption in OpenClaw operations while maintaining or improving response quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foinbo](https://clawhub.ai/user/foinbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide OpenClaw agents toward lower-token workflows for memory retrieval, document processing, tool calls, context summarization, and session pruning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Predictive preloading and heartbeat learning may lead an agent to access personal memories, documents, calendar context, or behavior patterns without explicit opt-in or task boundaries.

Mitigation: Disable or rewrite those behaviors unless the deployment provides explicit opt-in, scoped source limits, user visibility, and short-lived task-scoped caching.

Risk: Token-minimization workflows can omit relevant context when a request requires comprehensive analysis, legal review, compliance review, or broad evidence gathering.

Mitigation: Require agents to surface the trade-off and get user consent before applying aggressive minimization to comprehensive or high-stakes review tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foinbo/skills/token-efficient-agent)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on minimizing retrieved context, tool results, and session history while preserving task-relevant information.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
