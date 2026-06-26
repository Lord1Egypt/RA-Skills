## Description: <br>
智能公元 IoT 设备控制插件。可控制灯光、加湿器、窗帘等设备，支持查询设备状态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namishisu](https://clawhub.ai/user/namishisu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and control SmartPi IoT devices from an agent environment with curl-based commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using this skill can send credentialed requests that change real SmartPi device states. <br>
Mitigation: Use it only with a trusted SmartPi/aimachip service account and require explicit confirmation before commands that turn devices on or off, change brightness, start the humidifier, or open curtains. <br>
Risk: The skill depends on an API token and device key for SmartPi device access. <br>
Mitigation: Store SMARTPI_TOKEN and SMARTPI_DEVICE_KEY in configuration or environment variables rather than prompts, command history, or version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/namishisu/smartpi-iot) <br>
- [SmartPi official website](https://smartpi.cn/) <br>
- [SmartPi API base endpoint](https://mcp.aimachip.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples, environment variable setup, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus SMARTPI_TOKEN and SMARTPI_DEVICE_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
