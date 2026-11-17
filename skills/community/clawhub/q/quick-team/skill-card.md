## Description:

Quick Team helps OpenClaw users create AI team member directories and configuration files from natural-language requests, including SOUL, IDENTITY, TOOLS, HEARTBEAT, and MEMORY templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zwl](https://clawhub.ai/user/zhao-zwl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to define new AI team members, generate their standard markdown files, and receive guided configuration steps for openclaw.json and Gateway validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable templates can persist API-key instructions or someone else's personal profile into generated agent workspaces.

Mitigation: Review and edit templates before use, replace API-key notes with environment-variable or secret-manager references, and remove hard-coded personal profile details.

Risk: Updating openclaw.json can change agent spawn behavior and broaden subagent permissions.

Mitigation: Show the full diff before writing and keep allowAgents limited to the specific new agent IDs unless broader access is explicitly required.

Risk: Restarting OpenClaw Gateway can interrupt active sessions and running tasks.

Mitigation: Ask for confirmation before restart and warn users that active work may be interrupted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, JSON configuration examples, shell commands, and validation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed workspace files and configuration changes that should be reviewed before execution.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
