## Description:

This skill reviews skill packages before installation with a four-stage source, code, permissions, and risk checklist, producing a report for human decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to assess a skill package's source, code, permissions, and risks before installation and to record a structured decision. Its findings are preliminary and require human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean initial scan can miss content the checker skips, and the assessment does not cover future npm releases or external tools.

Mitigation: Treat findings as preliminary, review the package yourself, and assess future releases and external tools separately.

Risk: Untrusted packages, especially those containing symlinks, can pose risks during review.

Mitigation: Scan untrusted packages in isolation and choose a specific installation destination; pin a reviewed release when using npm.

## Reference(s):

- [Four-phase review checklist](artifact/references/checklist.md)
- [Vetting report template](artifact/references/vetting-report-template.md)
- [Project homepage](https://github.com/YottaMeta/yotta-vetter)
- [ClawHub skill listing](https://clawhub.ai/yottameta/skills/yotta-vetter)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-vetter)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands]

**Output Format:** [Text, JSON, or Markdown vetting reports, with a shell command for an optional deep-scan handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports provide an initial assessment and require human review.]

## Skill Version(s):

0.2.9 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
