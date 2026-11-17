## Description:

Collect server monitoring data (Zabbix / Prometheus / Alibaba / Tencent / Huawei Cloud), generate CSV/XLSX reports and send via email or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure and run monitoring collectors for Zabbix, Prometheus, and cloud VM providers, then generate CSV/XLSX reports and optional Feishu or email summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses infrastructure and cloud credentials for monitoring collection.

Mitigation: Install only in controlled monitoring environments and use read-only or narrowly scoped Zabbix and cloud credentials.

Risk: Monitoring reports can be sent automatically by email or Feishu.

Mitigation: Restrict SMTP recipients and Feishu destinations, and review one-time report output before enabling a daily cron schedule.

Risk: Zabbix collection may use insecure transport if configured with non-HTTPS endpoints.

Mitigation: Require HTTPS for Zabbix API URLs and keep credentials in the configured environment file rather than in scripts or prompts.

Risk: Generated spreadsheets and unpinned runtime dependencies need deployment review.

Mitigation: Prefer a release with spreadsheet sanitization and pinned dependencies before broad production deployment.

## Reference(s):

- [Server Monitor Collector on ClawHub](https://clawhub.ai/freepengyang/skills/server-monitor-collector)
- [Zabbix Configuration](references/zabbix-config.md)
- [Cloud Provider Configuration](references/cloud-config.md)
- [Notification Configuration](references/notification-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated CSV/XLSX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce monitoring summaries for Feishu or email and report files under the configured Hermes output directory.]

## Skill Version(s):

1.0.2 (source: server evidence release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
