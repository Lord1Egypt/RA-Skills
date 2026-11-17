## Description:

Provides structured server operations workflows for system identification, safety checks, command validation, troubleshooting, performance monitoring, and log analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoanco](https://clawhub.ai/user/zuoanco)

### License/Terms of Use:


## Use Case:

System administrators, SREs, and operations engineers use this skill to perform server diagnostics, maintenance planning, troubleshooting, log analysis, and performance checks while validating commands before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting recipes include direct remediation commands that can change services, firewall rules, DNS, packages, permissions, or files on production systems.

Mitigation: Keep default use to read-only diagnostics; require explicit approval, verified paths and services, backups, rollback steps, and environment-specific command checks before any state-changing command.

Risk: System inventory output can expose operational details about hosts, processes, resources, and disks.

Mitigation: Store generated reports only in approved locations, review them for sensitive infrastructure details, and limit sharing to intended operators.

## Reference(s):

- [Linux command reference](references/linux-commands.md)
- [Safety checklist](references/safety-checklist.md)
- [Troubleshooting guide](references/troubleshooting-guide.md)
- [System analysis script](scripts/analyze-system.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON diagnostic output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or invoke read-only diagnostics first, then propose state-changing commands only after validation and user approval.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
