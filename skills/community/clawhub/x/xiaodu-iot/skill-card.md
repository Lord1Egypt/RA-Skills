## Description: <br>
Controls Xiaodu smart speakers and IoT devices, including device discovery, status checks, voice commands, broadcasts, scenes, and batch smart-home actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vividlife](https://clawhub.ai/user/vividlife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to configure Xiaodu/DuerOS MCP access, inspect available devices, and issue controlled commands to speakers, lights, curtains, switches, and scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real smart-home actions, broadcasts, scenes, and privacy-sensitive device capabilities. <br>
Mitigation: Require explicit confirmation before broadcasts, scenes, device control, or photo capture actions, and limit use to trusted Xiaodu/DuerOS integrations. <br>
Risk: Access tokens, CUIDs, client IDs, device names, and logs can expose account or home information. <br>
Mitigation: Store tokens and device IDs as secrets, avoid sharing terminal logs or screenshots, and rotate credentials when exposed. <br>
Risk: The IoT MCP configuration runs an unpinned npx package. <br>
Mitigation: Review and pin the package before use, and run it in a constrained environment with only the required token access. <br>
Risk: The device update script can persist device information into MEMORY.md. <br>
Mitigation: Disable or modify MEMORY.md updates before running update_devices.sh when persistent device records are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vividlife/xiaodu-iot) <br>
- [Xiaodu speaker MCP guide](artifact/references/xiaodu_mcp.md) <br>
- [IoT device control API guide](artifact/references/iot_api.md) <br>
- [Xiaodu DuerOS MCP endpoint](https://xiaodu.baidu.com/dueros_mcp_server/mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided DuerOS access tokens, device identifiers, and configured MCP servers before commands can affect devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
