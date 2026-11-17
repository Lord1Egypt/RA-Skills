## Description:

Auto-create a new session when OpenClaw context usage reaches 80% without requiring Mem0 or file memory systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0range-x](https://clawhub.ai/user/0range-x)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to check context usage during long conversations and emit a new-session trigger before the context window fills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic session-rotation prompts may interrupt active work when context usage reaches the configured threshold.

Mitigation: Use the skill in a heartbeat or status-check workflow where the emitted new-session trigger can be reviewed before continuing work in the new session.

Risk: The released operational messages are Chinese-only, which may be unclear in non-Chinese workflows.

Mitigation: Review and localize the emitted trigger and handoff text before using the skill with non-Chinese users or teams.

## Reference(s):

- [Session Rotate 80 on ClawHub](https://clawhub.ai/0range-x/skills/session-rotate-80)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text status lines and Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emits threshold status, a new-session trigger, and a short handoff hint; operational messages are Chinese-only in the released artifact.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
