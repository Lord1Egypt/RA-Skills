## Description:

Seamless gateway restart with automatic context recovery and post-restart notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate intentional OpenClaw gateway restarts while preserving task state, notifying the user, and restoring context after the restart completes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants an agent broad authority to restart a gateway, schedule recovery, send messages, and persist recovery state.

Mitigation: Use it only for explicitly approved gateway restart workflows and require fresh user confirmation before applying configuration changes or resuming side-effecting tasks after restart.

Risk: Restart state can contain sensitive or private context if the agent writes too much to NOW.md.

Mitigation: Keep NOW.md concise, avoid secrets and private message contents, and delete recovery state after it is no longer needed.

Risk: Automatic recovery may resume interrupted work without enough human awareness.

Mitigation: Notify the user after restart, summarize the recovered state, and ask before continuing actions that change systems, configuration, or external services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zihaofeng2001/skills/seamless-restart)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zihaofeng2001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces state-capture, notification, recovery scheduling, and restart guidance for a single agent workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
