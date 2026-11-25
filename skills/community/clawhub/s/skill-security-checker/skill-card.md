## Description:

Scans agent skills for code, dependency, permission, and structural risks and produces findings and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use the scanner to screen agent skills before installation or release and to review findings in CI/CD workflows. Treat its verdict as one input to a broader review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is rated suspicious because of reported weaknesses in its checks, sandbox controls, and coverage. The scan was partial; the rating does not establish malicious intent.

Mitigation: Use results as screening guidance only. Independently inspect the target skill and do not rely on this scanner alone to establish that it is safe.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fyniujin/skills/skill-security-checker)
- [Scan patterns reference](artifact/references/scan-patterns.md)
- [OSV vulnerability database](https://osv.dev/)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, HTML, SARIF]

**Output Format:** [Plain-text findings and JSON, HTML, or SARIF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include a verdict, prioritized findings, and remediation guidance; scan coverage can be incomplete.]

## Skill Version(s):

3.7.0 (source: server release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
