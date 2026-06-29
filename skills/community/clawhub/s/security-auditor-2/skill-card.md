## Description: <br>
Security Auditor helps agents scan code and dependencies for known vulnerabilities, hardcoded secrets, API security issues, credential leaks, and Docker image risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nima54851](https://clawhub.ai/user/nima54851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to guide pre-commit or repository security audits and produce a security audit report with flagged risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern-based security checks can produce false positives or miss vulnerabilities. <br>
Mitigation: Review findings manually and pair the skill with established security tools such as Snyk, Dependabot, safety, or pip-audit where appropriate. <br>
Risk: Security audits can expose sensitive repository data or credentials. <br>
Mitigation: Run the skill only on code you are authorized to inspect and handle generated reports as sensitive material. <br>
Risk: Scanner telemetry is clean, but the accessible artifact evidence contains only SKILL.md while the skill describes scripts that are not present in the artifact. <br>
Mitigation: Review the installed skill files and referenced scripts before executing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nima54851/skills/security-auditor-2) <br>
- [Server-resolved GitHub provenance](https://github.com/nima54851/agent-studio/tree/main/skills/security-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/nima54851) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples and security report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may require human validation because the artifact notes that some rules can have a high false-positive rate.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
