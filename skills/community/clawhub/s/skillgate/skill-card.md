## Description:

SkillGate scans AI agent skill folders for security and quality issues and produces a Trust Score with reports in several formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use SkillGate to inspect AI agent skill packages and review findings, scores, and reports. Its bundled companion checks also provide document and medical-device compliance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted file links in an untrusted package may expose private document fields during scanning.

Mitigation: Until link containment is fixed, scan untrusted packages in an isolated environment without access to private files.

Risk: Scores and verification claims may suggest broader checks than the tool performs.

Mitigation: Treat scores as preliminary; benchmark previews execute no tests, dependency handling performs no vulnerability lookup, and JSON reports provide fuller self-scan suppression disclosure.

Risk: Packaged command examples may be incorrect, and platform-specific link behavior has not been tested.

Mitigation: Review command examples before use and do not assume link behavior is verified across platforms.

## Reference(s):

- [SkillGate on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/skillgate)

## Skill Output:

**Output Type(s):** [Text reports, JSON, SARIF, JUnit XML, Markdown, HTML, SVG badges, Compliance guidance]

**Output Format:** [Terminal text, JSON, SARIF, JUnit XML, Markdown, HTML, and SVG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include findings and a Trust Score; treat scores as preliminary review evidence.]

## Skill Version(s):

1.0.28 (source: release evidence, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
