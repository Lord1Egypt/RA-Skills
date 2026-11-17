## Description:

Snail Mail provides a slow-channel inbox for agents to leave non-urgent but important operator messages and render, read, or archive those messages on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvdegenz](https://clawhub.ai/user/dvdegenz)

### License/Terms of Use:


## Use Case:

Operators and their agents use this skill to record notable non-urgent events, decisions, abnormalities, and FYIs, then review or archive them later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbox content may include externally supplied text and can be rendered into chat formats.

Mitigation: Treat inbox entries as untrusted content and review rendered output before sharing it in Discord, Slack, or other channels.

Risk: If OPENCLAW_WORKSPACE is not set, inbox data may be stored under the agent user's home directory.

Mitigation: Set OPENCLAW_WORKSPACE to the intended workspace before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dvdegenz/skills/snail-mail)
- [Publisher profile](https://clawhub.ai/user/dvdegenz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON for management commands and HTML, Markdown, or plain text for rendered inbox views.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, writes local inbox data under OPENCLAW_WORKSPACE when set, and uses OPENCLAW_CHANNEL to choose render format.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
