## Description:

Controls Synology Surveillance Station cameras through the Web API for snapshots, live-stream URLs, recording control, PTZ movement, presets, and event log viewing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[photonixlaser-ux](https://clawhub.ai/user/photonixlaser-ux)

### License/Terms of Use:


## Use Case:

Developers, operators, and home-lab users use this skill to configure and run shell commands that interact with Synology Surveillance Station cameras. It is intended for camera inventory, snapshots, live-stream URL retrieval, recording controls, PTZ actions, presets, and event log review on a Synology NAS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials for a surveillance system and can expose camera access if those credentials are over-privileged or stored insecurely.

Mitigation: Use a dedicated least-privilege Surveillance Station account, avoid admin credentials, avoid storing the password in TOOLS.md, and protect any environment variables or shell history that contain credentials.

Risk: Camera commands can capture snapshots, start or stop recordings, move PTZ cameras, or activate presets, changing live surveillance behavior.

Mitigation: Review proposed commands before execution, restrict camera permissions to the required devices and operations, and run the skill only in environments where agent control of cameras is acceptable.

Risk: Unencrypted HTTP or disabled multi-factor authentication can increase exposure when connecting to a NAS API.

Mitigation: Require HTTPS where possible, keep 2FA enabled where compatible with the deployment, and isolate any API user that must operate without 2FA.

## Reference(s):

- [Synology Surveillance Station API Reference](references/api.md)
- [Synology Surveillance Station Web API Developer Guide](https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/SurveillanceStation/All/enu/SurveillanceStation_Web_API.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JPEG snapshot files when snapshot commands are executed.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
