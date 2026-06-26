## Description: <br>
A comprehensive security audit skill that checks file permissions, environment variables, dependency vulnerabilities, configuration files, network ports, Git security, shell security, macOS security, and secret detection, with CLI parameters, JSON output, and configuration-file support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13256659129](https://clawhub.ai/user/13256659129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security-conscious operators use this skill to run broad local checks across workspace files, configuration, dependencies, environment variables, Git state, listening ports, shell files, and macOS security settings. It can produce reports and optionally prepare them for Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs broad local security checks that may inspect sensitive configuration, environment, Git, port, and workspace details. <br>
Mitigation: Run scoped checks with --check when possible and review generated findings before storing or sharing reports. <br>
Risk: Feishu or webhook delivery can send security report details outside the local machine. <br>
Mitigation: Treat report delivery as external sharing and inspect reports for sensitive data before sending them. <br>


## Reference(s): <br>
- [Permissions Rules](references/permissions.md) <br>
- [Secrets Detection Rules](references/secrets-detection.md) <br>
- [Dependency Audit](references/dependency-audit.md) <br>
- [Code Security Best Practices](references/code-security.md) <br>
- [NPM Advisory Database](https://github.com/npm/advisories) <br>
- [PyPI Security](https://pypi.org/security) <br>
- [CVE Database](https://cve.mitre.org/) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown reports, JSON reports, and Feishu message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security findings, risk summaries, remediation suggestions, and optional formatted report content for sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
