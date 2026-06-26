## Description: <br>
Helps agents manage Tencent Cloud Lighthouse instances with tccli, including instance operations, application deployment, monitoring, firewall rules, snapshots, traffic packages, and remote commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhanyun](https://clawhub.ai/user/lhanyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Tencent Cloud Lighthouse resources through tccli. It supports routine operations such as listing and creating instances, configuring firewall rules, checking monitoring data, running remote commands, and managing snapshots or traffic packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer real Tencent Cloud Lighthouse resources using powerful cloud credentials. <br>
Mitigation: Install only on trusted machines and confirm region, instance ID, cost-impacting actions, firewall CIDR ranges, snapshot or blueprint IDs, and remote command contents before modifying resources. <br>
Risk: OAuth codes, tokens, and long-lived access keys may expose cloud access if shared in chat or stored insecurely. <br>
Mitigation: Use temporary OAuth credentials when possible, keep codes and tokens out of chat, avoid unnecessary AK/SK use, and check local tccli credential file permissions. <br>
Risk: Remote command and firewall workflows can change instance behavior or network exposure immediately. <br>
Mitigation: Review existing state before changes, require explicit confirmation for modifying operations, and restrict firewall rules to necessary ports and trusted CIDR ranges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhanyun/tencentcloud-lighthouse-skill) <br>
- [Publisher profile](https://clawhub.ai/user/lhanyun) <br>
- [Instance management](references/instance-management.md) <br>
- [Application deployment](references/application-deployment.md) <br>
- [Monitoring and alerting](references/monitoring-alerting.md) <br>
- [Firewall management](references/firewall-management.md) <br>
- [Remote command with TAT](references/remote-command-tat.md) <br>
- [Snapshot and blueprint management](references/snapshot-blueprint.md) <br>
- [Traffic package management](references/traffic-package.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline and fenced shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tccli command proposals, confirmation prompts for modifying actions, and credential setup guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
