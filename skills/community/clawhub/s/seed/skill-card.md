## Description: <br>
Grow firmware on any hardware through HTTP: upload C, compile on device, and apply with watchdog rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Awis13](https://clawhub.ai/user/Awis13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device administrators use this skill to connect an agent to an authorized seed node, inspect hardware capabilities, write C firmware, compile it on the device, and apply updates with rollback checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent remote firmware-control authority over a live device. <br>
Mitigation: Install only on devices you own or are authorized to administer, review generated firmware before applying it, and test on non-critical hardware first. <br>
Risk: Bearer-token exposure could allow unauthorized access to firmware-control endpoints. <br>
Mitigation: Keep the node on a trusted network, protect the token, rotate it when needed, and avoid sharing it in logs or untrusted channels. <br>
Risk: Downloaded source or firmware changes may not match the user's safety expectations. <br>
Mitigation: Verify the downloaded source and inspect generated C code before compiling or applying it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Awis13/seed) <br>
- [Seed project homepage](https://github.com/Awis13/seed) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with C snippets, JSON examples, and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for authorized seed nodes and may include firmware source changes, HTTP API calls, and deployment checks.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
