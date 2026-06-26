## Description: <br>
Review code changes for security vulnerabilities. Checks for OWASP Top 10, secrets exposure, injection flaws, auth issues, and insecure defaults. Use when reviewing PRs, commits, or code diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests, commits, and code diffs for high-impact security issues such as OWASP Top 10 weaknesses, exposed secrets, injection flaws, authentication and authorization problems, and insecure configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review requires the agent to read code, diffs, or repositories that may contain secrets or sensitive implementation details. <br>
Mitigation: Only provide code that is intended for review, and redact secrets, credentials, tokens, and sensitive personal data unless sharing them is explicitly required. <br>
Risk: Generated security findings and fix examples may miss context-specific business logic or authentication flow requirements. <br>
Mitigation: Have a qualified reviewer validate findings, fixes, and any manual-review areas before relying on the output. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, guidance] <br>
**Output Format:** [Markdown findings with severity, file location, issue explanation, fix guidance, code examples, and OWASP category references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes high and critical findings first and calls out areas needing manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
