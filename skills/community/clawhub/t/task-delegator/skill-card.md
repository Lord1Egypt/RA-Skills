## Description:

Task Delegator routes tool-using requests such as search, file work, code execution, API calls, and data analysis through temporary subagents while keeping the main conversation focused on concise results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekkolearnai](https://clawhub.ai/user/ekkolearnai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long sessions compact by delegating tool-heavy work and returning short result summaries. It is intended for workflows that involve search, file analysis or edits, code generation, command execution, API calls, configuration guidance, or data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly routes tool-based work through disposable subagents.

Mitigation: Install only when that delegation posture is intended, and require visible disclosure when work is delegated.

Risk: Delegation records are configured for deletion by default, which can reduce auditability.

Mitigation: Remove cleanup-by-default or retain delegation records for tasks that require review, audit trails, or incident investigation.

Risk: The skill includes memory and soul.md persistence patterns without clear user consent.

Mitigation: Make memory and soul.md writes opt-in, and review the exact content before anything is stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ekkolearnai/skills/task-delegator)
- [ClawHub publisher profile](https://clawhub.ai/user/ekkolearnai)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown text with optional code blocks, command snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns concise summaries of delegated work; cleanup behavior and memory-writing behavior should be reviewed before use in auditable workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
