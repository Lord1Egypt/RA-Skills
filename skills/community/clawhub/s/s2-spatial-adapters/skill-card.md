## Description: <br>
Provides a unified interface for agents to control Home Assistant, Xiaomi Mijia, and Tuya IoT devices through S2 spatial intent commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home automation operators use this skill to let agents translate user intent into Home Assistant, Xiaomi Mijia, or Tuya device commands. It should be used in monitored environments because real actuation can affect lights, HVAC, locks, alarms, and feeders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority over physical smart-home devices, including sensitive actions such as door-lock control. <br>
Mitigation: Use explicit device allowlists, keep locks, alarms, and other high-risk devices out of scope unless each action requires human confirmation, and avoid autonomous authority over safety-critical systems. <br>
Risk: Incorrect or stale device mappings could cause an agent to actuate the wrong physical device. <br>
Mitigation: Review protocol, device ID, and room mappings before use and re-check mappings after smart-home topology changes. <br>
Risk: Real actuation depends on environment-provided credentials and endpoint configuration. <br>
Mitigation: Inject credentials only through a managed runtime or secrets vault, avoid local plaintext credential files, and constrain runtime access to the minimum required devices and endpoints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SpaceSQ/s2-spatial-adapters) <br>
- [Publisher profile](https://clawhub.ai/user/SpaceSQ) <br>
- [Project homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands, JSON intent payloads, and runtime status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires environment variables for real device actuation; defaults to dry-run behavior when the actuation valve is not enabled.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
