## Description: <br>
Controls Xiaomi Home devices on a local network using miiocli, including status checks, power toggles, and MIOT property changes for supported appliances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pegasus02](https://clawhub.ai/user/Pegasus02) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and advanced smart-home users use this skill to turn natural-language device requests into miiocli commands, token extraction steps, and local device inventory guidance for Xiaomi Home devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a private device-token inventory and the security summary says Xiaomi account credentials and device-control tokens are handled too loosely. <br>
Mitigation: Review before installing, remove any published token inventories, and rotate exposed Xiaomi device tokens. <br>
Risk: The bundled token extractor accepts Xiaomi account credentials and can receive a password through command-line arguments. <br>
Mitigation: Prefer interactive credential entry, avoid passing account passwords on the command line, and keep debug logging disabled. <br>
Risk: The skill can generate commands that change the state of smart plugs, cameras, routers, appliances, and other physical devices. <br>
Mitigation: Require explicit user confirmation before executing commands that power, configure, or otherwise change connected devices. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Pegasus02/xiaomi-home) <br>
- [Device inventory template](references/devices.md) <br>
- [Token extractor script](scripts/token_extractor.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and device-control examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that operate physical devices and references to local device tokens supplied by the user.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
