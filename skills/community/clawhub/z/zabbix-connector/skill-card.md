## Description:

Skill for Zabbix API monitoring and interaction. Use it to check active alerts, list problems, manage hosts, and query monitoring data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to query Zabbix monitoring data, inspect active problems, list hosts and items, review history, and acknowledge events when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Zabbix API token and may send it to a configured endpoint that is not HTTPS.

Mitigation: Configure only an HTTPS Zabbix endpoint you control and use a dedicated least-privilege Zabbix token.

Risk: Credential files can expose Zabbix access if shared or packaged.

Mitigation: Keep the .env file out of release packages and avoid putting unrelated secrets in the skill .env file.

Risk: Event acknowledgement can change Zabbix operational state.

Mitigation: Reserve acknowledgement permissions for users who need them and confirm the target host or event before acknowledging.

## Reference(s):

- [Zabbix References](references/guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text, optionally including JSON returned from Zabbix API queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured ZABBIX_URL and ZABBIX_TOKEN for live Zabbix API queries.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact/release.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
