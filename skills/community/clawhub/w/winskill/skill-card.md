## Description:

A Windows server operations toolbox for disk diagnostics, system monitoring, security audits, maintenance, and remote administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Windows administrators and IT teams use this skill to inspect server health, diagnose incidents, prepare maintenance actions, and monitor multiple machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote administration can execute arbitrary commands on selected servers despite read-only claims.

Mitigation: Restrict access to trusted administrators and review commands and targets before using module 30.

Risk: Monitoring features can install long-lived, high-privilege scheduled tasks.

Mitigation: Before enabling modules 28 or 31, review task paths, run-as identity, permissions, duration, and cleanup.

## Reference(s):

- [Winskill ClawHub release](https://clawhub.ai/fyniujin/skills/winskill)
- [Disk health check](artifact/references/modules/module-34-磁盘体检.md)
- [Remote multi-server administration](artifact/references/modules/module-30-远程多服务器管理.md)
- [Scheduled monitoring](artifact/references/modules/module-31-轻量常驻监控.md)
- [Performance baselines and trends](artifact/references/modules/module-28-性能基线-&-趋势分析.md)
- [Monitoring thresholds](artifact/references/thresholds.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, PowerShell commands, Configuration guidance]

**Output Format:** [Markdown with PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide generation of local diagnostic reports, including HTML disk reports.]

## Skill Version(s):

3.4.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
