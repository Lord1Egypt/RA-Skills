## Description: <br>
DiGiCo mixer OSC protocol remote control system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Audio technicians and automation operators use this skill to connect to DiGiCo mixer infrastructure, send OSC control actions, monitor mixer status, and manage scenes or snapshots when remote operation is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send OSC actions that change live mixer state, including scenes, gain, compressor settings, routing-related controls, and snapshots. <br>
Mitigation: Restrict use to approved operators on trusted networks and require human confirmation before write actions against production mixer equipment. <br>
Risk: Incorrect target IP or port values could send control traffic to the wrong device or fail during time-sensitive audio operations. <br>
Mitigation: Verify the DiGiCo mixer IP address and OSC port before connection and maintain an allowlist for production devices. <br>
Risk: Automated operation can apply changes without built-in safety checks or confirmations. <br>
Mitigation: Add an external approval process for automated scene, gain, routing, compressor, and snapshot changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zimuge-doudou/skill-digico-mixer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zimuge-doudou) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration, Guidance] <br>
**Output Format:** [JSON status objects and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include success or error status, OSC target details, and action-specific fields such as scene, channel, gain, latency, or snapshot name.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
