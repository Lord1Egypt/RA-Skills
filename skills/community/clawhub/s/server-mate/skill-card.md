## Description: <br>
Build or extend a lightweight server monitoring and AI operations workflow for Linux hosts running Nginx or Apache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use Server Mate to build or extend Linux server monitoring workflows for Nginx or Apache hosts, including metric collection, log parsing, alerting, PDF reporting, natural-language operations answers, and guarded remediation plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads web server logs, authentication logs, and host metrics, then stores operational rollups and audit history locally. <br>
Mitigation: Restrict access to config.yaml, metrics.db, logs, reports, and any exported report directory; review retention and exposure settings before using public report URLs. <br>
Risk: Optional auto-ban and auto-heal features may run firewall or service restart commands when enabled. <br>
Mitigation: Keep automation.dry_run=true and leave auto_ban and auto_heal disabled until command templates, allowlists, cooldowns, TTLs, audit destinations, and rollback plans have been reviewed. <br>
Risk: Optional integrations can send data to configured webhooks, Telegram, OpenAI-compatible endpoints, and GeoIP download sources. <br>
Mitigation: Enable only required integrations, keep webhook URLs and tokens out of committed files, prefer local MaxMind GeoIP.conf with geoipupdate, and review any public mirror fallback before allowing that network path. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Data contracts](references/data-contracts.md) <br>
- [Ops playbook](references/ops-playbook.md) <br>
- [SQLite schema](references/sqlite-schema.md) <br>
- [Server Mate ClawHub listing](https://clawhub.ai/tankeito/server-mate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, Python, shell command, cron, and systemd examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local configuration paths, SQLite schema guidance, webhook payload designs, monitoring reports, and guarded automation recommendations.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
