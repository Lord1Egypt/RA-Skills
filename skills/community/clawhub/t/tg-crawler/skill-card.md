## Description:

TG-Crawler helps agents discover Telegram channels or groups, backfill or monitor messages, and export collected Telegram public-opinion data with retention cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhappy](https://clawhub.ai/user/zhappy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure and run Telegram channel discovery, historical message backfill, continuous monitoring, and export workflows for industry-specific public-opinion collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram credentials, session files, and 2FA secrets can expose an account if handled casually.

Mitigation: Use a dedicated Telegram account with scoped credentials, keep session files private, and avoid passing 2FA passwords on the command line.

Risk: Search terms and targets may be disclosed to Telegram search bots or unauthorized private channels.

Mitigation: Disable third-party bots for sensitive searches and use private invite-link targets only when authorization is clear.

Risk: Retention cleanup and purge options can remove collected data or media unexpectedly.

Mitigation: Review the configured database and media directory before enabling purge behavior or confirming cleanup operations.

Risk: Proxy setup guidance can create exposed infrastructure if reused without changes.

Mitigation: Use unique proxy credentials, restrict access with firewall rules, and review the proxy setup before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhappy/skills/tg-crawler)
- [Industry playbook](references/industry-playbook.md)
- [Proxy pool setup](references/proxy-pool-setup.md)
- [Targets format](references/targets-format.md)
- [TG crawler architecture](references/tg-crawler-architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus CSV, JSON, or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite data, media files, Telethon session files, and exported reports depending on the selected mode.]

## Skill Version(s):

3.12.0 (source: ClawHub release metadata; artifact changelog v3.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
