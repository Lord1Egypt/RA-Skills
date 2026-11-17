## Description:

Wenqu Publish prepares Chinese drafts for publication by cleaning internal creation markers, generating title and summary candidates, optionally creating a cover image, and writing a standalone local publish directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to turn Chinese articles, reports, tutorials, project introductions, and explanatory drafts into publication-ready local artifacts. It helps clean draft-only markers, prepare candidate titles and summaries, manage an optional cover image workflow, and preserve publication metadata separately from the cleaned article body.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may invoke an unpinned local wenqu-image skill for cover generation.

Mitigation: Install only when the local wenqu-image skill is trusted, and review generated cover prompts and resulting image URLs before publication.

Risk: Repeated publication of the same draft version may replace earlier publish/vN artifacts despite the workflow describing non-overwrite behavior.

Mitigation: Review target paths before writing, keep backups, or use immutable pubM-specific directories for repeated publication attempts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gogoingai/skills/wenqu-publish)
- [Metadata homepage](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-publish)
- [Publishing workflow](references/workflow.md)
- [Title and summary guidance](references/title-summary.md)
- [Cover prompt guidance](references/cover-prompt.md)
- [Automatic publishing extension point](references/auto-publish.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown files and concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cleaned article output and publication metadata to a local publish/vN directory; cover image generation is optional and depends on the local wenqu-image skill.]

## Skill Version(s):

0.1.19 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
