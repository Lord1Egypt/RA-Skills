## Description:

srv-guard helps administrators inspect Linux server configuration and logs, review security findings, plan or apply selected hardening actions, monitor attack indicators, and create security reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmccadmin12](https://clawhub.ai/user/cmccadmin12)

### License/Terms of Use:

MIT-0

## Use Case:

System administrators and developers use the skill to assess and harden Linux servers they are authorized to manage, review attack-related log events, and prepare security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags the test harness for potentially weakening live SSH settings and leaving an existing root private key with unsafe permissions; one referenced script was only partially analyzed.

Mitigation: Run the test harness only on a disposable VM or recoverable snapshot, protect existing SSH keys and configuration, and review the unanalyzed script before use.

Risk: Repair and defense actions can change server configuration, firewall rules, or kernel settings and may disrupt access or traffic.

Mitigation: Use the dry-run preview, confirm the target and proposed changes, keep backups and rollback commands, and apply changes only to authorized systems.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cmccadmin12/skills/srv-guard)
- [Scan checklist](references/scan-checklist.md)
- [Fix playbook](references/fix-playbook.md)
- [Attack signatures](references/attack-signatures.md)
- [Defense strategies](references/defense-strategies.md)
- [Linux test notes and scope](tests/README.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML reports, Shell commands, Configuration guidance]

**Output Format:** [JSON scan, repair, monitoring, and defense results; HTML security reports; and shell commands or remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repair and defense default to dry-run; selected changes require explicit application and review.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
