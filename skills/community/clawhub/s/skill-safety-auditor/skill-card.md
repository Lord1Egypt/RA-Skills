## Description:

Perform comprehensive security audits on skills to identify vulnerabilities, unsafe patterns, and compliance issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to scan skill directories for hardcoded secrets, unsafe code patterns, permission issues, dependency concerns, insecure URLs, and release-blocking findings before publication or deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quick scans may print suspected secrets to shared terminals or CI logs.

Mitigation: Run scans only on intended skill directories, avoid shared logs for sensitive targets, and redact suspected secret values before sharing results.

Risk: Audit reports are written to local history and may contain sensitive file paths or findings.

Mitigation: Store audit data in a protected location and periodically clear or restrict access to local report history.

Risk: Scanner output should not be treated as a complete release decision because the evidence verdict is suspicious.

Mitigation: Review or patch the scanner to redact secret values and escape JSON safely before relying on reports for release decisions.

## Reference(s):

- [Skill Safety Auditor ClawHub page](https://clawhub.ai/harrylabsj/skills/skill-safety-auditor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console output and JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity counts, findings, recommendations, and pass/fail status.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
