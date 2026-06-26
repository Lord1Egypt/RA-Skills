## Description: <br>
SearXNG Auto Proxy configures an adaptive proxy adapter that tests Clash availability, switches search engine routing, and performs periodic proxy-node optimization for SearXNG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengong101](https://clawhub.ai/user/pengong101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and self-hosted search operators use this skill to configure SearXNG with adaptive proxy rules, monitor engine reachability, and switch Clash proxy nodes for global and domestic search engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The adapter can run continuously and automatically change a shared Clash proxy route. <br>
Mitigation: Use a dedicated Clash instance or SearXNG-only proxy group, and keep the Clash API bound to a trusted local network. <br>
Risk: The startup flow can leave a nohup background process running after installation. <br>
Mitigation: Know how to stop the adapter process, review its log path, and confirm proxy settings can be reverted before deployment. <br>
Risk: External Docker or pip installation paths may introduce dependencies outside the reviewed artifact. <br>
Mitigation: Review the selected Docker image, pip package, and dependency versions before using those installation options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengong101/searxng-auto-proxy) <br>
- [Publisher profile](https://clawhub.ai/user/pengong101) <br>
- [README](artifact/README.md) <br>
- [Release notes](artifact/RELEASE-v3.0.0.md) <br>
- [Proxy rules](artifact/proxy-rules.yml) <br>
- [Final test report](artifact/FINAL-TEST-REPORT-v3.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python adapter code, YAML proxy rules, and operational status or log output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SearXNG and Clash; may start a persistent background adapter that writes logs and cache files and changes Clash proxy selection.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and clawhub.json; artifact/SKILL.md reports 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
