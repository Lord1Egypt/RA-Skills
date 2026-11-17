## Description:

Audits OpenClaw deployments for security misconfigurations, known vulnerabilities, malicious skills, and indicators of compromise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nx4dm1n](https://clawhub.ai/user/nx4dm1n)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run a local read-only security audit of an OpenClaw deployment and receive findings they can remediate before or during production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local OpenClaw state during audit.

Mitigation: Run from a low-privilege account, avoid running as root, and restrict access to generated reports.

Risk: The security summary flags an unsafe shell command path that crafted filenames could exploit.

Mitigation: Review or remediate the hashing path before use, or run only in a controlled environment without untrusted installed skill filenames.

## Reference(s):

- [ClawHub sec-audit skill page](https://clawhub.ai/nx4dm1n/skills/sec-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write a local JSON report file; evidence indicates audit results are not transmitted externally.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
