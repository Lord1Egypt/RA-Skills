## Description: <br>
Add HTTP OTA (Over-The-Air) firmware update capability to Unihiker K10 Arduino projects, including AP/STA projects and ESP-NOW projects that need a safe OTA maintenance mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockets-cn](https://clawhub.ai/user/rockets-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add HTTP firmware update workflows to Unihiker K10 Arduino projects, including projects that need AP/STA networking or an ESP-NOW maintenance mode instead of USB updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTP OTA examples can expose firmware flashing to anyone who can reach the device endpoint if access control is not added. <br>
Mitigation: Use only on trusted isolated networks or add a unique per-device credential or token, a short-lived physical maintenance mode, and firmware signature or hash verification before deployment. <br>
Risk: The examples include a default AP credential, which can make unauthorized access easier if copied unchanged. <br>
Mitigation: Replace default AP credentials such as 12345678 with deployment-specific credentials and disable OTA mode when maintenance is complete. <br>


## Reference(s): <br>
- [K10 HTTP OTA Implementation Guide](references/ota-implementation.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rockets-cn/unihiker-k10-ota) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with code blocks and helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Arduino CLI commands, C++ firmware snippets, partition table guidance, and Python or PowerShell OTA upload helpers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
