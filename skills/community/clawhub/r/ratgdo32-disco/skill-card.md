## Description: <br>
Control a ratgdo32 disco garage door opener via its local web API for door control, garage status, garage light, vehicle presence, parking assist, motion, and remote lockout on a LAN-only trust model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bolander72](https://clawhub.ai/user/bolander72) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and garage automation users use this skill to let an agent check and control a local ratgdo32 disco garage door opener. It supports status checks and physical actions such as opening or closing the door, toggling the light, and enabling or disabling remote lockout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause physical garage door actions if triggered too broadly or used without confirmation. <br>
Mitigation: Restrict use to explicit garage-control requests and require user confirmation before open, close, and remote-lockout actions. <br>
Risk: Closing the door without reliable status and obstruction checks could create a safety hazard. <br>
Mitigation: Verify status and obstruction data before close requests and refuse to close if those checks fail or report an obstruction. <br>
Risk: The local web API relies on LAN trust, so exposure beyond a trusted network increases control risk. <br>
Mitigation: Keep the device on a trusted WPA2/WPA3 network, avoid port forwarding, and use router isolation or VLAN segmentation where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bolander72/ratgdo32-disco) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and local HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RATGDO_HOST to identify the local ratgdo32 device; actions use LAN HTTP requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
