## Description:

Design and configure self-contained recurring agent checks with explicit targets, authority, change-sensitive reporting and stop conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

External users, developers and agent operators use Pulse to create bounded recurring checks for monitoring, reminders and follow-ups with clear evidence sources, notification rules, authority limits and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended installer command uses an unpinned remote npm CLI.

Mitigation: Review or pin the installer before use, or install manually into the agent's skill directory.

Risk: A recurring watch can exceed the user's intended authority or continue after the target is complete if it is underspecified.

Mitigation: Create watches with explicit targets, authority boundaries, notification rules and stop conditions, then read back the scheduler's identifier, cadence and enabled state.

## Reference(s):

- [Meta-Pulse: review the watch portfolio](references/meta-pulse.md)
- [Pulse ClawHub release](https://clawhub.ai/antreasantoniou/skills/pulse)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown guidance and self-contained watch prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only output; activation depends on the host agent's supported scheduler.]

## Skill Version(s):

1.0.0 (source: changelog and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
