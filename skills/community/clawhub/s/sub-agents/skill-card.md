## Description:

Spawn and coordinate sub-agent sessions for parallel work, including research, code, analysis, model routing, and multi-agent workflow management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate self-contained research, code, analysis, and workflow tasks to isolated sub-agent sessions with explicit handoff, routing, monitoring, and announce guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vague sub-agent handoffs can produce incomplete, incorrect, or hard-to-review results because child sessions receive only the task text, referenced files, and attachments supplied to them.

Mitigation: Use explicit objectives, context, inputs, success criteria, output contracts, constraints, and announce instructions in every spawned task.

Risk: Sub-agent orchestration can expose sensitive context if secrets or untrusted documents are attached to child sessions.

Mitigation: Scope tasks narrowly, avoid attaching secrets, prefer sandboxed children for sensitive work, and attach only the files needed for the task.

Risk: Unmonitored or unnecessary child sessions can add cost and operational complexity.

Mitigation: Spawn only for self-contained work that benefits from delegation, set run timeouts where appropriate, and monitor, kill, or archive sessions when they are no longer needed.

## Reference(s):

- [Model Reference](references/models.md)
- [ClawHub Skill Page](https://clawhub.ai/bill492/skills/sub-agents)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with structured task templates, command examples, and configuration parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sub-agent outputs may be announced, suppressed with ANNOUNCE_SKIP, or written to task-specified files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
