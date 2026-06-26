## Description: <br>
Use this skill when working with the Zhihu AIOps / 智护运维平台, including asset management, CMDB discovery, monitoring, alarm dashboards, Categraf SNMP metrics in VictoriaMetrics, managed asset inspection reports, and adding OS monitoring assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckypig1209](https://clawhub.ai/user/luckypig1209) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AIOps operators, platform administrators, and infrastructure engineers use this skill to query Zhihu AIOps assets, CMDB discovery results, monitoring data, alarm dashboards, VictoriaMetrics SNMP metrics, and managed asset inspection reports. It also guides adding operating-system monitoring assets after credentialed connectivity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflows require Zhihu platform credentials, an OAuth-style access token, and sometimes SSH credentials for monitored hosts. <br>
Mitigation: Use least-privilege platform and SSH accounts, keep credentials in environment variables or a secret store, and avoid pasting secrets into chat unless necessary. <br>
Risk: Configured AIOps and VictoriaMetrics endpoints may expose operational infrastructure data or accept privileged changes. <br>
Mitigation: Install only for trusted Zhihu AIOps environments, prefer HTTPS or protected internal network access, and review generated API calls before execution. <br>
Risk: OS monitor creation can submit SSH passwords to the configured backend. <br>
Mitigation: Confirm how the backend stores SSH passwords before use and prefer dedicated, least-privilege monitoring accounts over root or administrator accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckypig1209/zhihu-aiops) <br>
- [Publisher profile](https://clawhub.ai/user/luckypig1209) <br>
- [Asset center APIs](references/api_asset.md) <br>
- [CMDB discovery APIs](references/api_cmdb.md) <br>
- [Dashboard and alarm summary APIs](references/api_dashboard.md) <br>
- [Monitor center APIs](references/api_monitor.md) <br>
- [VictoriaMetrics APIs](references/api_victoriametrics.md) <br>
- [Categraf SNMP metrics](references/api_snmp_metrics.md) <br>
- [Add OS monitoring workflow](references/add-os-monitor.md) <br>
- [Managed asset inspection workflow](references/inspection-run.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request details and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-first skill; produces reference-guided workflows and example API calls rather than packaged executable CLI helpers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
