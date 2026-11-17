## Description:

Helps users plan smart-home systems, compare Home Assistant, Mijia/Xiaomi, and Apple HomeKit, and produce device, automation, purchase, and configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soullhcn](https://clawhub.ai/user/soullhcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home maintainers use this skill to plan device layouts, compare platforms, design automation scenes, generate purchase phases, and receive setup guidance for Home Assistant, Mijia/Xiaomi, and Apple HomeKit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart-home credentials and tokens may be stored or used by setup and automation flows.

Mitigation: Use dedicated low-privilege accounts, protect or delete token/profile files, avoid default admin credentials, and avoid LAN HTTP where possible.

Risk: Local automation can control locks, alarms, cameras, climate, plugs, and other safety-sensitive devices.

Mitigation: Require explicit manual confirmation, keep manual override paths, and use fail-safe defaults before enabling or running sensitive automations.

Risk: Setup scripts can install dependencies and enable local automation behavior on an always-on host.

Mitigation: Review and pin dependencies before running setup scripts, run on an isolated host, and disable Homebridge MCP admin tools unless they are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soullhcn/skills/smart-home-planner)
- [Mijia API Guide](artifact/knowledge/mijia-api-guide.md)
- [HomeKit Guide](artifact/knowledge/homekit-guide.md)
- [Automation Guide](artifact/knowledge/automation-guide.md)
- [Platform Reference](artifact/knowledge/platforms.md)
- [mijia-api](https://github.com/Do1e/mijia-api)
- [homebridge-mcp-server](https://github.com/mp-consulting/homebridge-mcp-server)
- [Homebridge](https://homebridge.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, YAML/configuration snippets, Python examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write profile or automation configuration files under user configuration paths when the user opts in; optional local automation setup can install dependencies and run a polling engine.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
