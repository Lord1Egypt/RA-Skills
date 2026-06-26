## Description: <br>
Controls Synology Surveillance Station cameras through the Web API for snapshots, live streams, recordings, PTZ movement, and event monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to control cameras on a Synology NAS with Surveillance Station, including listing cameras, creating snapshots, generating stream URLs, controlling recordings and PTZ movement, and reviewing events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent sensitive surveillance access, including snapshots, live streams, PTZ movement, recordings, and event logs. <br>
Mitigation: Review before installing and require explicit user approval before snapshots, live streams, PTZ movement, or recording changes. <br>
Risk: Credential and transport handling can expose Synology Surveillance credentials or camera data if configured insecurely. <br>
Mitigation: Use a dedicated least-privilege Synology Surveillance account, avoid admin credentials, do not store the password in TOOLS.md, and require HTTPS with a trusted certificate. <br>


## Reference(s): <br>
- [Synology Surveillance Station API Reference](references/api.md) <br>
- [Official Synology Surveillance Station Web API Guide](https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/SurveillanceStation/All/enu/SurveillanceStation_Web_API.pdf) <br>
- [ClawHub Release Page](https://clawhub.ai/photonixlaser-ux/synology-surveillance-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, command output text, URLs, and snapshot image files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Synology Surveillance Station access, jq, and configured Synology connection credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
