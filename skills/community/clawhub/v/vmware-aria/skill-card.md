## Description: <br>
Provides VMware Aria Operations monitoring assistance for querying metrics, alerts, capacity forecasts, anomalies, and automated reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operations teams use this skill to inspect VMware Aria Operations resources, investigate alerts and anomalies, plan capacity, and generate operational reports through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses VMware Aria Operations credentials and local configuration files. <br>
Mitigation: Use authorized targets only, prefer read-only credentials, protect ~/.vmware-aria/.env, or use a secret manager. <br>
Risk: Alert and report write actions can acknowledge or cancel alerts, change alert definitions, generate reports, or delete reports. <br>
Mitigation: Require explicit confirmation before write actions and review the intended target and operation before execution. <br>
Risk: Disabling TLS verification in production can weaken connection security. <br>
Mitigation: Keep TLS verification enabled for production Aria Operations targets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-aria) <br>
- [Project Homepage](https://github.com/zw008/VMware-Aria) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Investigation Protocol](references/investigation-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, CLI/MCP guidance, and operational report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide CLI or MCP calls against authorized VMware Aria Operations targets; write actions should require explicit confirmation.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
