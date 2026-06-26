## Description: <br>
Audits installed Skills for security risks such as command execution, network access, file access, data leakage, dependency risk, prompt injection, and broad trigger conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensu1234](https://clawhub.ai/user/chensu1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and skill maintainers use this skill to review user-provided skill files, identify risky behavior, assign severity, and produce remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit inputs may include secrets, credentials, or unrelated private documents. <br>
Mitigation: Provide only the skill files intended for review and exclude secrets, credentials, and unrelated private material. <br>
Risk: Audit findings and remediation text may be incomplete or require human judgment before deployment. <br>
Mitigation: Review recommendations before changing or deploying skills, and rescan after remediation. <br>


## Reference(s): <br>
- [Review Checklist](references/review-checklist.md) <br>
- [Skill Security Audit on ClawHub](https://clawhub.ai/chensu1234/skill-security-audit-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown security audit report with severity findings and remediation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviews user-provided skill materials and does not request execution, credentials, persistence, or outbound data transfer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CLAWHUB.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
