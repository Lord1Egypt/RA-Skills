## Description: <br>
Control IKEA TRÅDFRI lights and groups through a local TRÅDFRI gateway using the native gateway API via node-tradfri-client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymebosma](https://clawhub.ai/user/ymebosma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate IKEA TRÅDFRI lights and groups on a local network through a configured TRÅDFRI gateway, including listing devices, checking status, setting brightness, and running confirmed whole-house or floor actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real smart lights on the local network, including group, floor, and whole-house actions. <br>
Mitigation: Confirm broad household actions unless the user clearly requested them, prefer the script's verification option for bulk actions, and report exact targets and status after changes. <br>
Risk: Gateway credentials are required for local device control and should not be published or shared. <br>
Mitigation: Keep real TRADFRI host, identity, and PSK values local in config.json or environment variables, and publish only placeholder credentials. <br>
Risk: The skill requires installing an npm dependency and does not include a lockfile. <br>
Mitigation: Review the npm dependency installation before use and install only in the intended skill environment. <br>


## Reference(s): <br>
- [TRÅDFRI setup notes](references/setup.md) <br>
- [ClawHub release page](https://clawhub.ai/ymebosma/tradfri-lights) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally reachable IKEA TRADFRI gateway, node-tradfri-client, and local gateway credentials.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
