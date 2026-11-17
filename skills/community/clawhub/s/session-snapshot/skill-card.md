## Description:

Session Snapshot periodically saves session state so an agent can restore prior conversation context, task progress, workspace context, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soroyue](https://clawhub.ai/user/soroyue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve recent conversation history, task progress, workspace context, and timestamps for explicit session recovery or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session snapshots may persist credentials, personal data, or confidential workspace details from conversation history and context.

Mitigation: Enable the skill only where snapshots are protected, redacted before storage, and easy to delete.

Risk: Restoring a saved snapshot can reintroduce prior context without enough user awareness.

Mitigation: Restore snapshots only after explicit confirmation from the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soroyue/skills/session-snapshot)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON session snapshots with conversational restore guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshots may include conversation history, task state, workspace context, key variables, and timestamps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
