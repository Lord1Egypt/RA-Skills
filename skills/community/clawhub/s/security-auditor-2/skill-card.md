## Description:

Security Auditor helps an agent scan code and dependencies for known vulnerabilities, hardcoded secrets, API security issues, credential exposure, and Docker image risks, then produce a security audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before code submission or deployment to identify dependency vulnerabilities, leaked credentials, API exposure, and container risks that need review or remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced scanner scripts are missing from the package, so parts of the skill may be nonfunctional unless those scripts are supplied separately.

Mitigation: Verify the referenced scanner scripts are present and trusted before relying on automated scan results.

Risk: External tools such as safety and pip-audit may install or execute third-party packages in the user's environment.

Mitigation: Use a virtual environment, a trusted package index, and pinned versions or hashes when installing audit tooling.

Risk: Security scans may expose sensitive repository contents or credentials during inspection.

Mitigation: Run the skill only against repositories the user is authorized to inspect and review findings before sharing reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nima54851/skills/security-auditor-2)
- [Server-Resolved GitHub Provenance](https://github.com/nima54851/agent-studio/tree/main/skills/security-auditor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and security audit report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on external audit tools or scanner scripts that are not included in the package.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
