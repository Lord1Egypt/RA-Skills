## Description:

Audits installed skills for risky execution, data access, exfiltration, and overscoped triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensu1234](https://clawhub.ai/user/chensu1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to batch audit user-supplied installed skill files and produce security findings, severity ratings, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces advisory security findings that may be incomplete or misleading if the supplied skill files are partial or outdated.

Mitigation: Provide explicit, current file inputs and have a qualified reviewer confirm findings before making security or deployment decisions.

Risk: The skill is primarily written in Chinese, which may create review friction for users or agents expecting English instructions.

Mitigation: Use reviewers or translation support that can accurately interpret the Chinese audit criteria and remediation guidance.

## Reference(s):

- [Review Checklist](references/review-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/chensu1234/skills/skill-security-audit-v2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security audit report with summaries, findings, risk evidence, and remediation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are advisory and should be reviewed before acting on them.]

## Skill Version(s):

1.0.0 (source: server release metadata and CLAWHUB.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
