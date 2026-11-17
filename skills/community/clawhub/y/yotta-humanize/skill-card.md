## Description:

Scores existing Chinese text for AI-like phrasing and provides deterministic rewrites and suggestions for the author to review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agents use the skill to assess existing Chinese drafts and review edits that reduce clichés, jargon, repetitive phrasing, and chat residue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic rewrites may change factual claims or quotations despite promises to preserve them.

Mitigation: Compare every proposed edit with the original and verify facts, figures, quotations, and attribution before saving.

Risk: The remote npm package contents were not verified for this release.

Mitigation: Install only into intended agents; prefer reviewed local files or a pinned installer version.

## Reference(s):

- [Rule catalog](references/patterns.md)
- [Scoring method](references/scoring.md)
- [Rewrite behavior](references/rewriting.md)
- [YottaMeta yotta-humanize repository](https://github.com/YottaMeta/yotta-humanize)
- [yotta-humanize on npm](https://www.npmjs.com/package/@yottameta/yotta-humanize)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text results, Markdown reports, or JSON; rewrite output includes revised text and a change list.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes supplied text; deterministic rewrites and suggestions are reviewable against the original.]

## Skill Version(s):

0.2.5 (source: frontmatter, CHANGELOG.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
