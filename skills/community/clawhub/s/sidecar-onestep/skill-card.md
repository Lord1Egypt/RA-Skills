## Description:

Control SidecarOneStep, a macOS Sidecar enhancement tool for one-click iPad connection, remote control, and MCP-based automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zy84338719](https://clawhub.ai/user/zy84338719)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and automation-focused macOS users use this skill to configure and operate SidecarOneStep through MCP so an agent can list iPad devices, connect or disconnect Sidecar sessions, inspect status, manage the web control server, view logs, and use virtual display controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unverified external macOS app as an MCP server that can control Sidecar devices.

Mitigation: Install only when the publisher is trusted, prefer a fixed release, and verify the app signature, notarization, or a trusted hash when available before use.

Risk: The skill can start a local HTTP control server for Sidecar remote control.

Mitigation: Avoid starting the HTTP control server unless the user understands who can access it and how access is protected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zy84338719/skills/sidecar-onestep)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zy84338719)
- [SidecarOneStep Website](https://sidecaronestep.app.murphyyi.com/)
- [SidecarOneStep GitHub Repository](https://github.com/yi-nology/sidecarOneStep)
- [SidecarOneStep Latest Release](https://github.com/yi-nology/sidecarOneStep/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, mcporter, and SidecarOneStep.app installed in /Applications with MCP enabled.]

## Skill Version(s):

1.4.1 (source: server release metadata, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
