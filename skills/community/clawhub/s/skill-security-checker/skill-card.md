## Description:

Scans agent skills for security, dependency, permission, and quality issues and produces findings with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to assess agent skills before installation or release and to review findings in CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic scans with allowed domains may permit broader network access than intended.

Mitigation: Avoid dynamic scans with --allow-domain until network filtering is fixed.

Risk: Scanning directories containing symlinks may read files outside the intended target.

Mitigation: Scan directories without symlinks or validate symlink targets first.

Risk: Generated HTML reports from untrusted skills may be unsafe to open.

Mitigation: Prefer JSON or SARIF reports and treat HTML reports as untrusted.

Risk: Networked update and vulnerability-data features introduce avoidable exposure in untrusted environments.

Mitigation: Use networked update and OSV features only in trusted environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fyniujin/skills/skill-security-checker)
- [Scan patterns reference](artifact/references/scan-patterns.md)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, SARIF, Guidance]

**Output Format:** [Plain-text, JSON, HTML, or SARIF scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick verdicts highlight leading risks; full reports include findings and remediation suggestions.]

## Skill Version(s):

3.5.5 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
