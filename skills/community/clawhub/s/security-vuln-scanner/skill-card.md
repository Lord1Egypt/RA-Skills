## Description:

Scans code for common security vulnerability patterns such as SQL injection, XSS, hardcoded secrets, insecure random number use, command injection, and sensitive information leaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to perform lightweight, local pattern-based checks of source code and receive vulnerability findings, severity labels, line numbers, scores, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is lightweight and pattern-based, so it may produce false positives or miss real vulnerabilities.

Mitigation: Use the results as triage input and confirm findings with human review and established security testing tools before relying on them.

Risk: The generic "vulnerability" trigger may activate the skill in broad security discussions.

Mitigation: Confirm that the user wants a vulnerability scan before analyzing code when the trigger context is ambiguous.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/honestqiao/skills/security-vuln-scanner)
- [ClawHub Publisher Profile](https://clawhub.ai/user/honestqiao)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or JSON-style vulnerability report with code findings and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include vulnerability type, line number, severity, message, and a security score.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
