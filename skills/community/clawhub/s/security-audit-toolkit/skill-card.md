## Description: <br>
Audit codebases and infrastructure for security issues. Use when scanning dependencies for vulnerabilities, detecting hardcoded secrets, checking OWASP top 10 issues, verifying SSL/TLS, auditing file permissions, or reviewing code for injection and auth flaws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit projects for vulnerable dependencies, hardcoded secrets, OWASP-style code issues, SSL/TLS configuration problems, risky file permissions, and authentication or authorization gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret-scan results may expose real credentials or sensitive paths. <br>
Mitigation: Treat scan output as sensitive, rotate confirmed credentials, and avoid sharing raw findings outside trusted review channels. <br>
Risk: Dependency auto-fix commands can change package versions or application behavior. <br>
Mitigation: Review dependency changes, run tests, and commit only fixes that are understood. <br>
Risk: External audit tools and one-off commands can introduce supply-chain or execution risk. <br>
Mitigation: Trust or pin external tools where practical, inspect generated scripts before running them, and execute audits in workspaces you are comfortable auditing. <br>
Risk: The optional pre-commit hook can block commits based on pattern matches. <br>
Mitigation: Install the hook only when ongoing commit blocking is desired, and review false positives before bypassing or changing the hook. <br>


## Reference(s): <br>
- [Security Audit Toolkit on ClawHub](https://clawhub.ai/gitgoodordietrying/security-audit-toolkit) <br>
- [Trivy documentation](https://aquasecurity.github.io/trivy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that scan dependencies, secrets, TLS settings, permissions, and source patterns; users should review results and proposed fixes before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
