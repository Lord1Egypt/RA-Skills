## Description:

Rdk X5 Network helps agents guide RDK X5 users through WiFi, wired static IP, Bluetooth pairing, hotspot, SSH, and VNC network troubleshooting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and troubleshoot RDK X5 network connectivity, Bluetooth pairing, hotspot setup, and remote access. It is intended for agents assisting with normal device administration and network recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged network administration commands can disrupt connectivity or modify the active remote session.

Mitigation: Review commands before execution, avoid changing the connection that keeps the current session alive, and keep a recovery access path available.

Risk: Hotspot, SSH, and VNC setup can expose remote access or weak credentials on untrusted networks.

Mitigation: Replace sample hotspot passwords with strong unique values, enable SSH or VNC only when needed, and restrict remote access to trusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-network)
- [Publisher profile](https://clawhub.ai/user/katherineedwards2475)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires nmcli; several commands may require sudo privileges.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
