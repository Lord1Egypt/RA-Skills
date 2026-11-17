## Description:

Clean up stale or unwanted subagent sessions from the OpenClaw webchat sidebar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saybanet](https://clawhub.ai/user/saybanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to remove stale or unwanted subagent session entries from local sessions.json indexes so the webchat sidebar reflects current sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup changes local OpenClaw session indexes and can remove all subagent sidebar entries when --all is used.

Mitigation: Run --dry-run first, consider backing up ~/.openclaw/agents, use --agent for scoped cleanup, and reserve --all for intentional full subagent cleanup.

Risk: Users may think cleanup failed if the sidebar still shows old entries immediately after editing sessions.json.

Mitigation: Restart the OpenClaw gateway and refresh the webchat page after cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saybanet/skills/sayba-session-cleanup)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run mode, scoped agent cleanup, and gateway restart after cleanup.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
