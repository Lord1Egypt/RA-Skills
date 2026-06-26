## Description: <br>
Control WLED LED controllers via HTTP API for power, brightness, RGB color, effects, palettes, presets, and device status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rowbotik](https://clawhub.ai/user/rowbotik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to control WLED LED strips or matrices on their local network through a Python CLI and the WLED HTTP JSON API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can immediately change the visible light state of the targeted WLED device. <br>
Mitigation: Verify the device IP address, hostname, or configured alias before running power, color, brightness, effect, palette, or preset commands. <br>


## Reference(s): <br>
- [WLED HTTP API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a host, hostname, or configured alias to target a WLED device on the same network.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
