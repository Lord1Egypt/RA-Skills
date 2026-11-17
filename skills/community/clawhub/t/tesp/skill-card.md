## Description:

TESP enforces a task execution signal protocol for non-instant work so agent execution stays visible, staged, versioned, and auditable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wewehg](https://clawhub.ai/user/wewehg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent supervisors use TESP to keep long-running or multi-agent work visible through acknowledgements, staged progress, blocker escalation, active queues, archives, and handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may create or update persistent task queue and archive files outside the current project.

Mitigation: Review storage paths before installation and prefer project-local paths for task queue and archive files.

Risk: Broad triggers may cause task metadata to be recorded more often than intended.

Mitigation: Define what task details must not be recorded and require confirmation before persisting sensitive or unnecessary task metadata.

## Reference(s):

- [TESP Protocol Reference](references/protocol.md)
- [TESP Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task updates, task-board entries, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include staged progress, blocker escalation, task queue/archive updates, and handoff summaries.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
