## Description:

Server-Mate helps agents build or extend lightweight Linux server monitoring and AI operations workflows for Nginx or Apache hosts, including local and BT-Panel-based remote log collection, metrics, alerts, reports, and guarded remediation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and server operators use this skill to add observability, alerting, report generation, natural-language diagnostics, and guarded automation to Linux web hosts without replacing their existing Nginx, Apache, or BT-Panel setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap or daemon setup may create persistent root-level services.

Mitigation: Review bootstrap and service configuration before installation, prefer pinned releases or commits, and run the agent under a dedicated low-privilege user where possible.

Risk: Guarded automation can run firewall bans or service restarts when enabled.

Mitigation: Keep automation in dry-run until command templates, allowlists, cooldowns, TTLs, and audit destinations have been reviewed and approved.

Risk: BT-Panel API keys, webhook URLs, Telegram tokens, OpenAI API keys, and GeoIP credentials can grant sensitive access or leak data.

Mitigation: Inject secrets through environment variables or a secrets manager, keep config files containing credentials out of version control, and rotate any exposed keys before production use.

Risk: The built-in dashboard can expose operational metrics and controls if reachable without protection.

Mitigation: Expose the dashboard only behind authentication and TLS, preferably through a reviewed reverse proxy configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tankeito/skills/server-mate)
- [Architecture](references/architecture.md)
- [Data Contracts](references/data-contracts.md)
- [Ops Playbook](references/ops-playbook.md)
- [SQLite Schema](references/sqlite-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, JSON payloads, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include implementation guidance for Python collectors, SQLite rollups, webhook payloads, reports, dashboard setup, and guarded automation policies.]

## Skill Version(s):

1.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
