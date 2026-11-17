## Description:

Files, sockets, subscriptions, or other finite resources are acquired without a guaranteed release path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to identify resource leaks and recommend reliable acquire-and-release patterns for files, sockets, database clients, HTTP clients, event listeners, background tasks, and timers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Teardown tests that terminate processes or force error paths can disrupt live services if run against production systems.

Mitigation: Apply the skill's testing advice in development or staging environments and review teardown changes before deployment.

## Reference(s):

- [Resource Leak ClawHub release](https://clawhub.ai/mvogt99/skills/resource-leak)
- [mvogt99 ClawHub publisher profile](https://clawhub.ai/user/mvogt99)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with review findings and code or shell examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior is bundled in the skill artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
