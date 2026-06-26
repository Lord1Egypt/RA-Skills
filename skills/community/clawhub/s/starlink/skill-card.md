## Description: <br>
Control Starlink dish via local gRPC API, including status checks, WiFi client listing, speed tests, stow and unstow actions, reboot, and GPS location retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danfedick](https://clawhub.ai/user/danfedick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Starlink owners, operators, and network administrators use this skill to inspect local dish and router status, review connected clients, run connectivity checks, and perform service-impacting device actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can expose sensitive device, connected-client, and location data. <br>
Mitigation: Require user confirmation before showing client lists, GPS coordinates, or other local network details. <br>
Risk: Reboot, stow, and unstow commands can interrupt internet service or change hardware state. <br>
Mitigation: Ask for explicit approval before running service-impacting commands and confirm the user owns or administers the Starlink hardware. <br>
Risk: The release security verdict is suspicious because the skill exposes sensitive controls without enough explicit consent or warning. <br>
Mitigation: Verify the source repository, prefer a pinned install revision, and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub Starlink Skill](https://clawhub.ai/danfedick/starlink) <br>
- [starlink-cli install source](https://github.com/danfedick/starlink-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May expose device, client, and location data when commands are run against a local Starlink network.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
