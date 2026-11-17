## Description:

Audit codebases and infrastructure for security issues. Use when scanning dependencies for vulnerabilities, detecting hardcoded secrets, checking OWASP top 10 issues, verifying SSL/TLS, auditing file permissions, or reviewing code for injection and auth flaws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers, engineers, and authorized security reviewers use this skill to run practical audits for dependency vulnerabilities, hardcoded secrets, OWASP code patterns, SSL/TLS configuration, file permissions, and related secure-coding checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests broad host inspection, SSH-directory checks, and file-permission audits that can exceed a normal project audit scope.

Mitigation: Use it only for explicitly authorized security work and confirm the target scope before running host-wide or home-directory checks.

Risk: The skill includes unpinned scanner installation and execution commands.

Mitigation: Prefer pinned, trusted scanner versions and review tool provenance before installing or running them.

Risk: Automatic fix commands and persistent Git hooks can modify dependency files, lockfiles, or repository behavior.

Mitigation: Review proposed changes before applying fixes, and install persistent hooks only when they match the repository policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/security-audit-toolkit)
- [Trivy documentation](https://aquasecurity.github.io/trivy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise security guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that inspect dependencies, source files, Git history, TLS endpoints, local permissions, and project configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
