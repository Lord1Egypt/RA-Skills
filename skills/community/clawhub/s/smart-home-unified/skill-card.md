## Description: <br>
Helps agents configure and use smart-home command workflows for device discovery, status checks, device control, and scene-related operations across Xiaomi Mi Home and Apple HomeKit environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Smart-home users and automation developers use this skill to set up local device credentials, run smart-home CLI commands, and manage common device-control workflows from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to place Xiaomi passwords, Apple credentials, HomeKit PINs, and device tokens in local configuration. <br>
Mitigation: Use scoped tokens where possible, prefer a secret manager over plaintext files, avoid sharing configuration files, and install only when the publisher is trusted. <br>
Risk: Commands may control physical smart-home devices. <br>
Mitigation: Require manual confirmation before actions that affect device state, especially lights, plugs, thermostats, locks, alarms, or automation scenes. <br>
Risk: The security review says advertised HomeKit, AI, security, and multi-platform capabilities are not fully proven by the artifacts. <br>
Mitigation: Validate supported platforms and commands in a test environment before relying on the skill for real home automation. <br>


## Reference(s): <br>
- [Smart Home Unified ClawHub page](https://clawhub.ai/lvjunjie-byte/smart-home-unified) <br>
- [miio library documentation](https://github.com/aholstenson/miio) <br>
- [HAP-NodeJS documentation](https://github.com/homebridge/HAP-NodeJS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require local network access to devices and user-supplied smart-home credentials or device tokens.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
