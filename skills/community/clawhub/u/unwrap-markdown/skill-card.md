## Description:

Unwraps hard-wrapped Markdown prose into one line per paragraph while preserving code, tables, headings, lists, blockquotes, frontmatter, hard breaks, and CJK spacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to reflow hard-wrapped Markdown prose into one line per paragraph while preserving documented Markdown structures. It can also check folders for remaining hard-wrapped prose in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A write run can overwrite selected Markdown files, including files reached through a folder argument.

Mitigation: Preview with --dry-run, use explicit intended paths, and keep a backup or review the version-control diff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/unwrap-markdown)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Updated Markdown files and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves documented Markdown structures; CJK-to-CJK joins add no space.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
