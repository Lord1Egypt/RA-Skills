## Description: <br>
Run security audits on codebases using static analysis, dependency scanning, and manual code review patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review codebases before deployment, check for secrets and vulnerable dependencies, and organize findings around OWASP Top 10 security risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface real secrets or credentials while scanning local files. <br>
Mitigation: Redact discovered secret values before sharing reports and rotate any exposed credentials. <br>
Risk: The skill proposes package-install and audit commands that affect the local development environment. <br>
Mitigation: Review commands before execution and run the skill from the intended project root. <br>
Risk: Static and grep-based checks can miss logic flaws and produce false positives. <br>
Mitigation: Manually verify findings and use professional penetration testing for higher-assurance security review. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security audit report with inline shell commands and prioritized findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static, grep-based checks require manual verification and do not replace professional penetration testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
