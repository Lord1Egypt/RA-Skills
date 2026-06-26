## Description: <br>
Wake or shut down LAN devices by sending WOL-plus packets from the agent host when the user provides the needed MAC address, network interface, broadcast address, or target IPv4 address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeyeel](https://clawhub.ai/user/leeyeel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and advanced local-network users use this skill to wake devices or send compatible shutdown packets on a LAN. It also helps inspect and maintain a reusable device inventory for repeated power-control tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide package installation and service or configuration changes on LAN hosts. <br>
Mitigation: Require explicit user approval before installing packages or changing services or configuration, and prefer user-provided instructions when direct access is not appropriate. <br>
Risk: The WOL-plus Web UI has known default credentials in the provided evidence. <br>
Mitigation: Change the Web UI password before exposing or relying on the service on the network. <br>
Risk: Wake and shutdown packets affect local-network power state and may target the wrong host if device details are stale. <br>
Mitigation: Use dry-run and list mode first, verify the resolved MAC address, host, broadcast address, UDP port, and extra data, then send only to intended devices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeyeel/wolp) <br>
- [WOL-plus project](https://github.com/leeyeel/WOL-plus) <br>
- [WOL-plus releases](https://github.com/leeyeel/WOL-plus/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the local device inventory JSON after successful non-dry-run wake or shutdown actions.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
