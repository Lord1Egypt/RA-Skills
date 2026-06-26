## Description: <br>
Project health and best practices enforcer. Checks security, quality, documentation, CI/CD, and dependencies. Produces a letter grade (A-F) with actionable fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit repository health across security, quality, documentation, CI/CD, dependency management, and operational readiness. It produces a letter grade, categorized findings, and prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect sensitive repository contents while checking for secrets, dependency issues, and configuration gaps. <br>
Mitigation: Ask the agent to mask discovered secrets and avoid quoting sensitive values in reports. <br>
Risk: Dependency-audit commands or remediation steps may change project files or disclose package information to external tools. <br>
Mitigation: Ask before running audit commands or making remediation changes, especially on private or regulated codebases. <br>
Risk: Automated project grades and recommendations can be incomplete or context-dependent. <br>
Mitigation: Review findings before treating them as release blockers or applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryudi84/sovereign-project-guardian) <br>
- [Source Repository](https://github.com/ryudi84/sovereign-tools) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown report with tables, check results, prioritized action items, and optional inline code or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository health grades from A to F and prioritizes security findings before quality, documentation, CI/CD, and hygiene findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
