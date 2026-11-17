## Description:

Rename OpenClaw chat sessions by updating the session history store or calling the built-in `sessions.rename` backend path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to rename, retitle, or relabel the current or another OpenClaw chat session when a first-class chat tool is not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly modify an OpenClaw session history database if the normal product path is unavailable.

Mitigation: Confirm the exact OpenClaw instance, session, and new title before making changes.

Risk: Selecting the wrong session row could rename an unrelated or archived session.

Mitigation: Target only the intended row, prefer the active and most recently updated matching session, and read the updated row back after the change.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a confirmation query after a targeted session-history update.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
