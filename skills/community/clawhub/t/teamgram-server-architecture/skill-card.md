## Description: <br>
Teamgram Server architecture guide for designing Telegram-compatible backends, service topology, MTProto services, self-hosted deployment, data flow, and development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand Teamgram Server architecture, plan service topology and refactoring, and draft deployment or service-development steps for Telegram-compatible backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sample deployment credentials or weak defaults may be copied into production. <br>
Mitigation: Replace sample passwords and inject secrets through a managed secret store or environment-specific secret mechanism before deployment. <br>
Risk: Example service ports or database access patterns may expose infrastructure if used unchanged. <br>
Mitigation: Restrict exposed ports, avoid root database credentials where possible, and review the final network and database configuration before use. <br>
Risk: Unpinned container image versions and unsecured backups can make deployments harder to audit or recover safely. <br>
Mitigation: Pin container image versions, secure backups, and validate the deployment against official Teamgram and infrastructure security guidance. <br>


## Reference(s): <br>
- [Teamgram Server repository](https://github.com/teamgram/teamgram-server) <br>
- [Teamgram Server DeepWiki](https://deepwiki.com/teamgram/teamgram-server) <br>
- [Deployment Guide](references/deployment.md) <br>
- [Service Development Guide](references/service-development.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with architecture diagrams, tables, YAML examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; does not execute commands or modify files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
