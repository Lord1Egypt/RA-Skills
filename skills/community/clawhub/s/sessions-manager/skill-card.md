## Description:

Manage OpenClaw agent sessions - list active/completed sessions, view session details, and delete sessions by ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6eanut](https://clawhub.ai/user/6eanut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw session state, monitor concurrent work, debug stuck sessions, and remove stale or unwanted session metadata and history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The delete command can remove files outside the intended session directory if session metadata is malformed or tampered with.

Mitigation: Review or patch delete-path validation before use and manually confirm the target session ID or key before running delete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/6eanut/skills/sessions-manager)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces session listings and delete confirmations for local OpenClaw session files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
