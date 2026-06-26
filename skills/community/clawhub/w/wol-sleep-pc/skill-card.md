## Description: <br>
Sends Wake-on-LAN and Sleep-on-LAN packets for a configured PC on a local network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oblivisheee](https://clawhub.ai/user/oblivisheee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and local-network administrators use this skill to let an agent wake or sleep a PC by sending explicit LAN power-control packets with configured MAC, broadcast address, and port values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured MAC, inverted MAC, broadcast address, or port values could send wake or sleep packets to the wrong target or network segment. <br>
Mitigation: Configure only devices you control, verify all target network settings before use, and run the skill only after an explicit wake or sleep request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oblivisheee/wol-sleep-pc) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces UDP LAN power-control actions through bundled Python scripts; requires user-provided target network settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
