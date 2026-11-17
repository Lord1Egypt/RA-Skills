## Description: <br>
GoPlus安全扫描免费版 helps agents run one-time Go project security scans, review vulnerability details, and export Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan Go projects for common code and dependency security issues, inspect severity-classified findings, and prepare Markdown security reports for remediation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to read project files and run scanner commands in a target Go project. <br>
Mitigation: Run it only in intended repositories and review proposed commands before execution. <br>
Risk: A callback URL could send scan metadata outside the local environment. <br>
Mitigation: Leave callback_url unset unless external notification is required and approved. <br>
Risk: Scan inputs or reports may expose secrets if sensitive values are present in the project. <br>
Mitigation: Avoid including secrets in scan inputs and review exported Markdown reports before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text scan summaries with command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-classified findings and Markdown report exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
