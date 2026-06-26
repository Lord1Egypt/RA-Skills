## Description: <br>
Secure Linter helps agents review code for vulnerabilities, credential leaks, and code smells. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lig-8max](https://clawhub.ai/user/lig-8max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to review JavaScript, Python, Go, Rust, and similar code for common security issues and quality smells before relying on changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Static code review can miss issues in complex business logic or produce findings that need context. <br>
Mitigation: Review findings manually, validate suggested fixes, and run appropriate project tests or security scans before relying on the result. <br>
Risk: Use with sensitive repositories or data may expose broad local context to the reviewing agent workflow. <br>
Mitigation: Use confirmation, dry-run, restricted-access, or fallback-disabling options where available, and review behavior before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lig-8max/secure-linter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown findings with line numbers, risk levels, and remediation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static analysis only; it does not execute code and complex business logic may require human review.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
