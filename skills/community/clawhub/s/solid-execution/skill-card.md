## Description:

A workflow guidance skill that helps agents execute tasks step by step, track commitments, verify completion, and use oversight checks to reduce missed work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyunxiao-ai](https://clawhub.ai/user/yangyunxiao-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to structure multi-step work, maintain progress visibility, and check that stated actions are backed by verifiable outputs. It is intended for task execution discipline rather than domain-specific content generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill states its workflow rules as mandatory, which could conflict with higher-priority system, developer, or user instructions.

Mitigation: Use the skill only within the normal instruction hierarchy and make higher-priority instructions explicit before execution.

Risk: The skill encourages automatic tool use based on action wording, which may trigger tool calls without enough user intent or context.

Mitigation: Require tool calls to remain tied to the current task, available permissions, and explicit user goals.

Risk: The skill recommends persistent HEARTBEAT entries, pending queues, and Cron behavior without clear user controls.

Mitigation: Require explicit approval for persistent state or scheduled behavior, and provide a way to inspect and delete pending entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyunxiao-ai/skills/solid-execution)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown instructions and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
