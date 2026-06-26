## Description: <br>
Deprecated Cloud Zhi Lian IoT device management skill for reading soil temperature, soil humidity, and liquid-level data and sending remote valve control commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlkj](https://clawhub.ai/user/yzlkj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to query supported Cloud Zhi Lian IoT sensors and control supported remote water valves through natural-language requests or explicit shell commands. The release is deprecated and directs users to migrate to YZL-AIoT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actuate remote water valves from loose natural-language or generic commands without an evident confirmation step. <br>
Mitigation: Use it only where the YZL API key is intentionally allowed to control the target devices, avoid unattended automation, and require explicit operator review before valve commands. <br>
Risk: Valve commands are real-world physical actions and may affect connected equipment or environments. <br>
Mitigation: Test with noncritical devices first and prefer manual commands or a replacement skill with confirmations and tighter command scoping. <br>
Risk: The skill requires a sensitive YZLIOT_API_KEY credential. <br>
Mitigation: Store the key only in the intended runtime environment and avoid exposing it to broad or ambiguous agent workflows. <br>
Risk: The release is deprecated and no longer maintained. <br>
Mitigation: Plan migration to YZL-AIoT for ongoing support before relying on this skill in normal operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzlkj/yzl-iot-api) <br>
- [Publisher profile](https://clawhub.ai/user/yzlkj) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the YZLIOT_API_KEY environment variable; may perform real IoT device queries and valve-control actions.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata, _meta.json, and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
