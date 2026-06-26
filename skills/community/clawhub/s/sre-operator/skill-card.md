## Description: <br>
Provides structured server operations workflows for system identification, safety checks, command validation, troubleshooting, performance monitoring, and log analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoanCo](https://clawhub.ai/user/zuoanCo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
System administrators, SREs, and operations engineers use this skill to diagnose server health, evaluate risky commands, plan maintenance, and troubleshoot performance, disk, process, network, log, and package-management issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server operations guidance may involve privileged, destructive, or service-impacting commands. <br>
Mitigation: Manually review service, package, firewall, DNS, deletion, truncation, and privileged commands before execution; confirm the target host, backup state, and rollback plan. <br>
Risk: Diagnostic outputs and logs can expose sensitive host, service, network, or application details. <br>
Mitigation: Redact sensitive logs and environment details before sharing outputs, and prefer read-only diagnostics unless the operator explicitly approves a change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuoanCo/sre-operator) <br>
- [Linux command reference and risk guide](references/linux-commands.md) <br>
- [Safety checklist](references/safety-checklist.md) <br>
- [Troubleshooting guide](references/troubleshooting-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON from the diagnostic script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference a read-oriented diagnostic shell script that can emit text or JSON system snapshots.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
