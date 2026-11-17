## Description:

Suppresses the OpenClaw CLI startup banner by guiding an agent to set the documented OPENCLAW_HIDE_BANNER environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunobuddy](https://clawhub.ai/user/brunobuddy)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw CLI users use this skill when they want an agent to hide the recurring startup banner by updating shell configuration with OPENCLAW_HIDE_BANNER=1. The same guidance explains how to remove the setting later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to add one line to a user's shell configuration.

Mitigation: Review that the change only adds OPENCLAW_HIDE_BANNER=1, and remove that line later to restore the banner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brunobuddy/skills/shut-up-openclaw-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to add or remove a single shell environment variable in ~/.zshrc or ~/.bashrc.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
