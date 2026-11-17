## Description:

模仿社会洞察类文章风格进行写作的AI助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[titancheung](https://clawhub.ai/user/titancheung)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and content teams use this skill to draft, structure, and review Chinese social-insight articles with a rational, analytical, and constructive style. It provides writing templates, phrase patterns, structure suggestions, and local style analysis for user-provided text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The style analyzer processes user-selected text files locally, so users may expose sensitive draft content to the agent/runtime.

Mitigation: Only provide files and text that are appropriate for local processing in the target environment.

Risk: Generated social-commentary guidance may include unsupported claims, examples, or data if the user does not supply grounded material.

Mitigation: Review factual claims, add sources for statistics and cases, and edit drafts before publication.

Risk: The skill is tuned for Chinese social-insight writing and may be less suitable for other languages or article genres.

Mitigation: Use it for Chinese analytical or commentary writing, and choose another writing workflow for unrelated styles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/titancheung/skills/style-mimic)
- [Publisher profile](https://clawhub.ai/user/titancheung)
- [社会洞察类文章风格指南](references/style-guide.md)
- [Full writing example](examples/full-demo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and plain text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-focused writing guidance, generated article openings and structures, template-based drafts, style scores, and improvement suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
