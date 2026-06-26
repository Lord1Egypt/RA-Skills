## Description: <br>
Vmware Monitor helps agents query VMware vCenter or ESXi inventory, alarms, events, host health, and VM details through read-only CLI or MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to let an agent inspect VMware vCenter or ESXi inventory, alarms, events, host health, and VM details before planning changes or escalating to companion VMware skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose VMware infrastructure state to an agent. <br>
Mitigation: Review the upstream package before installing, configure a read-only VMware account, and limit access to intended vCenter or ESXi targets. <br>
Risk: Local configuration and .env files can contain sensitive VMware connection details. <br>
Mitigation: Protect local config files, use restrictive file permissions, and prefer environment or secret-manager injection for passwords where possible. <br>
Risk: Optional daemon notifications can send monitoring summaries outside the local environment. <br>
Mitigation: Enable the daemon and webhook URLs only for endpoints you control and keep notifications disabled unless they are required. <br>


## Reference(s): <br>
- [VMware Monitor source repository](https://github.com/zw008/VMware-Monitor) <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-monitor) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Investigation Protocol](references/investigation-protocol.md) <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text with CLI/MCP command suggestions and JSON-like tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only VMware/vSphere monitoring outputs; optional daemon notifications use user-configured webhooks.] <br>

## Skill Version(s): <br>
1.6.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
