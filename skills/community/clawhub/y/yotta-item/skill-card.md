## Description:

Builds reproducible exam papers from a local question bank and blueprint, and checks existing papers for coverage, scoring, and timing gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Teachers, exam setters, and education developers use this skill to assemble reproducible papers from local question banks and blueprints, and to check existing papers for coverage, point totals, difficulty quotas, and timing. Exam teams review and approve the final paper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation replaces skill files and removes specified development remnants.

Mitigation: Choose one installation destination, back up existing customizations, and review the target directory before installing.

Risk: Template generation can overwrite existing JSON files in its output directory.

Mitigation: Generate templates into a fresh directory.

Risk: The security review identifies a scoring defect that requires separate validation.

Mitigation: Run check with the blueprint and --gate findings=1, then review the exam before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-item)
- [Project homepage](https://github.com/YottaMeta/yotta-item)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-item)
- [Report format and findings](artifact/references/report-format.md)
- [Privacy and content boundaries](artifact/references/privacy.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [JSON and Markdown papers, validation reports, and starter templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper selection is reproducible for the same bank, blueprint, and seed; generated papers reference bank item IDs rather than generating item text.]

## Skill Version(s):

0.1.3 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
