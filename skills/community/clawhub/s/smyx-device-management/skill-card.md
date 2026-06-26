## Description: <br>
Manages cloud-registered cameras and monitoring devices, including device list, add, update, delete, live stream link retrieval, status checks, configuration, PTZ control, and audio control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage cloud-registered surveillance and IoT devices from an agent workflow, including listing devices, registering cameras, changing camera metadata, deleting devices, retrieving playable live-stream links, and issuing PTZ or audio controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal playable live-stream links for cloud-registered cameras. <br>
Mitigation: Install only in trusted environments and restrict use to authorized operators who are allowed to access surveillance feeds. <br>
Risk: The skill can delete or modify registered devices and issue PTZ or audio controls. <br>
Mitigation: Require human review for destructive or remote-control actions, and verify the target camera serial number before execution. <br>
Risk: The skill handles account identifiers, reusable tokens, and local configuration data. <br>
Mitigation: Store credentials and open-id values in protected configuration, avoid exposing them in chat output, and rotate tokens if the workspace is shared. <br>
Risk: The release bundles health and face-analysis code that is not clearly part of the advertised device-management function. <br>
Mitigation: Review bundled files before deployment and remove or disable unrelated analysis code if the deployment scope is limited to device management. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-device-management) <br>
- [Device management skill instructions](artifact/SKILL.md) <br>
- [Face analysis API documentation bundled with release](artifact/skills/face_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with command examples, tables, JSON-like device data, and playable stream links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output cloud camera identifiers, device status, m3u8 live-stream URLs, and operation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
