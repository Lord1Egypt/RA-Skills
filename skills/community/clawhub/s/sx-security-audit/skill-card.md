## Description: <br>
A local security audit skill that checks file permissions, environment variables, dependencies, configuration, network ports, Git settings, shell history, macOS security settings, and secrets, with CLI, JSON, configuration file, and Feishu report support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuxiaobao-y](https://clawhub.ai/user/zhuxiaobao-y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run targeted or full local security audits, review prioritized findings, and generate Markdown or JSON reports for remediation tracking or Feishu sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit inspects sensitive local configuration, environment, shell, Git, dependency, and network-port information. <br>
Mitigation: Run only the checks needed for the task, protect generated reports as confidential, and redact secrets or host details before sharing. <br>
Risk: Feishu delivery can send security findings outside the local machine. <br>
Mitigation: Use Feishu sending only after confirming the webhook or plugin destination and reviewing the report contents. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/zhuxiaobao-y/sx-security-audit) <br>
- [Permissions rules](references/permissions.md) <br>
- [Secrets detection rules](references/secrets-detection.md) <br>
- [Dependency audit guidance](references/dependency-audit.md) <br>
- [Code security best practices](references/code-security.md) <br>
- [NPM Advisory Database](https://github.com/npm/advisories) <br>
- [PyPI Security](https://pypi.org/security) <br>
- [CVE Database](https://cve.mitre.org/) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown reports, JSON reports, and Feishu message payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports selected check modules, severity filtering, quiet mode, output files, and optional Feishu delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
