## Description: <br>
Detect, attempt recovery from, report, and log errors to prevent silent data loss and ensure proper human intervention when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make AI agents recognize failures, attempt bounded recovery, report unresolved problems clearly, and record lessons learned for future runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Error journals may persist full error details that include secrets, headers, private paths, or sensitive API responses. <br>
Mitigation: Redact sensitive values before writing memory/errors/ and decide before installation whether local error journals are acceptable for the project. <br>
Risk: Recovery actions for authentication, dependencies, permissions, or documentation can change project state or expose sensitive workflows. <br>
Mitigation: Require explicit user approval before authentication recovery, dependency installation, permission changes, or documentation updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aptratcn/skill-error-recovery) <br>
- [Publisher profile](https://clawhub.ai/user/aptratcn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with structured error reports and optional CLI diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose retries, remediation steps, human escalation, and local error journal entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
