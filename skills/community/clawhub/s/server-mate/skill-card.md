## Description: <br>
Builds and extends a lightweight server monitoring and AI operations workflow for Linux hosts running Nginx or Apache, with optional centralized remote monitoring through the BT-Panel HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to add Linux web-server monitoring, log analysis, alerting, reporting, AI-assisted diagnosis, and guarded remediation workflows for Nginx or Apache environments. It can support local log collection or centralized agentless collection through BT-Panel when operators provide panel credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read web-server logs, authentication logs, host metrics, and IP-related rollups. <br>
Mitigation: Deploy it only where operators are authorized to process operational telemetry, and avoid exposing generated reports without authentication. <br>
Risk: Alert diagnostics and guarded remediation can run shell commands or service/firewall actions on monitored hosts. <br>
Mitigation: Keep automation disabled or in dry-run mode until command templates, allowlists, cooldowns, audit destinations, and operator approval are in place. <br>
Risk: Webhook, Telegram, AI-analysis, MaxMind, and BT-Panel integrations can send data or credentials to external services. <br>
Mitigation: Disable integrations that are not needed, store credentials only in environment variables or local secret files, and review webhook/report payloads before production use. <br>
Risk: BT-Panel API keys can grant broad panel privileges. <br>
Mitigation: Inject BT-Panel keys through environment variables, keep config files out of version control, restrict file permissions, and rotate keys if plaintext exposure occurs. <br>


## Reference(s): <br>
- [Server Mate on ClawHub](https://clawhub.ai/tankeito/skills/server-mate) <br>
- [Architecture](references/architecture.md) <br>
- [Data Contracts](references/data-contracts.md) <br>
- [Ops Playbook](references/ops-playbook.md) <br>
- [SQLite Schema](references/sqlite-schema.md) <br>
- [User Guide](user-guide.md) <br>
- [Example Configuration](config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or modify local configuration, SQLite-backed monitoring artifacts, logs, reports, webhook payloads, and Python monitoring scripts in the skill workspace.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
