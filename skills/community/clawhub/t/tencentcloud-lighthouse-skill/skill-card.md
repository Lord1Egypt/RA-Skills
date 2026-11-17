## Description:

Guides agents through Tencent Cloud Lighthouse administration with tccli, including instance lifecycle management, application deployment, firewall rules, monitoring, snapshots, traffic usage, and TAT remote commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhanyun](https://clawhub.ai/user/lhanyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Tencent Cloud Lighthouse resources through tccli, including provisioning, deployment checks, remote command execution, firewall changes, monitoring, snapshots, and traffic inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that use real Tencent Cloud credentials and can change billable cloud resources.

Mitigation: Use temporary OAuth credentials where possible, keep credential files restricted to the local user, and require explicit confirmation before mutating or billable actions.

Risk: Remote command execution and deployment steps can alter server state or run unpinned installation commands.

Mitigation: Review commands before execution, prefer pinned packages and images, and avoid the `curl | sudo bash` pattern unless the user accepts the risk.

Risk: Broad firewall rules such as `0.0.0.0/0` can unintentionally expose services.

Mitigation: Review existing rules first and use the narrowest CIDR and port range that satisfies the task.

## Reference(s):

- [Instance Management](references/instance-management.md)
- [Application Deployment](references/application-deployment.md)
- [Monitoring and Alerting](references/monitoring-alerting.md)
- [Firewall Management](references/firewall-management.md)
- [Remote Command TAT](references/remote-command-tat.md)
- [Snapshot and Blueprint](references/snapshot-blueprint.md)
- [Traffic Package](references/traffic-package.md)
- [Tencent Cloud OAuth Authorization](https://cloud.tencent.com/open/authorize)
- [Tencent Cloud CLI OAuth](https://cli.cloud.tencent.com/oauth)
- [Tencent Cloud CLI](https://cli.cloud.tencent.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tccli commands, confirmation prompts for mutating cloud actions, and code-block-wrapped command output guidance.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
