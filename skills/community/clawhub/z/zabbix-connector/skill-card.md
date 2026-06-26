## Description: <br>
Skill for Zabbix API monitoring and interaction. Use it to check active alerts, list problems, manage hosts, and query monitoring data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and engineers use this skill to query Zabbix monitoring data, review active alerts and problems, inspect hosts and metrics, and acknowledge events when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zabbix API token and can expose monitoring data if credentials are over-permissive or mishandled. <br>
Mitigation: Use a least-privilege token, keep the .env file private, and use HTTPS for ZABBIX_URL. <br>
Risk: The skill can acknowledge Zabbix events, which may change operational incident state. <br>
Mitigation: Require explicit confirmation and verify the target host or event before acknowledging any event or problem. <br>


## Reference(s): <br>
- [Zabbix References](references/guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rickkbarbosa/zabbix-connector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries, JSON API results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZABBIX_URL and ZABBIX_TOKEN from a local .env file when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: release.json and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
