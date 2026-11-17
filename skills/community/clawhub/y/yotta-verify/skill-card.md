## Description:

A deterministic pre-install scanner that checks skills and npm packages for prompt injection, dangerous patterns, skill-file integrity, and permissions, then reports a four-level verdict and can generate audited badges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before installing or evaluating an agent skill or npm package, to inspect likely risks, produce a report or audited badge, and optionally add a scan gate to CI. Its verdict is a static-analysis aid and requires human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that packages can bypass important checks and badges can be generated without scanning, so the verdict, CI gate, or badge may not establish that a package is safe.

Mitigation: Independently review this version before trusting its verdicts or badges. When installing, pin the reviewed version, preview one explicit destination with --dry-run, avoid global or linked destinations, and back up any existing installation.

## Reference(s):

- [Prompt injection detection patterns](references/injection-patterns.md)
- [Verification report template](references/verify-report-template.md)
- [Audited badge guide](references/badges.md)
- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-verify)
- [Project homepage](https://github.com/YottaMeta/yotta-verify)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, SVG badge]

**Output Format:** [Plain-text verdicts, Markdown or JSON reports, SVG badges and badge URLs, and a CI gate exit status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local static analysis; does not execute scanned code. Verdicts require human review.]

## Skill Version(s):

0.3.6 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
