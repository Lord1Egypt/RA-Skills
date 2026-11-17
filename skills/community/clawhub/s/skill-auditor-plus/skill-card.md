## Description:

Security, performance, and quality auditing for AgentSkills before installation or during development, including pattern scans for dangerous operations, credential leaks, token bloat, and quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caleb-niu007](https://clawhub.ai/user/caleb-niu007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit AgentSkill packages before installation, during development, or in batches for security, performance, and quality issues. It helps identify risky patterns, exposed credentials, token bloat, and skill-structure problems with actionable remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output may expose sensitive local data such as full secret values when scanning skill directories.

Mitigation: Treat audit reports as sensitive, avoid sharing raw findings publicly, and redact secrets before storing or transmitting results.

Risk: Running the auditor on untrusted directories may process attacker-controlled files or symlinks.

Mitigation: Run the auditor only on trusted or isolated skill directories and review file paths before acting on results.

Risk: Pattern-based scanning is not a complete security review and may miss vulnerabilities or produce false positives.

Mitigation: Use findings as triage input, manually review high and medium severity results, and supplement with human review before deployment.

## Reference(s):

- [AgentSkill Best Practices](references/best-practices.md)
- [ClawHub Skill Page](https://clawhub.ai/caleb-niu007/skills/skill-auditor-plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON audit-report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit scripts produce JSON reports with issue counts, severity labels, file locations, matched patterns, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
