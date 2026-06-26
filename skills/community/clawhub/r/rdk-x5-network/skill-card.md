## Description: <br>
Helps configure and troubleshoot RDK X5 networking, including WiFi connections, wired static IPs, Bluetooth pairing, WiFi hotspots, SSH access, and VNC connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and RDK X5 users use this skill to generate command guidance for network setup and connectivity troubleshooting on RDK X5 devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes sudo, nmcli, systemctl, SSH, VNC, and srpi-config steps that can change device network access or remote-access exposure. <br>
Mitigation: Review each command before running it, replace sample SSIDs, passwords, and IP addresses, and enable SSH or VNC only on trusted networks with strong access controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/katherineedwards2475/rdk-x5-network) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; commands require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
