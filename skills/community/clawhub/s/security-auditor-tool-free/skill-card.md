## Description: <br>
Helps developers perform OWASP Top 10-based code security reviews with checklists, secure coding examples, input validation guidance, authentication checks, HTTP header guidance, and dependency audit commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during code review and development self-checks to inspect application code, authentication flows, input validation, security headers, and dependencies for common security issues. It is intended for authorized project review, security learning, and secure coding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency or project-changing commands such as npm audit fix or npx npm-check-updates -u can modify files or dependency state. <br>
Mitigation: Confirm before running commands that can change dependencies or project files, and keep execution scoped to the intended project. <br>
Risk: Code review may expose secrets if sensitive configuration files are included unnecessarily. <br>
Mitigation: Avoid unnecessary exposure of secrets in .env files and redact sensitive values before sharing review context. <br>
Risk: Security review guidance may be incomplete for complex business logic or application-specific threat models. <br>
Mitigation: Use the skill as a review checklist and combine its findings with human security review for complex or high-risk applications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-auditor-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with code examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured review findings, BAD/GOOD code comparisons, remediation guidance, and dependency audit commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
