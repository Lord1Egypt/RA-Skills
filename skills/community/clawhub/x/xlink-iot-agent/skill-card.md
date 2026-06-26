## Description: <br>
Xlink IoT Agent - Query IoT devices and events via Xlink Gateway API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xlink-iot](https://clawhub.ai/user/xlink-iot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and IoT operations teams use this skill to query XLink device status, device lists, event instances, alert statistics, and supported device-control operations through the XLink Gateway API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send live IoT device-control commands. <br>
Mitigation: Use least-privilege or read-only XLink credentials where possible, restrict credentials to approved devices and services, and require external human approval before running device-control commands. <br>
Risk: Production IoT environments may be affected by mis-scoped queries or commands. <br>
Mitigation: Review commands before execution, test with non-production credentials or the TEST stage when available, and monitor XLink API usage for anomalies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xlink-iot/xlink-iot-agent) <br>
- [API authentication](references/api-auth.md) <br>
- [API documentation](references/api-doc.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Response schema](references/response-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XLINK_APP_ID, XLINK_APP_SECRET, and XLINK_API_GROUP environment variables; XLINK_BASE_URL defaults to https://api-gw.xlink.cn.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
