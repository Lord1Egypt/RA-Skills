## Description: <br>
Control smart home devices configured in Smart Plus APP, including querying devices and scenes, turning devices on or off, adjusting air conditioners, and triggering smart scenes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagxin](https://clawhub.ai/user/kagxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent control Smart Plus smart-home devices and automation scenes through the MXCHIP MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent live control over real smart-home devices and scenes. <br>
Mitigation: Configure agent workflows to ask before turning devices on or off, changing HVAC settings, or triggering scenes, especially scenes that affect multiple devices. <br>
Risk: The OAuth token grants access to Smart Plus devices if exposed. <br>
Mitigation: Keep MXCHIP_OAUTH_TOKEN private, avoid committing it to source control, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [Mxchip Smart Control API Reference](references/api_reference.md) <br>
- [Mxchip MCP Client SDK](scripts/mxchip_mcp_client.py) <br>
- [MXCHIP Official Website](https://www.mxchip.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/kagxin/smart-control-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown documentation with Python and shell examples; Python client methods return JSON-like dictionaries from MCP API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MXCHIP_OAUTH_TOKEN and can control configured Smart Plus devices and scenes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata, skill.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
