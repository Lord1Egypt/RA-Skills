## Description:

MCP tools for Anki Vector: speech, motion, camera, sensors, and automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danmartinez78](https://clawhub.ai/user/danmartinez78)

### License/Terms of Use:


## Use Case:

Developers and robot automation users use this skill to connect an agent to an Anki or Digital Dream Labs Vector robot for speech, movement, camera capture, sensor reads, and look-reason-act workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the vectorclaw-mcp package, which creates a supply-chain dependency.

Mitigation: Use a pinned, reviewed package version and install only when the package and publisher are trusted.

Risk: The skill can control a physical robot and access camera-related tools.

Mitigation: Run the robot under supervision, use a low-privilege account, and apply caution with motion and camera workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danmartinez78/skills/vectorclaw-mcp)
- [Project repository listed in skill](https://github.com/danmartinez78/VectorClaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing MCP setup and usage guidance; tool responses may include robot status, sensor readings, and camera outputs.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
