## Description: <br>
Send Wake-on-LAN magic packets to wake LAN devices by saved alias or direct MAC/IP commands on Linux, macOS, and Android. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofqin2026](https://clawhub.ai/user/kingofqin2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and homelab users use this skill to have an agent wake sleeping devices on networks they control and manage reusable Wake-on-LAN device aliases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Wake-on-LAN packets to network devices. <br>
Mitigation: Use it only on networks and devices you control, and verify the target MAC address and IP address before sending packets. <br>
Risk: Saved aliases store MAC and IP addresses locally in the skill directory. <br>
Mitigation: Review or remove the local devices file on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofqin2026/wake-lan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-managed device aliases containing MAC and IP addresses to a local devices.json file.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
