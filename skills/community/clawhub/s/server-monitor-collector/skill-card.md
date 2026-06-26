## Description: <br>
Collect server monitoring data from Zabbix, Prometheus, Alibaba Cloud, Tencent Cloud, and Huawei Cloud, generate CSV/XLSX reports, and send them by email or Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to configure and run monitoring collectors for server and cloud VM health reports. It supports manual checks and scheduled daily reports with optional email or Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses monitoring, cloud API, SMTP, and notification credentials. <br>
Mitigation: Use least-privilege credentials, protect the .env file, and install only where infrastructure metric collection is approved. <br>
Risk: Generated reports may contain hostnames, IP addresses, utilization data, and operational alerts. <br>
Mitigation: Verify SMTP_HOST, TARGET_EMAIL, and FEISHU_CHAT_ID before scheduling or sending reports outside the intended audience. <br>
Risk: Scheduled runs can repeatedly collect and store infrastructure metrics. <br>
Mitigation: Run the skill only in approved monitoring environments and restrict access to generated CSV/XLSX report files. <br>


## Reference(s): <br>
- [Server Monitor Collector ClawHub Page](https://clawhub.ai/freepengyang/server-monitor-collector) <br>
- [Zabbix Configuration](references/zabbix-config.md) <br>
- [Cloud Provider Monitoring Configuration](references/cloud-config.md) <br>
- [Feishu and Email Notification Configuration](references/notification-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash commands, Python scripts, environment configuration examples, and CSV/XLSX report outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When run, the scripts use configured environment variables and write monitoring reports under the Hermes cron output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
