## Description:

Session Relay helps agents preserve and restore recent task context by saving structured snapshots and recent conversation tails across context window boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianglingling007](https://clawhub.ai/user/jianglingling007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to carry active work, decisions, recent conversation context, and next steps across long sessions, compactions, and new-session handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently read, store, and reuse recent conversation text across sessions in ways users may not expect.

Mitigation: Use an opt-in restore flow, make stored memory inspectable and deletable, and apply clear retention rules before enabling it in sensitive or shared workspaces.

Risk: Snapshots may capture sensitive conversation content if automatic saving is enabled.

Mitigation: Strip API keys, tokens, passwords, and unnecessary personal data before saving snapshots, and prefer summary-only snapshots where verbatim history is not required.

## Reference(s):

- [Relay Snapshot Format Reference](references/snapshot-format.md)
- [Session Relay ClawHub Release](https://clawhub.ai/jianglingling007/skills/session-relay)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with snapshot templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces best-effort continuity state for agent sessions; snapshot size guidance targets concise handoff files.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
