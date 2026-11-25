## Description:

Provides Windows server operations guidance for diagnostics, monitoring, security and compliance audits, and selected maintenance tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Windows administrators and IT operators use the skill to investigate server health and security, monitor services and performance, review compliance, and carry out selected maintenance tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security assessment reports privileged persistent tasks, unsafe command and cleanup paths, and undeclared update behavior; inspection was partial.

Mitigation: Review task installation, command execution, cleanup, and update behavior before installation, and ensure you can control the privileges the skill would use.

## Reference(s):

- [Winskill 3.5.0 on ClawHub](https://clawhub.ai/fyniujin/skills/winskill)
- [Docker Engine installation on Windows Server](https://docs.docker.com/engine/install/windows-server/)
- [Install kubectl on Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
- [Automated repair workflow](references/modules/module-27-自动化修复向导.md)
- [Monitoring suite](references/modules/module-35-监控套件.md)
- [Compliance runner](references/modules/module-37-合规体检runner.md)
- [Monitoring configuration](references/monitor-config.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown reports, HTML and CSV reports]

**Output Format:** [Natural-language guidance, PowerShell command examples, configuration files, and HTML or CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some maintenance and monitoring operations require administrator privileges and explicit confirmation.]

## Skill Version(s):

3.5.0 (source: artifact SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
