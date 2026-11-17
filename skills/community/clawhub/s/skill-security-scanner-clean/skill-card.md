## Description:

Security scanner for OpenClaw skills that detects malicious backdoors, suspicious code patterns, data exfiltration risks, and security vulnerabilities in Python, JavaScript, and Shell code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cookiemikeliu](https://clawhub.ai/user/cookiemikeliu)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when installing, updating, or auditing OpenClaw skills to run static checks for risky code patterns and produce reviewable security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scan results can overstate how complete the review was, including PASS results.

Mitigation: Treat scanner output as triage, manually inspect unsupported files, and confirm flagged behavior matches the skill documentation before installation.

Risk: The install guard handles untrusted .skill archives unsafely and archive limits and temporary-directory cleanup are not evidenced.

Mitigation: Run scans only on skill copies in disposable directories, avoid elevated privileges, and be careful scanning .skill archives until archive limits and cleanup are added.

## Reference(s):

- [Security Scanner - Detection Rules Reference](references/rules-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and generated text, JSON, or Markdown scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include verdict, security score, risk distribution, findings, file locations, snippets, recommendations, and exit codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
