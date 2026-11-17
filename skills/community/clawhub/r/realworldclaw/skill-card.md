## Description:

RealWorldClaw lets an AI agent work with ESP32-based hardware by reading sensors, sending actuator commands, managing automation rules, and using the optional RealWorldClaw platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianzhibo-design](https://clawhub.ai/user/brianzhibo-design)

### License/Terms of Use:


## Use Case:

Developers and hardware operators use this skill to give an agent controlled access to RWC-compatible ESP32 devices for sensor readings, actuator actions, device status checks, and simple hardware automation rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send commands to real ESP32-connected hardware, including relays, servos, LEDs, and buzzers.

Mitigation: Use only with trusted devices and networks, review each configured device before use, and require human approval before actuator commands or rule changes.

Risk: Automation rules may repeatedly trigger physical actions during monitoring.

Mitigation: Review rules before enabling monitoring, keep intervals conservative, and stop monitoring when unattended operation is not intended.

Risk: The skill handles device access codes and platform account credentials with weak safety and security guardrails.

Mitigation: Avoid entering real passwords on the command line, keep config files private, use least-privileged test accounts where possible, and verify config.json before login or registration.

## Reference(s):

- [RWC Protocol v0.1 (Draft)](references/protocol.md)
- [RealWorldClaw API endpoint](https://realworldclaw-api.fly.dev/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local automation rule files and may send commands to configured ESP32 hardware or the RealWorldClaw platform API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
