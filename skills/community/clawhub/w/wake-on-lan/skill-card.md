## Description: <br>
Send Wake on LAN (WOL) magic packets to wake configured computers and network devices on a local network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonakic](https://clawhub.ai/user/tonakic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and homelab users use this skill to wake computers or network devices they own or manage, add and list local device profiles, and optionally wait for a configured device to respond. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wake-on-LAN packets may target the wrong system or network segment if device names, MAC addresses, or broadcast addresses are incorrect. <br>
Mitigation: Verify device names, MAC addresses, and broadcast addresses before use, and limit saved entries to systems the user owns or manages. <br>
Risk: The local device configuration can contain MAC addresses, IP addresses, and other network details. <br>
Mitigation: Keep references/devices.json scoped to necessary devices and protect it according to the user's normal local configuration handling practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonakic/wake-on-lan) <br>
- [Device configuration example](references/devices.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local JSON device configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may send UDP Wake-on-LAN packets, update references/devices.json, and print success or failure status when waiting for a device.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
