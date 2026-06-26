## Description: <br>
Control and monitor Red Sea ReefBeat aquarium equipment over the local HTTP API without cloud access, covering lighting, dosing, filter rolls, pumps, top-off, and wave devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piwi3910](https://clawhub.ai/user/piwi3910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium keepers, automation operators, and developers use this skill to discover local Red Sea ReefBeat devices, inspect status, and prepare HTTP control commands for supported aquarium equipment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad unauthenticated control over local aquarium life-support equipment. <br>
Mitigation: Use read-only commands by default and manually confirm every POST, PUT, or DELETE operation before execution. <br>
Risk: Incorrect device IPs or payloads could affect the wrong device or change dosing, pump, top-off, firmware, or reset behavior. <br>
Mitigation: Verify the target device IP, endpoint, and JSON payload against current device status before making changes. <br>
Risk: Discovery actively probes hosts on a local subnet. <br>
Mitigation: Run discovery only on networks you own or administer, preferably with an explicit subnet. <br>


## Reference(s): <br>
- [ReefBeat API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/piwi3910/reefbeat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local HTTP endpoints, device IP placeholders, and JSON request bodies for GET, POST, PUT, and DELETE operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
