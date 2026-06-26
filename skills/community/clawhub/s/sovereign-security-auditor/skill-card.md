## Description: <br>
Comprehensive code security audit covering OWASP Top 10, secrets detection, dependency vulnerabilities, and language-specific attack patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit codebases, repositories, and pull requests for OWASP Top 10 issues, exposed secrets, dependency risks, and language-specific vulnerability patterns. It produces structured findings with severity ratings, impact assessments, and concrete fix examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface real credentials or sensitive values while auditing repositories. <br>
Mitigation: Use it only on code you are authorized to audit, ask the agent to mask or truncate secret values in reports, and rotate any real credentials found in source control. <br>
Risk: A broad audit request may inspect files outside the intended review scope. <br>
Mitigation: Define the target repository, pull request, directories, and file exclusions before running the audit. <br>
Risk: Security findings and suggested fixes may be incomplete or incorrect without human review. <br>
Mitigation: Have qualified maintainers validate reported vulnerabilities and remediation code before merging changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-security-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/ryudi84) <br>
- [Forge Tools](https://ryudi84.github.io/sovereign-tools/) <br>
- [OWASP XSS reference](https://owasp.org/www-community/attacks/xss/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown security audit report with severity-ranked findings, impact notes, and code fix examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are grouped by severity and include affected locations, vulnerability category, impact, remediation guidance, and references when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
