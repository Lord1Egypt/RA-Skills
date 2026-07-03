## Description: <br>
Guides users through smart-home planning, device selection, automation design, platform comparison, and configuration for Home Assistant, Mijia/Xiaomi, and Apple HomeKit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soullhcn](https://clawhub.ai/user/soullhcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homeowners, smart-home hobbyists, and agents assisting them use this skill to plan device layouts, compare Home Assistant, Mijia/Xiaomi, and HomeKit, design automation scenes, and produce setup guidance or configuration snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence real smart-home devices, including sensitive automations for locks, cameras, alarms, and occupancy behavior. <br>
Mitigation: Review every generated automation before enabling it, test with noncritical devices first, require explicit confirmation for sensitive devices, and keep manual override and fail-safe behavior visible. <br>
Risk: Setup flows may involve smart-home credentials, long-lived tokens, and Homebridge access details. <br>
Mitigation: Avoid storing long-lived tokens in plaintext, rotate default credentials, prefer HTTPS or local-only access, and grant only the minimum access needed. <br>
Risk: Install scripts and background automation runners can modify the local environment and run continuously. <br>
Mitigation: Inspect scripts before running them, avoid remote install commands with elevated privileges unless independently verified, and run automation services with limited permissions and logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soullhcn/skills/smart-home-planner) <br>
- [Homebridge](https://homebridge.io) <br>
- [homebridge-mcp-server](https://github.com/mp-consulting/homebridge-mcp-server) <br>
- [mijia-api](https://github.com/Do1e/mijia-api) <br>
- [Local Automation Guide](knowledge/automation-guide.md) <br>
- [Platform Knowledge Base](knowledge/platforms.md) <br>
- [Plan Template](templates/plan-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, YAML snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated CNY prices, compatibility warnings, and user-confirmed automation plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
