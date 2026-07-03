## Description: <br>
VMware Aria helps agents query VMware Aria Operations metrics, alerts, capacity forecasts, anomalies, reports, and platform health through CLI or MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, infrastructure engineers, and operations teams use this skill to inspect VMware Aria Operations environments, investigate alerts, plan capacity, detect anomalies, and generate operational reports. Write-capable actions such as alert cancellation, alert-definition changes, and report deletion should be explicitly approved before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive VMware Aria Operations data and credentials. <br>
Mitigation: Install only for agents that need this access, use least-privilege Aria accounts, protect ~/.vmware-aria/.env, and avoid storing passwords in config files. <br>
Risk: Some actions can change alert state, alert definitions, or generated reports. <br>
Mitigation: Require explicit approval before alert cancellation, alert-definition changes, report deletion, or any future auto-remediation behavior. <br>
Risk: Misconfigured TLS could expose Aria Operations traffic in production. <br>
Mitigation: Keep TLS verification enabled for production targets and limit disabled verification to controlled lab environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-aria) <br>
- [Project Homepage](https://github.com/zw008/VMware-Aria) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Investigation Protocol](references/investigation-protocol.md) <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, JSON summaries, and table-style operational findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI or MCP workflow steps, capacity and alert summaries, setup guidance, and explicit approval boundaries for write operations.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
