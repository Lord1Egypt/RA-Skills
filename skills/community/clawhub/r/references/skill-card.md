## Description: <br>
This skill helps agents perform security audits across file permissions, environment variables, dependencies, configuration, network ports, Git settings, shell settings, macOS security posture, and secret detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13256659129](https://clawhub.ai/user/13256659129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run or plan security checks, generate audit findings, and review remediation guidance for local workspaces and agent skill packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit script may inspect local configuration, environment-variable names, Git history, ports, and write reports. <br>
Mitigation: Review the script before installation and run it only in workspaces where that level of local inspection is acceptable. <br>
Risk: The package includes unrelated reminder and payment scripts that can send chat messages or process payment files. <br>
Mitigation: Do not run or keep those scripts unless they are explicitly needed and reviewed. <br>
Risk: Audit reports may contain sensitive local findings and can be sent to Feishu or webhook destinations. <br>
Mitigation: Review and redact reports before sharing them, and confirm webhook destinations before enabling report delivery. <br>
Risk: An exposed WeCom webhook appears in the artifact behavior. <br>
Mitigation: Rotate the webhook if it belongs to you and remove hard-coded webhook URLs before use. <br>


## Reference(s): <br>
- [Code Security Best Practices](code-security.md) <br>
- [Dependency Audit](dependency-audit.md) <br>
- [Permissions Rules](permissions.md) <br>
- [Secrets Detection Rules](secrets-detection.md) <br>
- [NPM Advisory Database](https://github.com/npm/advisories) <br>
- [PyPI Security](https://pypi.org/security) <br>
- [CVE Database](https://cve.mitre.org/) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON reports, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audit reports and may send report content to Feishu or webhook destinations when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
