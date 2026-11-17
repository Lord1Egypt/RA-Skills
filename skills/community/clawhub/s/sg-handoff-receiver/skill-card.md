## Description:

Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to take over work from a prior session handoff, verify repository state against the handoff, continue the listed next step, and refresh the handoff artifact before yielding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or stale handoff may direct the agent to run inappropriate validation commands or continue the wrong work.

Mitigation: Use this only in repositories where the handoff files are trusted, review unusual commands or instructions, and reconcile branch, status, diff, and recent log before edits.

Risk: Parallel, orphan, or drifted handoffs can cause the agent to continue the wrong stream or expand scope.

Mitigation: Use CURRENT and INDEX.md to classify active, paused, orphan, done, or superseded streams, and ask a focused question when conflicts or index drift appear.

## Reference(s):

- [Handoff Receiver on ClawHub](https://clawhub.ai/clarezoe/skills/sg-handoff-receiver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown response with structured status sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update handoff files and index pointers as part of the agent workflow.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
