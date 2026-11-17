## Description:

Thumbnail QA browses a Next.js site, detects poorly cropped fill-mode images, computes object-position fixes, and applies verified before/after changes with atomic commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Next.js thumbnail crops, identify images whose focal points are clipped or poorly framed, and apply CSS object-position fixes with screenshot evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically edit project files and create git commits.

Mitigation: Review the working tree before and after execution, inspect proposed edits before committing when desired, and keep the generated commits small enough to revert individually.

Risk: The skill runs browser-based checks and local dev-server commands against the active project.

Mitigation: Run it only in a trusted Next.js workspace, confirm the localhost target, and review generated .gstack/thumbnail-qa artifacts before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/thumbnail-qa)
- [Project homepage](https://github.com/kaicianflone/thumbnail-qa-skill)
- [gstack browser tooling](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, code edits, shell commands, screenshots, and git commits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces before/after screenshot evidence and a structured thumbnail QA report under .gstack/thumbnail-qa/.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, changelog released 2026-05-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
