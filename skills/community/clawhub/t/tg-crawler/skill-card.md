## Description: <br>
Telegram 频道/群组舆情采集工具 v3.12，支持 hybrid、discover、backfill 和 monitor 四种模式，并内置数据保留策略以清理过期数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhappy](https://clawhub.ai/user/zhappy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, threat-intelligence analysts, brand-protection teams, and compliance teams use this skill for authorized Telegram channel discovery, historical message collection, monitoring, and export. It is intended for scoped public-channel collection where targets, credentials, proxies, retention, and exports are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a powerful Telegram collection tool with broad preset targets and monitoring behavior. <br>
Mitigation: Install and run it only for authorized threat-intelligence, brand-protection, or compliance work, and remove unrelated preset targets before collection. <br>
Risk: Bot-based discovery can send search keywords to third-party Telegram bots. <br>
Mitigation: Disable bot discovery with the skill's no-bot option unless the operator accepts that disclosure. <br>
Risk: Proxy-pool guidance can affect network posture and traffic routing. <br>
Mitigation: Use the proxy-pool setup only after review by a network or security owner. <br>
Risk: Telegram credentials, session files, databases, media, and export files can contain sensitive data. <br>
Mitigation: Protect .env, session, database, media, and export files, and confirm retention or purge settings before running collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhappy/tg-crawler) <br>
- [Industry playbook](references/industry-playbook.md) <br>
- [Proxy pool setup](references/proxy-pool-setup.md) <br>
- [Targets format](references/targets-format.md) <br>
- [TG-Crawler architecture](references/tg-crawler-architecture.md) <br>
- [Telegram API application portal](https://my.telegram.org/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command snippets, Python scripts, YAML configuration, and CSV/JSON/Markdown export data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces collection workflows that may create SQLite databases, session files, media files, and export files when run.] <br>

## Skill Version(s): <br>
3.12.0 (source: server release evidence, SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
