## Description:

A deterministic pre-install scanner for agent skills and packages that checks for prompt injection, dangerous patterns, file integrity, and permission needs, then produces a verdict, report, and audited badge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use it to review a skill or package before installation, generate an audit report or badge, and add a pre-install check to CI. Its findings require human review and do not replace the installation decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious, citing a mismatch between its stated static-scanning purpose and installer behavior, plus a scanner rule that can issue a safe-install badge without scanning.

Mitigation: Follow ClawScan guidance: avoid installing until installer behavior and badge handling have been reviewed and corrected or independently verified.

Risk: ClawScan analysis is partial: 12 of 14 components were scanned, and tool-misuse analysis was degraded, so unreported behavior is not established as safe.

Mitigation: Review the remaining components and independently assess behavior before relying on the result.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-verify)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-verify)
- [Prompt injection patterns](artifact/references/injection-patterns.md)
- [Verification report template](artifact/references/verify-report-template.md)
- [Badge documentation](artifact/references/badges.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Files]

**Output Format:** [Text verdicts, JSON and Markdown reports, and SVG audit badges]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory results require human review.]

## Skill Version(s):

0.3.7 (source: frontmatter, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
