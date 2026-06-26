## Description: <br>
Creates, edits, validates, and manages KNX Gateway scenes and automation workflows through a REST API for device control and workflow lifecycle tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmpbin](https://clawhub.ai/user/tmpbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to author, validate, import, export, enable, and execute KNX Gateway scenes and automation workflows on a trusted LAN or VPN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through physical smart-home actions, including locks, doors, windows, scenes, workflows, and device control. <br>
Mitigation: Install only for a trusted KNX Gateway and require explicit confirmation before unlock, garage or window movement, scene execution, workflow enable or execute actions, deletes, or other high-impact changes. <br>
Risk: A KNX token gives access to the gateway API and could expose device control if mishandled. <br>
Mitigation: Keep KNX_TOKEN in a secret store or local environment variable, avoid pasting it into conversations, and never hardcode it in shared files or examples. <br>
Risk: Gateway access over local HTTP or off-LAN integrations can weaken transport and network boundaries. <br>
Mitigation: Restrict the gateway to a trusted LAN or VPN, prefer HTTPS or isolated networking where available, and review any HTTP, MQTT, email, or webhook destination before enabling it. <br>


## Reference(s): <br>
- [KNX Gateway Skills Homepage](https://github.com/tmpbin/knx-gateway-skills) <br>
- [Device Reference](ref/devices.md) <br>
- [Scene Reference](ref/scenes.md) <br>
- [Trigger Reference](ref/triggers.md) <br>
- [Node Reference](ref/nodes.md) <br>
- [API Reference](ref/api.md) <br>
- [Workflow Examples](ref/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, JSON, API calls] <br>
**Output Format:** [Markdown with REST endpoint guidance and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoints, request bodies, validation steps, and lifecycle guidance for a user-provided KNX Gateway.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
