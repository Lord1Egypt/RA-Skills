## Description:

Display comprehensive system hardware and software information for diagnostics, inventory, and system profiling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and system administrators use this skill to collect local machine diagnostics such as CPU, memory, disk, operating system, uptime, network interface, and process information for troubleshooting or inventory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default and JSON reports can include full process command lines, which may expose tokens, passwords, internal paths, customer data, or other sensitive local details.

Mitigation: Use --brief or section-specific flags such as --cpu, --memory, --disk, or --network when full process details are not needed, and review output before sharing it in logs, support bundles, CI, or agent transcripts.

Risk: System diagnostics can reveal hostnames, operating system details, disk layout, uptime, and network interface data.

Mitigation: Run the skill only in contexts where local inventory disclosure is acceptable, and redact environment-specific details before sending results outside the trusted audience.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/sysinfo-tool)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON diagnostic output, with Markdown shell examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default and JSON reports include top process command lines unless brief or section-specific options are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
